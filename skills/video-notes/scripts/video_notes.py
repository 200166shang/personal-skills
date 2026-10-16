#!/usr/bin/env python3
"""Prepare, assemble, render and validate illustrated notes. Writing stays with the caller."""
import argparse
import hashlib
import html
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from urllib.parse import parse_qsl, unquote, urlencode, urlsplit, urlunsplit

from markdown_it import MarkdownIt
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name, TextLexer
from pygments.util import ClassNotFound

ASSETS = Path(__file__).resolve().parent.parent / "assets"
MARKER = re.compile(r"<!--\s*figure:([A-Za-z][A-Za-z0-9_-]{0,63})\s*-->")


def digest(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as stream:
        json.dump(data, stream, ensure_ascii=False, indent=2, allow_nan=False)
        stream.write("\n")
        temp = stream.name
    os.replace(temp, path)


def video_info(video):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_format", "-show_streams",
                             "-of", "json", str(video)], capture_output=True, text=True,
                            check=True, timeout=60)
    raw = json.loads(result.stdout)
    stream = next((s for s in raw["streams"] if s["codec_type"] == "video"), None)
    if stream is None:
        raise ValueError("Input has no video stream")
    return {"duration": float(raw["format"]["duration"]), "width": stream["width"], "height": stream["height"]}


def subtitle_segments(path, duration):
    text = Path(path).read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    if Path(path).suffix.lower() == ".json":
        source = json.loads(text)
        segments = source["segments"]
    elif Path(path).suffix.lower() == ".srt":
        pattern = re.compile(r"(\d{2,}):(\d{2}):(\d{2})[,.](\d{3})\s*-->\s*"
                             r"(\d{2,}):(\d{2}):(\d{2})[,.](\d{3})[^\n]*\n(.+?)(?=\n\s*\n|\Z)", re.S)
        segments = []
        for match in pattern.finditer(text):
            values = list(map(int, match.groups()[:8]))
            if any(values[i] >= 60 for i in (1, 2, 5, 6)):
                raise ValueError("Invalid minute/second in SRT")
            start = sum(v * scale for v, scale in zip(values[:4], (3600, 60, 1, .001)))
            end = sum(v * scale for v, scale in zip(values[4:], (3600, 60, 1, .001)))
            segments.append({"start": start, "end": end, "text": match.group(9).strip()})
        arrow_count = text.count("-->")
        if arrow_count != len(segments):
            raise ValueError("Some SRT cues could not be parsed; repair the source first")
    else:
        raise ValueError("Transcript must be SRT or timestamped JSON")
    normalized = []
    previous_start = -1
    for i, segment in enumerate(segments):
        start, end = float(segment["start"]), float(segment["end"])
        content = str(segment["text"]).strip()
        if not all(math.isfinite(t) for t in (start, end)) or not (0 <= start < end <= duration + .5):
            raise ValueError(f"Transcript time outside media at cue {i + 1}")
        if start < previous_start or not content:
            raise ValueError(f"Unordered or empty transcript cue {i + 1}")
        previous_start = start
        normalized.append({"id": f"seg{i + 1:05}", "start": start, "end": end, "text": content})
    if not normalized:
        raise ValueError("Transcript has no readable segments")
    if normalized[-1]["end"] < duration * .75:
        raise ValueError("Transcript ends before 75% of the video; verify media/part and supply a matching transcript")
    return normalized


def media_identity(url, fallback):
    parts = urlsplit(url)
    if parts.scheme and parts.scheme not in ("https", "http"):
        raise ValueError("Source URL must use HTTP(S)")
    if url and not parts.netloc:
        raise ValueError("Source URL requires a hostname")
    query = dict(parse_qsl(parts.query))
    match = re.search(r"/(BV[0-9A-Za-z]+)", parts.path)
    if parts.hostname in ("bilibili.com", "www.bilibili.com") and match:
        part = query.get("p", "1")
        if not part.isdigit() or int(part) < 1:
            raise ValueError("Invalid Bilibili part number")
        return f"{match.group(1)}_p{int(part)}", int(part)
    return fallback, None


