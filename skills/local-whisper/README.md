# local-whisper-skill

Local speech-to-text for AI coding agents, with Apple Silicon-aware backend selection, clean TXT/SRT/VTT/JSON output, word timestamps, mixed-language handling, and optional local subtitle translation through Ollama.

Maintained in [`personal-skills`](https://github.com/200166shang/personal-skills/tree/main/skills/local-whisper). The original repository history is retained in the collection.

## Install

```bash
npx skills add 200166shang/personal-skills --skill local-whisper -g -y
```

This installs the Agent Skill for Codex, Claude Code, Cursor, and other clients supported by the Skills CLI. Runtime dependencies and models are resolved on first use with shared caches; they are not written into transcript output directories.

## Why both MLX and faster-whisper?

- On Apple Silicon, MLX can use the Apple GPU and unified memory and is the normal performance-first choice.
- faster-whisper provides a mature CTranslate2 implementation, VAD, CUDA support, and multilingual-window behavior. On Apple Silicon it runs on CPU, not Metal/MPS/Core ML/ANE.
- Whisper's built-in translation direction is non-English speech to English. English speech to Chinese therefore uses ASR followed by timestamp-preserving text translation.

See [SKILL.md](./SKILL.md) for the agent workflow and commands.

## Direct command-line use

```bash
./scripts/run.sh recording.mp3 --output-dir ./out --word-timestamps
./scripts/validate_outputs.py ./out/recording.json
./scripts/translate.py ./out/recording.json --target-language zh-CN
```

Requirements: `uv`; `Ollama` plus an already-installed text model only when local subtitle translation is requested.

## License

MIT
