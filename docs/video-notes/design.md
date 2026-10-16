# Single-lesson illustrated notes

Status: current implemented design, 2026-10-16. The original implementation and faithful-mode correction were merged in PRs #12 and #14. This document describes the current boundary; the [initial proposal](history/initial-design.md) is history.

## Scope and composition

`video-notes` accepts one local video and a matching timestamped SRT/JSON transcript, with source identity and output scope. Preparation of missing inputs is owned by the calling agent using independent download/ASR capabilities. `video-frames` provides contact sheets and original-frame capture; the calling model reads the source, views images and decides which captures support nearby prose. A named dedicated agent is optional, not a production prerequisite.

[Faithful mode is the default](../adr/0002-faithful-notes-default.md). Retain original expression, sequence, reasons, examples, qualifications and substantive restatements; clean filler, clear recognition errors and paragraphing. An explicit summary request changes the permitted condensation. Readability or attractive HTML alone does not authorize summarization. Keep source transcription and old output editions intact.

## Work and delivery

Preparation freezes source fingerprints and mode and divides the selected source timeline into recoverable windows, preserving cue ownership. For each window, compare the complete owned transcript with its draft and view the corresponding visual previews. Save reviewed chunks and figure plans. Merge without a second summarization, capture the planned frames, then inspect every final image before recording accepted hashes.

Assemble the Markdown, render portable HTML and run structural validation. The delivery contains relative local images/styles and source/review evidence; source video and work previews remain outside it. Source-time links retain the original part and timeline. A screenshot cannot establish dynamic motion or recover detail absent from the original resolution.

Unchanged inputs can reuse a job. Changed source, mode, normalization or preparation settings require a new work directory, preserving previous work. Styling changes can rerender without rewriting content. Automatic checks verify file/source relationships; window review and final-image acceptance are caller judgments, not semantic proofs. Character ratios are audit signals, not coverage guarantees.

Authors and independent reviewers execute the [structure and HTML checklist](../../skills/video-notes/references/presentation-review.md): topic subheadings, complete Markdown/HTML correspondence and actual page inspection. Record presentation observations separately from content/image review and disclose unavailable browser checks. Observed presentation defects require repair; browser unavailability alone remains a limitation rather than a claim of tested usability. The CLI continues to enforce structural relationships, not these caller judgments.

## Authoritative runtime references

- [Note Skill](../../skills/video-notes/SKILL.md), [output contract](../../skills/video-notes/references/output-contract.md), [style](../../skills/video-notes/references/note-style.md).
- [Frame Skill](../../skills/video-frames/SKILL.md), [frame contract](../../skills/video-frames/references/cli-contract.md).
- [Host integration](integration.md), [P2 evidence](validation.md), [faithful correction evidence](fidelity.md).

Image viewing is required for completed illustrated production. Record missing browser interaction/viewport checks separately; do not silently claim they ran. The dated evidence documents report their actual scope, and future runs must report their own checks.
