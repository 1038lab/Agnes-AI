---
name: Agnes-AI Complete
version: 1.2.0
description: Unified skill for Agnes AI — text, image, and video generation via a single zero-dependency Python CLI
tags: [agnes-ai, text-generation, image-generation, video-generation, free]
dependencies: [python3]
env:
  - AGNES_API_KEY
  - AGNES_API_TOKEN
  - APIHUB_AGNES_API_KEY
---

# Agnes-AI Complete Skill

## Overview

This skill enables AI coding agents to generate text, images, and videos using
the free [Agnes AI](https://agnes-ai.com) API via a single zero-dependency
Python CLI (`scripts/agnes.py`).

**Compatible agents:** Codex, Claude Code, OpenCode, OpenClaw, Cursor, Hermes
Agent config files under `agents/` provide platform-specific metadata.

The CLI wraps three API domains under one command:

| Command | Capability |
|---------|-----------|
| `agnes text` | Chat completions / text generation |
| `agnes image` | Image generation (text2img, img2img, compose) |
| `agnes video` | Video generation (text2video, img2video, keyframes) |
| `agnes poll` | Poll async video generation status |
| `agnes smoke-test` | Dry-run validation of all modes |
| `agnes setup` | Persist API key to shell profile |

## Setup

### 1. API Key

Set one of these environment variables:

```bash
export AGNES_API_KEY="your-key-here"
export AGNES_API_TOKEN="your-token-here"
export APIHUB_AGNES_API_KEY="your-key-here"
```

Priority: `AGNES_API_KEY` > `AGNES_API_TOKEN` > `APIHUB_AGNES_API_KEY`

### 2. Shell Profile (Optional)

```bash
agnes setup
```

This persists the key to your shell profile (`.zshrc` / `.bashrc`).

### 3. Verify

```bash
agnes smoke-test
```

## CLI Reference

All commands use `python3 scripts/agnes.py` as the entry point. Agents should
invoke the CLI directly:

```bash
python3 scripts/agnes.py <command> [subcommand] [flags]
```

---

### Text Generation

Generate text using Agnes AI chat completion models.

```bash
agnes text --prompt "Tell me a story about a robot" [flags]
```

**Flags:**

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--prompt` | string | (required) | Input prompt text |
| `--system` | string | — | System prompt for model context |
| `--stream` | flag | false | Stream tokens as they arrive |
| `--temperature` | float | 0.7 | Sampling temperature (0.0–2.0) |
| `--top-p` | float | 0.9 | Nucleus sampling threshold |
| `--max-tokens` | int | 2048 | Maximum tokens to generate |
| `--tools-json` | string | — | JSON string defining function tools |
| `--tool-choice` | string | "auto" | Tool selection mode |
| `--json-output` | flag | false | Request structured JSON response |
| `--dry-run` | flag | false | Print request without sending |
| `--no-translate` | flag | false | Skip auto-translation of prompt |
| `--verbose` | flag | false | Show full API response |

**Examples:**

```bash
# Basic generation
agnes text --prompt "Write a haiku about the ocean"

# With system prompt and parameters
agnes text --prompt "Explain quantum computing" \
  --system "You are a patient physics tutor" \
  --temperature 0.3 --max-tokens 500

# Stream tokens
agnes text --prompt "Tell me a long story" --stream

# Tool use
agnes text --prompt "What's the weather in Tokyo?" \
  --tools-json '[{"type":"function","function":{"name":"get_weather","parameters":{"type":"object","properties":{"location":{"type":"string"}},"required":["location"]}}}]'

# Dry run (validate without consuming credits)
agnes text --prompt "Hello" --dry-run
```

---

### Image Generation

Generate images from text, transform existing images, or compose elements.

```bash
agnes image <subcommand> --prompt "description" [flags]
```

**Subcommands:**

| Subcommand | Description |
|-----------|-------------|
| `text2img` | Generate image from text prompt |
| `img2img` | Transform an existing image |
| `compose` | Compose multiple elements into an image |

**Flags:**

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--prompt` | string | (required) | Description of desired image |
| `--image-url` | string | — | Source image URL (img2img) |
| `--size` | string | "1024x1024" | Output dimensions (WxH) |
| `--output-dir` | string | "." | Directory to save images |
| `--dry-run` | flag | false | Print request without sending |
| `--no-translate` | flag | false | Skip auto-translation of prompt |

**Examples:**

```bash
# Text to image
agnes image text2img --prompt "A serene mountain landscape at sunset"

# Image to image (transform an existing image)
agnes image img2img --prompt "Make this look like a watercolor painting" \
  --image-url "https://example.com/photo.jpg"

# Compose elements
agnes image compose --prompt "A cat sitting on a wizard's hat"

# Custom size and output directory
agnes image text2img --prompt "Cyberpunk city street" \
  --size "1920x1080" --output-dir ./outputs

# Dry run
agnes image text2img --prompt "A dragon" --dry-run
```

---

### Video Generation

Generate videos from text, animate images, create multi-scene videos, or use
keyframe interpolation.

```bash
agnes video <subcommand> --prompt "description" [flags]
```

**Subcommands:**

| Subcommand | Description |
|-----------|-------------|
| `text2video` | Generate video from text prompt |
| `img2video` | Animate a source image |
| `keyframes` | Start and end frame animation |

**Flags:**

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--prompt` | string | (required) | Video description |
| `--image-url` | string | — | Source image URL (img2video) |
| `--seconds` | int | 5 | Duration in seconds (4–12) |
| `--aspect-ratio` | string | "16:9" | Aspect ratio (16:9, 9:16, 1:1, etc.) |
| `--size` | string | "720P" | Resolution (720P, 1080P, 1K, 2K) |
| `--width` | int | 1024 | Video width in pixels |
| `--height` | int | 576 | Video height in pixels |
| `--num-frames` | int | 81 | Number of frames (must be 8n+1) |
| `--frame-rate` | int | 8 | Frames per second (1–60) |
| `--seed` | int | — | Random seed for reproducibility |
| `--num-inference-steps` | int | 50 | Denoising steps |
| `--negative-prompt` | string | — | Things to avoid in generation |
| `--no-poll` | flag | false | Don't wait for completion |
| `--poll-interval` | int | 5 | Seconds between status checks |
| `--timeout` | int | 600 | Max seconds to wait |
| `--download` | flag | false | Download video when complete |
| `--output-dir` | string | "." | Directory to save videos |
| `--dry-run` | flag | false | Print request without sending |
| `--no-translate` | flag | false | Skip auto-translation of prompt |

**Examples:**

```bash
# Text to video
agnes video text2video --prompt "A rocket launching into space"

# Animate an image
agnes video img2video --prompt "Waves crashing on the shore" \
  --image-url "https://example.com/beach.jpg"

# Multi-scene video
agnes video keyframes --prompt "A smooth transition from morning to night in Tokyo"

# Keyframe interpolation
agnes video keyframes

# Custom dimensions and frame count
agnes video text2video --prompt "Drone flying over a canyon" \
  --width 1920 --height 1080 --num-frames 161 --frame-rate 24

# Reproducible generation
agnes video text2video --prompt "Aurora borealis" --seed 42

# Run in background (no polling, no download)
agnes video text2video --prompt "Fireworks display" --no-poll

# Download when ready
agnes video text2video --prompt "Corgi running on a beach" --download

# Dry run
agnes video text2video --prompt "Time-lapse of flowers blooming" --dry-run
```

---

### Polling

Check the status of an async video generation job.

```bash
agnes poll <video-id> [flags]
```

**Flags:**

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--poll-interval` | int | 5 | Seconds between status checks |
| `--timeout` | int | 600 | Max seconds to wait |
| `--download` | flag | false | Download video when complete |
| `--output-dir` | string | "." | Save location for download |

**Example:**

```bash
agnes poll abc123-xyz --download --output-dir ./videos
```

---

### Smoke Test

Validate that all API modes work without consuming credits.

```bash
agnes smoke-test
```

Runs dry-run requests for every subcommand and reports pass/fail for each.

---

### Setup

Persist API key to shell profile.

```bash
agnes setup
```

Prompts for an API key and appends the export to `.zshrc` or `.bashrc`.

---

## Workflow Rules

### Auto-Translation

For image and video generation prompts, the CLI automatically detects
non-English text and translates it to English before sending to the API.
Disable with:

```bash
agnes image text2img --prompt "Une montagne enneigée" --no-translate
```

### CLI-First Execution

Agents must invoke the CLI directly (`python3 scripts/agnes.py ...`) rather
than calling the API or generating Python requests inline. The CLI is the
single source of truth.

### JSON Output Convention

When `--json-output` is used with text generation, the response is formatted
as a JSON object. Use this for structured data extraction.

### Dry-Run Validation

Always use `--dry-run` first when testing new command variations to verify
the request payload without consuming API credits.

---

## Video Constraints

### Frame Count Formula

The `num-frames` parameter must satisfy: **`num_frames = 8n + 1`** where
`n` is a non-negative integer.

| n | frames | Use case |
|---|--------|----------|
| 0 | 1 | Static frame |
| 1 | 9 | Short clip (~1s at 8fps) |
| 10 | 81 | Default (exactly 81) |
| 20 | 161 | Medium clip |
| 30 | 241 | Longer clip |
| 55 | 441 | Maximum |

- **Minimum:** 1 frame
- **Maximum:** 441 frames
- **Default:** 81 frames

### Frame Rate

- **Range:** 1–60 fps
- **Default:** 8 fps

### Duration Calculation

```
duration = num_frames / frame_rate
```

Example: 81 frames at 8 fps ≈ 10 seconds of video.

---

## Example Workflows

### Generate a Short Video

```bash
# Step 1: Generate (async)
python3 scripts/agnes.py video text2video \
  --prompt "A cat playing piano" \
  --num-frames 81 --frame-rate 8

# Step 2: The output includes a video_id. Poll for completion:
python3 scripts/agnes.py poll VIDEO_ID --download
```

### Create and Download an Image

```bash
python3 scripts/agnes.py image text2img \
  --prompt "Japanese garden in autumn, cinematic lighting" \
  --size "1920x1080" --output-dir ./wallpapers
```

### Structured Text Extraction

```bash
python3 scripts/agnes.py text \
  --prompt "Extract the name, date, and amount from this invoice: ..." \
  --json-output
```

### Stream a Long Generation

```bash
python3 scripts/agnes.py text \
  --prompt "Write a 500-word blog post about renewable energy" \
  --stream
```

### Batch Smoke Test

```bash
# Validate all modes before running a batch
python3 scripts/agnes.py smoke-test

# Then execute the batch
python3 scripts/agnes.py image text2img --prompt "Scene 1" --dry-run --no-translate
python3 scripts/agnes.py image text2img --prompt "Scene 2" --dry-run --no-translate
python3 scripts/agnes.py video text2video --prompt "Clip 1" --dry-run --no-translate
```

### Multi-Scene Video with Custom Settings

```bash
python3 scripts/agnes.py video keyframes \
  --prompt "A journey through a fantasy forest, emerging into a castle" \
  --width 1920 --height 1080 \
  --num-frames 241 --frame-rate 24 \
  --seed 777 --download --output-dir ./renders
```

---

## Advanced Usage

### Using with Tool Calls

```bash
agnes text \
  --prompt "What's the weather in Paris and London?" \
  --tools-json '[{"type":"function","function":{"name":"get_weather","description":"Get weather for a city","parameters":{"type":"object","properties":{"city":{"type":"string"}},"required":["city"]}}}]' \
  --tool-choice "auto"
```

### Chaining with Negative Prompts

```bash
agnes video text2video \
  --prompt "Peaceful ocean waves" \
  --negative-prompt "storm, lightning, ship, people, ugly, blurry" \
  --num-frames 161 --frame-rate 30 \
  --seed 123 --download
```

### Keyframe Animation Flow

```bash
# 1. Generate keyframe images
agnes image text2img --prompt "Frame 1: sunrise" --seed 1
agnes image text2img --prompt "Frame 2: noon" --seed 2
agnes image text2img --prompt "Frame 3: sunset" --seed 3

# 2. Interpolate between keyframes
agnes video keyframes \
  --image-url "file://./frame1.png" \
  --num-frames 81 --frame-rate 8 \
  --download
```
