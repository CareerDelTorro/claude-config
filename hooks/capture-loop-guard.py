#!/usr/bin/env python3
"""UserPromptSubmit guard (half 1 of the prime-directive enforcement pair).

If the user's message reads as a correction / pushback about my behaviour:
  1. inject a mandatory reminder to run the capture loop FIRST (before answering/resuming), and
  2. ARM the Stop-gate — drop a marker recording the session + the config-repo HEAD right now, so
     the companion Stop hook (capture-gate.py) can BLOCK turn-end unless a new capture commit lands.

Prose in CLAUDE.md provably could not GUARANTEE the loop fires (skipped twice). These two hooks fire
deterministically at the exact trigger, which memory cannot. Acting is still on me — but the gate
won't let the turn end quietly if I skip it.
"""
import sys
import json
import re
import os
import subprocess

# Correction / pushback phrasings. Kept focused so it fires on real corrections, not every prompt.
PATTERNS = [
    r"why did you\b",
    r"why did ?n'?t you\b",
    r"why are ?n'?t you\b",
    r"why have ?n'?t you\b",
    r"why do you keep\b",
    r"why was that (missed|skipped|dropped|forgotten)\b",
    r"you (should|could) have\b",
    r"you were supposed to\b",
    r"you (missed|skipped|forgot|failed to|ignored|overlooked)\b",
    r"you did ?n'?t\b",
    r"you keep\b",
    r"that'?s (wrong|not right|not what)",
    r"not what i (asked|wanted|said|meant)",
    r"i (told|asked) you (to|not to)\b",
    r"you (never|always)\b",
    r"stop (skipping|ignoring|doing)\b",
    r"you (were|are) (supposed|meant) to\b",
    r"don'?t skip\b",
    r"skip(ped)? (it|the loop|the check)\b",
]

MANDATE = (
    "[PRIME-DIRECTIVE GUARD] This message reads as a correction or pushback about your behaviour. "
    "Per ~/.claude/CLAUDE.md's Prime directive, BEFORE answering the substance or resuming any task, "
    "run the mistake-capture loop: (1) diagnose the root cause, (2) distill a generic reusable "
    "learning, (3) edit ~/.claude/CLAUDE.md (+ working-style-lessons.md if it earns a case study), "
    "(4) commit and push to the config repo (push a SANITIZED version). A one-line acknowledgement is "
    "NOT the loop. The Stop-gate is now armed: the turn cannot end until a new capture commit lands in "
    "~/.claude, OR you clear the gate after HONESTLY concluding there is no generic lesson. If there "
    "genuinely is none, say so explicitly — do not silently skip the check."
)

CLAUDE_DIR = os.path.expanduser("~/.claude")
MARKER = os.path.join(CLAUDE_DIR, "hooks", ".pending-capture")


def repo_head():
    try:
        return subprocess.check_output(
            ["git", "-C", CLAUDE_DIR, "rev-parse", "HEAD"],
            stderr=subprocess.DEVNULL).decode().strip()
    except Exception:
        return ""


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return
    prompt = (data.get("prompt") or "").lower()
    if not prompt:
        return
    if any(re.search(p, prompt) for p in PATTERNS):
        # Arm the Stop-gate: record which session + the HEAD to beat (a capture must advance HEAD).
        try:
            with open(MARKER, "w", encoding="utf-8") as f:
                json.dump({"session": data.get("session_id", ""), "head": repo_head()}, f)
        except Exception:
            pass
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": MANDATE,
            }
        }))


if __name__ == "__main__":
    main()
