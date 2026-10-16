from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit
from urllib.request import urlopen
from urllib.error import URLError

import yt_dlp
from yt_dlp.utils import DownloadError


DEFAULT_DATA_DIR = Path("/tmp/yt-dlp-download")
BROWSERS = ("chrome", "chromium", "edge", "firefox", "safari", "brave", "opera")


def _base_options(browser: str | None = None) -> dict[str, Any]:
    options: dict[str, Any] = {
        "ignoreconfig": True,
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
        "noprogress": True,
        "continuedl": True,
        "retries": 10,
        "fragment_retries": 10,
        "file_access_retries": 3,
        "socket_timeout": 30,
        "concurrent_fragment_downloads": 4,
    }
    if browser:
        options["cookiesfrombrowser"] = (browser,)
    return options


def _extract(url: str, browser: str | None = None) -> dict[str, Any]:
    options = {**_base_options(browser), "skip_download": True}
    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=False)
    if not isinstance(info, dict) or info.get("_type") == "playlist":
        raise ValueError("expected one media URL, not a playlist")
    return info


def _selection(expression: str, count: int) -> list[int]:
    selected = set()
    if not expression:
        raise ValueError("empty playlist selection")
    for token in expression.split(","):
        match = re.fullmatch(r"([1-9][0-9]*)(?::([1-9][0-9]*))?", token.strip())
        if not match:
            raise ValueError("use positive item positions, inclusive start:end ranges, or comma combinations")
        start, end = int(match[1]), int(match[2] or match[1])
        if not 1 <= start <= end <= count:
            raise ValueError(f"playlist selection outside 1:{count}")
        selected.update(range(start, end + 1))
    return sorted(selected)


def _public_bili_catalog(url: str) -> dict[str, Any] | None:
    parts = urlsplit(url)
    match = re.search(r"/video/(BV[A-Za-z0-9]+)", parts.path)
    if parts.hostname not in {"www.bilibili.com", "bilibili.com"} or not match:
        return None
    bvid = match[1]
    # Public directory metadata only; media remains obtained through official yt-dlp.
    with urlopen(f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}", timeout=30) as response:
        payload = json.load(response)
    if payload.get("code") != 0 or not payload.get("data", {}).get("pages"):
        raise ValueError("Bilibili public catalog is unavailable")
    data = payload["data"]
    entries = []
    for position, page in enumerate(data["pages"], 1):
        if page.get("page") != position:
            raise ValueError("Bilibili part positions are not contiguous")
        entries.append(dict(index=position, id=f"{bvid}_p{position}", title=page["part"],
                            url=f"https://www.bilibili.com/video/{bvid}/?p={position}",
                            duration=page.get("duration"), available=True,
                            provider=dict(bvid=bvid, cid=page["cid"], page=position)))
    return dict(ok=True, status="catalogued", platform="bilibili", id=bvid, title=data["title"],
                source_url=url, complete=True, count=len(entries), entries=entries)


def _catalog_result(info: dict[str, Any], url: str) -> dict[str, Any]:
    if not isinstance(info, dict):
        raise ValueError("catalog extraction returned no metadata")
    raw = list(info.get("entries", [])) if info.get("_type") in {"playlist", "multi_video"} else [info]
    entries = []
    for position, value in enumerate(raw, 1):
        item = value or {}
        if item.get("_type") in {"playlist", "multi_video"}:
            raise ValueError("nested catalog requires a more specific playlist URL")
        media_url = item.get("url") or item.get("webpage_url") or ""
        if media_url and not urlsplit(media_url).scheme and _platform(info) == "youtube":
            media_url = f"https://www.youtube.com/watch?v={item.get('id') or media_url}"
        available = bool(value and media_url and item.get("availability") not in {"private", "premium_only", "subscriber_only", "needs_auth"})
        entries.append(dict(index=position, id=item.get("id"), title=item.get("title") or "Unavailable item",
                            url=media_url or None, duration=item.get("duration"), available=available,
                            availability=item.get("availability")))
    if not entries:
        raise ValueError("catalog is empty")
    expected = info.get("playlist_count") or info.get("n_entries")
    return dict(ok=True, status="catalogued", platform=_platform(info), id=info.get("id"),
                title=info.get("title") or "Playlist", source_url=url,
                complete=expected is None or int(expected) == len(entries), count=len(entries), entries=entries)


