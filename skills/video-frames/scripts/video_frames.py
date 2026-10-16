#!/usr/bin/env python3
"""Time-labelled video previews and verified single-frame captures. No model calls."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import os

from PIL import Image, ImageDraw, ImageFont, ImageOps


def digest(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def save_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as stream:
        json.dump(data, stream, ensure_ascii=False, indent=2, allow_nan=False)
        stream.write("\n")
        temp = stream.name
    os.replace(temp, path)


def probe(video):
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_format", "-show_streams", "-of", "json", str(video)],
        capture_output=True, text=True, check=True, timeout=60,
    )
    data = json.loads(result.stdout)
    stream = next((s for s in data["streams"] if s["codec_type"] == "video"), None)
    if stream is None:
        raise ValueError("Input has no video stream")
    duration = float(data["format"]["duration"])
    if not math.isfinite(duration) or duration <= 0:
        raise ValueError("Video duration must be finite and positive")
    try:
        video_duration = float(stream.get("duration", duration))
        if not math.isfinite(video_duration) or video_duration <= 0:
            video_duration = duration
    except (TypeError, ValueError):
        video_duration = duration
    return {"duration": duration, "video_duration": min(duration, video_duration),
            "width": stream["width"], "height": stream["height"]}


def timestamp(value):
    milliseconds = round(value * 1000)
    hours, remainder = divmod(milliseconds, 3600000)
    minutes, remainder = divmod(remainder, 60000)
    seconds, milliseconds = divmod(remainder, 1000)
    return f"{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:03}"


def sample_times(start, end, interval):
    if not all(math.isfinite(v) for v in (start, end, interval)):
        raise ValueError("Times and interval must be finite")
    if start < 0 or end <= start or interval <= 0:
        raise ValueError("Require 0 <= start < end and interval > 0")
    count = math.ceil((end - start) / interval)
    if count > 10000:
        raise ValueError("Preview would exceed 10000 frames; use a shorter window or larger interval")
    times = [round(start + i * interval, 6) for i in range(count)]
    tail = round(max(start, end - min(0.1, (end - start) / 2)), 6)
    if tail - times[-1] > min(0.2, interval / 2):
        times.append(tail)
    return times


def extract(video, seconds, target):
    target = Path(target)
    temporary = target.with_name(target.stem + ".partial.jpg")
    try:
        result = subprocess.run(
            ["ffmpeg", "-nostdin", "-v", "error", "-y", "-ss", str(seconds),
             "-i", str(video), "-map", "0:v:0", "-frames:v", "1", "-q:v", "2", str(temporary)],
            capture_output=True, text=True, timeout=90,
        )
        if result.returncode or not temporary.exists() or not temporary.stat().st_size:
            raise ValueError(f"No frame at {seconds}: {result.stderr[-500:]}")
        with Image.open(temporary) as im:
            im.verify()
        temporary.replace(target)
    finally:
        temporary.unlink(missing_ok=True)
    return target


def preview(args):
    video = args.video.resolve(strict=True)
    info = probe(video)
    end = info["duration"] if args.end is None else args.end
    if end > info["duration"]:
        raise ValueError("Preview end exceeds video duration")
    end = min(end, info["video_duration"])
    match = re.fullmatch(r"([1-4])x([1-4])", args.grid)
    if not match:
        raise ValueError("Grid must be COLSxROWS, each between 1 and 4")
    cols, rows = map(int, match.groups())
    if not 160 <= args.cell_width <= 1600:
        raise ValueError("Cell width must be between 160 and 1600")
    times = sample_times(args.start, end, args.interval)
    out = args.output_dir.resolve()
    out.mkdir(parents=True, exist_ok=True)
    manifest = out / "preview.json"
    signature = {"video_sha256": digest(video), "start": args.start, "end": end,
                 "interval": args.interval, "grid": args.grid, "cell_width": args.cell_width, "layout_version": 1}
    if manifest.exists():
        previous = json.loads(manifest.read_text())
        if previous["input"] != signature:
            raise ValueError("Preview inputs changed; choose a new output directory")
        if all((out / p["file"]).exists() and digest(out / p["file"]) == p.get("sha256")
               for p in previous["sheets"]):
            return {"ok": True, "cache_hit": True, "manifest": str(manifest), "sheets": previous["sheets"]}
    frame_dir = out / "frames"
    frame_dir.mkdir(exist_ok=True)
    paths = [frame_dir / f"{i:05}.jpg" for i in range(len(times))]
    def run(item):
        i, value = item
        extract(video, value, paths[i])
    with ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(run, enumerate(times)))
    cell_width = min(args.cell_width, info["width"])
    image_height = max(1, round(info["height"] * cell_width / info["width"]))
    label_height = 28
    cell_height = image_height + label_height
    font = ImageFont.load_default(size=17)
    sheets = []
    for group_start in range(0, len(times), cols * rows):
        indices = list(range(group_start, min(group_start + cols * rows, len(times))))
        actual_rows = math.ceil(len(indices) / cols)
        canvas = Image.new("RGB", (cols * cell_width, actual_rows * cell_height), "#19242b")
        draw = ImageDraw.Draw(canvas)
        cells = []
        for slot, index in enumerate(indices):
            x, y = (slot % cols) * cell_width, (slot // cols) * cell_height
            with Image.open(paths[index]) as im:
                image = ImageOps.contain(im, (cell_width, image_height))
                canvas.paste(image, (x + (cell_width - image.width) // 2, y + label_height))
            draw.text((x + 8, y + 4), timestamp(times[index]), fill="#ffe3a2", font=font)
            cells.append({"slot": slot, "timestamp": times[index], "frame": str(paths[index].relative_to(out))})
        name = f"preview-{len(sheets) + 1:03}.jpg"
        canvas.save(out / name, quality=88)
        sheets.append({"file": name, "sha256": digest(out / name), "cells": cells})
    data = {"schema_version": 1, "input": signature, "media": info, "sheets": sheets}
    save_json(manifest, data)
    return {"ok": True, "cache_hit": False, "manifest": str(manifest), "sheets": sheets}


def capture(args):
    video = args.video.resolve(strict=True)
    info = probe(video)
    plan = json.loads(args.plan.read_text())
    figures = plan.get("figures")
    if not isinstance(figures, list):
        raise ValueError("Plan requires a figures array")
    seen = set()
    for figure in figures:
        identifier = figure.get("id", "")
        if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]{0,63}", identifier) or identifier in seen:
            raise ValueError(f"Invalid or duplicate figure ID: {identifier}")
        seen.add(identifier)
        value = float(figure["timestamp"])
        if not math.isfinite(value) or not 0 <= value < info["duration"]:
            raise ValueError(f"Timestamp outside video: {identifier}")
    out = args.output_dir.resolve()
    out.mkdir(parents=True, exist_ok=True)
    media_hash = digest(video)
    results = []
    failures = []
    for figure in figures:
        path = out / f"{figure['id']}.jpg"
        try:
            extract(video, figure["timestamp"], path)
            results.append({"id": figure["id"], "timestamp": figure["timestamp"],
                            "file": path.name, "sha256": digest(path), "frame_pts": None})
        except (ValueError, subprocess.TimeoutExpired, OSError) as exc:
            failures.append({"id": figure["id"], "error": str(exc)})
    manifest = out / "captures.json"
    save_json(manifest, {"schema_version": 1, "video_sha256": media_hash,
                         "figures": results, "failures": failures})
    return {"ok": not failures, "manifest": str(manifest), "figures": results, "failures": failures}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("preview", help="Create time-labelled contact sheets")
    p.add_argument("--video", type=Path, required=True)
    p.add_argument("--start", type=float, default=0)
    p.add_argument("--end", type=float)
    p.add_argument("--interval", type=float, default=6)
    p.add_argument("--grid", default="2x2")
    p.add_argument("--cell-width", type=int, default=640)
    p.add_argument("--output-dir", type=Path, required=True)
    p.set_defaults(handler=preview)
    p = sub.add_parser("capture", help="Extract figures listed in a JSON plan")
    p.add_argument("--video", type=Path, required=True)
    p.add_argument("--plan", type=Path, required=True)
    p.add_argument("--output-dir", type=Path, required=True)
    p.set_defaults(handler=capture)
    args = parser.parse_args()
    try:
        result = args.handler(args)
    except (ValueError, KeyError, OSError, subprocess.SubprocessError) as exc:
        result = {"ok": False, "error": str(exc)}
    print(json.dumps(result, ensure_ascii=False, allow_nan=False))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
