#!/usr/bin/env python3
"""Stop-gate (half 2 of the prime-directive enforcement pair).

Runs when the turn tries to end. If capture-loop-guard.py armed the gate this session (a correction
arrived) and NO capture landed since — i.e. the config-repo HEAD has not advanced — BLOCK the stop
and feed back the mandate. The gate clears itself once a capture commit lands (HEAD moves).

Escape valve: if I have HONESTLY concluded there is no generic lesson (a true one-off), I clear the
gate by deleting the marker file named in the block reason — consistent with the directive's
"say so explicitly" clause. Fails OPEN (never traps) if git or the marker can't be read.
"""
import sys
import json
import os
import subprocess

CLAUDE_DIR = os.path.expanduser("~/.claude")
MARKER = os.path.join(CLAUDE_DIR, "hooks", ".pending-capture")


def repo_head():
    try:
        return subprocess.check_output(
            ["git", "-C", CLAUDE_DIR, "rev-parse", "HEAD"],
            stderr=subprocess.DEVNULL).decode().strip()
    except Exception:
        return ""


def allow():
    sys.exit(0)  # no output, no block


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        data = {}
    session = data.get("session_id", "")

    if not os.path.exists(MARKER):
        allow()
    try:
        with open(MARKER, encoding="utf-8") as f:
            m = json.load(f)
    except Exception:
        # unreadable marker — fail open, clean it up
        try:
            os.remove(MARKER)
        except Exception:
            pass
        allow()

    # Only gate the session that armed it (a stale marker from another session must not block this one).
    if m.get("session") != session:
        allow()

    head = repo_head()
    if not head or head != m.get("head", ""):
        # HEAD advanced (a capture committed) OR git unreadable (fail open). Clear + allow.
        try:
            os.remove(MARKER)
        except Exception:
            pass
        allow()

    # A correction was armed, HEAD has not moved -> the capture loop did not complete. BLOCK.
    reason = (
        "[PRIME-DIRECTIVE GATE] A correction/pushback arrived this session and the mistake-capture "
        "loop has NOT completed — no new commit landed in the config repo (~/.claude) since. Before "
        "ending the turn: diagnose the root cause, distill a generic learning, edit CLAUDE.md "
        "(+ working-style-lessons.md if warranted), and COMMIT it (the gate clears automatically once "
        "HEAD advances). If you have HONESTLY concluded there is genuinely no generic lesson (a true "
        "one-off), state that in your reply, then clear the gate: rm \"" + MARKER + "\"."
    )
    print(json.dumps({"decision": "block", "reason": reason}))
    sys.exit(0)


if __name__ == "__main__":
    main()
