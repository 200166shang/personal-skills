---
name: local-whisper
description: Use when the user asks to transcribe audio or video locally/offline, mentions Whisper, faster-whisper, mlx-whisper, Apple Silicon/M-series Macs, speech-to-text, subtitles, SRT/VTT/JSON, word timestamps, mixed-language audio, or translating a transcript while preserving timestamps.
compatibility: Requires macOS or Linux, uv, and local model storage; translated subtitles optionally require Ollama with an installed text model.
---

# Local Whisper

## Overview

Run speech recognition locally with reproducible commands and clean output directories. Prefer MLX on Apple Silicon for ordinary transcription, retain faster-whisper for its mature CPU/CUDA path and multilingual-window mode, and treat target-language subtitle translation as a separate text step.

## Workflow

1. Confirm the input path, desired output formats, source-language hint, target language, and whether word timestamps are actually needed.
2. Run `scripts/run.sh`; it uses `uv` and shared caches, so model files and virtual environments never pollute the output directory.
3. Inspect the emitted JSON summary and validate the result with `scripts/validate_outputs.py`.
4. If the requested text language differs from the spoken language, translate the ASR JSON with `scripts/translate.py`. Preserve every segment's original `start` and `end`.
5. Report the selected backend/model, detected language, output paths, and any low-confidence or mixed-language caveats.

## Commands

Resolve this Skill's directory from the loaded `SKILL.md`, then run:

```bash
"<skill-dir>/scripts/run.sh" input.mp3 \
  --output-dir ./transcript \
  --formats txt,srt,vtt,json \
  --word-timestamps
```

Apple Silicon defaults to MLX. To honor an explicit faster-whisper request:

```bash
"<skill-dir>/scripts/run.sh" input.mp3 \
  --backend faster-whisper \
  --model small \
  --output-dir ./transcript
```

For code-switching or mixed-language audio, prioritize correctness:

```bash
"<skill-dir>/scripts/run.sh" mixed.wav \
  --mixed-language \
  --word-timestamps \
  --output-dir ./transcript
```

`--mixed-language` makes `auto` choose faster-whisper, divides audio into five-second core windows with a small right-context overlap, detects each window independently, and keeps only words belonging to the core region. This avoids forcing one global language across the recording without hard-coding a language-switch timestamp. Its per-segment `language` and probability come from the corresponding Whisper window; ordinary MLX output uses a transparently labeled text-script heuristic because MLX does not expose calibrated per-segment language probabilities.

For English audio to Simplified Chinese subtitles, first transcribe, then translate locally:

```bash
"<skill-dir>/scripts/translate.py" ./transcript/input.json \
  --target-language zh-CN \
  --output-dir ./transcript
```

The translator uses an already-installed Ollama model and refuses to silently download a multi-gigabyte model. If none is installed, explain the choices and ask before running `ollama pull`.

## Backend decisions

When the user asks for a recommendation, benchmark interpretation, or a factual comparison between implementations, read `references/backends.md` before answering.

| Situation | Default | Reason |
|---|---|---|
| Apple Silicon, one main language | MLX | Uses Apple GPU/unified memory |
| Mixed/code-switched audio | faster-whisper | Its multilingual-window mode is more explicit |
| Linux/Windows CPU | faster-whisper `int8` | Portable CTranslate2 path |
| NVIDIA CUDA | faster-whisper `float16` | Mature CUDA acceleration |
| Exact backend requested | Requested backend | Honor user intent and report tradeoffs |

On Apple Silicon, faster-whisper is CPU-only: never claim that it uses MPS, Metal, Core ML, or the Neural Engine. For a 16 GB M-series Mac, `large-v3-turbo` is the accuracy/speed default for MLX; use `small` when memory, thermals, or download size matter more.

## Translation rule

Whisper's native `translate` task means non-English speech to English text. It does not mean arbitrary target-language translation and cannot reliably perform English speech to Chinese text. Always use ASR followed by segment-preserving text translation for English-to-Chinese and other arbitrary language pairs.

## Output contract

- JSON is the source of truth and records backend, model, global language metadata, segment timestamps, segment language provenance, and optional word timestamps.
- SRT and VTT use segment-level cues.
- TXT contains readable plain text; TSV is suitable for spreadsheets.
- All timestamps are seconds in JSON and are rendered as standard subtitle timestamps elsewhere.
- Output directories contain deliverables only; shared `uv` and Hugging Face caches stay outside them.

## Common mistakes

- Do not pass a target language to Whisper as though it were a translation target.
- Do not use `.en` models for multilingual audio.
- Do not force one detected language across code-switched audio.
- Do not promise word timestamps as forced-alignment ground truth; they are model estimates.
- Do not place virtual environments or model caches beside user deliverables.
- Do not download large translation models without making the size and purpose clear.
