#!/usr/bin/env python3
"""Bring an app to the foreground by bundle id."""
import json
import subprocess
import sys


def main() -> int:
    if len(sys.argv) < 2:
        print(json.dumps({"ok": False, "error": "usage: activate <bundle_id>"}))
        return 2
    bundle_id = sys.argv[1]
    res = subprocess.run(
        ["osascript", "-e", f'tell application id "{bundle_id}" to activate'],
        capture_output=True,
        text=True,
    )
    ok = res.returncode == 0
    out = {"ok": ok, "bundle_id": bundle_id}
    if not ok:
        out["error"] = res.stderr.strip()
    print(json.dumps(out))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
