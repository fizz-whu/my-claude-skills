#!/usr/bin/env python3
"""Capture the full screen at logical-pixel resolution and save as PNG."""
import json
import os
import sys
import time

import pyautogui
from PIL import Image

OUT_DIR = "/tmp/cu"


def main() -> int:
    os.makedirs(OUT_DIR, exist_ok=True)
    logical_w, logical_h = pyautogui.size()
    img = pyautogui.screenshot()
    if img.size != (logical_w, logical_h):
        img = img.resize((logical_w, logical_h), Image.LANCZOS)
    path = os.path.join(OUT_DIR, f"cu-{int(time.time() * 1000)}.png")
    img.save(path, "PNG", optimize=True)
    print(json.dumps({"ok": True, "path": path, "width": logical_w, "height": logical_h}))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(json.dumps({"ok": False, "error": f"{type(e).__name__}: {e}"}))
        sys.exit(1)
