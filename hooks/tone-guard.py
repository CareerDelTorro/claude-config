#!/usr/bin/env python3
"""Stop hook: tone-guard.

Flags two Register-and-tone violations in my FINAL assistant message so I rewrite them
before the turn ends:
  1. performative-honesty framing  ("to be honest", "honestly", "honest status/take/...")
  2. narration of my own compliance/process  ("going forward", "per the materiality check", ...)

Why a hook and not prose: ~/.claude/CLAUDE.md already forbids both, yet I violated them while
literally discussing them this session. Prose rules depend on in-the-moment attention and attention
misses; a hook fires deterministically. (Same reasoning as the capture-gate pair.)

Behaviour: BLOCKS once with the offending fragments, giving me one revision. Guarded by
`stop_hook_active`, it then lets the turn end so it can NEVER loop. Fails OPEN on any parse error or
missing transcript — a tone nudge must never trap a turn. Known limitation: it cannot tell a phrase
I'm *committing* from one I'm *quoting to discuss*; a quoted offender costs one harmless revision
cycle, then passes.
"""
import sys
import json
import re
import os


def allow():
    sys.exit(0)  # no output, no block


# Kept tight: fire on the performative USES, not every appearance of a word.
# "honest <noun>" is an OPEN class (scoping, implication, take, ...) -> match the STRUCTURE and
# denylist the small, stable set of legitimate collocations/conjunctions, rather than allowlisting
# nouns (which leaks on every novel one -- the bug that let "honest scoping" through).
HONESTY = re.compile(
    r"\b(?:to be honest|to be frank|honestly|in all honesty|i'?ll be honest|let me be honest|"
    r"i'?ll be upfront|being honest|if i'?m honest|"
    r"honest (?!(?:and|but|or|nor|yet|so|about|with|in|to|as|than|enough|broker|brokers|mistake|"
    r"mistakes|work|working|living|day|days|person|people|man|men|woman|women|effort|efforts|"
    r"wage|wages|labou?r|dealing|dealings|trade|trades|feedback)\b)\w+)\b",
    re.I)

COMPLIANCE = re.compile(
    r"(\bgoing forward\b|\bfrom now on\b|\bi'?ll keep that in mind\b|\bi'?ll bear that in mind\b|"
    r"\bdropped from my vocabulary\b|\bi wo ?n'?t manufacture\b|\bnoted[.,]|"
    r"\bper (my|the) [\w\s]{0,25}?(rule|check|gate|directive|materiality)\b)",
    re.I)


def last_assistant_text(path):
    """Return the text of the most recent assistant message in the JSONL transcript, robust to
    the {message:{role,content:[{type:text,text}]}} shape and simpler variants."""
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
        # assistant event carried no text (tool_use only) -> keep walking back
    return ""


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        allow()

    # Never loop: if this stop is already a hook-triggered continuation, let it through.
    if data.get("stop_hook_active"):
        allow()

    path = data.get("transcript_path", "")
    if not path or not os.path.exists(path):
        allow()

    text = last_assistant_text(path)
    if not text:
        allow()

    hits = []
    for label, rx in (("performative-honesty", HONESTY), ("compliance-narration", COMPLIANCE)):
        for m in rx.finditer(text):
            frag = m.group(0).strip()
            if (label, frag) not in hits:
                hits.append((label, frag))
    if not hits:
        allow()

    listed = "; ".join('{}: "{}"'.format(lbl, frag) for lbl, frag in hits[:8])
    reason = (
        "[TONE-GUARD] Your reply contains framing your own Register-and-tone rules say to cut -- "
        + listed + ". These are performative-honesty prefaces or narration of your own "
        "compliance/process; they carry no information. Rewrite those sentences to state the "
        "substance directly (delete the framing, keep the content), then end the turn. "
        "(If a flagged phrase is one you are QUOTING to discuss, not committing, just re-send as-is: "
        "this gate blocks only once and will then let the turn end.)"
    )
    print(json.dumps({"decision": "block", "reason": reason}))
    sys.exit(0)


if __name__ == "__main__":
    main()
