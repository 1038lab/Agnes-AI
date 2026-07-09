# Agnes-AI

Agnes AI 模型的统一 Python CLI — 文本生成、图片理解、图片生成、视频生成，
零外部依赖。

由 [AI Lab](https://github.com/1038lab) 开发。本仓库将所有 Agnes API 端点封装为
一个 `agnes.py`，提供智能默认值、自动翻译和 dry-run 验证，
无需 pip install。

**仓库内容：**

```
scripts/agnes.py   →  CLI（文本、图片理解、图片、视频）
SKILL.md           →  AI 编程助手 Skill
examples/server.py →  Web Playground（http://localhost:8888）
```

**为什么用它？**

- **零依赖** — 仅用 Python 标准库，开箱即用
- **Agent 就绪** — 附带 SKILL.md 和 Playground
- **自动翻译** — 中文 prompt 直接写
- **Dry-run 模式** — 先验证再消耗额度
- **智能默认值** — 尺寸、帧数、轮询策略预配好
- **免费使用** — 不需要 GPU，只需要 API Key

## 项目简介

- **文本生成** — 对话、工具调用、流式输出
- **图片理解** — 用 agnes-2.0-flash 描述图片内容
- **图片生成** — text2img、img2img、多图 compose
- **视频生成** — text2video、img2video、keyframe 动画
- **自动翻译** — 中文 prompt 自动转为英文
- **零依赖** — 仅用 Python 标准库

## 安装

只需要 Python 3.8+ 和 Agnes AI API Key。

```bash
# 下载或克隆仓库后，直接使用
git clone https://github.com/your-org/Agnes-AI.git
cd Agnes-AI

# 将脚本目录添加到 PATH（可选）
export PATH="$PWD/scripts:$PATH"
```

## 获取 API Key

1. 访问 [https://apihub.agnes-ai.com](https://apihub.agnes-ai.com) 注册账号
2. 登录后进入 **API Keys** 页面
3. 点击 **Create API Key**，复制生成的 `sk-...` 密钥

## 快速开始

```bash
# 设置 API Key
export AGNES_API_KEY="your-key-here"

# 或使用交互式设置
python scripts/agnes.py setup

# 生成文本
python scripts/agnes.py text --prompt "你好，请介绍一下你自己"

# 描述图片
python scripts/agnes.py text --prompt "详细描述这张图片" --image-url photo.jpg

# 生成图像
python scripts/agnes.py image text2img --prompt "一只穿着宇航服的猫，数字艺术"

# 生成视频
python scripts/agnes.py video text2video --prompt "日落时分的海浪，电影画质"
```

## CLI 命令大全

### 全局选项

| 选项 | 说明 |
|------|------|
| `--dry-run` | 只打印请求，不调用 API |
| `--no-translate` | 禁用自动翻译 |
| `--verbose` | 打印调试信息到 stderr |

### `agnes setup`

将 API Key 写入 shell 配置文件 (`~/.zshrc` / `~/.bashrc` / `~/.profile`)。

```bash
agnes setup
```

### `agnes text`

文本 / 对话生成 & 图片理解（多模态）。

```bash
# 文本对话
agnes text --prompt "写一首关于 AI 的诗"
agnes text --prompt "用 Python 写一个排序算法" --system "你是一位资深工程师"
agnes text --prompt "讲个笑话" --stream
agnes text --prompt "回顾历史" --temperature 0.9 --max-tokens 2048
agnes text --prompt "1+1=?" --message "user: 2+2=?" --message "assistant: 4"

# 图片描述（多模态）
agnes text --prompt "详细描述这张图片" --image-url photo.jpg
agnes text --system "分析这张画的艺术风格" --image-url painting.png
agnes text --image-url img1.jpg --image-url img2.jpg --prompt "对比这两张图"
```

| 参数 | 说明 |
|------|------|
| `--prompt` | 提示词（使用 `--image-url` 时可省略） |
| `--image-url` | 图片文件路径或 URL（多模态理解） |
| `--system` | 系统提示词 |
| `--message` | 多轮对话消息（可多次使用，格式 `role: content`） |
| `--stream` | 流式输出 |
| `--temperature` | 温度参数 (默认 0.7) |
| `--top-p` | Top-p 采样 (默认 0.9) |
| `--max-tokens` | 最大 token 数 (默认 4096) |
| `--tools-json` | 工具定义 JSON |
| `--tool-choice` | 工具选择策略 |
| `--json-output` | JSON 格式输出 |

### `agnes image`

图像生成。

```bash
# 文生图
agnes image text2img --prompt "赛博朋克风格的都市夜景"

# 图生图
agnes image img2img --prompt "改成水彩画风格" --image-url https://example.com/photo.jpg

# 多图融合
agnes image compose --prompt "融合这两张图" \
  --image-url https://example.com/img1.jpg \
  --image-url https://example.com/img2.jpg

# 指定尺寸和输出目录
agnes image text2img --prompt "一幅油画" --size "1920x1080" --output-dir ./output
```

| 参数 | 说明 |
|------|------|
| `mode` | 模式：`text2img` / `img2img` / `compose`（必填） |
| `--prompt` | 提示词（必填） |
| `--image-url` | 参考图片 URL（可多次使用） |
| `--size` | 图片尺寸 (默认 `1024x768`) |
| `--output-dir` | 下载目录（不指定则只打印 URL） |

### `agnes video`

视频生成。支持自动轮询和下载。

```bash
# 文生视频（自动轮询）
agnes video text2video --prompt "一只蝴蝶在花丛中飞舞"

# 图生视频
agnes video img2video --prompt "让这张图动起来" --image-url https://example.com/photo.jpg

# 首尾帧动画
agnes video keyframes --prompt "动画序列" \
  --image-url https://example.com/frame1.jpg \
  --image-url https://example.com/frame2.jpg

# 自定义参数
agnes video text2video --prompt "瀑布" \
  --width 1920 --height 1080 \
  --num-frames 241 --frame-rate 30 \
  --seed 42 --negative-prompt "模糊, 噪声" \
  --download --output-dir ./videos

# 不轮询，只获取 task_id
agnes video text2video --prompt "日落" --no-poll
```

| 参数 | 说明 |
|------|------|
| `mode` | 模式：`text2video` / `img2video` / `keyframes`（必填） |
| `--prompt` | 提示词（必填） |
| `--image-url` | 参考图片 URL（可多次使用） |
| `--width` | 视频宽度 (默认 1152) |
| `--height` | 视频高度 (默认 768) |
| `--num-frames` | 帧数 (默认 121，需满足 8n+1，最大 441) |
| `--frame-rate` | 帧率 (默认 24，范围 1–60) |
| `--seed` | 随机种子 |
| `--num-inference-steps` | 推理步数 |
| `--negative-prompt` | 负面提示词 |
| `--no-poll` | 不自动轮询 |
| `--poll-interval` | 轮询间隔秒数 (默认 10) |
| `--timeout` | 超时秒数 (默认 900) |
| `--download` | 完成后下载到本地 |
| `--output-dir` | 输出目录 |

### `agnes poll`

查询视频生成状态。

```bash
agnes poll VIDEO_ID
agnes poll VIDEO_ID --poll-interval 5 --timeout 600
agnes poll VIDEO_ID --download --output-dir ./videos
```

### `agnes smoke-test`

运行端到端冒烟测试（dry-run 模式，不调用实际 API）。

```bash
agnes smoke-test
agnes smoke-test --video-case text2video
```

## 功能展示

### 自动翻译

当 prompt 包含非英文字符时，`agnes` 会自动调用 `agnes-2.0-flash` 将其翻译为英文，再发送给对应的生成模型。可通过 `--no-translate` 禁用。

```bash
# 自动翻译（默认）
agnes image text2img --prompt "一只橘猫在窗台上晒太阳"

# 等价于手动翻译后
agnes image text2img --prompt "An orange cat basking in the sun on a windowsill" --no-translate
```

### 自动媒体上传

`img2img`、`compose`、`img2video`、`keyframes` 模式支持本地图片路径：系统会自动上传到 Litterbox 获取公网 URL。

```bash
agnes image img2img --prompt "改成卡通风格" --image-url ./my-photo.jpg
agnes video keyframes --prompt "动画过渡" --image-url ./frame1.png --image-url ./frame2.png
```

### 视频自动轮询

视频生成默认自动轮询结果，完成后可选自动下载。无需手动调用 poll。

### Dry-Run 模式

使用 `--dry-run` 查看实际发送的请求体，不调用 API：

```bash
agnes image text2img --prompt "test" --dry-run
agnes video text2video --prompt "test" --dry-run
```

## 使用限制

| 计划 | 价格 | 限制 |
|------|------|------|
| 免费 (Free Access) | $0 | 公平使用配额（无硬性上限），基础 TPS 限速 |
| Starter | $2/月 | 每5小时 1500 次请求，更高 RPM |
| Plus | $5/月 | 每5小时 7500 次请求，更高 RPM |
| Pro | $25/月 | 每5小时 30000 次请求，更高 RPM |

免费账号无每日硬性配额限制，但受公平使用原则约束。付费计划可通过 [platform.agnes-ai.com](https://platform.agnes-ai.com) 订阅获得更高并发和优先级。

## 更新记录

| 日期 | 内容 |
|------|------|
| 2026-07-09 | 新增图片理解（multimodal describe）；Playground Text 下新增 Describe Image 子模式；CLI 预览占位符改用 `{image}`（避免 innerHTML 吞标签）；修复输出区文字居中问题；补全 API Key 申请流程；README 重写，改名 Agnes-AI，加 AILab 署名 |
| 2026-07 | 修复 Image API 格式：img2img/compose 的 `image` 字段改到顶层（非 `extra_body` 内），`response_format` 保留在 `extra_body`；Playground 尺寸选择改为比例/分辨率/时长（Pavo AI 风格）；Playground 结果区修复：max-width 限制、height auto 保持比例、flex 去掉避免图片变形；图片超时 120s → 300s；`text.py` `resp.read()` 移入 try 块 |

## 零依赖说明

整个项目仅使用 Python 标准库，无任何第三方依赖：

- `urllib.request` — HTTP 请求
- `argparse` — 命令行参数
- `json` — JSON 序列化
- `os`, `sys`, `time`, `mimetypes` — 系统工具
- `re` — 字符串处理（setup 命令）

## 交互式 Playground

提供 Web UI 可视化操作所有功能，无需命令行：

```bash
# 一键启动
open examples/start.command

# 或手动启动
python3 examples/server.py
```

打开 http://localhost:8888 后可见：
- **文本** — 对话 / 流式 / JSON 输出 / 图片描述
- **图像** — text2img / img2img / compose，全部分辨率带比例标注
- **视频** — text2video / img2video / 首尾帧动画，支持 FPS 和时长预览

## 项目结构

```
Agnes-AI/
├── scripts/          # 核心 Python 模块
│   ├── agnes.py      # CLI 入口与命令分发
│   ├── text.py       # 文本生成
│   ├── image.py      # 图像生成
│   ├── video.py      # 视频生成（含轮询）
│   ├── translate.py  # 自动翻译
│   └── media.py      # 媒体上传与下载
├── references/       # API 参考文档
├── tests/            # 测试
└── agents/           # Agent 配置文件
```

## 环境变量

| 变量 | 说明 |
|------|------|
| `AGNES_API_KEY` | API Key（首选） |
| `AGNES_API_TOKEN` | API Key 备选 |
| `APIHUB_AGNES_API_KEY` | API Key 备选 |
| `AGNES_API_BASE` | API 基础 URL（默认 `https://apihub.agnes-ai.com`） |

## 许可证

GNU General Public License v3.0。详见 [LICENSE](LICENSE)。

## 链接

- [API 参考文档](references/api.md)
- [错误代码](references/errors.md)
- [Agnes AI](https://agnes-ai.com)
- [API Hub](https://apihub.agnes-ai.com)
- [ComfyUI-Agnes-AI](https://github.com/1038lab/ComfyUI-Agnes-AI) — 基于本工具包开发的 ComfyUI 自定义节点
