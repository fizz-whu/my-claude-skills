#!/usr/bin/env python3
"""List on-screen windows belonging to apps with the given bundle id."""
import json
import sys

import Quartz
from AppKit import NSWorkspace


def main() -> int:
    if len(sys.argv) < 2:
        print(json.dumps({"ok": False, "error": "usage: list_windows <bundle_id>"}))
        return 2
    target = sys.argv[1]

    pids = [
        a.processIdentifier()
        for a in NSWorkspace.sharedWorkspace().runningApplications()
        if a.bundleIdentifier() == target
    ]
    if not pids:
        print(json.dumps({"ok": True, "windows": [], "pids": [], "note": "app not running"}))
        return 0

    opts = Quartz.kCGWindowListOptionOnScreenOnly | Quartz.kCGWindowListExcludeDesktopElements
    windows = Quartz.CGWindowListCopyWindowInfo(opts, Quartz.kCGNullWindowID) or []
    out = []
    for w in windows:
        if w.get("kCGWindowOwnerPID") in pids:
            b = w.get("kCGWindowBounds", {}) or {}
            out.append(
                {
                    "id": w.get("kCGWindowNumber"),
                    "title": w.get("kCGWindowName", "") or "",
                    "owner_pid": w.get("kCGWindowOwnerPID"),
                    "bounds": {
                        "x": b.get("X"),
                        "y": b.get("Y"),
                        "w": b.get("Width"),
                        "h": b.get("Height"),
                    },
                }
            )
    print(json.dumps({"ok": True, "windows": out, "pids": list(pids)}))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(json.dumps({"ok": False, "error": f"{type(e).__name__}: {e}"}))
        sys.exit(1)
