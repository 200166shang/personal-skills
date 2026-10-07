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

The repository is the source of truth for the personal Learning skills:

- `learning` — routes to an explicit learning workflow.
- `learning-plan` — keeps a small Markdown state page for long-term direction, current focus, resume bookmark, next step, and deferred topics.
- `learning-learn` — teaches and records durable learning.
- `learning-review` — builds a fixed-scope technical interview bank from saved or supplied learning material and drills it one question at a time.
- `learning-practice` — applies saved understanding in a small exercise.
- `learning-resources` — curates external learning materials.
- `learning-organize` — organizes pursued questions into topic articles.
- `learning-transcript` — turns ASR files into faithful lecture scripts.

Maintain these skills in this repository. Their complete directories, including any
`agents/` metadata and `references/`, are managed as a unit.

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

## License

License information will be added later.
