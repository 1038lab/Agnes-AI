# Agnes-AI

[English](README.md) | [中文说明](README_zh.md)

![Agnes-AI](https://github.com/user-attachments/assets/4cbcaa09-e704-4c9b-90ba-b89b1b7fbc90)
面向 Agnes AI 模型的统一 Python 命令行工具集 —— 涵盖文本生成、图像理解反推、图像创作以及 AI 视频生成，零任何外部第三方依赖。

由 [AI Lab](https://github.com/1038lab) 构建与维护。本项目将 Agnes AI 的所有 API 端点封装进单个开箱即用的 `agnes.py` 中，提供合理的默认参数、智能自动翻译以及 dry-run 验证 —— 完全免安装（无需 `pip install`）。

**项目包含：**

```
scripts/agnes.py   →  命令行工具 CLI（文本、图像理解、生图、生视频）
SKILL.md           →  面向 AI 编程助手的 Agent Skill 指南
examples/server.py →  本地可视化测试操练场 (http://localhost:8888)
```

**为什么选择它？**

- **零依赖** — 纯 Python 标准库构建，下载即用
- **面向 Agent 设计** — 自带 SKILL.md 与可视化操练场，适配各类 AI 助手
- **智能自动翻译** — 用任意母语书写提示词，后台自动精准翻译
- **Dry-run 校验模式** — 真实调用前校验请求体结构，避免浪费额度
- **开箱即用的预设** — 尺寸、帧数、轮询机制均已配置优化
- **免费使用** — 无需本地独立显卡，只需一个 API Key 即可畅享云端算力

## 项目功能概览

- **文本大模型** — 对话、工具调用、流式输出，基于 `agnes-3.0-flash`
- **图像多模态理解** — 基于 `agnes-3.0-flash` 多模态视觉详细反推图片
- **图像生成** — 文生图、图生图、多图融合，基于 `agnes-image-2.5-flash`
- **AI 视频生成** — 文生视频、图生视频、首尾帧关键帧动画，基于 `agnes-video-2.5-flash`
- **智能自动翻译** — 非英文字符提示词自动翻译为地道英文
- **零依赖环境** — 仅使用 Python 标准库，零环境配置门槛

## 安装方法

仅需 Python 3.8+ 及 Agnes AI API Key。

```bash
# 克隆代码仓库
git clone https://github.com/1038lab/Agnes-AI.git
cd Agnes-AI

# （可选）将脚本目录添加至系统 PATH
export PATH="$PWD/scripts:$PATH"
```

## 获取 API Key

1. 前往 [https://apihub.agnes-ai.com](https://apihub.agnes-ai.com) 注册账号
2. 进入控制台的 **API Keys** 页面
3. 点击 **Create API Key** 并复制获取的 `sk-...` 密钥

## 快速上手

```bash
# 设置环境变量 API Key
export AGNES_API_KEY="你的API密钥"

# 或使用交互式一键保存设置
python scripts/agnes.py setup

# 文本对话生成
python scripts/agnes.py text --prompt "你好，请介绍一下你自己"

# 图像视觉反推与描述
python scripts/agnes.py text --prompt "详细描述这张图片的内容" --image-url photo.jpg

# 图像生成
python scripts/agnes.py image text2img --prompt "一只穿着宇航服的猫，数字艺术风格"

# 视频生成
python scripts/agnes.py video text2video --prompt "日落时分的海浪拍打礁石，电影级光影" --seconds 5
```

## CLI 详细使用指南

### 全局通用参数

| 参数 | 说明 |
|---|---|
| `--dry-run` | 仅打印请求体内容，不进行真实 API 调用 |
| `--no-translate` | 禁用非英文提示词的自动翻译 |
| `--verbose` | 向 stderr 输出详细调试信息 |

### `agnes setup`

交互式将你的 API Key 保存至当前系统的 Shell 配置文件（`~/.zshrc` / `~/.bashrc` / `~/.profile`）。

```bash
agnes setup
```

### `agnes text`

文本生成、大模型对话与多模态图像理解反推。

```bash
agnes text --prompt "写一首关于人工智能的优美短诗"
agnes text --prompt "详细描述这张照片的细节" --image-url photo.jpg
agnes text --system "分析画面艺术流派与笔触" --image-url painting.png
agnes text --prompt "用 Python 编写快速排序算法" --system "你是一名资深架构师"
agnes text --prompt "讲一个幽默的笑话" --stream
agnes text --prompt "计算机科学简史" --temperature 0.9 --max-tokens 2048
agnes text --prompt "1+1等于几？" --message "user: 2+2等于几？" --message "assistant: 4"
```

| 参数 | 说明 |
|---|---|
| `--prompt` | 提示词文本（提供 `--image-url` 时可选） |
| `--image-url` | 用于多模态理解的本地图片路径或公网 URL |
| `--system` | 系统提示词 System Prompt |
| `--message` | 多轮对话消息（可多次指定，格式为 `role: content`） |
| `--stream` | 开启打字机流式输出 |
| `--temperature` | 采样温度（默认 0.7） |
| `--top-p` | 核采样阈值（默认 0.9） |
| `--max-tokens` | 最大输出 token 数量（默认 4096） |
| `--tools-json` | JSON 格式的工具定义 |
| `--tool-choice` | 工具调用策略 |
| `--json-output` | 以结构化 JSON 格式输出结果 |
| `--model` | 模型名称（默认 `agnes-3.0-flash`） |

### `agnes image`

图像生成与画面融合。

![Agnes-AI Image](https://github.com/user-attachments/assets/dd371b71-e93a-4fb4-b98a-ad6ef4ffc78c)

```bash
# 文生图
agnes image text2img --prompt "夜晚赛博朋克风格的雨夜街景"

# 图生图（风格变换）
agnes image img2img --prompt "转换成水彩插画风格" --image-url https://example.com/photo.jpg

# 多图融合
agnes image compose --prompt "将这两张图片的元素融合"   --image-url https://example.com/img1.jpg   --image-url https://example.com/img2.jpg

# 自定义分辨率并保存至指定目录
agnes image text2img --prompt "古典油画质感肖像" --size "1816x1024" --output-dir ./output
```

| 参数 | 说明 |
|---|---|
| `mode` | 模式：`text2img` / `img2img` / `compose`（必填） |
| `--prompt` | 画面描述提示词（必填） |
| `--image-url` | 参考图片路径或 URL，可多次指定 |
| `--size` | 画面分辨率（默认 `1024x768`，支持各类宽高比例） |
| `--output-dir` | 本地下载目录（留空则直接打印图片 URL） |
| `--model` | 模型名称（默认 `agnes-image-2.5-flash`） |

### `agnes video`

AI 视频创作（支持终端自动轮询与结果下载）。

![Agnes-AI Video](https://github.com/user-attachments/assets/6ea1e190-412a-4950-913b-9f30d8aa7d1e)

```bash
# 文生视频（新一代 2.5-flash，指定秒数时长，自动轮询）
agnes video text2video --prompt "一只蝴蝶在花丛中轻盈飞舞" --seconds 5

# 图生视频（首帧赋予动态）
agnes video img2video --prompt "让人物带着自然呼吸感微笑着动起来" --image-url https://example.com/photo.jpg --seconds 5

# 关键帧过渡（首尾帧平滑变形动画）
agnes video keyframes --prompt "丝滑变形过渡动画"   --image-url https://example.com/frame1.jpg   --image-url https://example.com/frame2.jpg --seconds 6

# 现代画幅比例与清晰度（Flash 720P 兼容）
agnes video text2video --prompt "宏伟的高山瀑布"   --seconds 6 --aspect-ratio 16:9 --size 720P   --download --output-dir ./videos

# 兼容旧版帧数计算模式 (agnes-video-v2.0)
agnes video text2video --prompt "壮丽的海浪" --model agnes-video-v2.0   --width 1920 --height 1080 --num-frames 241 --frame-rate 30

# 禁用自动轮询，仅提交任务并返回 task_id
agnes video text2video --prompt "海边落日" --no-poll
```
https://github.com/user-attachments/assets/25af3d70-c242-4c10-9320-6107f23b9320

| 参数 | 说明 |
|---|---|
| `mode` | 模式：`text2video` / `img2video` / `keyframes` / `reference`（必填） |
| `--prompt` | 视频画面与动作描述提示词（必填） |
| `--image-url` | 参考图片路径或 URL，可多次指定 |
| `--audio-url` | 参考音频路径或 URL，可多次指定 |
| `--ref-video-url` | 参考视频路径或 URL，可多次指定 |
| `--model` | 视频模型名称（默认 `agnes-video-2.5-flash`，可选 `agnes-video-2.5`、`agnes-video-v2.0`） |
| `--seconds` | 视频时长秒数（默认 `5`，范围 4~12 秒） |
| `--aspect-ratio` | 画面比例（默认 `16:9`，可选：`16:9`, `9:16`, `1:1`, `4:3`, `3:4`, `21:9`） |
| `--size` | 分辨率档位（默认 `720P`，可选：`720P`, `1080P`, `1K`, `2K`） |
| `--width` | 视频宽度（像素，旧版 v2.0 专用） |
| `--height` | 视频高度（像素，旧版 v2.0 专用） |
| `--num-frames` | 视频总帧数（旧版 v2.0 专用，默认 121，满足 8n+1 且 ≤441） |
| `--frame-rate` | 视频帧率 FPS（旧版 v2.0 专用，默认 24，范围 1~60） |
| `--seed` | 随机种子（用于结果复现） |
| `--num-inference-steps` | 去噪步数（旧版 v2.0 专用） |
| `--negative-prompt` | 负向提示词（旧版 v2.0 专用） |
| `--no-poll` | 禁用自动轮询等待 |
| `--poll-interval` | 轮询查询间隔秒数（默认 5 秒） |
| `--timeout` | 最大超时秒数（默认 900 秒） |
| `--download` | 生成完成后自动下载到本地 |
| `--output-dir` | 本地视频下载保存目录 |

### `agnes poll`

根据 `video_id` 手动查询视频渲染状态。

```bash
agnes poll VIDEO_ID
agnes poll VIDEO_ID --poll-interval 5 --timeout 600
agnes poll VIDEO_ID --download --output-dir ./videos
```

### `agnes smoke-test`

在 dry-run 模式下运行端到端冒烟测试（不消耗任何额度）。

```bash
agnes smoke-test
agnes smoke-test --video-case text2video
```

## 功能特性

### 智能自动翻译

当提示词中包含非 ASCII 字符时，`agnes` 会在调用生图/生视频模型前自动使用 `agnes-3.0-flash` 将其翻译为专业的英文描述。如需原样发送，可使用 `--no-translate` 禁用。

```bash
# 自动翻译（默认启用）
agnes image text2img --prompt "一只橘猫在窗台上晒太阳"

# 等价于手动翻译后的英文调用：
agnes image text2img --prompt "An orange cat basking in the sun on a windowsill" --no-translate
```

### 媒体自动上传

在 `img2img`、`compose`、`img2video` 以及 `keyframes` 模式中，可以直接传入本地图片路径：工具会自动将其上传并获取可访问的公共临时 URL。

```bash
agnes image img2img --prompt "转换成卡通风格" --image-url ./my-photo.jpg
agnes video keyframes --prompt "场景过渡转换" --image-url ./start.png --image-url ./end.png
```

### 视频实时进度轮询

视频生成任务提交后默认自动进行轮询，并在终端实时打印渲染百分比进度（`0%` ~ `100%`）。添加 `--download` 参数可在完成后自动下载保存至本地。

### Dry-Run 校验模式

使用 `--dry-run` 可以完整预览即将发送给云端 API 的请求体 JSON，不产生任何真实调用：

```bash
agnes image text2img --prompt "test" --dry-run
agnes video text2video --prompt "test" --dry-run
```

## 平台使用额度对照

| 计划等级 | 价格 | 额度限制 |
|---|---|---|
| Free Access (免费版) | $0 | 公平使用原则配额（无每日硬性上限），基础 TPS 速率 |
| Starter | $2/月 | 每 5 小时 1500 次请求，更高并发 RPM |
| Plus | $5/月 | 每 5 小时 7500 次请求，更高并发 RPM |
| Pro | $25/月 | 每 5 小时 30000 次请求，更高并发 RPM |

详见 [常见错误代码参考手册](references/errors.md)。

## 更新日志 (Changelog)

| 日期 | 更新内容 |
|---|---|
| 2026-09-15 | 全面升级默认模型至 Agnes AI 新一代旗舰：`agnes-3.0-flash`、`agnes-image-2.5-flash`、`agnes-video-2.5-flash`；增加现代化视频秒数时长 (`--seconds`)、画面比例 (`--aspect-ratio`) 与分辨率档位 (`--size`)，支持终端实时渲染百分比进度条及 Flash 720P 保护，并完整保留对旧版 v2.0 的向下兼容 |
| 2026-07-09 | 新增图像理解功能（多模态 describe）；操练场 Text 选项卡中增加 Describe Image 子模式；CLI 预览占位符改用 `{image}`；修复结果展示区域文字居中问题；文档体系重构 |
| 2026-07 | 修复 Image API 传参结构；操练场尺寸选择重构为比例/分辨率/时长联合面板；修复结果区域排版；图像生成超时时间调整为 300s；优化异常处理 |

## 零第三方依赖理念

本项目完全使用 Python 标准库构建 —— 真正无需执行任何 `pip install`：

- `urllib.request` — 发送 HTTP 请求
- `argparse` — 命令行参数解析
- `json` — JSON 序列化与解析
- `os`, `sys`, `time`, `mimetypes` — 系统、时间与文件类型工具
- `re` — 正则匹配（setup 命令配置环境）

## 本地交互式操练场 (Playground)

无需命令行，纯图形化 Web 界面体验全部功能：

```bash
# 一键启动
open examples/start.command

# 或命令行启动
python3 examples/server.py
```

在浏览器中访问 http://localhost:8888 即可使用：
- **文本** — 对话 / 流式 / JSON 输出 / 图像反推描述
- **图像** — text2img / img2img / compose，所有分辨率带比例标注
- **视频** — text2video / img2video / 首尾关键帧，带帧率与时长实时预览

## 项目文件结构

```
Agnes-AI/
├── scripts/          # 核心 Python 功能模块
│   ├── agnes.py      # CLI 主入口与命令分发
│   ├── text.py       # 文本大模型生成
│   ├── image.py      # 图像生成与融合
│   ├── video.py      # 视频生成与轮询
│   ├── translate.py  # 智能自动翻译
│   └── media.py      # 媒体上传与下载
├── references/       # API 规范手册与错误码说明
├── examples/         # 本地 Playground Web UI 与后台服务
├── tests/            # 冒烟测试（无需额外测试框架）
└── agents/           # 针对各主流 Agent 的配置文件
```

## 环境变量说明

| 变量名 | 说明 |
|---|---|
| `AGNES_API_KEY` | 主要 API 密钥（首选） |
| `AGNES_API_TOKEN` | 备用 API 密钥 |
| `APIHUB_AGNES_API_KEY` | 备用 API 密钥 |
| `AGNES_API_BASE` | API 基础服务地址（默认 `https://apihub.agnes-ai.com`） |

## 开源许可证

本项目遵循 GNU 通用公共许可证 v3.0 (GPL-3.0)。详见 [LICENSE](LICENSE)。

## 实用链接

- [API 参考手册](references/api.md)
- [错误码对照表](references/errors.md)
- [Agnes AI 官网](https://agnes-ai.com)
- [Agnes API Hub](https://apihub.agnes-ai.com)
- [ComfyUI-Agnes-AI](https://github.com/1038lab/ComfyUI-Agnes-AI) — 基于本工具集构建的 ComfyUI 原生插件
