# Agnes-AI

[English](README.md) | [中文说明](README_zh.md)

基于 **Agnes AI API** 的零依赖 Python 命令行工具 (CLI)、SDK 与交互式 Web 测试操练场。支持免本地显卡一键生成文本、反推图片、生成艺术图像以及创作 AI 视频。

由 [AILab](https://github.com/1038lab) 构建与维护。

---

## 最新动态

- **v1.2.0 (2026-09-15)**：
  - 全面升级默认模型至 Agnes AI 新一代旗舰：`agnes-3.0-flash`、`agnes-image-2.5-flash` 与 `agnes-video-2.5-flash`。
  - 现代化视频生成：支持直接指定秒数时长 (`--seconds 4..12`)、画面比例 (`16:9`、`9:16`、`1:1` 等) 及清晰度档位 (`720P`、`1080P`、`1K`、`2K`)。
  - 终端视频渲染实时进度条展示 (`0%` ~ `100%`)。
  - Flash 模型智能兼容保护机制（自动规整为 720P 规避 400 错误）。
  - 保持对 `agnes-video-v2.0` 旧版帧数计算公式的完整向下兼容。

---

## 核心功能

- **文本大模型与视觉反推**：由 `agnes-3.0-flash` 驱动，具备 512K 上下文，支持高速对话与多模态图像反推理解。
- **图像生成与融合**：基于 `agnes-image-2.5-flash`，提供高质量文生图、图生图与风格融合。
- **AI 视频创作**：基于 `agnes-video-2.5-flash`，支持文生视频、首帧生视频、首尾帧过渡动画以及多模态素材参考。
- **智能自动翻译**：非英文提示词在请求前会自动智能翻译为英文，确保最优模型生成效果。
- **Web 交互操练场**：内置纯原生轻量 Web 界面（`examples/server.py`），直观预览各模式效果。
- **100% 零第三方依赖**：纯 Python 标准库开发，无需执行 `pip install` 即可开箱即用。

---

## 快速上手

### 1. 克隆代码仓库
```bash
git clone https://github.com/1038lab/Agnes-AI.git
cd Agnes-AI
```

### 2. 配置 API Key
在 [platform.agnes-ai.com](https://platform.agnes-ai.com) 免费注册获取 API Key：
```bash
export AGNES_API_KEY="你的API密钥"
```

### 3. 内容生成示例

#### 文本对话：
```bash
python3 scripts/agnes.py text --prompt "用一句话解释量子力学"
```

#### 图像生成：
```bash
python3 scripts/agnes.py image text2img --prompt "清晨薄雾中的高山湖泊，油画质感"
```

#### 视频生成：
```bash
python3 scripts/agnes.py video text2video --prompt "雄鹰在阿尔卑斯雪山顶峰上空翱翔，电影级光影" --seconds 5
```

---

## 本地交互式操练场 (Playground)

一键启动本地轻量 Web UI：
```bash
python3 examples/server.py
```
在浏览器中打开 **http://localhost:8888** 即可体验。

---

## 许可证

本项目遵循 GNU 通用公共许可证 v3.0 (GPL-3.0)。详见 [LICENSE](LICENSE)。
