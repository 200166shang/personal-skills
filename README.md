# Personal Skills

**English** | [简体中文](README.zh-CN.md)

Small, independent AI agent Skills for learning, journaling and illustrated video notes. Use a Skill directly or compose several capabilities through your existing agent.

- **Video materials**: download media/subtitles, transcribe locally, inspect frames and produce single-lesson or batch illustrated scripts.
- **Learning**: explore questions, maintain direction and materials, organize topics and practice interview explanations.
- **Journaling**: record Obsidian diary entries and learning time.

## Quick start

The installer requires Node.js 18+. Media tools also require `uv` and the system dependencies listed below.

```bash
git clone https://github.com/200166shang/personal-skills.git
cd personal-skills

# Example: install only the five video-note capabilities
node bin/install.mjs \
  --skill yt-dlp-download --skill local-whisper \
  --skill video-frames --skill video-notes --skill video-notes-batch
```

The installer writes to `$CODEX_HOME/skills`, defaulting to `~/.codex/skills`. Let the host discover the installed Skills, starting a new session if necessary, then give your agent a complete request:

```text
Use yt-dlp-download, local-whisper, video-frames and video-notes to turn
<video URL> into a faithful illustrated lecture script.
Reuse matching local media and subtitles first; acquire or transcribe missing inputs.
Preserve the complete lecture and deliver Markdown plus portable offline HTML.
```

With a local video and matching timestamped transcript already available, only `video-notes` and `video-frames` are needed for a single lesson. Reading all development plans is not a prerequisite for using them.

## Capabilities

### Video and transcription

| Skill | Use it for |
| --- | --- |
| [yt-dlp-download](skills/yt-dlp-download/SKILL.md) | Catalog inspection and authorized video, audio or exact-language subtitle downloads, including explicit playlist ranges |
| [local-whisper](skills/local-whisper/SKILL.md) | Local MLX/faster-whisper ASR with timestamped text, subtitles and JSON |
| [video-frames](skills/video-frames/SKILL.md) | Time-labelled contact sheets and original-frame captures at selected timestamps |
| [video-notes](skills/video-notes/SKILL.md) | Illustrated Markdown and offline HTML for one video with its matching transcript |
| [video-notes-batch](skills/video-notes-batch/SKILL.md) | Independent writing/review tasks for prepared local lessons, with progress, retry and recovery management |

Illustrated notes preserve original expression and order by default, cleaning speech and clear recognition errors. Request summary mode explicitly for condensation. Media-note delivery does not automatically register Learning materials.

### Learning

| Skill | Use it for |
| --- | --- |
| [learning](skills/learning/SKILL.md) | Choosing the appropriate learning capability from the learner's current intent |
| [learning-plan](skills/learning-plan/SKILL.md) | Goals, current direction, bookmarks and next steps |
| [learning-library](skills/learning-library/SKILL.md) | Saved materials for one learning topic |
| [learning-learn](skills/learning-learn/SKILL.md) | Root-guided exploration, durable explanations and resuming a learning route |
| [learning-review](skills/learning-review/SKILL.md) | Interview explanations, spoken practice and feedback on studied topics/modules |
| [learning-practice](skills/learning-practice/SKILL.md) | Applying existing learning through concrete tasks |
| [learning-resources](skills/learning-resources/SKILL.md) | Finding and curating materials for a topic or question |
| [learning-organize](skills/learning-organize/SKILL.md) | Organizing cross-question exploration into topic direction and carrying it forward |
| [learning-transcript](skills/learning-transcript/SKILL.md) | Complete Markdown lecture scripts from existing ASR, retaining substantive content and source order |

### Journaling

| Skill | Use it for |
| --- | --- |
| [daily-journal](skills/daily-journal/SKILL.md) | Recording, correcting and reading Obsidian diaries, tracking learning time and archiving older months |

## Common requests

**A course is already downloaded**: prepare matching transcripts with existing subtitles or `local-whisper`, then request a batch:

