#!/usr/bin/env python3
"""Validate the timestamp and text invariants of local-whisper JSON output."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("json_path", type=Path)
    args = parser.parse_args()
    payload = json.loads(args.json_path.read_text())
    segments = payload.get("segments")
    if not isinstance(segments, list) or not segments:
        raise SystemExit("FAIL: segments must be a non-empty list")
    previous_end = 0.0
    for index, segment in enumerate(segments):
        start = float(segment["start"])
        end = float(segment["end"])
        if start < 0 or end <= start:
            raise SystemExit(f"FAIL: invalid segment interval at index {index}")
        if start + 0.05 < previous_end:
            raise SystemExit(f"FAIL: non-monotonic segment interval at index {index}")
        if not str(segment.get("text", "")).strip():
            raise SystemExit(f"FAIL: empty segment text at index {index}")
        previous_end = max(previous_end, end)
        for word_index, word in enumerate(segment.get("words") or []):
            word_start = word.get("start")
            word_end = word.get("end")
            if word_start is None or word_end is None:
                continue
            if float(word_start) > float(word_end):
                raise SystemExit(
                    f"FAIL: invalid word interval at segment {index}, word {word_index}"
                )
            if float(word_start) + 0.05 < start or float(word_end) > end + 0.05:
                raise SystemExit(
                    f"FAIL: word outside segment at segment {index}, word {word_index}"
                )
    print(f"PASS: {len(segments)} segments, timestamps and text are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
