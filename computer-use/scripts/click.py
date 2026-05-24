#!/usr/bin/env python3
"""Click at (x, y)."""
import argparse
import json
import sys

import pyautogui


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("x", type=int)
    ap.add_argument("y", type=int)
    ap.add_argument("--button", default="left", choices=["left", "right", "middle"])
    ap.add_argument("--count", type=int, default=1)
    args = ap.parse_args()

    pyautogui.click(args.x, args.y, clicks=args.count, button=args.button, interval=0.05)
    print(json.dumps({"ok": True, "x": args.x, "y": args.y, "button": args.button, "count": args.count}))
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
