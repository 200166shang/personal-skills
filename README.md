# Personal Skills

**English** | [简体中文](./README.zh-CN.md)

A personal collection of small, reusable AI agent skills.

This repository is intended to be a lightweight home for practical skills that can be reused across AI coding agents and related workflows. The focus is on keeping each skill small, clear, composable, and easy to understand.

## Purpose

The repository is designed for personal skills that are useful enough to keep and reuse, but not large enough to justify a standalone project.

More complex projects with their own architecture, release cycle, or long-term roadmap should remain in separate repositories.

## Principles

- **Small** — each skill should solve a focused problem.
- **Reusable** — skills should be useful across multiple tasks or projects.
- **Composable** — simple skills should work well together instead of growing into one large workflow.
- **Readable** — the behavior of a skill should be easy to inspect and understand.
- **Lightweight** — avoid unnecessary infrastructure until real usage requires it.

## Skills

The repository is the source of truth for these personal skills:

- `daily-journal` — records, corrects, and reads Obsidian diaries with deep-learning time totals and lazy monthly archiving. Use `$daily-journal` with a supplied Vault path.
- `learning` — routes to an explicit learning workflow.
- `learning-plan` — keeps a small Markdown state page for long-term direction, current focus, resume bookmark, next step, and deferred topics.
- `learning-library` — manages materials saved for a Learning Workspace.
- `learning-learn` — teaches and records durable learning.
- `learning-review` — selects representative interview questions, records why they are worth practicing and their spoken answers, then practices them one at a time.
- `learning-practice` — applies saved understanding in a small exercise.
- `learning-resources` — curates external learning materials.
- `learning-organize` — organizes pursued questions into topic articles.
- `learning-transcript` — turns ASR files into faithful lecture scripts.
- `yt-dlp-download` — reads catalogs and downloads authorized video, audio or exact-language subtitles, including explicit playlist ranges.
- `local-whisper` — runs local MLX/faster-whisper ASR with timestamped outputs and optional local subtitle translation.
- `video-frames` — creates time-labelled video contact sheets and extracts selected screenshots.
- `video-notes` — preserves the complete lecture's voice, substance and order in illustrated Markdown and offline HTML; summarizes only on explicit request.

Maintain these skills in this repository. Their complete directories, including any
`agents/` metadata and `references/`, are managed as a unit.

The illustrated-note tools (`video-frames` and `video-notes`) require `uv`, Python 3.11–3.13 (managed by uv), and FFmpeg/FFprobe.
Their locked Python environments live in the user cache. They contain no model API
client; the calling agent needs file, image-viewing and command tools. Downloads and
ASR remain separate capabilities. Use the [documentation index](docs/README.md) for current designs, integration and dated validation.

## Install

From a local checkout, run:

```bash
node bin/install.mjs
```

Install only selected skills (repeat `--skill`), or list available names without writing files:

```bash
node bin/install.mjs --skill local-whisper --skill yt-dlp-download
node bin/install.mjs --list
```

To replace selected installed copies, preserving the previous versions under
`$CODEX_HOME/skill-backups/` and removing stale files from the new active copies:

```bash
node bin/install.mjs --skill local-whisper --skill yt-dlp-download --force
```

Once these changes are merged into `main`, the skills can also be installed directly from GitHub:

```bash
npx --yes github:200166shang/personal-skills
```

## Dedicated video-note agent

`video_notes_operator` turns a YouTube/Bilibili/Xiaoetong link or local video into a faithful illustrated lecture script in Markdown and offline HTML. A bare input requests the complete lecture in the speaker's voice and order, with speech cleanup rather than condensation. Ask explicitly for summary mode when desired. It inherits the calling model and reuses existing media/transcripts.

With `yt-dlp-download`, `xiaoetong-download`, `local-whisper`, `video-frames` and `video-notes` already installed, run:

```bash
node bin/install-video-notes-agent.mjs
```

The installer resolves skill paths into `$CODEX_HOME/agents/video_notes_operator.toml`, validates the five skill definitions and leaves other agents unchanged. Use `--skills-dir PATH` for another skill directory, `--dry-run` to inspect the resolved configuration, and `--force` to back up and replace only this agent. This repository supplies `yt-dlp-download`, `local-whisper`, `video-frames`, `video-notes` and `video-notes-batch`; install `xiaoetong-download` separately when needed. The agent installer does not install dependencies or change existing agents automatically.

Example request: “Use video_notes_operator to create illustrated notes from this video: URL.” A course page containing multiple lessons requires choosing the intended scope. The [agent template](agents/video_notes_operator.toml.in) owns the routing and defaults; detailed processing remains in the skills. Codex custom agents use [standalone TOML files](https://learn.chatgpt.com/docs/agent-configuration/subagents#custom-agents); start a new chat if the current session has not discovered the new agent.


## Batch illustrated notes

`video-notes-batch` dispatches prepared local lessons to fresh single-lesson writers
and independent reviewers. It uses the caller's existing agent, with at most two
active children, persistent claims, checkpoints, hash-bound reviews and a course
index. It does not download, transcribe or install an agent. Use download/ASR skills
separately, then provide a local manifest. Read the
[batch skill](skills/video-notes-batch/SKILL.md) for commands and host adapters.
Python 3.10+ on macOS/Linux and a host capable of fresh child contexts are required;
`video-notes` and `video-frames` remain the single-lesson production tools. Claude
Code has an adapter guide; live verification is reported separately.

## Media skill maintenance

`local-whisper` and `yt-dlp-download` are maintained here alongside the note skills.
Their runtime scripts, dependency versions and CLI behavior are unchanged by the
migration. `uv` and the required system media tools remain prerequisites; first-use
setup and model caching follow each skill's instructions. Download environments currently
live under the installed skill's `runtime/.venv`; Whisper uses shared uv/model caches.
The installer excludes environments, bytecode and setup markers from copied skills.
Maintenance, provenance and validation are indexed in [docs](docs/README.md).

## License

`skills/local-whisper/LICENSE` retains its original MIT license. No collection-wide
license is assigned by this migration; other existing license notices remain unchanged.

## Development

Start with [AGENTS.md](AGENTS.md) and the [documentation index](docs/README.md). Small edits go directly through verification and a PR; larger multi-session changes use specs and self-contained tickets in GitHub Issues. No retrospective issues are created for completed work.
