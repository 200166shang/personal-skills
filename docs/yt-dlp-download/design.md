# Download wrapper

Status: current implemented design, 2026-10-16. Playlist support was merged in the original wrapper repository; its history and source now live here following PR #16.

`yt-dlp-download` is an independent wrapper around upstream yt-dlp. A normal download remains single-media, with the original lowest-resolution and exact-language rules. Explicit catalog requests discover metadata without authorizing media downloads; explicit playlist/range flags select multiple positions. An unavailable item retains its position, partial results retain successful files, and an access rejection stops subsequent item requests. Catalog discovery does not prove media availability.

The caller maps course chapter labels to actual entries. The wrapper returns source identities and actual file paths; a later note batch receives prepared local videos/transcripts rather than invoking this wrapper internally. The wrapper changes no upstream yt-dlp source. Original dependency locking, data-root behavior and first-use environment setup are preserved by the source consolidation.

Use [the Skill](../../skills/yt-dlp-download/SKILL.md), [CLI contract](../../skills/yt-dlp-download/references/cli-contract.md) and `--help` for current arguments/result fields. [Playlist validation](validation.md) is dated evidence; [the extension proposal](history/playlist-extension-plan.md) preserves an earlier schema/ownership design that is not the current contract. [Course catalog evidence](../../research/video-notes-batch-course-catalog.md) and the public-metadata test fixture explain the P5–P9 selection without claiming new online success.
