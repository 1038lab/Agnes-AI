#!/usr/bin/env python3
"""Lightweight HTTP server for the Agnes playground.
Serves playground.html and proxies API calls to Agnes AI via scripts/ modules.
Usage: python3 examples/server.py [port]
"""

import io, json, os, sys
from contextlib import redirect_stdout
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse

# Ensure scripts/ is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import text, image, video

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)


class Handler(SimpleHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(204)
        self.send_cors_headers()
        self.end_headers()

    def do_POST(self):
        path = urlparse(self.path).path
        if path == "/api/run":
            self.handle_run()
        else:
            self.send_error(404)

    def send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def read_body(self):
        length = int(self.headers.get("Content-Length", 0))
        return json.loads(self.rfile.read(length))

    def json_response(self, data, status=200):
        self.send_response(status)
        self.send_cors_headers()
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode())

    def error_response(self, msg):
        self.json_response({"ok": False, "error": msg})

    def handle_run(self):
        try:
            body = self.read_body()
        except Exception as e:
            self.error_response(f"Invalid request: {e}")
            return

        api_key = body.get("api_key", "")
        mode = body.get("mode", "text")
        sub_mode = body.get("sub_mode", "chat")
        prompt = body.get("prompt", "")
        extra = body.get("extra", {})

        if not api_key:
            self.error_response("API key is required")
            return
        if not prompt and mode != "video" and sub_mode != "poll" and sub_mode != "describe":
            self.error_response("Prompt is required")
            return

        os.environ["AGNES_API_KEY"] = api_key

        try:
            if mode == "text":
                result = self.run_text(sub_mode, prompt, extra)
            elif mode == "image":
                result = self.run_image(sub_mode, prompt, extra)
            elif mode == "video":
                result = self.run_video(sub_mode, prompt, extra)
            else:
                self.error_response(f"Unknown mode: {mode}")
                return
            self.json_response({"ok": True, **result})
        except SystemExit as e:
            self.error_response(str(e))
        except Exception as e:
            self.error_response(f"{type(e).__name__}: {e}")

    def run_text(self, sub_mode, prompt, extra):
        system = extra.get("system", "")
        image_b64 = extra.get("image_data", "")
        image_b64s = [image_b64] if image_b64 else None
        buf = io.StringIO()
        if sub_mode == "describe":
            with redirect_stdout(buf):
                text.chat(prompt or "Describe this image in detail",
                          system=system or None, image_b64s=image_b64s,
                          max_tokens=extra.get("max_tokens", 2048))
            return {"type": "text", "content": buf.getvalue()}
        if sub_mode == "stream":
            with redirect_stdout(buf):
                r = text.chat(prompt, system=system or None, stream=True, max_tokens=extra.get("max_tokens", 512))
            return {"type": "text", "content": r or buf.getvalue()}
        elif sub_mode == "json":
            r = text.chat(prompt, system=system or None, json_output=True, max_tokens=extra.get("max_tokens", 512))
            return {"type": "json", "content": r}
        else:
            with redirect_stdout(buf):
                text.chat(prompt, system=system or None, max_tokens=extra.get("max_tokens", 512))
            return {"type": "text", "content": buf.getvalue()}

    def _image_b64s(self, extra):
        raw = []
        for k in ("image_data", "image_data1", "image_data2", "image_data3", "image_data4"):
            v = extra.get(k)
            if v:
                raw.append(v)
        return raw or None

    def run_image(self, sub_mode, prompt, extra):
        image_b64s = self._image_b64s(extra)
        size = extra.get("size") or "1024x768"
        r = image.generate(prompt, mode=sub_mode, image_b64s=image_b64s, size=size, output_dir=OUTPUT_DIR)
        local_path = r[0] if isinstance(r, list) and r else None
        return {"type": "image", "url": f"/outputs/{os.path.basename(local_path)}" if local_path else None, "local_path": local_path}

    def run_video(self, sub_mode, prompt, extra):
        image_b64s = self._image_b64s(extra)
        width = int(extra.get("vid_w", 1152))
        height = int(extra.get("vid_h", 768))
        num_frames = int(extra.get("vid_frames", 17))
        frame_rate = 24
        r = video.create(
            prompt, mode=sub_mode, image_b64s=image_b64s,
            width=width, height=height, num_frames=num_frames, frame_rate=frame_rate,
            download=True, output_dir=OUTPUT_DIR, poll=True,
            poll_interval=5, timeout=300
        )
        local_path = r.get("local_path")
        video_url = r.get("video_url")
        return {
            "type": "video",
            "url": f"/outputs/{os.path.basename(local_path)}" if local_path else video_url,
            "local_path": local_path,
            "video_url": video_url,
            "status": r.get("status")
        }

    def translate_path(self, path):
        # Serve playground.html by default, serve outputs/ from examples/outputs
        if path == "/" or path == "/index.html":
            return os.path.join(os.path.dirname(__file__), "playground.html")
        if path.startswith("/outputs/"):
            return os.path.join(OUTPUT_DIR, os.path.basename(path))
        if path.startswith("/examples/"):
            return os.path.join(os.path.dirname(__file__), os.path.basename(path))
        return super().translate_path(path)


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8888
    os.chdir(os.path.join(os.path.dirname(__file__), ".."))
    server = HTTPServer(("0.0.0.0", port), Handler)
    print(f"Agnes Playground → http://localhost:{port}")
    print("Press Ctrl+C to stop")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()


if __name__ == "__main__":
    main()
