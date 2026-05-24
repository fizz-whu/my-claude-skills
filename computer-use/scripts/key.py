#!/usr/bin/env python3
"""Press a key or chord. Examples: cmd+t, ctrl+shift+a, enter, esc."""
import json
import sys

import pyautogui

ALIAS = {
    "cmd": "command",
    "command": "command",
    "ctrl": "ctrl",
    "control": "ctrl",
    "alt": "option",
    "opt": "option",
    "option": "option",
    "win": "command",
    "meta": "command",
    "return": "enter",
    "escape": "esc",
    "del": "delete",
}


def normalize(part: str) -> str:
    p = part.strip().lower()
    return ALIAS.get(p, p)


def main() -> int:
    if len(sys.argv) < 2:
        print(json.dumps({"ok": False, "error": "usage: key <combo>  (e.g. cmd+t, enter)"}))
        return 2

    parts = [normalize(p) for p in sys.argv[1].split("+") if p.strip()]
    if not parts:
        print(json.dumps({"ok": False, "error": "empty key combo"}))
        return 2

    if len(parts) == 1:
        pyautogui.press(parts[0])
    else:
        pyautogui.hotkey(*parts)

    print(json.dumps({"ok": True, "keys": parts}))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except pyautogui.FailSafeException:
        print(json.dumps({"ok": False, "error": "failsafe"}))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"ok": False, "error": f"{type(e).__name__}: {e}"}))
        sys.exit(1)
