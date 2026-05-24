#!/usr/bin/env python3
"""Move the cursor to (x, y) without clicking."""
import json
import sys

import pyautogui


def main() -> int:
    if len(sys.argv) < 3:
        print(json.dumps({"ok": False, "error": "usage: move <x> <y>"}))
        return 2
    x, y = int(sys.argv[1]), int(sys.argv[2])
    pyautogui.moveTo(x, y, duration=0.1)
    print(json.dumps({"ok": True, "x": x, "y": y}))
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
