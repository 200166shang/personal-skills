#!/usr/bin/env python3
"""Unified local Whisper transcription with stable, inspectable outputs."""

from __future__ import annotations

import argparse
import csv
import json
import os
import platform
import shutil
import subprocess
import sys
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any, Iterable


ALL_FORMATS = ("txt", "srt", "vtt", "json", "tsv")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Transcribe audio/video locally with MLX or faster-whisper."
    )
    parser.add_argument("input", type=Path, help="Audio or video input path")
    parser.add_argument(
        "--backend",
        choices=("auto", "mlx", "faster-whisper", "faster"),
        default="auto",
    )
    parser.add_argument("--model", default="auto", help="Backend model name or model ID")
    parser.add_argument("--language", default="auto", help="Spoken language code or auto")
    parser.add_argument("--output-dir", type=Path, default=Path("."))
    parser.add_argument("--basename", help="Output basename; defaults to input stem")
    parser.add_argument(
        "--formats",
        default="txt,srt,vtt,json",
        help="Comma-separated txt,srt,vtt,json,tsv or all",
    )
    parser.add_argument("--word-timestamps", action="store_true")
    parser.add_argument("--mixed-language", action="store_true")
    parser.add_argument(
        "--mixed-chunk-seconds",
        type=float,
        default=5.0,
        help="Core window length for mixed-language detection",
    )
    parser.add_argument(
        "--mixed-overlap-seconds",
        type=float,
        default=0.5,
        help="Context overlap added to both sides of mixed-language windows",
    )
    parser.add_argument("--beam-size", type=int, default=5)
    parser.add_argument("--cpu-threads", type=int, default=0)
    parser.add_argument("--device", choices=("auto", "cpu", "cuda"), default="auto")
    parser.add_argument("--compute-type", default="auto")
    parser.add_argument("--no-vad", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def memory_gib() -> float | None:
    if platform.system() == "Darwin":
        try:
            value = subprocess.check_output(
                ["sysctl", "-n", "hw.memsize"], text=True
            ).strip()
            return int(value) / (1024**3)
        except (OSError, subprocess.SubprocessError, ValueError):
            return None
    try:
        pages = os.sysconf("SC_PHYS_PAGES")
        page_size = os.sysconf("SC_PAGE_SIZE")
        return pages * page_size / (1024**3)
    except (AttributeError, OSError, ValueError):
        return None


def resolve_backend(requested: str, mixed_language: bool) -> str:
    if requested in ("faster", "faster-whisper"):
        return "faster-whisper"
    if requested == "mlx":
        return "mlx"
    if mixed_language:
        return "faster-whisper"
    if platform.system() == "Darwin" and platform.machine() == "arm64":
        return "mlx"
    return "faster-whisper"


def resolve_model(backend: str, requested: str) -> str:
    if requested != "auto":
        return requested
    if backend == "mlx":
        available_memory = memory_gib()
        if available_memory is not None and available_memory >= 15:
            return "mlx-community/whisper-large-v3-turbo"
        return "mlx-community/whisper-small-mlx"
    return "small"


def resolve_device(requested: str) -> str:
    if requested != "auto":
        return requested
    return "cuda" if shutil.which("nvidia-smi") else "cpu"


def resolve_compute_type(requested: str, device: str) -> str:
    if requested != "auto":
        return requested
    return "float16" if device == "cuda" else "int8"


def dataclass_or_dict(value: Any) -> dict[str, Any]:
    if value is None:
        return {}
    if isinstance(value, dict):
        return value
    if is_dataclass(value):
        return asdict(value)
    if hasattr(value, "_asdict"):
        return value._asdict()
    raise TypeError(f"Unsupported result type: {type(value)!r}")


def infer_text_language(text: str, global_language: str | None) -> tuple[str, str]:
    cjk = sum(
        1
        for char in text
        if "\u3400" <= char <= "\u9fff" or "\uf900" <= char <= "\ufaff"
    )
    latin = sum(1 for char in text if char.isascii() and char.isalpha())
    if cjk and latin:
        return "mixed", "text-script-heuristic"
    if cjk:
        code = global_language if global_language in {"zh", "yue", "ja"} else "zh"
        return code, "text-script-heuristic"
    if latin:
        if global_language and global_language not in {"zh", "yue", "ja", "ko"}:
            return global_language, "text-script-heuristic"
        return "en", "text-script-heuristic"
    return global_language or "und", "global-model-fallback"


def normalize_words(words: Iterable[Any] | None) -> list[dict[str, Any]]:
    normalized: list[dict[str, Any]] = []
    for item in words or []:
        word = dataclass_or_dict(item)
        normalized.append(
            {
                "start": float(word["start"]) if word.get("start") is not None else None,
                "end": float(word["end"]) if word.get("end") is not None else None,
                "word": str(word.get("word", "")),
                "probability": (
                    float(word["probability"])
                    if word.get("probability") is not None
                    else None
                ),
            }
        )
    return normalized


def normalize_segments(
    raw_segments: Iterable[Any], global_language: str | None
) -> list[dict[str, Any]]:
    normalized: list[dict[str, Any]] = []
    for index, item in enumerate(raw_segments):
        segment = dataclass_or_dict(item)
        text = str(segment.get("text", "")).strip()
        language, language_source = infer_text_language(text, global_language)
        normalized.append(
            {
                "id": int(segment.get("id", index)),
                "start": float(segment.get("start", 0.0)),
                "end": float(segment.get("end", 0.0)),
                "text": text,
                "language": language,
                "language_source": language_source,
                "avg_logprob": (
                    float(segment["avg_logprob"])
                    if segment.get("avg_logprob") is not None
                    else None
                ),
                "no_speech_prob": (
                    float(segment["no_speech_prob"])
                    if segment.get("no_speech_prob") is not None
                    else None
                ),
                "words": normalize_words(segment.get("words")),
            }
        )
    return normalized


def remove_boundary_overlap(previous: str, current: str) -> str:
    """Remove short exact suffix/prefix repetition introduced by adjacent windows."""
    previous = previous.rstrip()
    current = current.lstrip()
    max_length = min(24, len(previous), len(current))
    for length in range(max_length, 0, -1):
        if previous[-length:] != current[:length]:
            continue
        overlap = current[:length]
        has_cjk = any("\u3400" <= char <= "\u9fff" for char in overlap)
        if has_cjk or length >= 3:
            return current[length:].lstrip()
    return current


def transcribe_mlx(args: argparse.Namespace, model: str) -> dict[str, Any]:
    import mlx_whisper

    options: dict[str, Any] = {
        "path_or_hf_repo": model,
        "word_timestamps": args.word_timestamps,
        "condition_on_previous_text": not args.mixed_language,
        "verbose": False,
        "task": "transcribe",
    }
    if args.language != "auto":
        options["language"] = args.language
    result = mlx_whisper.transcribe(str(args.input), **options)
    language = result.get("language")
    segments = normalize_segments(result.get("segments", []), language)
    return {
        "language": language,
        "language_probability": None,
        "duration_seconds": max((s["end"] for s in segments), default=0.0),
        "segments": segments,
    }


def transcribe_faster(
    args: argparse.Namespace, model: str, device: str, compute_type: str
) -> dict[str, Any]:
    from faster_whisper import WhisperModel
    from faster_whisper.audio import decode_audio

    model_options: dict[str, Any] = {"device": device, "compute_type": compute_type}
    if args.cpu_threads > 0:
        model_options["cpu_threads"] = args.cpu_threads
    whisper = WhisperModel(model, **model_options)
    if args.mixed_language:
        if args.mixed_chunk_seconds <= 0:
            raise SystemExit("--mixed-chunk-seconds must be greater than zero")
        if args.mixed_overlap_seconds < 0:
            raise SystemExit("--mixed-overlap-seconds cannot be negative")
        sampling_rate = whisper.feature_extractor.sampling_rate
        audio = decode_audio(str(args.input), sampling_rate=sampling_rate)
        duration = len(audio) / sampling_rate
        segments: list[dict[str, Any]] = []
        windows: list[dict[str, Any]] = []
        core_start = 0.0
        while core_start < duration:
            core_end = min(duration, core_start + args.mixed_chunk_seconds)
            window_start = core_start
            window_end = min(duration, core_end + args.mixed_overlap_seconds)
            chunk = audio[
                round(window_start * sampling_rate) : round(window_end * sampling_rate)
            ]
            raw_segments, info = whisper.transcribe(
                chunk,
                language=None,
                task="transcribe",
                beam_size=args.beam_size,
                word_timestamps=True,
                vad_filter=not args.no_vad,
                multilingual=False,
                condition_on_previous_text=False,
            )
            chunk_segments = normalize_segments(list(raw_segments), info.language)
            for segment in chunk_segments:
                segment["start"] += window_start
                segment["end"] += window_start
                for word in segment["words"]:
                    if word["start"] is not None:
                        word["start"] += window_start
                    if word["end"] is not None:
                        word["end"] += window_start
                core_words = [
                    word
                    for word in segment["words"]
                    if word["start"] is not None
                    and word["end"] is not None
                    and (word["start"] + word["end"]) / 2 >= core_start
                    and (
                        (word["start"] + word["end"]) / 2 < core_end
                        or core_end >= duration
                    )
                ]
                if segment["words"]:
                    if not core_words:
                        continue
                    segment["words"] = core_words
                    segment["start"] = max(core_start, core_words[0]["start"])
                    segment["end"] = min(core_end, core_words[-1]["end"])
                    segment["text"] = "".join(
                        word["word"] for word in core_words
                    ).strip()
                else:
                    midpoint = (segment["start"] + segment["end"]) / 2
                    if midpoint < core_start or (
                        midpoint >= core_end and core_end < duration
                    ):
                        continue
                    segment["start"] = max(segment["start"], core_start)
                    segment["end"] = min(segment["end"], core_end)
                segment["language"] = info.language
                segment["language_source"] = "whisper-window-detection"
                segment["language_probability"] = float(info.language_probability)
                segments.append(segment)
            windows.append(
                {
                    "core_start": core_start,
                    "core_end": core_end,
                    "window_start": window_start,
                    "window_end": window_end,
                    "language": info.language,
                    "language_probability": float(info.language_probability),
                }
            )
            core_start = core_end
        segments.sort(key=lambda item: (item["start"], item["end"]))
        deduplicated: list[dict[str, Any]] = []
        for segment in segments:
            if deduplicated and deduplicated[-1]["language"] == segment["language"]:
                segment["text"] = remove_boundary_overlap(
                    deduplicated[-1]["text"], segment["text"]
                )
            if segment["text"]:
                deduplicated.append(segment)
        segments = deduplicated
        for index, segment in enumerate(segments):
            segment["id"] = index
        languages = {segment["language"] for segment in segments}
        return {
            "language": next(iter(languages)) if len(languages) == 1 else "mixed",
            "language_probability": None,
            "language_source": "whisper-window-detection",
            "duration_seconds": duration,
            "duration_after_vad_seconds": None,
            "language_windows": windows,
            "segments": segments,
        }
    raw_segments, info = whisper.transcribe(
        str(args.input),
        language=None if args.language == "auto" else args.language,
        task="transcribe",
        beam_size=args.beam_size,
        word_timestamps=args.word_timestamps,
        vad_filter=not args.no_vad,
        multilingual=args.mixed_language,
        condition_on_previous_text=not args.mixed_language,
    )
    segments = normalize_segments(list(raw_segments), info.language)
    return {
        "language": info.language,
        "language_probability": float(info.language_probability),
        "language_source": "whisper-global-detection",
        "duration_seconds": float(info.duration),
        "duration_after_vad_seconds": float(info.duration_after_vad),
        "language_windows": None,
        "segments": segments,
    }


def format_srt(seconds: float) -> str:
    milliseconds = max(0, round(seconds * 1000))
    hours, milliseconds = divmod(milliseconds, 3_600_000)
    minutes, milliseconds = divmod(milliseconds, 60_000)
    secs, milliseconds = divmod(milliseconds, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{milliseconds:03d}"


def format_vtt(seconds: float) -> str:
    return format_srt(seconds).replace(",", ".")


def render_srt(segments: list[dict[str, Any]]) -> str:
    cues = []
    for index, segment in enumerate(segments, start=1):
        cues.append(
            f"{index}\n{format_srt(segment['start'])} --> {format_srt(segment['end'])}\n"
            f"{segment['text']}\n"
        )
    return "\n".join(cues)


def render_vtt(segments: list[dict[str, Any]]) -> str:
    cues = ["WEBVTT\n"]
    for segment in segments:
        cues.append(
            f"{format_vtt(segment['start'])} --> {format_vtt(segment['end'])}\n"
            f"{segment['text']}\n"
        )
    return "\n".join(cues)


def requested_formats(value: str) -> tuple[str, ...]:
    formats = ALL_FORMATS if value.strip().lower() == "all" else tuple(
        item.strip().lower() for item in value.split(",") if item.strip()
    )
    invalid = sorted(set(formats) - set(ALL_FORMATS))
    if invalid:
        raise ValueError(f"Unsupported formats: {', '.join(invalid)}")
    return formats


def write_outputs(
    payload: dict[str, Any], output_dir: Path, basename: str, formats: tuple[str, ...]
) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    segments = payload["segments"]
    written: list[Path] = []
    if "json" in formats:
        path = output_dir / f"{basename}.json"
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
        written.append(path)
    if "txt" in formats:
        path = output_dir / f"{basename}.txt"
        path.write_text("\n".join(s["text"] for s in segments) + "\n")
        written.append(path)
    if "srt" in formats:
        path = output_dir / f"{basename}.srt"
        path.write_text(render_srt(segments))
        written.append(path)
    if "vtt" in formats:
        path = output_dir / f"{basename}.vtt"
        path.write_text(render_vtt(segments))
        written.append(path)
    if "tsv" in formats:
        path = output_dir / f"{basename}.tsv"
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle, delimiter="\t")
            writer.writerow(("start", "end", "language", "text"))
            for segment in segments:
                writer.writerow(
                    (segment["start"], segment["end"], segment["language"], segment["text"])
                )
        written.append(path)
    return written


def main() -> int:
    args = parse_args()
    input_path = args.input.expanduser().resolve()
    if not input_path.is_file():
        raise SystemExit(f"Input file not found: {input_path}")
    args.input = input_path
    backend = resolve_backend(args.backend, args.mixed_language)
    if backend == "mlx" and not (
        platform.system() == "Darwin" and platform.machine() == "arm64"
    ):
        raise SystemExit("The MLX backend requires an Apple Silicon Mac.")
    model = resolve_model(backend, args.model)
    device = resolve_device(args.device) if backend == "faster-whisper" else "metal"
    compute_type = (
        resolve_compute_type(args.compute_type, device)
        if backend == "faster-whisper"
        else "mlx"
    )
    plan = {
        "input": str(input_path),
        "backend": backend,
        "model": model,
        "device": device,
        "compute_type": compute_type,
        "mixed_language": args.mixed_language,
    }
    if args.dry_run:
        print(json.dumps(plan, ensure_ascii=False, indent=2))
        return 0

    result = (
        transcribe_mlx(args, model)
        if backend == "mlx"
        else transcribe_faster(args, model, device, compute_type)
    )
    payload = {
        "schema_version": 1,
        "input": str(input_path),
        "backend": backend,
        "model": model,
        "device": device,
        "compute_type": compute_type,
        "language": {
            "code": result.get("language"),
            "probability": result.get("language_probability"),
            "source": result.get("language_source", "whisper-global-detection"),
        },
        "duration_seconds": result.get("duration_seconds"),
        "duration_after_vad_seconds": result.get("duration_after_vad_seconds"),
        "language_windows": result.get("language_windows"),
        "options": {
            "word_timestamps": args.word_timestamps or args.mixed_language,
            "mixed_language": args.mixed_language,
            "beam_size": args.beam_size,
            "vad_filter": backend == "faster-whisper" and not args.no_vad,
            "condition_on_previous_text": not args.mixed_language,
            "mixed_chunk_seconds": (
                args.mixed_chunk_seconds if args.mixed_language else None
            ),
            "mixed_overlap_seconds": (
                args.mixed_overlap_seconds if args.mixed_language else None
            ),
        },
        "text": " ".join(s["text"] for s in result["segments"]).strip(),
        "segments": result["segments"],
    }
    formats = requested_formats(args.formats)
    basename = args.basename or input_path.stem
    output_dir = args.output_dir.expanduser().resolve()
    paths = write_outputs(payload, output_dir, basename, formats)
    summary = {
        **plan,
        "detected_language": payload["language"],
        "segments": len(payload["segments"]),
        "outputs": [str(path) for path in paths],
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        raise SystemExit(130)
