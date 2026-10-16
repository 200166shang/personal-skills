# Playlist wrapper validation — 2026-10-16

Scope: modify only this Skill and its Python wrapper. Upstream `yt-dlp[default]==2026.8.19` and its source remain unchanged.

- Original tests: 4 pass before extension. New catalog/range tests initially failed because the wrapper only exposed inspect/download and rejected playlists.
- Extended suite: actual local HTTP HTML5 playlist with two FFmpeg-generated MP4s exercises native yt-dlp metadata extraction and downloads only selected item 2. FFprobe confirms the resulting file has video and audio. The test's loopback server uses direct loopback access, independent of the machine's external proxy; it does not contact a blocked platform.
- Fixtures: sanitized public first-party Bilibili directory captured earlier on 2026-10-16, 54 parts. Positions 5–9 map exactly to 2.1–2.5, cid values preserved, total 7322 seconds. This fixture is directory evidence, not current online access success.
- Current live Bilibili catalog request: HTTP 412 from public metadata and the native extractor. Further live requests stopped. Real five-lesson notes use existing downloaded local media, so no successful new Bilibili download is claimed.
- Tests also cover single-video defaults, inclusive range/position validation, unavailable slots, partial success preservation and stopping requests after a platform access rejection.

The new CLI's online YouTube/Bilibili catalog/download behavior still depends on provider availability and normal authorization. Only the local playlist test and offline provider metadata fixtures passed here. Existing browser-session reading remains opt-in; no cookies were read for this run.
