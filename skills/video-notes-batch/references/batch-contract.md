# Batch files and commands

Run `scripts/video-notes-batch --help` and subcommand help. JSON stdout, nonzero errors. No network, downloader, ASR or model dependency is embedded. The CLI uses Python standard-library file locks on macOS/Linux.

## Inputs

```json
{
  "title": "My course",
  "entries": [{
    "id": "lesson-01", "label": "2.1", "title": "2.1 Output modes",
    "source_key": "provider:stable-media-id", "source_url": "https://example.com/lesson",
    "video": "/absolute/video.mp4", "transcript": "/absolute/transcript.srt"
  }]
}
```

`id` uses letters/digits/underscore/hyphen/dot and starts with a letter/digit. IDs are unique and stable, separate from labels. Both input files must exist. JSON transcripts contain timestamped `segments`; SRT is accepted by `video-notes`. Relative paths resolve against the manifest. Identity matching is reviewed by the writer/reviewer; a hash alone does not establish that subtitles describe a video.

`scan --directory DIR --output manifest.json` inventories local MP4/MKV/WebM/MOV/M4V and adjacent `<stem>.srt`, `transcript.srt`, or `<stem>.json`. Missing transcripts cause an explicit error; prepare them separately. Scan infers Bilibili part URLs only from an explicit `BV…_pN` filename/directory; inspect the inventory before init. Other platforms can supply a manifest directly. Do not pass a network catalog as if it contained downloaded media paths.

```sh
video-notes-batch init --manifest manifest.json --labels 2.1,2.2,2.3,2.4,2.5 \
  --work-dir /path/jobs/batch-01 --output-dir /path/notes/course-edition-01 \
  --notes-cli /path/video-notes/scripts/video-notes --mode faithful
```

Exact label matching preserves manifest order. `2.1` never matches `2.10`; missing/duplicate selected labels fail. Omit `--labels` to use the entire explicit manifest. Input hashes, mode and output root are frozen. Reinitializing changed inputs requires a new batch; the output must be separate from work, with neither nesting inside the other.

## Cooperative scheduling

- `next --batch DIR`: compact status, ready actions, active tokens; does not claim anything.
- `claim --batch DIR [--lesson ID] [--stage writer|reviewer]`: atomic allocation; creates an isolated attempt and task file. Review-ready work has priority by default. Capacity defaults to two (`init --max-active 1` lowers it).
- `attach --batch DIR --token TOKEN --agent-id ACTUAL_ID --host HOST --isolation fresh`: record actual host dispatch. An ID cannot cross lessons or serve as both writer/reviewer. Host audit records must corroborate freshness; this declaration cannot inspect another model's context.
- `record --batch DIR --token TOKEN --result PATH`: result must be inside its assigned attempt and copy all binding fields from `task.result_template`. Consumed/revoked tokens and mismatched results fail.
- `publish --batch DIR --lesson ID`: snapshot/hash-bound PASS required. Uses staging and preserves existing different editions.
- `index --batch DIR`: generate portable `index.md`, `index.html`, `batch-report.json`, including unfinished lessons.
- `resume --batch DIR`: verify sources/progress, candidates or published hashes; makes no state changes. Already published notes remain verifiable without retained source caches.
- `recover --batch DIR --token TOKEN --reason TEXT`: explicitly revoke a stopped/lost worker. Preserve old attempts; late results fail. Three forced recoveries need attention. Never revoke a known living worker merely because it is slow.

State: ready → writing → review_ready → reviewing → passed → published. FIX → repair_ready → writing. Checkpoint → ready with saved progress. Error → retry-ready, failed or needs_attention. No timed auto-expiration guesses worker liveness. `recover` of an uncheckpointed writer restarts from the last accepted snapshot; unverified partial files remain in its old attempt.

Each attempt gets a task, job and delivery directory. The coordinator snapshots accepted work before review. Checkpoints copy/hash the job and reviewed chunks; continue the first pending window in the next attempt. Checkpoints preserve preparation parameters: rerun `prepare` only with identical settings or continue the existing job. Old workers have no valid token for a new attempt.

Published lesson directories contain single-lesson Markdown/HTML/images/assets/sources, `validation.json`, and reviewer evidence in the batch report. Work directories hold original attempts, tokens and dispatch events. Do not place media, caches, transcripts or runtime job files in the source repository. Cleanup is explicit; there is no automatic retention policy.
