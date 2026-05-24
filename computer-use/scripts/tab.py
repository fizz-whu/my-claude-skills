#!/usr/bin/env python3
"""Press Tab N times. Useful for stepping through form fields when click-to-focus
doesn't work (common in Citrix/RDP/VNC remoted apps)."""
import argparse
import json
import sys
import time

import pyautogui


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("count", nargs="?", type=int, default=1)
    ap.add_argument("--shift", action="store_true", help="Shift+Tab (move backward)")
    ap.add_argument("--interval", type=float, default=0.08, help="Seconds between presses")
    args = ap.parse_args()

    if args.count < 1:
        print(json.dumps({"ok": False, "error": "count must be >= 1"}))
        return 2

    for i in range(args.count):
        if args.shift:
            pyautogui.hotkey("shift", "tab")
        else:
            pyautogui.press("tab")
        if i < args.count - 1:
            time.sleep(args.interval)

    print(json.dumps({"ok": True, "count": args.count, "shift": args.shift}))
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
