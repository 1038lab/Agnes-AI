# Agnes AI API Reference

**Base URL:** `https://apihub.agnes-ai.com`

**Authentication:** Bearer token via `Authorization` header

```
Authorization: Bearer <your-agnes-api-key>
```

**Models:**

| Model | ID | Endpoint |
|-------|-----|----------|
| Agnes 3.0 Flash (text & vision, Default) | `agnes-3.0-flash` | `/v1/chat/completions` |
| Agnes 2.5 Pro (text) | `agnes-2.5-pro` | `/v1/chat/completions` |
| Agnes 2.0 Flash (text, legacy) | `agnes-2.0-flash` | `/v1/chat/completions` |
| Agnes Image 2.5 Flash (image, Default) | `agnes-image-2.5-flash` | `/v1/images/generations` |
| Agnes Image 2.1 Flash (image, legacy) | `agnes-image-2.1-flash` | `/v1/images/generations` |
| Agnes Video 2.5 Flash (video 720P, Default) | `agnes-video-2.5-flash` | `/v1/videos` |
| Agnes Video 2.5 (video 720P–2K) | `agnes-video-2.5` | `/v1/videos` |
| Agnes Video v2.0 (video, legacy) | `agnes-video-v2.0` | `/v1/videos` |

---

## Text: Chat Completions

**Endpoint:** `POST /v1/chat/completions`

### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `model` | string | yes | — | Must be `agnes-3.0-flash` (or `agnes-2.5-pro`, `agnes-2.0-flash`) |
| `messages` | array | yes | — | Array of `{role, content}` objects |
| `temperature` | float | no | `0.7` | Sampling temperature (0–2) |
| `top_p` | float | no | `0.9` | Nucleus sampling threshold |
| `max_tokens` | int | no | `4096` | Maximum output tokens |
| `stream` | bool | no | `false` | Enable streaming (SSE) |
| `tools` | array | no | — | Tool definitions (JSON) |
| `tool_choice` | string | no | — | `"auto"`, `"none"`, or `{"type":"function","function":{"name":"..."}}` |

### Request

```json
{
  "model": "agnes-3.0-flash",
  "messages": [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Write a haiku about AI."}
  ],
  "temperature": 0.7,
  "max_tokens": 1024
}
```

### Response (non-streaming)

```json
{
  "id": "chatcmpl-xxx",
  "object": "chat.completion",
  "created": 1700000000,
  "model": "agnes-3.0-flash",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Silicon dreams wake,\nLearning patterns in the dark,\nA new dawn awaits."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 28,
    "completion_tokens": 12,
    "total_tokens": 40
  }
}
```

### Streaming (SSE)

Each line is `data: {...}` with a `delta` field instead of `message`. Terminates with `data: [DONE]`.

```
data: {"id":"...","object":"chat.completion.chunk","choices":[{"index":0,"delta":{"role":"assistant"},"finish_reason":null}]}

data: {"id":"...","object":"chat.completion.chunk","choices":[{"index":0,"delta":{"content":"Silicon"},"finish_reason":null}]}

data: {"id":"...","object":"chat.completion.chunk","choices":[{"index":0,"delta":{"content":" dreams"},"finish_reason":null}]}

...

data: [DONE]
```

### curl Example

```bash
curl -s https://apihub.agnes-ai.com/v1/chat/completions \
  -H "Authorization: Bearer $AGNES_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "agnes-3.0-flash",
    "messages": [{"role": "user", "content": "Hello!"}],
    "stream": true
  }'
```

```bash
# With tools
curl -s https://apihub.agnes-ai.com/v1/chat/completions \
  -H "Authorization: Bearer $AGNES_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "agnes-3.0-flash",
    "messages": [{"role": "user", "content": "What is the weather in Tokyo?"}],
    "tools": [
      {
        "type": "function",
        "function": {
          "name": "get_weather",
          "description": "Get weather for a city",
          "parameters": {
            "type": "object",
            "properties": {
              "location": {"type": "string"}
            },
            "required": ["location"]
          }
        }
      }
    ],
    "tool_choice": "auto"
  }'
```

