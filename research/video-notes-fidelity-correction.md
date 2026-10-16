# Faithful lecture mode: correction and P2 regeneration

Date: 2026-10-16. The user found that the condensed note lost too much of the tutorial's original expression and requested fuller transcript-based narration. This supersedes the earlier condensation preference; the original condensed edition remains intact.

## Changed default

Both `video-notes` and the dedicated `video_notes_operator` now default to a cleaned faithful lecture script. Preserve the speaker's first/second-person voice, original progression, every substantive reason/example/qualification and meaningful restatements. Improve readability through punctuation, paragraphing, light sectioning, confirmed ASR corrections and separate captions. Summary mode requires an explicit request. Merging concatenates reviewed prose with local join repairs, rather than performing another summarization pass.

`prepare --mode faithful|summary` records the mode in the input fingerprint and source metadata. A mode change rejects reuse of previous drafts; old jobs without a mode remain legacy jobs, not automatically relabelled faithful. Review and assembly record length-reduction signals, with a warning below 70% for faithful mode. These signals are not semantic fidelity scores or pass/fail guarantees; full source-to-script comparison remains necessary.

## Regenerated P2 case

Source: [STM32 tutorial P2, installing the development environment](https://www.bilibili.com/video/BV11X4y1j7si/?p=2), 1288.362 seconds and 582 transcript cues. Reused the previously matched media/transcript and 14 previously viewed screenshot files after verifying their source and file hashes. A separate job under the new operator's job directory preserves all original outputs.

The full transcript was read in order and rewritten across 11 continuous windows. The new script retains the original greeting and closing, first-person demonstration, rhetorical questions, compiler explanation, each UI action, repeated compiler-setting confirmation, the breadboard/encoder example and full download-log explanations. Paragraphs remain prose instead of turning these explanations into tables or highlights. Two cross-window sentence joins were repaired locally.

Known ASR terms were corrected against context and actual UI: Keil 5, Core/Pack, Browse, STM32F1 support package, CID, compiler setting names and download log labels. A targeted source-frame check at 661.8 seconds resolved the registration program filename as `keygen.exe`; the original transcript was not edited.

The raw source contains 7,349 non-whitespace characters. The faithful speaker prose contains 6,422 after excluding headings, editorial source metadata and figure markers, about 87.4% of the raw source. Each window is about 82–94%; the removed material is speech filler, accidental repetitions and unambiguous recognition cleanup. These counts describe the edit; the completeness judgment comes from comparing every source segment and the merged script, not from the ratio. The prior condensed draft was approximately 3,000 characters under the same rough counting convention.

Final Markdown and HTML use the same 14 figures with source-part/time links. New outputs are a distinct faithful edition; no old summary, source transcript or video is replaced. Generated lecture content and media remain outside Git.

## Verification

- Two new behavioral tests cover faithful default/mode-cache separation and large-reduction warnings without heading, source-metadata or figure-marker padding.
- Existing source, window, capture, portability and HTML checks remain applicable. Structural reports include the content mode and audit signals while retaining the distinction from semantic review.
- The dedicated agent installer updates only that agent, backing up its previous configuration. Only the affected video-notes skill is reinstalled; unrelated learning and media skills are unchanged.
- All 15 checks passed (8 note-tool tests, 4 frame-tool tests and 3 agent-installer tests), along with skill validation and package inclusion checks. The installed skill and dedicated agent were updated, with backups; installed-entrypoint validation passed for the regenerated faithful edition.
- The browser rejected automated `file://` navigation under its URL policy. No alternate browser/protocol workaround was attempted. The new edition was checked through source comparison, saved Markdown/HTML and asset/hash validation; a new browser visual review is not claimed. The previously tested HTML/CSS template was unchanged.
