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

# Text dry-run
r = text.chat("test", dry_run=True)
check("text dry-run returns dict", isinstance(r, dict) and r.get("dry_run"))

# Text streaming dry-run
r = text.chat("test", stream=True, dry_run=True)
check("text stream dry-run returns dict", isinstance(r, dict) and r.get("dry_run"))

# Image dry-run
r = image.generate("test", dry_run=True)
check("image text2img dry-run returns dict", isinstance(r, dict) and r.get("dry_run"))

# Image img2img dry-run (with placeholder base64)
r = image.generate("test", mode="img2img", image_b64s=["dGVzdA=="], dry_run=True)
check("image img2img dry-run returns dict", isinstance(r, dict) and r.get("dry_run"))

# Video dry-run
r = video.create("test", dry_run=True)
check("video dry-run returns dict", isinstance(r, dict) and r.get("dry_run"))

# Translation detection
check("English text needs no translation", not translate.needs_translation("hello world"))
check("Chinese text needs translation", translate.needs_translation("你好世界"))

print(f"\n{'='*30}")
print(f"Results: {passed} passed, {failed} failed")
sys.exit(0 if failed == 0 else 1)