---

## Image: Generations

**Endpoint:** `POST /v1/images/generations`

### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `model` | string | yes | — | Must be `agnes-image-2.5-flash` or `agnes-image-2.1-flash` |
| `prompt` | string | yes | — | Text description of the image |
| `n` | int | no | `1` | Number of images to generate |
| `size` | string | yes | — | Image dimensions (e.g. `1024x768`, `1024x1024`) |
| `return_base64` | bool | no | — | Set to `true` for Base64 output (text2img only) |
| `extra_body` | object | no | — | Advanced workflow parameters |
| `extra_body.image` | string[] | no* | — | Reference image URLs (array) |
| `extra_body.response_format` | string | no | — | Output format: `"url"` or `"b64_json"` (img2img) |

\* `extra_body.image` is required for `img2img` and `compose` modes.

**Important:** Do NOT place `response_format` at the top level. Use `extra_body.response_format` instead.

### Modes

| Mode | Description |
|------|-------------|
| `text2img` | Generate image from text prompt only |
| `img2img` | Transform a reference image using a text prompt |
| `compose` | Blend multiple reference images with a text prompt |

### Request (text2img)

```json
{
  "model": "agnes-image-2.5-flash",
  "prompt": "A serene mountain lake at sunset, digital art",
  "n": 1,
  "size": "1024x768"
}
```

### Request (img2img)

```json
{
  "model": "agnes-image-2.5-flash",
  "prompt": "Transform the scene into a rain-soaked cyberpunk night with neon reflections while preserving the original composition",
  "n": 1,
  "size": "1024x768",
  "extra_body": {
    "image": ["https://example.com/input-photo.jpg"],
    "response_format": "url"
  }
}
```

### Request (compose)

```json
{
  "model": "agnes-image-2.5-flash",
  "prompt": "Merge these two images",
  "n": 1,
  "size": "1024x768",
  "extra_body": {
    "image": ["https://example.com/image1.jpg", "https://example.com/image2.jpg"],
    "response_format": "url"
  }
}
```

### Response

```json
{
  "created": 1700000000,
  "data": [
    {
      "url": "https://apihub.agnes-ai.com/storage/images/abc123.png"
    }
  ]
}
```

### curl Example

```bash
curl -s https://apihub.agnes-ai.com/v1/images/generations \
  -H "Authorization: Bearer $AGNES_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "agnes-image-2.5-flash",
    "prompt": "A cat wearing a spacesuit, digital art",
    "n": 1,
    "size": "1024x768"
  }'
```

---

## Video: Create (Modern 2.5 Protocol)

**Endpoint:** `POST /v1/videos`

Video generation is asynchronous. Submit a job, then poll for the result.

### Parameters (Agnes Video 2.5 Series)

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `model` | string | yes | `agnes-video-2.5-flash` | `agnes-video-2.5-flash` or `agnes-video-2.5` |
| `prompt` | string | yes | — | Video motion and scene description |
| `mode` | string | no | `text` | Generation mode: `"text"`, `"img2video"`, `"keyframe"`, `"reference"` |
| `seconds` | string / int | no | `5` | Duration in seconds (`4` to `12`) |
| `size` | string | no | `720P` | Resolution: `720P`, `1080P`, `1K`, `2K` (*Flash model is restricted to 720P*) |
| `aspect_ratio` | string | no | `16:9` | Aspect ratio: `16:9`, `9:16`, `1:1`, `4:3`, `3:4`, `21:9` |
| `seed` | int | no | — | Random seed for reproducibility |
| `first_frame` | string | no | — | Base64 or URL for the starting frame (`img2video` / `keyframe`) |
| `last_frame` | string | no | — | Base64 or URL for the ending frame (`keyframe`) |
| `images` | array | no | — | Array of reference images (up to 5, `reference` mode) |
| `audios` | array | no | — | Array of reference audios (up to 3, `reference` mode) |
| `videos` | array | no | — | Array of reference videos (up to 3, `agnes-video-2.5` only) |

### Request (Modern 2.5 text2video)

