# Personal Skills

[English](README.md) | **简体中文**

一组小而独立、可组合的 AI Agent Skills，集中维护学习辅助、日记记录和视频图文笔记能力。支持直接调用某个 Skill，也支持由现有智能体组合使用。

- **视频资料**：下载视频或字幕、本地转写、提取画面，制作单课或多课图文讲稿。
- **学习辅助**：围绕问题学习，维护方向、资料和主题，练习面试表达。
- **日记记录**：在 Obsidian 中记录日记和学习时长。

## 快速开始

需要 Node.js 18 或更新版本运行安装器。媒体能力另外需要 `uv` 及对应系统工具，见下方依赖表。

```bash
git clone https://github.com/200166shang/personal-skills.git
cd personal-skills

# 例如：只安装视频笔记相关的五个 Skill
node bin/install.mjs \
  --skill yt-dlp-download --skill local-whisper \
  --skill video-frames --skill video-notes --skill video-notes-batch
```

安装器默认写入 `$CODEX_HOME/skills`，未设置时为 `~/.codex/skills`。让宿主重新发现已安装的 Skills，必要时新开会话，然后向你的智能体提出完整请求：

```text
请组合使用 yt-dlp-download、local-whisper、video-frames 和 video-notes，
把这个视频制作成忠实图文讲稿：<视频链接>。
优先复用匹配的视频和字幕，缺少时再下载或转写。
保留完整讲述，输出 Markdown 和可离线阅读的 HTML。
```

已有本地视频和匹配的时间戳转写时，可以只安装并使用 `video-notes`、`video-frames`。详细开发方案不必在使用前通读。

## 能力目录

### 视频与转写

| Skill | 适合的任务 |
| --- | --- |
| [yt-dlp-download](skills/yt-dlp-download/SKILL.md) | 读取目录，下载授权范围内的视频、音频或指定语言字幕，支持显式播放列表范围 |
| [local-whisper](skills/local-whisper/SKILL.md) | 使用 MLX/faster-whisper 本地转写，输出带时间戳的文本、字幕和 JSON |
| [video-frames](skills/video-frames/SKILL.md) | 浏览带时间标记的联系表，提取指定时刻的单帧截图 |
| [video-notes](skills/video-notes/SKILL.md) | 将一课视频和匹配转写制作成配图 Markdown 与离线 HTML |
| [video-notes-batch](skills/video-notes-batch/SKILL.md) | 为多课本地素材分发独立写作、审稿任务，管理进度、重试和恢复 |

图文笔记默认保留原表达与顺序，只清理口语及明确识别错误；需要提炼时明确要求总结模式。媒体笔记交付不自动触发 Learning 资料登记。

### 学习辅助

| Skill | 适合的任务 |
| --- | --- |
| [learning](skills/learning/SKILL.md) | 不确定用哪个学习能力时，按当前意图选择入口 |
| [learning-plan](skills/learning-plan/SKILL.md) | 记录目标、当前方向、书签和下一步 |
| [learning-library](skills/learning-library/SKILL.md) | 管理一个学习主题中保存的资料 |
| [learning-learn](skills/learning-learn/SKILL.md) | 围绕根问题逐步探索，保存解释并恢复学习路线 |
| [learning-review](skills/learning-review/SKILL.md) | 为已学主题准备面试表达，进行口述练习与反馈 |
| [learning-practice](skills/learning-practice/SKILL.md) | 用具体任务练习已有学习内容 |
| [learning-resources](skills/learning-resources/SKILL.md) | 为主题或问题寻找、筛选资料 |
| [learning-organize](skills/learning-organize/SKILL.md) | 将跨问题的探索组织成主题方向，并逐步执行整理 |
| [learning-transcript](skills/learning-transcript/SKILL.md) | 将已有 ASR 转录整理为保留完整内容和原顺序的 Markdown 讲稿 |

### 日记

| Skill | 适合的任务 |
| --- | --- |
| [daily-journal](skills/daily-journal/SKILL.md) | 记录、修正和查询 Obsidian 日记，统计学习时长并归档历史月份 |

## 常见用法

**已经下载好一套课程**：先用已有字幕或 `local-whisper` 准备匹配转写，再交给批量笔记能力：