def _catalog(url: str, browser: str | None = None) -> dict[str, Any]:
    try:
        public = _public_bili_catalog(url)
        if public is not None:
            return public
    except (URLError, ValueError, KeyError, OSError):
        pass  # Try the normal extractor; no media access workaround is attempted.
    parts = urlsplit(url)
    if parts.hostname in {"bilibili.com", "www.bilibili.com"} and re.search(r"/video/BV[A-Za-z0-9]+", parts.path):
        url_to_extract = urlunsplit((parts.scheme, parts.netloc, parts.path,
                                    urlencode([(k, v) for k, v in parse_qsl(parts.query) if k != "p"]), parts.fragment))
    else:
        url_to_extract = url
    options = {**_base_options(browser), "noplaylist": False, "extract_flat": "in_playlist", "skip_download": True}
    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(url_to_extract, download=False)
        if isinstance(info, dict) and "entries" in info:
            info["entries"] = list(info["entries"])
    return _catalog_result(info, url)


def _download_batch(args: argparse.Namespace) -> dict[str, Any]:
    catalog = _catalog(args.url, args.cookies_from_browser)
    if not catalog.get("complete", True):
        raise ValueError("catalog is incomplete; do not download an unverified selection")
    positions = _selection(args.playlist_items, len(catalog["entries"])) if args.playlist_items else list(range(1, len(catalog["entries"]) + 1))
    results = []
    for position in positions:
        entry = catalog["entries"][position - 1]
        try:
            if not entry.get("available") or not entry.get("url"):
                raise ValueError("selected item is unavailable")
            child = argparse.Namespace(**vars(args))
            child.url, child.playlist, child.playlist_items = entry["url"], False, None
            result = _download(child)
        except (DownloadError, OSError, RuntimeError, ValueError) as exc:
            result = dict(ok=False, status="failed", error=str(exc))
        results.append(dict(result, index=position, source_url=entry.get("url"), catalog_id=entry.get("id")))
        # An access rejection is a platform condition; preserve partial results and stop requests.
        if not result["ok"] and any(x in str(result.get("error", "")).lower() for x in ("412", "403", "429", "login", "sign in", "cookies", "drm")):
            for skipped in positions[len(results):]:
                e = catalog["entries"][skipped - 1]
                results.append(dict(ok=False, status="not_attempted", index=skipped,
                                    catalog_id=e.get("id"), source_url=e.get("url"), error="platform access blocked"))
            break
    success = all(x["ok"] for x in results)
    return dict(ok=success, status="completed" if success else "partial", catalog=catalog,
                selected_indices=positions, results=results)


def _codes(info: dict[str, Any]) -> tuple[list[str], list[str], list[str]]:
    audio = sorted(
        {
            str(item["language"])
            for item in info.get("formats") or []
            if isinstance(item, dict)
            and item.get("acodec") not in {None, "none"}
            and item.get("language")
        },
        key=str.casefold,
    )
    subtitles = sorted((info.get("subtitles") or {}).keys(), key=str.casefold)
    automatic = sorted((info.get("automatic_captions") or {}).keys(), key=str.casefold)
    return audio, subtitles, automatic


def _platform(info: dict[str, Any]) -> str:
    key = str(info.get("extractor_key") or info.get("extractor") or "unknown").casefold()
    if "youtube" in key:
        return "youtube"
    if "bili" in key:
        return "bilibili"
    return key or "unknown"


