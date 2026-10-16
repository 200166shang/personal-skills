# Video notes: P2 validation

Date: 2026-10-16. Source: [STM32 tutorial, P2 — installing the development environment](https://www.bilibili.com/video/BV11X4y1j7si/?p=2).

This record describes the original condensed-note case. The user subsequently requested fuller preservation of the lecture; [the fidelity correction](video-notes-fidelity-correction.md) changes the default and documents a separate faithful edition. The original output remains intact for comparison.

## Executed case

The existing downloader resolved `BV11X4y1j7si_p2` and acquired the P2 video. FFprobe reported 1288.362 seconds total, 640×360 video, and a video track ending at 1288.200 seconds. An existing SRT had 582 cues ending at 1288.060 seconds. It was stored under an unrelated older download directory, so directory identity was not trusted. The full transcript and time-corresponding previews were read; the introduction, license dialog, compiler setup, download logs and final reset/LED demonstration matched this P2.

The transcript was reused, normalized and preserved rather than retranscribed. Source matching was recorded as a caller judgment, not an automatic identity guarantee.

Two deliverables were produced outside this repository:

| Scope | Windows | Accepted screenshots | Result |
| --- | ---: | ---: | --- |
| Sample from 00:00 to 06:01.740 (extended to finish the subtitle cue) | 3 | 3 | Markdown, HTML, sources and structural validation passed |
| Complete P2, 00:00 to 21:28.362 | 11 | 14 | Markdown, HTML, sources and structural validation passed |

Content organization and screenshot selection were performed by the calling conversation model. Tools made no model API calls. Each window was reviewed against all its owned transcript segments and visual previews; every final screenshot was opened and accepted by hash. The merged note was reviewed in source order.

Visual checking caught a real selection error: the candidate at 357 seconds still displayed the download client's Basic settings rather than Transfer settings. It was replaced with the frame at 361 seconds. The LED caption explicitly links to the video for the dynamic flashing result; a still image does not claim to demonstrate motion.

## Executed technical checks

- Ten unit/integration tests passed: observable red/blue frame extraction, aspect ratio and short grids, hour/invalid timestamps and duplicate IDs, corrupt preview cache recovery, audio-only tail handling, portable HTML packaging and source-part links, stale review/source/render detection, missing/unreviewed figures, malformed/wrong-time subtitles and path containment, scoped windows and omitted-window rejection, and changed part identity. Some test methods exercise multiple related invariants.
- Both skill definitions passed the skill-creator validator.
- The existing installer copied complete skills into an isolated temporary `CODEX_HOME`. Installed launchers produced both the sample and full delivery; no runtime environment or generated media was placed in the repository.
- The full HTML was opened in the in-app browser. Desktop viewport 1280×900 and narrow viewport 390×844 were inspected. All 14 images loaded, the document width matched the narrow viewport (no horizontal page overflow), source links retained `p=2`, heading navigation rendered, and the image enlargement dialog opened successfully.
- A complete delivery directory was copied to a different path and passed structural validation there. The output uses local assets, without a CDN or backend requirement for reading.
- Source videos, notes, screenshots, test environments and work state remain outside Git. The PR includes only implementation, instructions, templates, locks, tests and documentation.

## Limits

The source is 360p. Main dialogs, wiring labels and output states are useful, but small interface text has source-resolution limits. The implementation does not recover missing detail, perform OCR, or certify the tutorial's software licensing or technical claims. It records source-based notes.

The structural validator checks matching inputs, complete window ownership, caller review attestations, figure/file hashes and current rendering. It does not automatically prove summary accuracy or visual relevance. Playback PTS is not measured; capture metadata honestly reports the requested timestamp with null frame PTS.

Changing task inputs intentionally rejects old work-state reuse and preserves previous drafts in place. Start a new work directory for changed inputs. Style-only changes rerender without redownloading, ASR or model writing. This conservative recovery boundary is narrower than automatic partial invalidation proposed in the original plan.

Browser verification used a temporary local file server for convenience; delivered HTML can be opened directly. No application server is part of either skill.
