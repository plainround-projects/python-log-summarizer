#!/usr/bin/env bash
# Copy the project to a scratch folder, change the latency suffix the parser accepts from "ms" to "s",
# and run the unit tests there. They must fail: that proves the parser tests would catch the mistake.
set -euo pipefail

root=$(cd "$(dirname "$0")/.." && pwd)
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT

cp -R "$root/src" "$root/tests" "$root/docs" "$root/pyproject.toml" "$root/README.md" "$root/LICENSE" "$work/"
sed -i.bak 's/_LATENCY_SUFFIX = "ms"/_LATENCY_SUFFIX = "s"/' "$work/src/logsum/domain/request.py"
rm "$work/src/logsum/domain/request.py.bak"
grep -n '_LATENCY_SUFFIX = ' "$work/src/logsum/domain/request.py"

cd "$work"
if PYTHONPATH="$work/src" "$root/.venv/bin/python" -m pytest tests/unit -q -p no:cacheprovider 2>&1 | tail -15; then
  :
fi
status=${PIPESTATUS[0]}
if [ "$status" -eq 0 ]; then
  echo "MUTANT SURVIVED: the tests did not notice the change" >&2
  exit 1
fi
echo "mutant killed: the tests failed as they should"
