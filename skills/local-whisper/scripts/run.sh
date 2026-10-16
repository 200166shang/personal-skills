#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)

if ! command -v uv >/dev/null 2>&1; then
  echo "local-whisper requires uv. Install it with 'brew install uv' on macOS or see https://docs.astral.sh/uv/." >&2
  exit 2
fi

backend=auto
mixed=false
expect_backend=false

for arg in "$@"; do
  if [ "$expect_backend" = true ]; then
    backend=$arg
    expect_backend=false
    continue
  fi
  case "$arg" in
    --backend) expect_backend=true ;;
    --backend=*) backend=${arg#--backend=} ;;
    --mixed-language) mixed=true ;;
    -h|--help)
      exec python3 "$script_dir/transcribe.py" --help
      ;;
  esac
done

if [ "$backend" = auto ]; then
  if [ "$mixed" = true ]; then
    backend=faster-whisper
  elif [ "$(uname -s)" = Darwin ] && [ "$(uname -m)" = arm64 ]; then
    backend=mlx
  else
    backend=faster-whisper
  fi
fi

case "$backend" in
  mlx)
    exec uv run --isolated --python 3.11 --with 'mlx-whisper==0.4.3' --with 'socksio>=1.0.0' \
      python "$script_dir/transcribe.py" "$@"
    ;;
  faster-whisper|faster)
    exec uv run --isolated --python 3.11 --with 'faster-whisper==1.2.1' --with 'socksio>=1.0.0' \
      python "$script_dir/transcribe.py" "$@"
    ;;
  *)
    echo "Unsupported backend: $backend (expected auto, mlx, or faster-whisper)" >&2
    exit 2
    ;;
esac
