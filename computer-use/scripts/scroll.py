#!/usr/bin/env python3
"""Scroll at (x, y) by dy clicks. dy>0 scrolls up, dy<0 scrolls down."""
import json
import sys

import pyautogui


def main() -> int:
    if len(sys.argv) < 4:
        print(json.dumps({"ok": False, "error": "usage: scroll <x> <y> <dy>"}))
        return 2
    x, y, dy = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    pyautogui.moveTo(x, y, duration=0.05)
    pyautogui.scroll(dy)
    print(json.dumps({"ok": True, "x": x, "y": y, "dy": dy}))
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