```json
{
  "model": "agnes-video-2.5-flash",
  "prompt": "A beautiful sunset over the ocean, cinematic quality",
  "mode": "text",
  "seconds": "5",
  "size": "720P",
  "aspect_ratio": "16:9",
  "n": 1
}
```

### Request (Modern 2.5 img2video)

```json
{
  "model": "agnes-video-2.5-flash",
  "prompt": "Animate this portrait with natural subtle head movement",
  "mode": "img2video",
  "first_frame": "<BASE64_OR_IMAGE_URL>",
  "seconds": "5",
  "size": "720P",
  "aspect_ratio": "16:9",
  "n": 1
}
```

### Request (Modern 2.5 keyframe)

```json
{
  "model": "agnes-video-2.5-flash",
  "prompt": "Smooth morphing transition between two scene frames",
  "mode": "keyframe",
  "first_frame": "<BASE64_FIRST_FRAME>",
  "last_frame": "<BASE64_LAST_FRAME>",
  "seconds": "6",
  "size": "720P",
  "aspect_ratio": "16:9",
  "n": 1
}
```

### Request (Modern 2.5 reference)

```json
{
  "model": "agnes-video-2.5",
  "prompt": "Cinematic sequence guided by reference visual styles and audio rhythm",
  "mode": "reference",
  "images": ["<BASE64_IMG_1>", "<BASE64_IMG_2>"],
  "audios": ["<BASE64_AUDIO_1>"],
  "videos": ["<BASE64_VIDEO_1>"],
  "seconds": "8",
  "size": "1080P",
  "aspect_ratio": "16:9",
  "n": 1
}
```

### Modern 2.5 curl Example

```bash
# Submit modern video creation job
curl -s https://apihub.agnes-ai.com/v1/videos \
  -H "Authorization: Bearer $AGNES_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "agnes-video-2.5-flash",
    "prompt": "A rocket launching into space, cinematic lighting",
    "mode": "text",
    "seconds": "5",
    "size": "720P",
    "aspect_ratio": "16:9",
    "n": 1
  }'

# Poll for status with progress (0% to 100%)
curl -s "https://apihub.agnes-ai.com/agnesapi?video_id=VIDEO_ID&model_name=agnes-video-2.5-flash" \
  -H "Authorization: Bearer $AGNES_API_KEY"
```

---

## Video: Create (Legacy v2.0 Protocol)

**Endpoint:** `POST /v1/videos`

Video generation is asynchronous. Submit a job, then poll for the result.

### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `model` | string | yes | — | Must be `agnes-video-v2.0` |
| `prompt` | string | yes | — | Text description of the video |
| `image` | string | no* | — | Reference image URL for img2video (singular string) |
| `width` | int | no | `1152` | Video width in pixels |
| `height` | int | no | `768` | Video height in pixels |
| `num_frames` | int | no | `121` | Number of frames (≤441, must satisfy 8n+1) |
| `frame_rate` | int | no | `24` | Frames per second (1–60) |
| `seed` | int | no | — | Random seed for reproducibility |
| `num_inference_steps` | int | no | — | Number of denoising steps |
| `negative_prompt` | string | no | — | Things to avoid in the video |
| `extra_body` | object | no | — | Advanced workflow parameters |
| `extra_body.image` | string[] | no† | — | Reference image URLs (array, keyframes mode) |
| `extra_body.mode` | string | no | — | Set to `"keyframes"` for keyframe animation |

\* `image` is required for `img2video`.  
† `extra_body.image` is required for `keyframes`.

### Modes

| Mode | Request field | Description |
|------|---------------|-------------|
| `text2video` | *(none)* | Generate video from text prompt |
| `img2video` | `image` (1 URL, string) | Generate video from text + reference image |
| `keyframes` | `extra_body.image` (2+ URLs, array), `extra_body.mode: "keyframes"` | Keyframe animation |

### Frame Constraints

- `num_frames` must satisfy the formula `8n + 1` (e.g. 9, 17, 25, 33, 41, ..., 441)
- Maximum: 441 frames
- `frame_rate` range: 1–60
- Duration: `seconds = num_frames / frame_rate`

