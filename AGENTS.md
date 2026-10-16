# Working in personal-skills

Maintain reusable Skills in `skills/`; installed copies are generated artifacts. Keep runtime media, transcripts, models, credentials and job state outside this repository. The user's agent configuration is separate from repository templates.

## Development

Use a separate worktree and `codex/` branch for changes, then submit a PR. Merge or publish only when requested. For a small change, implement and verify directly; for a cross-Skill or multi-session change, follow [the development workflow](docs/development.md). Parallel execution is optional: split only independent work and pass self-contained task pointers to fresh contexts.

Before changing a capability, use [the documentation index](docs/README.md) to read its current design and relevant ADRs. Treat dated validation as evidence from that run, and history/research as background. Follow the applicable `skills/*/SKILL.md`, references and script interfaces; surface conflicts between implementation and accepted intent. Update the affected docs with the change. Use the workflow's affected-area verification; a link-only change needs link/packaging checks, not media regeneration.

## Agent skills

### Issue tracker

Future substantial work uses this repository's GitHub Issues for specs and tickets. See [tracker conventions](docs/agents/issue-tracker.md). Do not retroactively create issues for completed work.

### Domain docs

One root [CONTEXT.md](CONTEXT.md) defines project vocabulary. Read/update the relevant section when terminology changes; preserve unrelated definitions. Important decisions live in `docs/adr/`. See [domain document rules](docs/agents/domain.md).
