---
name: video-notes
description: Turn a local video and timestamped transcript into readable illustrated Markdown and portable HTML notes, using the calling model to organize content and select screenshots.
---

# Video Notes

Input: a local video, matching SRT or timestamped JSON, output directory, and optional source URL/title. Obtain missing media or transcription through the caller's existing tools. Keep the source's part number and original timeline. This skill produces notes directly, without a learning catalog or knowledge-management workflow.

Use `scripts/video-notes` relative to this skill. Requires uv and FFprobe. Locate the available `video-frames` skill through the host or an explicit caller-supplied path; read its CLI contract for image operations. Core instructions are model-independent; use the host's file, image and command tools.

1. **Prepare.** Read [the output contract](references/output-contract.md). Verify media/transcript identity using metadata and matching content at the beginning, middle and end; record the evidence. Run `prepare`, or reopen a matching job. Use `--start/--end` for a sample. Existing inputs with different fingerprints need a new work directory, preserving old drafts.
2. **Write.** Read [the note style](references/note-style.md). For each pending window, read all its owned transcript segments and view contact sheets from that same range. Keep a little prior context for continuity. Write its Markdown chunk; record proposed figure IDs, times, source IDs and captions in `note-plan.json`. The model performs this work itself; tools never call another LLM.
3. **Review the window.** Compare the draft with its source for important explanations, steps and examples. After actually viewing the previews, use `review` to save explicit text/visual review evidence and a useful note. Save after each window. This attestation records the caller's judgment, not an automatic semantic guarantee.
4. **Merge and capture.** Read every chunk in order, merge into `draft.md`, repair boundary repeats and incomplete steps. Preserve `<!-- figure:ID -->` at each intended location. Capture planned single frames with `video-frames`; open every final image. Adjust times when pictures are transitional, unclear or unrelated. Record each accepted capture's SHA-256 as `reviewed_sha256` in the figure plan.
5. **Deliver.** Run `assemble`, `render`, then `validate`. Inspect the full note against the transcript and the HTML on desktop and narrow layouts; test image zoom and source-time links. Correct affected drafts/figures and repeat the downstream steps. Return Markdown/HTML paths, source scope, checks and unresolved limitations.

Completion requires every scoped window reviewed, captions grounded in viewed images, actual captures matching the plan, resolved markers and portable local assets. Structural validation complements the caller's content and visual review. With no image-viewing capability, report the missing capability rather than calling an unviewed illustrated result complete.