```text
使用 video-notes-batch 处理 <本地课程目录> 中的 2.1–2.5。
先核对视频与转写清单；每课使用新的写作和独立审稿上下文，
最多同时运行两个子 Agent。生成忠实图文讲稿和课程目录页，保留进度以便恢复。
```

批量层接收已准备的本地视频/转写清单，不负责下载或 ASR。每课写作者组合使用 `video-notes` 与 `video-frames`；现有智能体负责安排阶段和实际创建子 Agent。

**只有转录文本，需要文字稿**：

```text
使用 learning-transcript 整理 <转录文件或目录>，保留原讲述顺序和有信息量的表达，
清理口误及明确识别错误，输出完整 Markdown 讲稿。
```

**准备面试或记录学习**：

```text
使用 learning-review，针对 <已学主题或模块> 帮我练习清楚地讲解。
使用 daily-journal，在 <Obsidian Vault 路径> 记录今天学习 STM32 GPIO 45 分钟。
```

## 安装与更新

```bash
# 查看可用名称；不写入安装目录
node bin/install.mjs --list

# 不带选择参数则安装全部；已有同名副本默认跳过
node bin/install.mjs

# 按需安装其他能力，可重复指定 --skill
node bin/install.mjs --skill daily-journal --skill learning-transcript

# 更新指定副本，旧版本先备份到 $CODEX_HOME/skill-backups/
node bin/install.mjs --skill video-notes --skill video-frames --force
```

也可以使用 GitHub 包入口，例如：

```bash
npx --yes github:200166shang/personal-skills --skill daily-journal
```

安装器只复制 Skill 文件，不会预先下载 ASR 模型或修改智能体配置；运行缓存和机器相关 setup 标记不随源码复制。其他宿主需按自己的 Skill 发现机制安装，这个安装器不会自动配置它们。

## 依赖与宿主能力

| 能力 | 要准备什么 |
| --- | --- |
| 安装器 | Node.js 18+；默认安装目标为 Codex 的 Skill 目录 |
| 视频下载 | `uv`、FFmpeg/FFprobe；首次启动自动准备锁定的 yt-dlp 环境 |
| 本地转写 | `uv`；首次使用准备后端依赖和模型，音频解码依赖按后端要求配置 |
| 图文与截图 | `uv`、FFmpeg/FFprobe；宿主能读写文件、运行命令并实际查看图片 |
| 批量笔记 | macOS/Linux、Python 3.10+，以及宿主创建独立新上下文子 Agent 的能力 |
| 可选字幕翻译 | Ollama 和已安装的文本模型；与 ASR 分开处理 |

模型和运行依赖首次准备需要网络，缓存后能否离线运行取决于所需资源是否齐全。系统工具和 GPU 驱动不由 Skill 自动安装。视频读取取决于正常的平台访问权限，小鹅通使用另行安装的 `xiaoetong-download`。

批量流程已在 Codex 验证；Claude Code 提供调度适配说明，尚无对应实测记录。通用 Skill 规则可复用，子 Agent 接口、图片查看能力和权限需要在实际宿主确认。

## 可选：专用单课 Agent

如果希望有固定名称入口，仓库保留了 Codex 的 [video_notes_operator 模板](agents/video_notes_operator.toml.in)。它是可选的单课入口；批量制作使用当前智能体与 `video-notes-batch`，不要求安装这个模板。

安装前需具备模板要求的五个 Skill，包括仓库外的 `xiaoetong-download`：

```bash
node bin/install-video-notes-agent.mjs --dry-run
node bin/install-video-notes-agent.mjs
```

安装器会检查依赖并写入专用配置；用 `--help` 查看路径选项及带备份的替换方式。它不会自动安装缺失的 Skill。

## 开发与文档

本仓库是这些 Skills 的源码维护位置。保持能力小而独立，通过调用智能体组合；安装目录是部署副本，模型、媒体和运行状态留在仓库外。

- [文档导航](docs/README.md)：当前设计、关键决策、调研与有日期的验收记录。
- [AGENTS.md](AGENTS.md)：面向开发 Agent 的约定和按需阅读入口。

小修改验证后直接提 PR；跨 Skill 或多会话需求先形成 Spec 和自包含 Ticket，再按依赖推进。完整开发约定从文档导航进入。

## 许可证

[local-whisper 的 MIT 许可证](skills/local-whisper/LICENSE) 保留原声明。本仓库尚未为其他内容指定统一许可证，各已有声明继续适用。
