# CLI contract

Invoke all commands through `scripts/yt-dlp-download`. Results are JSON on stdout. Progress and diagnostics go to stderr.

## Inspect

```bash
scripts/yt-dlp-download inspect URL [--cookies-from-browser BROWSER]
```

Returns the platform, stable media ID, title, duration, available audio-language codes, manual subtitle codes, and automatic subtitle codes. Inspect does not download media.

## Download

```bash
scripts/yt-dlp-download download URL [OPTIONS]
```

Options:

- `--media video|audio|subtitles|all` defaults to `video`.
- `--audio-language CODE` selects an exact audio-language code returned by `inspect`.
- `--subtitle-language CODE` selects an exact manual or automatic subtitle code returned by `inspect`.
- `--cookies-from-browser chrome|chromium|edge|firefox|safari|brave|opera` reads an existing authorized browser session.
- `--data-dir PATH` overrides the default `/tmp/yt-dlp-download` root.

Video uses the lowest available video resolution with an audio stream. Audio uses the lowest available audio stream. `subtitles` requires `--subtitle-language`. `all` requires `--subtitle-language` and keeps the video while extracting an M4A audio copy.

Successful downloads return `ok`, `status`, platform, ID, title, media type, selected language codes, output directory, and absolute file paths. A failed command returns `ok: false` and an error object, then exits nonzero.

Do not pass arbitrary raw yt-dlp arguments. This narrow contract is the stable Agent integration surface.

