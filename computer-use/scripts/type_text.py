#!/usr/bin/env python3
"""Type a string into the focused field.

Default: type each character individually (cross-app safe — no cmd+V hotkey
that some remoted-app hosts like Citrix Viewer intercept and mishandle).
With --paste, copy to clipboard and send cmd+V (faster, unicode-safe, but
fragile in Citrix/RDP/VNC sessions)."""
import argparse
import json
import subprocess
import sys
import time

import pyautogui


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("text")
    ap.add_argument(
        "--paste",
        action="store_true",
        help="Use cmd+V from clipboard. Faster but breaks in Citrix/RDP. Default off.",
    )
    # accept the legacy --no-paste flag as a no-op so existing callers don't break
    ap.add_argument("--no-paste", action="store_true", help=argparse.SUPPRESS)
    args = ap.parse_args()

    if args.paste:
        prev = subprocess.run(["pbpaste"], capture_output=True).stdout
        subprocess.run(["pbcopy"], input=args.text.encode("utf-8"), check=True)
        time.sleep(0.05)
        pyautogui.hotkey("command", "v")
        time.sleep(0.1)
        try:
            subprocess.run(["pbcopy"], input=prev, check=False)
        except Exception:
            pass
        mode = "paste"
    else:
        pyautogui.write(args.text, interval=0.01)
        mode = "type"

    print(json.dumps({"ok": True, "len": len(args.text), "mode": mode}))
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
