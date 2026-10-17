# Files and commands

Run `scripts/video-notes --help` and each subcommand's help for arguments. These are deterministic utilities, with JSON stdout and nonzero errors. Launchers use locked Python dependencies in the user cache. FFprobe is required for preparation; rendering is offline.

```text
prepare --video PATH --transcript PATH --work-dir PATH
        [--source-url URL] [--title TEXT] [--source-note TEXT]
        [--window-seconds 120] [--start 0] [--end SECONDS]
        [--mode faithful|summary]
review --work-dir PATH --window w001 --source-reviewed --visual-reviewed --note TEXT
assemble --draft PATH --plan PATH --captures PATH --output-dir PATH
render --markdown PATH --output-dir PATH
validate --plan PATH --output-dir PATH
```

## Preparation and recovery

`prepare` accepts SRT (including multiline cues) or JSON with `segments[{start,end,text}]`. Times are absolute seconds. Source text remains unchanged; normalized segments receive `seg00001` IDs. Out-of-order, empty, unparseable or out-of-range cues fail. A transcript ending before 75% of the video fails pending source matching; use a matching full transcript rather than stretching times.

The work directory contains `job.json`, `transcript.json`, `note-plan.json`, and `chunks/`. The job stores input fingerprints, media URL/path/part, source review and continuous windows. Boundaries extend to finish transcript cues. A sample range may therefore include a little extra time. Owned segment IDs appear in exactly one window. Previous text may be read as context without becoming new owned content.

Write each chunk to its job-defined path, then call `review` after reading source and viewing previews. The command hashes the draft and stores the review note. If a chunk changes, review it again. Record media/subtitle matching with `--source-note` initially or update `job.source.source_review` once evidence is available. Do not mark pending windows reviewed merely to satisfy validation.

Re-running `prepare` on identical inputs returns a cache hit. Mode defaults to `faithful`; use `summary` only for explicit condensation requests. Mode is part of the input fingerprint and source metadata. Changed media, source transcript, normalization, title, range, mode or window size rejects reuse; select a new directory. Old jobs without mode are legacy jobs, not silently certified as faithful. This preserves previous drafts rather than guessing how to invalidate them. CSS-only edits require only rendering again.

`review` and `assemble` record source/script non-whitespace character counts (excluding Markdown headings, blockquote metadata and figure markers from the script), length ratio and a warning when faithful text is below 70% of the source length. A warning requires the caller to repeat the complete comparison and explain justified removals. Counts do not establish semantic coverage; a longer script can still omit content, and short source windows can legitimately consist mostly of speech noise. Blockquoted source text is also excluded by this conservative heuristic. The structural validator returns these audit signals without claiming an automatic fidelity verdict.

## Writing and figure plan

The caller writes Markdown chunks, merges `draft.md`, and maintains `note-plan.json` next to `job.json`:

```json
{
  "schema_version": 1,
  "figures": [{
    "id": "f001",
    "timestamp": 143.2,
    "caption": "A description grounded in the viewed frame",
    "source_segment_ids": ["seg00042"],
    "reason": "Why this image supports the adjacent text"
  }]
}
```

These times and IDs are illustrative. In `draft.md`, place `<!-- figure:f001 -->` where the figure belongs. Every plan figure has exactly one marker and capture. Frame extraction follows the `video-frames` contract. Open the final images; add `reviewed_sha256` to each plan figure using the corresponding hash from `captures.json`. Changing a capture invalidates this acceptance. Final figures lie inside the job's scoped range.

## Delivery

For default Library placement and an optional selected-file Obsidian copy after acceptance, follow [Library and Obsidian delivery](library-and-obsidian.md). This caller procedure leaves the full validated edition and its reports intact; the reading copy has its own path/link checks and does not inherit stale render hashes. CLI arguments and output contracts below remain unchanged.

`assemble` requires matching source hashes, all windows reviewed, accepted captures and consistent figure IDs. It copies used images, resolves markers to Markdown images/captions/time links, and packages sources and review evidence. Use a delivery directory separate from the work directory. These commands update their own generated outputs; preserve a previous published edition in a different directory when needed.

`render` reads the final Markdown, creates heading anchors/TOC, copies local images if necessary, and writes `note.html`, `assets/note.css` and `render.json`. It rejects remote images, missing files and escaping asset paths. Raw HTML in Markdown is escaped. Local CSS, image zoom and code highlighting work without a server or CDN. Time links to the source need network access.

Before delivery, execute the [structure and HTML review checklist](presentation-review.md). Heading coverage and Markdown/HTML correspondence are caller checks; `validate` does not detect missing topic subheadings or establish page usability. Record presentation observations separately from content/image evidence and name untested browser checks.

`validate` verifies current sources/window evidence, figure plan, delivered image hashes, Markdown, HTML and CSS hashes. `validation.json` explicitly distinguishes these structural checks from the caller's semantic/visual judgments. Final delivery includes `note.md`, `note.html`, `images/`, `assets/`, original/normalized transcripts and source/review metadata under `sources/`. Source video, previews and machine-specific work state stay outside the delivery and repository.
