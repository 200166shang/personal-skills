# CLI contract

Resolve the launcher from this skill, not from a fixed installation path:

```text
scripts/video-frames preview --video PATH --start 0 --end 120
  --interval 6 --grid 2x2 --cell-width 640 --output-dir PATH
scripts/video-frames capture --video PATH --plan PATH --output-dir PATH
```

Times are absolute seconds, including decimals and values beyond one hour. Omit `--end` for the media end. The interval must be positive; grid dimensions are 1–4. Cell width is 160–1600 and is capped at source width to avoid enlarging the source. Contact sheets preserve aspect ratio and add timestamp labels above each cell. A tail sample is included; incomplete grids retain their frames. Audio-only tails are excluded.

`preview.json` maps sheet filenames and cell slots to timestamps and individual frame paths, relative to its directory. Its input includes the source SHA-256 and preview settings. A cache hit reuses the sheets; changed inputs require a new output directory.

Capture plan:

```json
{"figures":[{"id":"f001","timestamp":24.5}]}
```

IDs must be unique, begin with a letter, and contain only letters, digits, underscores or hyphens. Timestamps must lie inside media duration. `captures.json` contains source video SHA-256, successful `figures[{id,timestamp,file,sha256,frame_pts}]` and `failures`. File paths are relative to that manifest. PTS is currently null. A failure yields nonzero exit status, even if other figures succeeded; fix the plan and retry.

Commands return JSON on stdout and progress/dependency messages on stderr. `--help` lists supported flags. Requires Python 3.11–3.13 through uv, plus FFmpeg/FFprobe on PATH. No model API is called.
