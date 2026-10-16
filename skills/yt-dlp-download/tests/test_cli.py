from pathlib import Path

from yt_dlp_download.cli import DEFAULT_DATA_DIR, _codes, _exact_language, _files, _platform


def test_defaults_use_temp_directory() -> None:
    assert DEFAULT_DATA_DIR == Path("/tmp/yt-dlp-download")


def test_inventory_codes_and_platform() -> None:
    info = {
        "extractor_key": "BiliBili",
        "formats": [
            {"acodec": "aac", "language": "zh-CN"},
            {"acodec": "none", "language": "ja"},
        ],
        "subtitles": {"zh-CN": []},
        "automatic_captions": {"en": []},
    }
    assert _platform(info) == "bilibili"
    assert _codes(info) == (["zh-CN"], ["zh-CN"], ["en"])


def test_language_requires_exact_inventory_code() -> None:
    assert _exact_language("zh_cn", ["zh-CN", "en"], "subtitle") == "zh-CN"


def test_result_files_are_scoped_to_requested_media(tmp_path: Path) -> None:
    (tmp_path / "video.mp4").write_bytes(b"video")
    (tmp_path / "audio.m4a").write_bytes(b"audio")
    (tmp_path / "title.en.srt").write_text("subtitle")
    assert _files(tmp_path, "audio") == [str((tmp_path / "audio.m4a").absolute())]
    assert _files(tmp_path, "subtitles", "en") == [str((tmp_path / "title.en.srt").absolute())]
