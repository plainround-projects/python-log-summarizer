#!/usr/bin/env bash
# Build the wheel, install it into a brand-new virtual environment with nothing else, and run the command
# from a different directory with PYTHONPATH unset, so success means the packaged wheel works and not that
# Python found this source tree by accident.
set -euo pipefail

log=$(cd "$(dirname "${1:?usage: install_check.sh LOG_FILE}")" && pwd)/$(basename "$1")
root=$(cd "$(dirname "$0")/.." && pwd)
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT

cd "$root"
uv build --out-dir "$work/dist" >/dev/null
uv venv --quiet "$work/venv"
uv pip install --quiet --python "$work/venv/bin/python" "$work"/dist/*.whl
echo "installed into a fresh environment: $(uv pip list --python "$work/venv/bin/python" 2>/dev/null | tail -n +3 | tr -s ' ' | tr '\n' ';')"

cd "$work"
env -u PYTHONPATH "$work/venv/bin/logsum" --help | head -1
env -u PYTHONPATH "$work/venv/bin/logsum" "$log"