def prepare(args):
    video = args.video.resolve(strict=True)
    transcript = args.transcript.resolve(strict=True)
    info = video_info(video)
    if not math.isfinite(args.window_seconds) or args.window_seconds <= 0:
        raise ValueError("Window seconds must be finite and positive")
    segments = subtitle_segments(transcript, info["duration"])
    scope_end = info["duration"] if args.end is None else args.end
    if not all(math.isfinite(t) for t in (args.start, scope_end)) or not 0 <= args.start < scope_end <= info["duration"]:
        raise ValueError("Require 0 <= start < end <= media duration")
    scoped = [s for s in segments if s["end"] > args.start and s["start"] < scope_end]
    if not scoped:
        raise ValueError("Requested scope has no transcript segments")
    scope_start = min(args.start, scoped[0]["start"])
    media_id, part = media_identity(args.source_url, video.stem)
    fingerprint = {"video_sha256": digest(video), "transcript_sha256": digest(transcript),
                   "window_seconds": args.window_seconds, "source_url": args.source_url,
                   "title": args.title or video.stem, "start": args.start, "end": scope_end, "contract_version": 1}
    work = args.work_dir.resolve()
    work.mkdir(parents=True, exist_ok=True)
    job_file = work / "job.json"
    if job_file.exists():
        old = read_json(job_file)
        if old["input"] != fingerprint:
            raise ValueError("Inputs changed; use a new work directory. Existing drafts were preserved")
        if old["normalized_sha256"] != digest(work / "transcript.json"):
            raise ValueError("Normalized transcript changed; use a new work directory")
        return {"ok": True, "cache_hit": True, "job": str(job_file), "windows": len(old["windows"])}
    normalized = {"schema_version": 1, "segments": segments}
    save_json(work / "transcript.json", normalized)
    windows = []
    start = scope_start
    cursor = 0
    while start < scope_end:
        end = min(start + args.window_seconds, scope_end)
        owned = []
        while cursor < len(scoped) and scoped[cursor]["start"] < end:
            segment = scoped[cursor]
            owned.append(segment["id"])
            end = min(info["duration"], max(end, segment["end"]))
            cursor += 1
        identifier = f"w{len(windows) + 1:03}"
        windows.append({"id": identifier, "start": start, "end": end, "segment_ids": owned,
                        "status": "pending", "chunk": f"chunks/{identifier}.md"})
        start = end
    (work / "chunks").mkdir(exist_ok=True)
    source = {"title": fingerprint["title"], "url": args.source_url, "media_id": media_id,
              "part": part, **info, "range": {"start": scope_start, "end": windows[-1]["end"]},
              "source_review": args.source_note}
    job = {"schema_version": 1, "input": fingerprint, "video": str(video),
           "transcript_source": str(transcript), "normalized_sha256": digest(work / "transcript.json"),
           "source": source, "windows": windows}
    save_json(job_file, job)
    save_json(work / "note-plan.json", {"schema_version": 1, "figures": []})
    return {"ok": True, "cache_hit": False, "job": str(job_file), "source": source, "windows": len(windows)}


def inside(root, relative):
    root = Path(root).resolve()
    if Path(relative).is_absolute():
        raise ValueError("Expected a relative asset path")
    path = (root / relative).resolve()
    if not path.is_relative_to(root):
        raise ValueError(f"Asset escapes its directory: {relative}")
    return path


def review(args):
    work = args.work_dir.resolve()
    job = read_json(work / "job.json")
    window = next((w for w in job["windows"] if w["id"] == args.window), None)
    if window is None:
        raise ValueError("Unknown window")
    chunk = inside(work, window["chunk"])
    if not chunk.exists() or not chunk.read_text().strip():
        raise ValueError("Write the window's Markdown chunk first")
    if not args.source_reviewed or not args.visual_reviewed or not args.note.strip():
        raise ValueError("Explicit source and visual review attestations and a review note are required")
    window.update(status="reviewed", sha256=digest(chunk), review_note=args.note)
    save_json(work / "job.json", job)
    return {"ok": True, "window": window["id"], "status": "reviewed"}


