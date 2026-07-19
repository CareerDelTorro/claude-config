#!/usr/bin/env python3
"""Stop hook: completion-gate (enforces the Run-to-completion rule).

The failure it targets: ending a turn on a PRESENT-TENSE continuation claim -- "continuing now",
"starting now", "back to the grind" -- when a text promise continues nothing (the turn ends the
instant I stop emitting tool calls). This hook BLOCKS that specific sign-off and feeds back the
real options.

What a Stop hook can and cannot do: it CANNOT itself launch a loop, a ScheduleWakeup, or a
background task -- it is a shell script with no access to my tools. It CAN block turn-end and tell
me what to do. So it forces ME to either (a) make the next tool call in THIS turn, or (b) call
ScheduleWakeup / start a background task so continuation is real, or (c) restate an honest pause
without the false claim.

Deliberately NARROW: it fires only on present-tense "I'm doing it right now" sign-offs, NOT on
future-tense progress reporting ("next I'll rework the decks") -- otherwise it would fight every
legitimate turn-end and the user's own "stop here" instructions. BLOCKS once (stop_hook_active
guard) so it can never tight-loop; fails OPEN on any error.
"""
import sys
import json
import re
import os


def allow():
    sys.exit(0)


# Present-tense continuation CLAIMS (the sign-off lie). Future-tense planning is intentionally NOT here.
CLAIM = re.compile(
    r"("
    r"\bcontinuing now\b|\bstarting now\b|\bresuming now\b|\bproceeding now\b|\bon it now\b|"
    r"\bback to (it|the grind|work)\b|\bgrinding (on|now)\b|"
    r"\blet me (continue|keep going|pick (this|it) (back )?up|get back to it)\b|"
    r"\bi(?:'ll| will) (continue|resume|keep going|pick (this|it) (back )?up|press on|carry on|crack on|grind) "
    r"(now|right now|from here)\b|"
    r"\bpicking (this|it) (back )?up now\b|\bkicking (this|it|things) off\b|"
    r"\bhere goes\b|\boff i go\b|\bstarting (the|on) .{0,30}? now\b"
    r")",
    re.I)


def last_assistant_text(path):
    try:
        with open(path, encoding="utf-8") as f:
            lines = f.readlines()
    except Exception:
        return ""
    for line in reversed(lines):
        line = line.strip()
        if not line:
            continue
        try:
            ev = json.loads(line)
        except Exception:
            continue
        if not isinstance(ev, dict):
            continue
        msg = ev.get("message") if isinstance(ev.get("message"), dict) else None
        role = (msg.get("role") if msg else None) or ev.get("role") or ev.get("type") or ""
        if role != "assistant":
            continue
        content = (msg.get("content") if msg else None)
        if content is None:
            content = ev.get("content")
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            parts = [b.get("text", "") for b in content
                     if isinstance(b, dict) and b.get("type") == "text"]
            if parts:
                return "\n".join(parts)
    return ""


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        allow()

    # Never tight-loop: if this stop is already a hook-triggered continuation, let it through.
    if data.get("stop_hook_active"):
        allow()

    path = data.get("transcript_path", "")
    if not path or not os.path.exists(path):
        allow()

    text = last_assistant_text(path)
    if not text:
        allow()

    m = CLAIM.search(text)
    if not m:
        allow()

    reason = (
        "[COMPLETION-GATE] Your reply ends on a present-tense continuation claim (\""
        + m.group(0).strip() + "\") but you are STOPPING -- a text promise continues nothing; the "
        "turn ends the moment you stop emitting tool calls. Do ONE of these instead, then end:\n"
        " 1. If work remains and you can do it now: make the next tool call in THIS turn.\n"
        " 2. If you must yield across turns: call ScheduleWakeup (or start a background task/loop) "
        "so continuation is REAL, then it's fine to stop.\n"
        " 3. If you are deliberately pausing (the user asked you to stop, or you hit a blocker): "
        "restate that plainly WITHOUT a 'continuing now' claim.\n"
        "(If the flagged phrase was a quote you were discussing, just re-send: this blocks only once.)"
    )
    print(json.dumps({"decision": "block", "reason": reason}))
    sys.exit(0)


if __name__ == "__main__":
    main()
