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
- `video-frames` — creates time-labelled video contact sheets and extracts selected screenshots.
- `video-notes` — preserves the complete lecture's voice, substance and order in illustrated Markdown and offline HTML; summarizes only on explicit request.

Maintain these skills in this repository. Their complete directories, including any
`agents/` metadata and `references/`, are managed as a unit.

The video skills require `uv`, Python 3.11–3.13 (managed by uv), and FFmpeg/FFprobe.
Their locked Python environments live in the user cache. They contain no model API
client; the calling agent needs file, image-viewing and command tools. Downloads and
ASR remain separate capabilities. See [media operator integration](research/media-operator-video-notes.md)
for the pipeline and [case validation](research/video-notes-case-validation.md) for a tested example.

## Install

From a local checkout, run:

```bash
node bin/install.mjs
```

To replace installed copies and remove files no longer present in this repository:

```bash
node bin/install.mjs --force
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

The installer resolves skill paths into `$CODEX_HOME/agents/video_notes_operator.toml`, validates the five skill definitions and leaves other agents unchanged. Use `--skills-dir PATH` for another skill directory, `--dry-run` to inspect the resolved configuration, and `--force` to back up and replace only this agent. This repository supplies the two video skills; install the acquisition/ASR skills separately if missing. It does not download them automatically.

Example request: “Use video_notes_operator to create illustrated notes from this video: URL.” A course page containing multiple lessons requires choosing the intended scope. The [agent template](agents/video_notes_operator.toml.in) owns the routing and defaults; detailed processing remains in the skills. Codex custom agents use [standalone TOML files](https://learn.chatgpt.com/docs/agent-configuration/subagents#custom-agents); start a new chat if the current session has not discovered the new agent.

## License

License information will be added later.