### Request (text2video)

```json
{
  "model": "agnes-video-v2.0",
  "prompt": "A beautiful sunset over the ocean, cinematic quality",
  "width": 1152,
  "height": 768,
  "num_frames": 121,
  "frame_rate": 24
}
```

### Request (img2video)

```json
{
  "model": "agnes-video-v2.0",
  "prompt": "The woman slowly turns around and looks back at the camera",
  "image": "https://example.com/image.png",
  "num_frames": 121,
  "frame_rate": 24
}
```

### Request (keyframes)

```json
{
  "model": "agnes-video-v2.0",
  "prompt": "Generate a smooth cinematic transition between the keyframes",
  "extra_body": {
    "image": [
      "https://example.com/keyframe1.png",
      "https://example.com/keyframe2.png"
    ],
    "mode": "keyframes"
  },
  "num_frames": 121,
  "frame_rate": 24
}
```

### Response

```json
{
  "id": "task_YOUR_TASK_ID",
  "task_id": "task_YOUR_TASK_ID",
  "video_id": "video_YOUR_VIDEO_ID",
  "object": "video",
  "model": "agnes-video-v2.0",
  "status": "queued",
  "progress": 0,
  "created_at": 1780457477,
  "seconds": "5.0",
  "size": "1280x768"
}
```

---

## Video: Poll Result

**Endpoint:** `GET /agnesapi?video_id={video_id}&model_name=agnes-video-v2.0`

Poll this endpoint to check video generation status.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `video_id` | string | yes | Video ID from the create response |
| `model_name` | string | yes | Must be `agnes-video-v2.0` |

### Response (progress)

```json
{
  "id": "task_YOUR_TASK_ID",
  "video_id": "video_YOUR_VIDEO_ID",
  "object": "video",
  "model": "agnes-video-v2.0",
  "status": "in_progress",
  "progress": 45,
  "error": null
}
```

### Response (completed)

```json
{
  "id": "task_YOUR_TASK_ID",
  "video_id": "video_YOUR_VIDEO_ID",
  "object": "video",
  "model": "agnes-video-v2.0",
  "status": "completed",
  "progress": 100,
  "seconds": "5.0",
  "size": "1280x768",
  "url": "https://platform-outputs.agnes-ai.space/videos/agnes-video-v2.0/video_xxxxxx.mp4",
  "error": null
}
```

### Response (failed)

```json
{
  "id": "task_YOUR_TASK_ID",
  "video_id": "video_YOUR_VIDEO_ID",
  "object": "video",
  "model": "agnes-video-v2.0",
  "status": "failed",
  "progress": 0,
  "error": "Details about the failure"
}
```

### curl Example

```bash
# Create text2video job
curl -s https://apihub.agnes-ai.com/v1/videos \
  -H "Authorization: Bearer $AGNES_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "agnes-video-v2.0",
    "prompt": "A rocket launching into space, cinematic",
    "width": 1152,
    "height": 768,
    "num_frames": 121,
    "frame_rate": 24
  }'

# Poll for result (replace VIDEO_ID with actual value)
curl -s "https://apihub.agnes-ai.com/agnesapi?video_id=VIDEO_ID&model_name=agnes-video-v2.0" \
  -H "Authorization: Bearer $AGNES_API_KEY"
```

---

## Response Status Fields

Video polling checks these status values:

| Status | Meaning |
|--------|---------|
| `completed` | Video ready, `url` field available |
| `failed` | Generation failed, check `error` field |
| `queued`, `in_progress`, *others* | Still generating, poll again |

---

## Notes

- All endpoints use standard HTTPS (443).
- Authentication is via Bearer token in the `Authorization` header.
- The API base URL can be overridden via the `AGNES_API_BASE` environment variable.
- Response formats follow OpenAI conventions for chat and image endpoints where applicable.
- For img2video the `image` field is a top-level **string** (singular URL), not an array.
- For keyframes, `image` is a string array inside `extra_body`, along with `mode: "keyframes"`.
- Do NOT use `image_urls`, `multi-image` mode, or top-level `response_format` — these are invalid for V2.0.
