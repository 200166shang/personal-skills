#!/usr/bin/env python3
"""Translate Whisper JSON segments with an already-installed local Ollama model."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any


LANGUAGE_NAMES = {
    "zh": "Simplified Chinese",
    "zh-CN": "Simplified Chinese",
    "zh-TW": "Traditional Chinese",
    "en": "English",
    "ja": "Japanese",
    "ko": "Korean",
    "fr": "French",
    "de": "German",
    "es": "Spanish",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Translate ASR JSON while preserving segment timestamps."
    )
    parser.add_argument("source_json", type=Path)
    parser.add_argument("--target-language", required=True)
    parser.add_argument("--model", default="auto", help="Installed Ollama model name")
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--basename")
    parser.add_argument("--batch-size", type=int, default=40)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def installed_models() -> list[str]:
    if not shutil.which("ollama"):
        raise SystemExit(
            "Ollama is not installed. Install it first, or translate with another explicitly approved provider."
        )
    result = subprocess.run(
        ["ollama", "list"], text=True, capture_output=True, check=False
    )
    if result.returncode != 0:
        raise SystemExit(f"Could not list Ollama models: {result.stderr.strip()}")
    lines = [line.split() for line in result.stdout.splitlines()[1:] if line.strip()]
    return [fields[0] for fields in lines if fields]


def choose_model(requested: str, available: list[str]) -> str:
    if requested != "auto":
        if requested not in available:
            raise SystemExit(
                f"Ollama model '{requested}' is not installed. Installed models: {', '.join(available) or 'none'}. "
                "Ask before downloading a large model."
            )
        return requested
    preferred_prefixes = ("qwen3:", "qwen2.5:", "gemma3:", "llama3.2:")
    for prefix in preferred_prefixes:
        for model in available:
            if model.startswith(prefix):
                return model
    if available:
        return available[0]
    raise SystemExit(
        "No Ollama text model is installed. Ask before running a multi-gigabyte 'ollama pull'."
    )


def extract_json(text: str) -> dict[str, Any]:
    stripped = re.sub(r"\x1b\[[0-?]*[ -/]*[@-~]", "", text).strip()
    try:
        return json.loads(stripped, strict=False)
    except json.JSONDecodeError:
        start = stripped.find("{")
        end = stripped.rfind("}")
        if start >= 0 and end > start:
            return json.loads(stripped[start : end + 1], strict=False)
        raise


def translate_batch(
    model: str, target_language: str, segments: list[dict[str, Any]]
) -> dict[int, str]:
    target_name = LANGUAGE_NAMES.get(target_language, target_language)
    items = [{"id": int(item["id"]), "text": item["text"]} for item in segments]
    prompt = f"""Translate each subtitle into {target_name}.
Return only JSON in this exact shape: {{"translations":[{{"id":0,"text":"..."}}]}}.
Keep every id exactly once and in the same order. Preserve names, numbers, and technical terms. Do not merge, split, summarize, explain, or include timestamps.

Subtitles:
{json.dumps(items, ensure_ascii=False)}
"""
    command = [
        "ollama",
        "run",
        model,
        "--format",
        "json",
        "--think=false",
        "--nowordwrap",
    ]
    environment = {**os.environ, "NO_COLOR": "1", "TERM": "dumb"}
    result = subprocess.run(
        command,
        input=prompt,
        text=True,
        capture_output=True,
        check=False,
        env=environment,
    )
    if result.returncode != 0:
        raise SystemExit(f"Ollama translation failed: {result.stderr.strip()}")
    payload = extract_json(result.stdout)
    translated = payload.get("translations")
    if not isinstance(translated, list):
        raise SystemExit("Ollama response did not contain a translations list.")
    mapping = {
        int(item["id"]): " ".join(str(item["text"]).split()) for item in translated
    }
    expected = {item["id"] for item in items}
    if set(mapping) != expected or any(not mapping[item] for item in expected):
        raise SystemExit("Ollama response omitted, duplicated, or emptied a subtitle segment.")
    return mapping


def format_srt(seconds: float) -> str:
    milliseconds = max(0, round(seconds * 1000))
    hours, milliseconds = divmod(milliseconds, 3_600_000)
    minutes, milliseconds = divmod(milliseconds, 60_000)
    secs, milliseconds = divmod(milliseconds, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{milliseconds:03d}"


def render_srt(segments: list[dict[str, Any]]) -> str:
    return "\n".join(
        f"{index}\n{format_srt(item['start'])} --> {format_srt(item['end'])}\n{item['text']}\n"
        for index, item in enumerate(segments, start=1)
    )


def render_vtt(segments: list[dict[str, Any]]) -> str:
    return "WEBVTT\n\n" + "\n".join(
        f"{format_srt(item['start']).replace(',', '.')} --> "
        f"{format_srt(item['end']).replace(',', '.')}\n{item['text']}\n"
        for item in segments
    )


def main() -> int:
    args = parse_args()
    source_path = args.source_json.expanduser().resolve()
    source = json.loads(source_path.read_text())
    segments = source.get("segments")
    if not isinstance(segments, list) or not segments:
        raise SystemExit("Source JSON has no segments.")
    available = installed_models()
    model = choose_model(args.model, available)
    plan = {
        "source": str(source_path),
        "target_language": args.target_language,
        "translator": "ollama",
        "model": model,
        "segments": len(segments),
    }
    if args.dry_run:
        print(json.dumps(plan, ensure_ascii=False, indent=2))
        return 0

    translations: dict[int, str] = {}
    batch_size = max(1, args.batch_size)
    for offset in range(0, len(segments), batch_size):
        translations.update(
            translate_batch(model, args.target_language, segments[offset : offset + batch_size])
        )
    localized = []
    for index, segment in enumerate(segments):
        segment_id = int(segment.get("id", index))
        localized.append(
            {
                "id": segment_id,
                "start": float(segment["start"]),
                "end": float(segment["end"]),
                "source_language": segment.get("language") or source.get("language", {}).get("code"),
                "target_language": args.target_language,
                "source_text": segment["text"],
                "text": translations[segment_id],
            }
        )
    output = {
        "schema_version": 1,
        "source_json": str(source_path),
        "translator": {"backend": "ollama", "model": model},
        "target_language": args.target_language,
        "segments": localized,
    }
    output_dir = (args.output_dir or source_path.parent).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    basename = args.basename or f"{source_path.stem}.{args.target_language}"
    paths = {
        "json": output_dir / f"{basename}.json",
        "srt": output_dir / f"{basename}.srt",
        "vtt": output_dir / f"{basename}.vtt",
        "txt": output_dir / f"{basename}.txt",
    }
    paths["json"].write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n")
    paths["srt"].write_text(render_srt(localized))
    paths["vtt"].write_text(render_vtt(localized))
    paths["txt"].write_text("\n".join(item["text"] for item in localized) + "\n")
    print(
        json.dumps(
            {**plan, "outputs": [str(path) for path in paths.values()]},
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
