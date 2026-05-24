---
name: computer-use
description: Drive a macOS GUI app by taking screenshots and dispatching clicks, key presses, and text. Use when the user asks you to interact with a desktop application (Safari, Mail, Finder, any Mac app) — open it, navigate it, fill forms, click buttons, run a UI test. Do NOT use for terminal-only or web-headless work where a CLI/HTTP tool would do.
---

# computer-use

Drive a macOS app by looking at screenshots and acting one step at a time.

## First-time setup

The user must run this once:

```
~/.claude/skills/computer-use/setup.sh
```

That creates a venv and installs `pyautogui`, `pyobjc`, `Pillow`. On first action macOS will prompt for **Screen Recording** and **Accessibility** for whatever process is running `cu` (your terminal, iTerm, Claude Code, etc.). Both must be granted in System Settings → Privacy & Security or commands silently no-op.

## Commands

All commands print a single JSON object to stdout. Invoke via:

```
~/.claude/skills/computer-use/bin/cu <command> [args...]
```

| Command | Args | Returns |
|---|---|---|
| `screenshot` | — | `{ok, path, width, height}` — PNG saved to `/tmp/cu/`, sized in **click coordinates** so coords read off the image map 1:1 to `click` |
| `activate <bundle_id>` | e.g. `com.apple.Safari` | `{ok, bundle_id}` |
| `click <x> <y>` | `[--button left\|right\|middle]` `[--count N]` | `{ok}` |
| `type <text>` | `[--paste]` (default: char-by-char — cross-app safe; `--paste` uses cmd+V — faster but Citrix/RDP intercept the hotkey) | `{ok, mode}` |
| `key <combo>` | `cmd+t`, `ctrl+shift+a`, `enter`, `esc` | `{ok, keys}` |
| `tab [count]` | `[--shift]` press Tab (or Shift+Tab) N times — **preferred** way to step through form fields in remoted apps | `{ok, count}` |
| `scroll <x> <y> <dy>` | dy>0 up, dy<0 down | `{ok}` |
| `move <x> <y>` | move cursor without clicking | `{ok}` |
| `list_windows <bundle_id>` | | `{ok, windows: [{id, title, bounds, owner_pid}]}` |

Read the JSON. If `ok: false`, look at `error` and decide whether to retry or stop.

## How to drive a task

1. **Activate** the target app first (`cu activate <bundle_id>`).
2. **Screenshot** → read it with vision.
3. Decide ONE next action.
4. Execute it → **screenshot again** → re-evaluate.
5. Stop when the task is visibly done. Describe what's on the final screenshot.

Do not chain more than one action between screenshots. The UI may not be where you expected — clicking blindly damages state.

## Coordinates

`screenshot` returns the image at logical-pixel resolution (the same coordinate space `click` accepts), so you can read coordinates directly off the screenshot. No Retina scaling math required.

## Common failure modes and what to do

- **Nothing seems to happen**: permissions. Tell the user to grant Screen Recording + Accessibility to whatever process is running `cu`. Until granted, every command silently no-ops.
- **A different app is in front**: a notification stole focus. Re-`activate` the target and re-screenshot.
- **A modal dialog appeared**: just screenshot — same loop, same rules. Decide what the dialog wants.
- **App crashed**: the next screenshot won't show it. Stop and report.
- **Failsafe abort**: the user moved the mouse to a screen corner. Commands return `{ok: false, error: "failsafe"}`. Stop immediately and tell the user.

## Hard limits

- macOS cannot drive an app on a Space (workspace) the user isn't currently viewing. `activate` will switch Spaces, which is intrusive. Do NOT try to "drive in the background" — there is no such mode.
- While the skill runs, the foreground belongs to it. Don't run it on apps the user is actively using without warning them.
- If 8 iterations don't make visible progress toward the goal, stop and report — don't loop forever.

## Citrix / RDP / VNC remoted apps (Bloomberg in Citrix Viewer, etc.)

Remoted apps are a different beast from native macOS apps. Several things to know:

- **`type --paste` is unreliable.** Citrix Viewer in particular intercepts `cmd+V` and may release mouse capture, change zoom, or switch windows instead of pasting. The default char-by-char mode (no flag) is what you want here.
- **Click-to-focus on form fields often does not work.** A click that visibly lands inside a Bloomberg orange input may register as a click but **not transfer keyboard focus** — subsequent keystrokes still go to whatever had focus before (typically the command/search bar at the top). Symptoms: you click on a form field, type, and the text appears in the search/command bar instead.
- **Use Tab navigation instead of clicking form fields.** From a known-focused element (typically the command bar after a function navigation), use `cu tab N` to step into and between fields. Verify by screenshot after each tab.
- **Layout zoom can change between iterations.** Bloomberg/Citrix may rescale the view (e.g., after a click on certain controls). Coordinates from one screenshot will not be valid after a zoom change — always re-screenshot before clicking again.
- **Some clicks cause Citrix to release input capture entirely**, surfacing the macOS desktop with other windows. If your screenshot suddenly shows the desktop, re-`activate` the Citrix Viewer bundle id and start fresh from a known anchor (the command line).

## Finding bundle IDs

If the user names an app but not its bundle ID:

```
osascript -e 'id of app "Safari"'
```
