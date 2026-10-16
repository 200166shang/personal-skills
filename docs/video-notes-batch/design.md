# Batch production of prepared local lessons

Status: current implemented design, 2026-10-16; merged in PR #15. Downloads/ASR and batch note production remain separate stages. The download/ASR Skills subsequently moved into this collection in PR #16; that source migration did not widen the batch's runtime scope.

## Boundaries

The user's current calling agent is the entry point. It can download/transcribe an entire series first, then pass a local manifest to `video-notes-batch`. The batch has no embedded downloader, ASR/model API or required named agent configuration. Each writing task composes [single-lesson notes and frames](../video-notes/design.md). See [ADR 0001](../adr/0001-composable-media-skills.md) for the reason this stays separate from a full media workflow.

The batch freezes selected lesson identities, input hashes, order, mode and output destination. Labels select exact entries, not decimal approximations or source identities. A changed source or mode requires a new batch. Default faithful production is complete-lesson work; summary requires explicit user intent.

## Isolation and progress

The host creates a fresh writer for each lesson and a separate fresh reviewer; task pointers give each instance only its own inputs and attempt directory. The coordinator handles statuses, paths and concise issues, keeping full lesson prose out of its context. At most two writers/reviewers are active together, reduced to host capacity. The deterministic CLI manages cooperative claims, attempt tokens and result binding; it does not create agents itself or provide an OS sandbox.

A completed writer candidate is snapshotted before independent source/image review. PASS binds the current candidate; FIX creates a bounded repair attempt, while unavailable source/image judgments require attention. Reviewers also execute the single-lesson structure/HTML checklist and record `presentation_review` observations. Missing topic subheadings or observed presentation defects require FIX; incomplete structure/correspondence review requires UNCERTAIN. Browser interaction checks have their own limitations field and are not inferred from content PASS. These additional observations are instruction-level evidence preserved by the recorder, not new CLI-enforced fields. A checkpoint preserves verified partial progress for a fresh continuation and never means a finished lesson. The CLI rejects consumed/revoked tokens and late results from another attempt.

On resume, preserve known live claims and verify stored evidence. Revoke only a confirmed stopped/lost worker, retaining old attempts and invalidating its token. Publish only a current independent PASS, preserve prior different editions and update a course index that links rather than summarizes each script. Already published lessons can be checked by their delivery hashes after source caches are removed. Failed lessons remain visible while other eligible lessons continue.

## Runtime contracts and evidence

[Batch Skill](../../skills/video-notes-batch/SKILL.md), [manifest/CLI contract](../../skills/video-notes-batch/references/batch-contract.md), [host dispatch](../../skills/video-notes-batch/references/host-dispatch.md), [writer](../../skills/video-notes-batch/references/lesson-worker.md) and [reviewer](../../skills/video-notes-batch/references/lesson-reviewer.md) own detailed fields and commands. Read those when changing the relevant stage instead of duplicating their schemas here.

[Five-lesson acceptance](validation.md) records the STM32 2.1–2.5 / P5–P9 run, state/claim checks and limitations. [Directory evidence](../../research/video-notes-batch-course-catalog.md) records the original selection. Codex isolation was exercised; Claude Code has an adapter guide but no live verification in that record. Neither the task graph nor image/character counts prove complete semantic or visual coverage.
