#!/usr/bin/env bash
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

if ! command -v python3 >/dev/null 2>&1; then
  echo "error: python3 not found on PATH" >&2
  exit 1
fi

if [ ! -d .venv ]; then
  echo "creating venv..."
  python3 -m venv .venv
fi

echo "installing dependencies..."
.venv/bin/pip install --quiet --upgrade pip
.venv/bin/pip install --quiet -r requirements.txt

chmod +x bin/cu scripts/*.py 2>/dev/null || true

cat <<EOF

computer-use skill installed at $DIR

Try it:
  $DIR/bin/cu screenshot
  $DIR/bin/cu list_windows com.apple.finder

First time you run an action, macOS will prompt for:
  - Screen Recording  (for screenshots)
  - Accessibility     (for clicks and keystrokes)

Grant both to whatever process is running cu (Terminal / iTerm / Claude Code),
then re-run. Until granted, commands silently no-op.
EOF
