# Backend facts and tradeoffs

Use this reference when explaining why the Skill selected a backend or why arbitrary target-language translation is a separate step.

## faster-whisper

- The official API returns timestamped segments and optionally word timestamps. It also integrates Silero VAD: <https://github.com/SYSTRAN/faster-whisper#word-level-timestamps>
- `multilingual=True` performs language detection across windows, but the public `Segment` object does not expose a calibrated language field. This Skill's mixed-language mode therefore runs independent short windows and records each window's detected language and probability: <https://github.com/SYSTRAN/faster-whisper/blob/master/faster_whisper/transcribe.py>
- CTranslate2 supports ARM64 CPUs, while its documented GPU path is CUDA. Do not describe faster-whisper on Apple Silicon as Metal/MPS/Core ML/ANE accelerated: <https://opennmt.net/CTranslate2/hardware_support.html>
- Published faster-whisper speed tables are hardware- and configuration-specific. Do not transfer x86/NVIDIA results directly to an M-series Mac: <https://github.com/SYSTRAN/faster-whisper#benchmark>

## MLX Whisper

- MLX Whisper is the Apple MLX implementation and installs as `mlx-whisper`: <https://github.com/ml-explore/mlx-examples/tree/main/whisper>
- The `mlx-community/whisper-small-mlx` weights are about 481 MB; `mlx-community/whisper-large-v3-turbo` is about 1.61 GB. Model cache size is distinct from peak runtime memory:
  - <https://huggingface.co/mlx-community/whisper-small-mlx>
  - <https://huggingface.co/mlx-community/whisper-large-v3-turbo>
- `mlx-whisper` 0.4.3 does not implement beam search. The shared CLI accepts `--beam-size` for faster-whisper compatibility but intentionally omits it from MLX calls.

## whisper.cpp

- whisper.cpp treats Apple Silicon as a first-class platform and documents ARM NEON, Accelerate, Metal, and optional Core ML encoder acceleration: <https://github.com/ggml-org/whisper.cpp>
- It is a strong native CLI/embedding alternative. This Skill does not bundle it because that would add a second model format and build/install path; recommend it when a user prioritizes a standalone native binary over Python/MLX workflows.

## Translation direction

- OpenAI describes Whisper transcription as speech to text in the spoken language, and translation as non-English speech to English. `turbo` is not trained for translation: <https://github.com/openai/whisper#available-models-and-languages>
- Therefore English audio to Chinese is ASR followed by text translation. Copy each ASR segment's time interval to its translated subtitle instead of asking Whisper for a Chinese target language.

## Interpreting “fastest”

There is no universal winner. Compare the same audio, model family, decoding settings, timestamps, VAD, and accuracy target on the user's hardware. Separate first-run model download and process startup from warm inference time. On a fanless MacBook Air, also test sustained long recordings because thermal behavior can differ from a short clip.