def _inventory(info: dict[str, Any]) -> dict[str, Any]:
    audio, subtitles, automatic = _codes(info)
    return {
        "ok": True,
        "status": "inspected",
        "platform": _platform(info),
        "id": str(info.get("id") or ""),
        "title": str(info.get("title") or info.get("id") or "untitled"),
        "duration": info.get("duration"),
        "audio_languages": audio,
        "subtitle_languages": subtitles,
        "automatic_subtitle_languages": automatic,
    }


def _normalize(code: str) -> str:
    return code.replace("_", "-").casefold()


def _exact_language(requested: str, available: list[str], kind: str) -> str:
    wanted = _normalize(requested)
    exact = [code for code in available if _normalize(code) == wanted]
    if len(exact) == 1:
        return exact[0]
    raise ValueError(
        f"requested {kind} language {requested!r} is unavailable; inspect the URL and use an exact returned code"
    )


def _safe_component(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "-", value).strip("-.")
    return cleaned[:100] or "media"


def _files(directory: Path, media: str, subtitle_language: str | None = None) -> list[str]:
    ignored = (".part", ".ytdl", ".temp")
    audio_extensions = {".aac", ".flac", ".m4a", ".mp3", ".ogg", ".opus", ".wav"}
    subtitle_extensions = {".ass", ".lrc", ".srt", ".ssa", ".ttml", ".vtt"}
    video_extensions = {".avi", ".flv", ".m4v", ".mkv", ".mov", ".mp4", ".webm"}
    selected: list[Path] = []
    for path in directory.rglob("*"):
        if not path.is_file() or path.name.endswith(ignored):
            continue
        suffix = path.suffix.casefold()
        is_requested_subtitle = suffix in subtitle_extensions and (
            not subtitle_language or f".{subtitle_language}." in path.name
        )
        if media == "video" and suffix in video_extensions:
            selected.append(path)
        elif media == "audio" and suffix in audio_extensions:
            selected.append(path)
        elif media == "subtitles" and is_requested_subtitle:
            selected.append(path)
        elif media == "all" and (suffix in video_extensions or suffix in audio_extensions or is_requested_subtitle):
            selected.append(path)
    return sorted(str(path.absolute()) for path in selected)