def checked_job(work):
    job = read_json(work / "job.json")
    expected_id, expected_part = media_identity(job["input"]["source_url"], Path(job["video"]).stem)
    if (job["source"]["url"] != job["input"]["source_url"] or job["source"]["media_id"] != expected_id
            or job["source"]["part"] != expected_part):
        raise ValueError("Source URL, media ID or part changed since preparation")
    if digest(job["video"]) != job["input"]["video_sha256"]:
        raise ValueError("Source video changed")
    if digest(job["transcript_source"]) != job["input"]["transcript_sha256"]:
        raise ValueError("Source transcript changed")
    if digest(work / "transcript.json") != job["normalized_sha256"]:
        raise ValueError("Normalized transcript changed")
    scope = job["source"]["range"]
    segments = read_json(work / "transcript.json")["segments"]
    expected = [s["id"] for s in segments if s["end"] > scope["start"] and s["start"] < scope["end"]]
    assigned = [identifier for w in job["windows"] for identifier in w["segment_ids"]]
    if assigned != expected:
        raise ValueError("Work windows do not cover the scope's transcript exactly once in order")
    cursor = scope["start"]
    for window in job["windows"]:
        if window["start"] != cursor or window["end"] <= cursor:
            raise ValueError("Work windows have a gap or overlap")
        cursor = window["end"]
        path = inside(work, window["chunk"])
        if window["status"] != "reviewed" or not path.exists() or digest(path) != window.get("sha256"):
            raise ValueError(f"Window {window['id']} is unreviewed or its draft changed")
    if cursor != scope["end"]:
        raise ValueError("Work windows do not reach the end of scope")
    if not job["source"].get("source_review", "").strip():
        raise ValueError("Record media/transcript source matching in job.source.source_review first")
    return job


def source_link(url, seconds):
    if not url:
        return ""
    parts = urlsplit(url)
    values = dict(parse_qsl(parts.query))
    values["t"] = str(int(seconds))
    return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(values), parts.fragment))


def time_label(seconds):
    hours, remainder = divmod(int(seconds), 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}" if hours else f"{minutes:02}:{seconds:02}"


def markdown_escape(text):
    return re.sub(r"([\\`*{}\[\]<>_])", r"\\\1", str(text).replace("\n", " "))


def assemble(args):
    work = args.plan.resolve().parent
    job = checked_job(work)
    plan = read_json(args.plan)
    captures = read_json(args.captures)
    if captures.get("failures") or captures["video_sha256"] != job["input"]["video_sha256"]:
        raise ValueError("Capture failures or wrong source video")
    draft = args.draft.resolve(strict=True)
    out = args.output_dir.resolve()
    if out == work or (out / "note.md") == draft:
        raise ValueError("Choose a separate delivery directory; preserve the source draft")
    text = draft.read_text(encoding="utf-8")
    if not text.strip():
        raise ValueError("Draft must contain readable Markdown")
    identifiers = MARKER.findall(text)
    if len(identifiers) != len(set(identifiers)):
        raise ValueError("Each figure marker must occur once")
    figures = plan["figures"]
    figure_map = {f["id"]: f for f in figures}
    if len(figure_map) != len(figures) or set(identifiers) != set(figure_map):
        raise ValueError("Figure markers and plan IDs must match exactly")
    if any(not re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]{0,63}", identifier) for identifier in identifiers):
        raise ValueError("Invalid figure ID")
    capture_map = {f["id"]: f for f in captures["figures"]}
    if len(capture_map) != len(captures["figures"]) or set(capture_map) != set(figure_map):
        raise ValueError("Captures must match the figure plan exactly")
    segment_ids = {s["id"] for s in read_json(work / "transcript.json")["segments"]}
    replacements = {}
    verified_paths = []
    for identifier, figure in figure_map.items():
        capture = capture_map[identifier]
        value = float(figure["timestamp"])
        if not math.isfinite(value) or not job["source"]["range"]["start"] <= value < job["source"]["range"]["end"]:
            raise ValueError(f"Invalid figure time: {identifier}")
        if value != capture["timestamp"]:
            raise ValueError(f"Capture time differs from plan: {identifier}")
        path = inside(args.captures.resolve().parent, capture["file"])
        actual_hash = digest(path)
        if actual_hash != capture["sha256"] or figure.get("reviewed_sha256") != actual_hash:
            raise ValueError(f"View this final screenshot and record reviewed_sha256: {identifier}")
        refs = figure.get("source_segment_ids", [])
        if not refs or not set(refs).issubset(segment_ids):
            raise ValueError(f"Unknown or missing source segment IDs: {identifier}")
        caption = markdown_escape(figure.get("caption", "").strip())
        if not caption:
            raise ValueError(f"Missing caption: {identifier}")
        link = source_link(job["source"]["url"], value)
        label = time_label(value)
        locator = f"[原片 {label}]({link})" if link else label
        replacements[identifier] = f"![{caption}](images/{identifier}.jpg)\n\n*{caption} · {locator}*"
        verified_paths.append((path, f"images/{identifier}.jpg"))
    rendered = MARKER.sub(lambda m: replacements[m[1]], text)
    if "<!--" in rendered and "figure:" in rendered:
        raise ValueError("Unrecognized figure marker remains")
    out.mkdir(parents=True, exist_ok=True)
    for path, name in verified_paths:
        target = out / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
    (out / "note.md").write_text(rendered, encoding="utf-8")
    sources = out / "sources"
    sources.mkdir(exist_ok=True)
    shutil.copy2(work / "transcript.json", sources / "transcript.json")
    shutil.copy2(job["transcript_source"], sources / ("transcript.srt" if Path(job["transcript_source"]).suffix.lower() == ".srt" else "transcript.original.json"))
    save_json(sources / "source.json", job["source"])
    save_json(sources / "review.json", {"windows": job["windows"], "figures": figures,
                                       "draft_sha256": digest(draft), "note_sha256": digest(out / "note.md")})
    return {"ok": True, "markdown": str(out / "note.md"), "figures": len(figures)}


