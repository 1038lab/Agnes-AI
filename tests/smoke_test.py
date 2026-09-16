#!/usr/bin/env python3
"""Standalone smoke test — no test framework needed."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import text, image, video, translate

passed = 0
failed = 0

def check(name, ok):
    global passed, failed
    if ok:
        passed += 1
        print(f"  PASS  {name}")
    else:
        failed += 1
        print(f"  FAIL  {name}")

# Text dry-run with agnes-3.0-flash
r = text.chat("test", dry_run=True)
check("text dry-run returns dict", isinstance(r, dict) and r.get("dry_run"))
check("text default model is agnes-3.0-flash", r.get("request", {}).get("model") == "agnes-3.0-flash")

# Text streaming dry-run
r = text.chat("test", stream=True, dry_run=True)
check("text stream dry-run returns dict", isinstance(r, dict) and r.get("dry_run"))

# Text multimodal image description
r = text.chat("describe", image_b64s=["dGVzdA=="], dry_run=True)
check("text multimodal vision dry-run returns dict", isinstance(r, dict) and r.get("dry_run"))

# Image dry-run with agnes-image-2.5-flash
r = image.generate("test", dry_run=True)
check("image text2img dry-run returns dict", isinstance(r, dict) and r.get("dry_run"))
check("image default model is agnes-image-2.5-flash", r.get("request", {}).get("model") == "agnes-image-2.5-flash")

# Image img2img dry-run (with placeholder base64)
r = image.generate("test", mode="img2img", image_b64s=["dGVzdA=="], dry_run=True)
check("image img2img dry-run returns dict", isinstance(r, dict) and r.get("dry_run"))

# Modern video dry-run (agnes-video-2.5-flash)
r = video.create("test", dry_run=True)
check("video 2.5-flash dry-run returns dict", isinstance(r, dict) and r.get("dry_run"))
check("video default model is agnes-video-2.5-flash", r.get("request", {}).get("model") == "agnes-video-2.5-flash")
check("video 2.5-flash has seconds and size 720P", r.get("request", {}).get("seconds") == "5" and r.get("request", {}).get("size") == "720P")

# Legacy video dry-run backward compatibility (agnes-video-v2.0)
r_legacy = video.create("test", mode="text2video", num_frames=121, dry_run=True, model="agnes-video-v2.0")
check("legacy video v2.0 backward compatibility", r_legacy.get("request", {}).get("model") == "agnes-video-v2.0")

# Translation detection
check("English text needs no translation", not translate.needs_translation("hello world"))
check("Chinese text needs translation", translate.needs_translation("你好世界"))

print(f"\n{'='*30}")
print(f"Results: {passed} passed, {failed} failed")
sys.exit(0 if failed == 0 else 1)
