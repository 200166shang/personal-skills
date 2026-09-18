from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

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

    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([args.url])

    files = _files(output_dir, args.media, subtitle_language)
    if not files:
        raise RuntimeError("yt-dlp completed without producing an output file")
    return {
        "ok": True,
        "status": "completed",
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

    download = commands.add_parser("download", help="download video, audio, or an exact subtitle language")
    download.add_argument("url")
    download.add_argument("--media", choices=("video", "audio", "subtitles", "all"), default="video")
    download.add_argument("--audio-language")
    download.add_argument("--subtitle-language")
    download.add_argument("--cookies-from-browser", choices=BROWSERS)
    return parser


def main() -> int:
    args = _parser().parse_args()
    try:
        result = _inventory(_extract(args.url, args.cookies_from_browser)) if args.command == "inspect" else _download(args)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (DownloadError, OSError, RuntimeError, ValueError) as exc:
        payload = {"ok": False, "error": {"code": "download_failed", "message": str(exc)}}
        print(json.dumps(payload, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