def code_highlight(code, language, attrs=""):
    try:
        lexer = get_lexer_by_name(language) if language else TextLexer()
    except ClassNotFound:
        lexer = TextLexer()
    return highlight(code, lexer, HtmlFormatter(nowrap=False))


def markdown_engine():
    return MarkdownIt("commonmark", {"html": False, "highlight": code_highlight}).enable("table").enable("strikethrough")


def image_refs(tokens):
    refs = []
    for token in tokens:
        if token.type == "image":
            refs.append(token.attrGet("src"))
        if token.children:
            refs.extend(image_refs(token.children))
    return refs


def checked_images(markdown_path, tokens):
    found = []
    for ref in image_refs(tokens):
        parts = urlsplit(ref)
        if parts.scheme or parts.netloc or parts.query or parts.fragment:
            raise ValueError(f"Offline notes require plain relative image paths: {ref}")
        path = inside(markdown_path.parent, unquote(parts.path))
        if not path.is_file() or path.stat().st_size == 0:
            raise ValueError(f"Missing or empty image: {ref}")
        found.append((path, unquote(parts.path)))
    return found


def render(args):
    markdown = args.markdown.resolve(strict=True)
    text = markdown.read_text(encoding="utf-8")
    if MARKER.search(text):
        raise ValueError("Assemble screenshot markers before rendering")
    engine = markdown_engine()
    tokens = engine.parse(text)
    images = checked_images(markdown, tokens)
    used = set()
    headings = []
    title = "视频笔记"
    for i, token in enumerate(tokens):
        if token.type != "heading_open":
            continue
        content = tokens[i + 1].content
        if token.tag == "h1":
            title = content
        slug = re.sub(r"[^\w-]+", "-", content.lower()).strip("-") or "section"
        base, suffix = slug, 1
        while slug in used:
            suffix += 1
            slug = f"{base}-{suffix}"
        used.add(slug)
        token.attrSet("id", slug)
        if token.tag in ("h2", "h3"):
            headings.append((token.tag, slug, content))
    body = engine.renderer.render(tokens, engine.options, {})
    toc = "".join(f'<a class="{tag}" href="#{html.escape(slug, quote=True)}">{html.escape(text)}</a>'
                  for tag, slug, text in headings)
    page = (ASSETS / "note.html").read_text()
    replacements = {"title": html.escape(title), "toc": toc, "body": body}
    page = re.sub(r"\{\{(title|toc|body)\}\}", lambda match: replacements[match[1]], page)
    out = args.output_dir.resolve()
    out.mkdir(parents=True, exist_ok=True)
    for source, name in images:
        target = inside(out, name)
        if source != target:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
    css = out / "assets/note.css"
    css.parent.mkdir(exist_ok=True)
    css.write_text((ASSETS / "note.css").read_text() + "\n" + HtmlFormatter().get_style_defs(".highlight"))
    page_path = out / "note.html"
    page_path.write_text(page, encoding="utf-8")
    save_json(out / "render.json", {"markdown_sha256": digest(markdown), "html_sha256": digest(page_path),
                                   "css_sha256": digest(css), "images": {name: digest(path) for path, name in images}})
    return {"ok": True, "html": str(page_path), "headings": len(headings), "images": len(images)}


