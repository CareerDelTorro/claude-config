# Enforcement hooks

A rule written in `CLAUDE.template.md` only fires if the model remembers to apply it — and the
rules that matter most are exactly the ones that slip under pressure. These Claude Code
**Stop** / **UserPromptSubmit** hooks enforce a few of them *deterministically*, so the harness
catches the lapse instead of relying on attention. Prose can't guarantee an every-turn behaviour;
a hook can.

They are **examples to adapt, not drop-ins** — tune the phrase lists, patterns, and thresholds to
your own config, and delete the ones you don't want.

## The hooks

| Hook | Event | What it does |
|------|-------|--------------|
| `capture-loop-guard.py` | UserPromptSubmit | When your message reads as a correction/pushback, injects a reminder to run the mistake-capture loop *first*, and **arms** the Stop-gate below. |
| `capture-gate.py` | Stop | Blocks turn-end if a correction was armed this session but no capture landed — detected by the config repo's `HEAD` advancing. Clears itself once a capture commits. |
| `tone-guard.py` | Stop | Blocks turn-end if the final message contains performative-honesty framing (`to be honest`, `honest <noun>`) or narration of the model's own compliance. |
| `completion-gate.py` | Stop | Blocks turn-end when the reply ends on a present-tense continuation *claim* (`continuing now`) — a promise that continues nothing — pushing a real next action or a scheduled continuation instead. |

Design notes shared by all of them:
- **Fail open.** Any parse error, missing transcript, or unreadable state → allow the turn. A guard must never trap you.
- **No loops.** The Stop gates block at most once per stop-cycle (via `stop_hook_active`) or clear on a state change, so they can't tight-loop.
- **Known limit.** The tone/completion gates match on text, so they also fire when you *quote* a trigger phrase to discuss it. They block once, then let the re-send through.
- `capture-*` assume your config dir is a git repo (they track `HEAD` to detect a capture commit).

## Wiring

Point Claude Code at them in `~/.claude/settings.json` (use an absolute path if `~` isn't expanded
on your platform — e.g. `C:\Users\<you>\.claude\hooks\...` on Windows):

```json
{
  "hooks": {
    "Stop": [
      { "hooks": [{ "type": "command", "command": "python ~/.claude/hooks/capture-gate.py", "shell": "bash" }] },
      { "hooks": [{ "type": "command", "command": "python ~/.claude/hooks/tone-guard.py", "shell": "bash" }] },
      { "hooks": [{ "type": "command", "command": "python ~/.claude/hooks/completion-gate.py", "shell": "bash" }] }
    ],
    "UserPromptSubmit": [
      { "hooks": [{ "type": "command", "command": "python ~/.claude/hooks/capture-loop-guard.py", "shell": "bash" }] }
    ]
  }
}
```

Config changes are picked up when a session starts; an already-running session may need a restart
(or a `/hooks` reload) to load a newly-added hook.
