# local-whisper-skill

面向 AI 编码 Agent 的本地语音识别 Skill：针对 Apple Silicon 自动选择后端，稳定导出 TXT/SRT/VTT/JSON，支持词级时间戳、混合语言处理，并可通过 Ollama 在本地翻译字幕且保持原时间轴。

统一维护位置为 [`personal-skills`](https://github.com/200166shang/personal-skills/tree/main/skills/local-whisper)，原仓库历史已保留在集合仓库中。

## 一行安装

```bash
npx skills add 200166shang/personal-skills --skill local-whisper -g -y
```

首次运行会通过 `uv` 解析运行依赖并下载模型；以后复用全局缓存，不会把虚拟环境或数 GB 模型塞进转写结果目录。

## 设计结论

- Apple Silicon 常规转写默认使用 MLX，利用 Apple GPU 和统一内存。
- faster-whisper 保留为兼容后端，并用于更明确的混合语言窗口模式；它在 Mac 上只使用 CPU，不支持 MPS、Metal、Core ML 或 ANE。
- Whisper 原生 `translate` 只支持“非英语语音 → 英文”。英语语音转中文采用“ASR → 本地文本翻译”，逐段复用原时间戳。

直接命令与 Agent 工作流见 [SKILL.md](./SKILL.md)。