def _download(args: argparse.Namespace) -> dict[str, Any]:
    info = _extract(args.url, args.cookies_from_browser)
    audio_codes, subtitle_codes, automatic_codes = _codes(info)
    audio_language = None
    subtitle_language = None
    if args.audio_language:
        audio_language = _exact_language(args.audio_language, audio_codes, "audio")
    if args.subtitle_language:
        subtitle_language = _exact_language(
            args.subtitle_language, sorted(set(subtitle_codes + automatic_codes)), "subtitle"
        )
    if args.media in {"subtitles", "all"} and not subtitle_language:
        raise ValueError(f"--media {args.media} requires --subtitle-language with an exact code from inspect")

    media_id = str(info.get("id") or "").strip()
    if not media_id:
        raise ValueError("media metadata has no stable ID")
    platform = _platform(info)
    output_dir = args.data_dir.expanduser().absolute() / _safe_component(platform) / _safe_component(media_id)
    output_dir.mkdir(parents=True, exist_ok=True)

    options = {
        **_base_options(args.cookies_from_browser),
        "outtmpl": str(output_dir / "%(title).160B [%(id)s].%(ext)s"),
        "overwrites": False,
    }
    if args.media in {"video", "all"}:
        if audio_language:
            options["format"] = (
                f"worstvideo+worstaudio[language={audio_language}]/worst[language={audio_language}]"
            )
        else:
            options["format"] = "worstvideo*+worstaudio/worst"
    elif args.media == "audio":
        options["format"] = f"worstaudio[language={audio_language}]" if audio_language else "worstaudio/worst"
        options["postprocessors"] = [{"key": "FFmpegExtractAudio", "preferredcodec": "m4a"}]
    elif args.media == "subtitles":
        options["skip_download"] = True

    if args.media in {"subtitles", "all"}:
        options.update(
            {
                "writesubtitles": True,
                "writeautomaticsub": True,
                "subtitleslangs": [subtitle_language],
                "subtitlesformat": "srt/best",
            }
        )
        options.setdefault("postprocessors", []).append(
            {"key": "FFmpegSubtitlesConvertor", "format": "srt"}
        )
    if args.media == "all":
        options["keepvideo"] = True
        options.setdefault("postprocessors", []).append(
            {"key": "FFmpegExtractAudio", "preferredcodec": "m4a"}
        )

    before = {str(p) for p in output_dir.iterdir() if p.is_file()}
    with yt_dlp.YoutubeDL(options) as ydl:
        downloaded = ydl.extract_info(args.url, download=True)
        if not isinstance(downloaded, dict) or str(downloaded.get("id")) != media_id:
            raise ValueError("download returned a different media identity")
        expected_name = Path(ydl.prepare_filename(downloaded)).name
    marker = f"[{media_id}]"
    if marker not in expected_name:
        raise ValueError("download output filename has no matching media identity")
    prefix = expected_name[:expected_name.rindex(marker) + len(marker)]
    files = [p for p in _files(output_dir, args.media, subtitle_language)
             if Path(p).name.startswith(prefix + ".")]
    if args.media == "all":
        suffixes = {Path(p).suffix.lower() for p in files}
        if not (suffixes & {".mp4", ".mkv", ".webm", ".mov", ".flv", ".avi", ".m4v"}
                and suffixes & {".m4a", ".mp3", ".wav", ".opus", ".ogg", ".aac", ".flac"}
                and suffixes & {".srt", ".vtt", ".ass", ".ttml"}):
            raise RuntimeError("some requested media types were not produced")
    if not files:
        raise RuntimeError("yt-dlp completed without producing an output file")
    return {
        "ok": True,
        "status": "completed",
        "reused": bool(files and all(p in before for p in files)),
        "source_url": args.url,
        "platform": platform,
        "id": media_id,
        "title": str(info.get("title") or media_id),
        "media": args.media,
        "audio_language": audio_language,
        "subtitle_language": subtitle_language,
        "output_dir": str(output_dir),
        "files": files,
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Download authorized web media with official yt-dlp")
    parser.add_argument("--data-dir", type=Path, default=DEFAULT_DATA_DIR)
    commands = parser.add_subparsers(dest="command", required=True)

    inspect = commands.add_parser("inspect", help="list media and language inventory without downloading")
    inspect.add_argument("url")
    inspect.add_argument("--cookies-from-browser", choices=BROWSERS)

    catalog = commands.add_parser("catalog", help="read the containing catalog without downloading media")
    catalog.add_argument("url")
    catalog.add_argument("--cookies-from-browser", choices=BROWSERS)

    download = commands.add_parser("download", help="download video, audio, or an exact subtitle language")
    download.add_argument("url")
    download.add_argument("--media", choices=("video", "audio", "subtitles", "all"), default="video")
    download.add_argument("--playlist", action="store_true")
    download.add_argument("--playlist-items", help="positive positions and inclusive ranges, e.g. 2,5:9")
    download.add_argument("--audio-language")
    download.add_argument("--subtitle-language")
    download.add_argument("--cookies-from-browser", choices=BROWSERS)
    return parser


def main() -> int:
    args = _parser().parse_args()
    try:
        if args.command == "inspect":
            result = _inventory(_extract(args.url, args.cookies_from_browser))
        elif args.command == "catalog":
            result = _catalog(args.url, args.cookies_from_browser)
        elif args.playlist or args.playlist_items is not None:
            result = _download_batch(args)
        else:
            result = _download(args)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result["ok"] else 1
    except (DownloadError, OSError, RuntimeError, ValueError) as exc:
        payload = {"ok": False, "error": {"code": "download_failed", "message": str(exc)}}
        print(json.dumps(payload, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
