---
name: Agnes-AI
description: "Generate text, analyze/describe images, create AI images, and render AI videos using Agnes AI free cloud APIs (agnes-3.0-flash, agnes-image-2.5-flash, agnes-video-2.5-flash). Pure Python stdlib, zero dependencies."
tags: [agnes-ai, text-generation, image-generation, video-generation, multimodal-vision, prompt-engineer]
metadata:
  version: "1.2.0"
  platform: "https://platform.agnes-ai.com"
---

# Agnes-AI Skill

This skill allows agents to generate high-quality text, describe images, create artwork, and render AI videos using the [Agnes AI Platform](https://platform.agnes-ai.com) without requiring a local GPU or third-party dependencies.

## Models Overview

- **Text & Vision**: `agnes-3.0-flash` (Default, 512K context, multimodal vision)
- **Image**: `agnes-image-2.5-flash` (Default, 1K–4K, text2img & compose)
- **Video**: `agnes-video-2.5-flash` (Default, 720P, 4–12s) / `agnes-video-2.5` (720P–2K)

---

## CLI Usage for Agents

All commands use `python3 scripts/agnes.py`:

### 1. Text & Multimodal Vision
```bash
# Text generation / chat
python3 scripts/agnes.py text --prompt "Draft a sci-fi character backstory"

# Multimodal image description (vision)
python3 scripts/agnes.py text --prompt "Describe what is in this image" --image-url /path/to/photo.jpg

# JSON output for structured parsing
python3 scripts/agnes.py text --prompt "Extract key entities as JSON" --json-output
```

### 2. Image Generation
```bash
# Text-to-image
python3 scripts/agnes.py image text2img --prompt "Futuristic glass skyscraper in morning mist" --size 1024x768

# Image-to-image / style transfer
python3 scripts/agnes.py image img2img --prompt "Cyberpunk watercolor aesthetic" --image-url /path/to/input.png
```

### 3. Video Generation
```bash
# Text-to-video (4-12 seconds duration)
python3 scripts/agnes.py video text2video --prompt "Camera slowly tracks through a neon cyber alley" --seconds 5 --aspect-ratio 16:9

# Image-to-video (from first frame)
python3 scripts/agnes.py video img2video --prompt "Bring the character portrait to life with gentle breathing" --image-url /path/to/first_frame.png

# Keyframe transition (morph between two frames)
python3 scripts/agnes.py video keyframes --prompt "Seamless transformation animation" --image-url /path/to/start.png --image-url /path/to/end.png

# Video polling
python3 scripts/agnes.py poll <VIDEO_ID> --download --output-dir ./outputs
```

---

## Environment & Authentication

Set the API Key via environment variable:
```bash
export AGNES_API_KEY="your-api-key"
```
Get a free API key at [platform.agnes-ai.com](https://platform.agnes-ai.com).
