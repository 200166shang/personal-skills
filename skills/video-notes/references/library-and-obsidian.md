# Library storage and optional Obsidian copy

Read when choosing an unspecified delivery location, organizing existing course outputs, or copying notes into Obsidian. This is a caller-managed delivery procedure using file tools, not a new CLI subcommand. Keep the validated original edition intact; create the reading copy after validation, and after independent PASS/publication for batch lessons. Importing existing notes does not certify a new content review.

## Locations and identity

Use the user's explicit output path first. Otherwise use the host/user's configured Library root; if none is configured, default to `~/Media/Library`. Expand home on the current host. Organize finished editions as `<Library>/<platform>/<course>/`, using `bilibili`, `youtube`, `xiaoetong`, or a verified provider name. Downloads hold raw inputs; job/checkpoint and disposable preview caches stay outside the Library delivery and Vault. Existing batch CLI output paths remain explicit: the caller resolves the default before init, never relocates an active batch's frozen output path.

Copy into Obsidian only when requested. Resolve its target root from this request or an established host/user preference; if unavailable, request the destination while completing Library delivery. Keep personal absolute paths in host/user configuration, outside Skill source/templates. Do not discover or select another Vault by guessing. An output path explicitly inside a Vault signals a reading-copy destination: produce the full validated edition outside it first and then copy the selected files.

Match a course and lesson by verified provider/source ID and part, not title alone. Merge separate generation batches into one course reading index without conflating summary/sample/faithful editions. Prefer an explicitly selected edition; when intent is unclear, preserve alternatives and report the ambiguity. Sort by numeric source order, using zero-padded part numbers (P002 before P010), and retain course labels such as 2.1. Use readable, filesystem-safe lesson filenames and check sanitization/case collisions. Retain the real content mode; migration never upgrades a summary into faithful mode.

## Obsidian reading layout

The destination is a real-file copy, never a move or symlink. Copy this subset from each selected completed lesson:

```text
<Obsidian target>/<course>/
  <course>-课程目录.md
  assets/note.css
  P002-安装开发环境/
    P002-安装开发环境.md
    P002-安装开发环境.html
    images/                    # images actually used by the note
    sources/
      transcript.srt
      source.json
```

Use the part/title filename for both Markdown and HTML, so search results distinguish lessons. Preserve prose, headings, captions and original source-time/part links. Keep existing Markdown properties; add verified course/source identity only when missing. Original source links remain useful in the prose even if JSON is not visible in Obsidian's file tree.

Markdown and HTML share each lesson's real `images/` files with relative links. Course HTML shares `assets/note.css`; lesson HTML references `../assets/note.css`. Share styles only when CSS bytes match. If editions use different styles, retain separate hash-named CSS files and point each HTML to its own style; never overwrite one style with another. Preserve necessary referenced fonts/resources as well. A standalone lesson export must include the stylesheet and repair its path.

Retain `sources/transcript.srt` and `sources/source.json`. Copy existing files unchanged. If the validated source only supplies timestamped JSON, convert it losslessly to SRT when possible and compare segment timing/text; preserve the original externally. Report any missing provenance or conversion loss rather than inventing source identity. The CLI may package JSON instead of SRT depending on its input; do not assume both always exist.

Leave transcript JSON duplicates, review/validation/render reports, migration manifests, old editions, ZIPs, raw video, temporary audio, contact sheets, intermediate frames, drafts and job state outside the Vault. Save copy provenance/checks outside the Vault. Preserve the Library original and external source transcript for future correction. Cache deletion and Library cleanup are separate explicit actions; never delete unfinished checkpoints or assume an archive is disposable.

## Copy and verify

1. Preflight source/destination identity and the full file map before writing. Skip byte-identical existing files. Preserve existing different user files; compare and report conflicts, or use a distinct edition directory. A known prior import may be updated only under the user's update instruction, preserving the previous edition outside the Vault. Never silently overwrite user edits or unrelated files.
2. Stage the selected copy outside the Vault, repair relative paths, then check copied image/SRT/JSON hashes and unchanged Markdown body. Only expected filename/link adjustments are permitted. CSS/HTML path changes invalidate original render hashes; keep old audit reports with the original edition rather than claiming they validate the copy.
3. Check every local Markdown/HTML image, stylesheet and file link in the copied layout. In particular, assert the shared CSS file exists and matches its intended bytes. An apparently empty assets folder in Obsidian can contain CSS and must remain. Inspect the resulting HTML as prescribed by the presentation checklist; report browser checks that could not run separately.
4. Copy staged files into the destination only after checks, then repeat link/hash checks at the final path. Update the course Markdown index with relative Markdown and HTML links, preserving user sections. Include only imported lessons and explicitly identify known missing parts; a partial import is not a complete course. Use a searchable course index name; do not claim a numeric prefix overrides a folders-first file explorer.
5. Return the course/index path, lessons copied/skipped/conflicted, files retained, verification and limitations. Source media and Library editions remain available. This step does not push Git, publish to GitBook, configure sync or alter Obsidian settings.
