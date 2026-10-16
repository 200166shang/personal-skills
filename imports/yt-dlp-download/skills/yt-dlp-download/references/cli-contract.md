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


## Catalog and explicit playlists

```sh
scripts/yt-dlp-download catalog URL
scripts/yt-dlp-download --data-dir PATH download URL --media video --playlist
scripts/yt-dlp-download --data-dir PATH download URL --media video --playlist-items 5:9
```

`catalog` reads metadata without downloading. Bilibili multipart video URLs discover
all parts even when the original URL has `p=2`; this catalog request alone does not
authorize downloading all parts. Public Bilibili view metadata supplies part title,
page, cid and duration; other supported catalogs use yt-dlp's native flat inventory.
Nested catalogs require a more specific URL. Incomplete catalogs cannot be downloaded
as a verified selection. Private/deleted items keep their positions and availability.

`--playlist-items` accepts positive positions, inclusive `start:end` and commas,
e.g. `2,5:9`. Selection is unique and follows catalog order. It takes precedence over
`--playlist`. Invalid/out-of-range/empty selections fail before media downloads.
No list flags preserves existing single-video behavior. Chapter labels such as 2.1
must first be mapped to actual positions, not interpreted as decimal indices.

Catalog JSON includes `source_url`, `platform`, `id`, `title`, `complete`, `count`,
and `entries[{index,id,title,url,duration,available,provider?}]`. Unknown fields are
null rather than invented. Batch JSON includes the catalog, `selected_indices`, and
`results` with index, catalog ID, exact source URL and each original single-download
result or failure. `status: partial` and nonzero exit preserve successful results.
Access rejection stops subsequent requests and marks remaining items not_attempted.
Media paths remain `<data-dir>/<platform>/<media-id>/`; parts use distinct IDs.
Single results include `reused` for preexisting confirmed outputs and `source_url`.
Output files must match the current yt-dlp-resolved filename/ID and requested type;
other files in that media directory do not establish successful output.

This wrapper modifies no upstream yt-dlp source and does not override its platform
access requirements. Existing authorized browser cookies remain opt-in. HTTP 412 or
login conditions are not solved by repeatedly retrying the whole selected range.