def validate(args):
    out = args.output_dir.resolve()
    job = checked_job(args.plan.resolve().parent)
    plan = read_json(args.plan)
    md = out / "note.md"
    text = md.read_text(encoding="utf-8")
    if MARKER.search(text) or re.search(r"<!--\s*figure:", text):
        raise ValueError("Unresolved figure markers")
    refs = checked_images(md, markdown_engine().parse(text))
    expected = {f"images/{f['id']}.jpg" for f in plan["figures"]}
    if expected != {name for _, name in refs}:
        raise ValueError("Delivered images differ from figure plan")
    review_data = read_json(out / "sources/review.json")
    if (review_data["note_sha256"] != digest(md) or review_data["figures"] != plan["figures"]
            or review_data["windows"] != job["windows"]):
        raise ValueError("Delivered note or figure plan changed since assembly")
    source = read_json(out / "sources/source.json")
    if source != job["source"]:
        raise ValueError("Source metadata differs from reviewed job")
    rendered = read_json(out / "render.json")
    if (rendered["markdown_sha256"] != digest(md) or rendered["html_sha256"] != digest(out / "note.html")
            or rendered["css_sha256"] != digest(out / "assets/note.css")):
        raise ValueError("HTML/CSS is stale; render the current Markdown again")
    for path, name in refs:
        if digest(path) != rendered["images"].get(name):
            raise ValueError(f"Image changed after rendering: {name}")
    for figure in plan["figures"]:
        if digest(out / "images" / f"{figure['id']}.jpg") != figure["reviewed_sha256"]:
            raise ValueError("Delivered screenshot differs from visually reviewed file")
    report = {"ok": True, "scope": "structural checks; semantic and visual review are caller attestations",
              "media_id": source["media_id"], "windows": len(job["windows"]), "figures": len(refs),
              "markdown": str(md), "html": str(out / "note.html")}
    save_json(out / "validation.json", report)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("prepare", help="Normalize subtitles and create recoverable work windows")
    p.add_argument("--video", type=Path, required=True)
    p.add_argument("--transcript", type=Path, required=True)
    p.add_argument("--source-url", default="")
    p.add_argument("--title", default="")
    p.add_argument("--source-note", default="")
    p.add_argument("--work-dir", type=Path, required=True)
    p.add_argument("--window-seconds", type=float, default=120)
    p.add_argument("--start", type=float, default=0)
    p.add_argument("--end", type=float)
    p.set_defaults(handler=prepare)
    p = sub.add_parser("review", help="Record the caller's completed text and visual review for one window")
    p.add_argument("--work-dir", type=Path, required=True)
    p.add_argument("--window", required=True)
    p.add_argument("--source-reviewed", action="store_true")
    p.add_argument("--visual-reviewed", action="store_true")
    p.add_argument("--note", required=True)
    p.set_defaults(handler=review)
    p = sub.add_parser("assemble", help="Resolve reviewed figures and package Markdown plus sources")
    p.add_argument("--draft", type=Path, required=True)
    p.add_argument("--plan", type=Path, required=True)
    p.add_argument("--captures", type=Path, required=True)
    p.add_argument("--output-dir", type=Path, required=True)
    p.set_defaults(handler=assemble)
    p = sub.add_parser("render", help="Render portable HTML from a Markdown document")
    p.add_argument("--markdown", type=Path, required=True)
    p.add_argument("--output-dir", type=Path, required=True)
    p.set_defaults(handler=render)
    p = sub.add_parser("validate", help="Check sources, review evidence, images and rendered output")
    p.add_argument("--plan", type=Path, required=True)
    p.add_argument("--output-dir", type=Path, required=True)
    p.set_defaults(handler=validate)
    args = parser.parse_args()
    try:
        result = args.handler(args)
    except (ValueError, KeyError, TypeError, OSError, subprocess.SubprocessError) as exc:
        result = {"ok": False, "error": str(exc)}
    print(json.dumps(result, ensure_ascii=False, allow_nan=False))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
