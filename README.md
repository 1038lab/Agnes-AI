# Agnes-AI

[English](README.md) | [中文说明](README_zh.md)

Zero-dependency Python CLI, SDK, and interactive web playground for the **Agnes AI API** — a free, cloud-based platform for text generation, multimodal vision, image synthesis, and AI video creation.

Built by [AILab](https://github.com/1038lab).

---

## News & Updates

- **v1.2.0 (2026-09-15)**:
  - Upgraded default models to next-gen Agnes AI: `agnes-3.0-flash`, `agnes-image-2.5-flash`, and `agnes-video-2.5-flash`.
  - Modern Video Generation: Added duration in seconds (`--seconds 4..12`), aspect ratios (`16:9`, `9:16`, `1:1`, etc.), and resolutions (`720P`, `1080P`, `1K`, `2K`).
  - Real-time video rendering progress bar (`0%` to `100%`).
  - Automatic Flash model safeguards (720P auto-adjustment to prevent API 400 errors).
  - Preserved backward compatibility for `agnes-video-v2.0` legacy frame calculation.

---

## Features

- **Text & Vision** — Ultra-fast chat and prompt enhancement powered by `agnes-3.0-flash` with 512K context.
- **Multimodal Image Understanding** — Describe and analyze images using `agnes text --image-url`.
- **Image Generation** — High-fidelity text2img and image-to-image fusion with `agnes-image-2.5-flash`.
- **Video Generation** — Text2video, image2video, keyframe animation, and multimodal reference generation with `agnes-video-2.5-flash`.
- **Automatic Translation** — Non-English prompts are automatically translated to English for optimal model adherence.
- **Interactive Web Playground** — Visual playground with real-time preview (`examples/server.py`).
- **Zero Third-Party Dependencies** — Runs purely on the Python standard library.

---

## Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/1038lab/Agnes-AI.git
cd Agnes-AI
```

### 2. Set your API Key
Sign up for a free key at [platform.agnes-ai.com](https://platform.agnes-ai.com).
```bash
export AGNES_API_KEY="your-api-key"
```

### 3. Generate Content

#### Text Generation:
```bash
python3 scripts/agnes.py text --prompt "Explain quantum computing in one sentence"
```

#### Image Generation:
```bash
python3 scripts/agnes.py image text2img --prompt "A serene mountain lake at sunrise, oil painting style"
```

#### Video Generation:
```bash
python3 scripts/agnes.py video text2video --prompt "A majestic golden eagle soaring above misty alpine peaks" --seconds 5
```

---

## Interactive Playground

Run the included local web UI for an intuitive visual experience:

```bash
python3 examples/server.py
```
Open **http://localhost:8888** in your browser.

---

## CLI Reference

### `agnes text`
```bash
agnes text --prompt "PROMPT" [--system "SYSTEM"] [--image-url PATH] [--stream] [--json-output] [--model agnes-3.0-flash]
```

### `agnes image`
```bash
agnes image text2img --prompt "PROMPT" [--size 1024x768] [--model agnes-image-2.5-flash]
agnes image img2img --prompt "PROMPT" --image-url PATH [--size 1024x768]
```

### `agnes video`
```bash
agnes video text2video --prompt "PROMPT" [--seconds 5] [--aspect-ratio 16:9] [--size 720P]
agnes video img2video --prompt "PROMPT" --image-url PATH [--seconds 5]
agnes video keyframes --prompt "PROMPT" --image-url START.png --image-url END.png [--seconds 6]
agnes video poll VIDEO_ID --download --output-dir ./videos
```

---

## License

GNU General Public License v3.0. See [LICENSE](LICENSE).