```text
Use video-notes-batch for lessons 2.1–2.5 in <local course directory>.
Check the video/transcript inventory first. Use fresh writers and independent
reviewers per lesson, with at most two active child agents. Produce faithful
illustrated scripts and a course index, preserving progress for recovery.
```

The batch accepts prepared local video/transcript manifests; download and ASR stay separate. Each writer composes `video-notes` and `video-frames`. Your existing agent arranges the stages and actually creates the children.

**Only a transcript is available and a text script is wanted**:

```text
Use learning-transcript on <transcript file or directory>. Preserve the original
order and substantive expression, clean speech errors and clear recognition
mistakes, and produce a complete Markdown lecture script.
```

**Interview practice or a learning log**:

```text
Use learning-review to help me explain <studied topic or module> clearly.
Use daily-journal to record 45 minutes studying STM32 GPIO today in <Obsidian Vault path>.
```

## Install and update

```bash
# Read available names without writing to the installation directory
node bin/install.mjs --list

# No selection installs all; existing copies are skipped by default
node bin/install.mjs

# Select other capabilities; repeat --skill as needed
node bin/install.mjs --skill daily-journal --skill learning-transcript

# Replace selected copies, backing up originals under $CODEX_HOME/skill-backups/
node bin/install.mjs --skill video-notes --skill video-frames --force
```

The GitHub package entry point is also available, for example:

```bash
npx --yes github:200166shang/personal-skills --skill daily-journal
```

Installation copies Skill files; it does not preload ASR models or change agent configurations. Runtime caches and machine-specific setup markers are excluded. Other hosts need their own Skill discovery/installation mechanism; this installer does not configure them automatically.

## Dependencies and host capabilities

| Capability | Requirements |
| --- | --- |
| Installer | Node.js 18+; defaults to the Codex Skill directory |
| Video download | `uv`, FFmpeg/FFprobe; locked yt-dlp environment prepared on first use |
| Local transcription | `uv`; backend packages/models prepared on first use, with audio decoding dependencies appropriate to that backend |
| Illustrated notes and frames | `uv`, FFmpeg/FFprobe; host file, command and actual image-viewing tools |
| Batch notes | macOS/Linux, Python 3.10+, and host support for fresh child-agent contexts |
| Optional subtitle translation | Ollama with an already-installed text model; separate from ASR |

First-time dependency/model preparation needs network access; offline use requires complete caches. Skills do not install system tools or GPU drivers. Media access depends on normal platform permissions; Xiaoe/Xiaoetong uses the separately installed `xiaoetong-download` Skill.

Batch execution has been exercised in Codex. Claude Code has a dispatch adapter guide but no corresponding live validation record. General Skill rules can be reused; child-agent interfaces, image viewing and permissions must be checked in the actual host.

## Optional single-lesson agent

The repository retains a Codex [video_notes_operator template](agents/video_notes_operator.toml.in) for users who want a named entry point. It is optional and handles single lessons; batch production uses your current agent with `video-notes-batch` and does not require this template.

Install its five required Skills first, including the external `xiaoetong-download`:

```bash
node bin/install-video-notes-agent.mjs --dry-run
node bin/install-video-notes-agent.mjs
```

The installer checks dependencies and writes the dedicated configuration. Run `--help` for path options and backed-up replacement. It does not install missing Skills automatically.

## Development and documentation

This collection is the maintained Skill source. Keep capabilities small and independent, compose them through the calling agent, and treat installed directories as deployments. Models, media and runtime state stay outside the repository.

- [Documentation index](docs/README.md): current designs, important decisions, research and dated verification.
- [AGENTS.md](AGENTS.md): development-agent conventions and conditional reading pointers.

Small changes go directly through verification and a PR. Cross-Skill or multi-session work starts with a spec and self-contained tickets, then follows their dependencies. Find the full development conventions through the documentation index.

## License

[local-whisper's original MIT license](skills/local-whisper/LICENSE) is retained. No collection-wide license has been assigned to the remaining content; existing notices continue to apply.
