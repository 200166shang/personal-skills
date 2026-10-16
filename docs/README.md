# Documentation index

Updated: 2026-10-16. This is the entry point for maintaining personal-skills. Read only the capability and decisions relevant to the change; the repository does not require loading every document into an agent context.

## Development foundations

| Document | Purpose |
| --- | --- |
| [AGENTS.md](../AGENTS.md) | Concise repository instructions and conditional reading pointers |
| [CONTEXT.md](../CONTEXT.md) | Shared vocabulary; existing Learning terms plus media-note terms |
| [Development workflow](development.md) | Small changes versus spec/ticket work, handoffs, verification and PRs |
| [Issue tracker](agents/issue-tracker.md) | GitHub Issues for future substantial work; no retrospective tickets |
| [Domain documents](agents/domain.md) | Glossary and ADR maintenance rules |

This is a lightweight adaptation of Matt Pocock's workflow, not an installation of his Skills or a mandatory multi-agent process.

## Current capability designs

| Area | Current design or integration | Dated verification |
| --- | --- | --- |
| Learning and journal Skills | [Learning router](../skills/learning/SKILL.md), [daily journal](../skills/daily-journal/SKILL.md) and the applicable [Skill directory](../skills/) remain their current contracts | The [earlier transcript investigation](../research/transcript-batch-workflow.md) is background, not validation or current policy |
| Single-lesson notes and frames | [Design](video-notes/design.md), [optional host integration](video-notes/integration.md) | [Original P2 case](video-notes/validation.md), [faithful-mode correction](video-notes/fidelity.md) |
| Batch lesson production | [Design](video-notes-batch/design.md) | [Five-lesson acceptance](video-notes-batch/validation.md) |
| Download wrapper | [Design](yt-dlp-download/design.md) | [Playlist validation](yt-dlp-download/validation.md) |
| Media Skill consolidation | [Design and provenance](media-skills-migration/design.md) | [Migration validation](media-skills-migration/validation.md) |

Current design describes accepted boundaries. Exact command/data contracts live with the applicable `skills/*/SKILL.md`, `references/`, scripts and tests. If code conflicts with accepted intent, report it and resolve the discrepancy rather than treating a historical proposal as a new requirement.

Validation is a snapshot of what was executed on its recorded date. Preserve untested portions, access limitations and the distinction between semantic/image review and structural/browser checks; do not present old evidence as a fresh run.

## Accepted decisions

- [0001: composable media capabilities](adr/0001-composable-media-skills.md).
- [0002: faithful lecture scripts by default](adr/0002-faithful-notes-default.md).
- [0003: one maintained media-Skill source](adr/0003-one-media-skill-source.md).

## Background and historical plans

[Research index](../research/README.md) lists dated investigations and their scope. The [initial single-lesson design](video-notes/history/initial-design.md) and [playlist extension draft](yt-dlp-download/history/playlist-extension-plan.md) are historical sources, not execution instructions. Their proposed interfaces, source locations and defaults may differ from current contracts.

The duplicate local single-lesson draft was already represented by the committed original plan. The earlier long batch draft mixed full acquisition orchestration with note scheduling; its final boundaries are captured in the current design and ADR 0001, so it is not imported as a second active plan. Original local backups remain outside Git. The unique course-directory evidence and playlist draft are preserved through the research/history links above.

For later changes: update one current design per capability, add a dated verification section/file when new evidence matters, and create an ADR only for a consequential trade-off. Keep secrets, original media, generated lectures and runtime state outside these documents; link necessary source evidence or summarize its verified properties.
