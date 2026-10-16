# Personal Skills

[English](./README.md) | **简体中文**

一个用于集中维护个人小型、可复用 AI Agent Skill 的仓库。

这个仓库主要用来存放那些值得长期保留和重复使用、但又没有复杂到需要单独建立项目的 Skill。整体目标是让每个 Skill 都保持轻量、清晰、可组合，并且方便直接阅读和理解。

## 仓库定位

这里适合存放职责明确、可以在不同任务或项目中重复使用的小型 Skill。

如果某个项目已经有独立的架构设计、版本演进、发布流程或长期路线图，则更适合继续作为独立仓库维护，而不是放进这里。

## 基本原则

- **小而专注**：一个 Skill 尽量解决一个明确的问题。
- **可复用**：优先沉淀能够跨任务、跨项目重复使用的能力。
- **可组合**：多个简单 Skill 可以协作完成复杂任务，而不是不断膨胀成一个大型 Workflow。
- **可阅读**：Skill 的行为应该容易检查、理解和修改。
- **轻量化**：在真实需求出现之前，不提前引入复杂的基础设施。

## Skills

本仓库是以下个人 skills 的唯一维护来源：

- `daily-journal`：记录、增量修改和查询 Obsidian 日记，统计深度学习时长并惰性归档历史月份。通过 `$daily-journal` 调用并提供 Vault 路径。
- `learning`：根据意图选择学习工作流。
- `learning-plan`：用一个简短 Markdown 状态页记录长期方向、当前主线、学习书签、下一步和暂缓主题。
- `learning-library`：管理某个学习主题目录中的资料。
- `learning-learn`：讲解问题并保存持久化学习记录。
- `learning-review`：从已学资料中筛选代表性面试问题，记录练习价值和口述答案，确认后逐题练习。
- `learning-practice`：用小型练习应用已学内容。
- `learning-resources`：整理外部学习资料。
- `learning-organize`：把已探索的问题组织成主题文章。
- `learning-transcript`：将 ASR 文件整理为忠实讲稿。
- `yt-dlp-download`：读取目录，下载授权范围内的视频、音频、指定语言字幕，支持显式列表范围。
- `local-whisper`：使用 MLX/faster-whisper 本地转写，输出带时间戳文本，并可使用本地模型翻译字幕。
- `video-frames`：生成带时间标记的视频预览图，并提取指定时刻的截图。
- `video-notes`：保留完整讲述、讲者视角和原顺序，清理口语并配图，输出 Markdown 和离线 HTML；仅在明确要求时生成摘要。

在本仓库维护完整 skill 目录，包括可选的 `agents/` 元数据和 `references/`。不在其他项目或本机安装目录维护另一份副本。

`video-frames` 和 `video-notes` 需要 `uv`、Python 3.11–3.13（由 uv 管理）和 FFmpeg/FFprobe。锁定的 Python 环境位于用户缓存目录。工具不调用模型 API；调用智能体需具备文件读写、查看图片和执行命令的能力。下载、ASR 仍使用独立工具。当前设计、接入说明和历史验收统一从[文档导航](docs/README.md)进入。

## 安装

在本地仓库运行：

```bash
node bin/install.mjs
```

可以定向安装，重复使用 `--skill`；`--list` 仅读取列表：

```bash
node bin/install.mjs --skill local-whisper --skill yt-dlp-download
node bin/install.mjs --list
```

替换指定技能时，旧版本会先保存在 `$CODEX_HOME/skill-backups/`，新副本清除不再存在的旧文件，其他已安装技能保持原样：

```bash
node bin/install.mjs --skill local-whisper --skill yt-dlp-download --force
```

这些改动合并到 `main` 后，也可以从 GitHub 直接安装：

```bash
npx --yes github:200166shang/personal-skills
```

## 专用视频笔记智能体

`video_notes_operator` 接收 YouTube、哔哩哔哩、小鹅通链接或本地视频，默认生成忠实图文讲稿：保留原讲述顺序、讲者视角和完整内容，只清理口语及明确识别错误，输出 Markdown 和离线 HTML。需要归纳版时明确要求“总结／提炼”。它继承调用方模型，优先复用已有媒体和转写。

已安装 `yt-dlp-download`、`xiaoetong-download`、`local-whisper`、`video-frames`、`video-notes` 后运行：

```bash
node bin/install-video-notes-agent.mjs
```

安装器检查五个技能，将实际路径写入 `$CODEX_HOME/agents/video_notes_operator.toml`，不改其他智能体。支持 `--skills-dir PATH` 指定技能目录、`--dry-run` 预览配置、`--force` 在备份后只替换此智能体。本仓库提供 `yt-dlp-download`、`local-whisper`、`video-frames`、`video-notes` 和 `video-notes-batch`；小鹅通能力仍单独安装。智能体安装器不会自动安装依赖，本次迁移不会修改已有智能体配置。

以后可以说：“请用 video_notes_operator 把这个视频做成图文笔记：链接。”本地视频同样直接提供路径。课程页有多个课时时，先选择所需课时。[配置模板](agents/video_notes_operator.toml.in)维护来源路由和默认行为，具体操作规则继续由各 Skill 维护。配置采用[官方自定义智能体 TOML 形式](https://learn.chatgpt.com/docs/agent-configuration/subagents#custom-agents)；当前会话尚未发现新智能体时，可新开聊天后调用。

## 媒体技能维护

`local-whisper` 和 `yt-dlp-download` 与笔记技能集中在此维护。迁移保持原运行脚本、依赖版本和 CLI 行为不变，系统仍需 `uv` 及对应媒体工具。下载器隔离环境目前位于安装目录的 `runtime/.venv`；Whisper 使用共享 uv/模型缓存，首次使用按原机制准备依赖和模型。安装器不会复制虚拟环境、字节码或机器相关的 setup 标记。维护与迁移依据见[文档导航](docs/README.md)。

## License

`skills/local-whisper/LICENSE` 保留原 MIT 许可证；本次迁移不为整个仓库新增统一许可证，其他已有声明保持原样。

## 多课图文笔记

`video-notes-batch` 接收已准备的本地视频/转写清单，通过当前智能体为每课新建
写作者与独立审稿者；默认最多两个活跃子 Agent，支持任务领取、检查点、哈希绑定
审稿、恢复与课程目录页。下载/转写独立执行，不安装或修改智能体。
见[批量 Skill](skills/video-notes-batch/SKILL.md)。要求 macOS/Linux、Python 3.10+
及宿主的新上下文子 Agent 能力；单课继续组合使用 `video-notes`、`video-frames`。
Claude Code 提供适配说明，实际运行验证单独披露。

## 开发

从 [AGENTS.md](AGENTS.md) 和[文档导航](docs/README.md)开始。小修改验证后直接提 PR；跨 Skill 或多会话需求使用 GitHub Issues 中的 Spec 与自包含 Ticket，不为已完成工作补造任务。
