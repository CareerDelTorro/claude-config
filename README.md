# claude-config

A portable **working-style config for Claude Code** — a starter `CLAUDE.md` that shapes how
Claude reasons and communicates: verifying before asserting, self-checking load-bearing claims,
calibrated confidence, a terse functional tone, and a set of debugging habits.

It's a **template, not a drop-in.** It was distilled from a heavily-iterated personal config, so
spend ~15 minutes adapting it to yourself — a blind copy will fit someone else's brain, not yours.

## What's here

- **`CLAUDE.template.md`** — the working-style file itself. Named `.template` so cloning this repo
  into a project directory doesn't auto-activate it as your live config before you've adapted it.
- **`ADAPT-WITH-CLAUDE.md`** — a paste-ready prompt that has Claude Code do the adaptation for you,
  as a short interview. Easiest path — start there.
- **`README.md`** — this file: manual install + adaptation steps.

## 1. Where to install it

Claude Code loads `CLAUDE.md` files automatically at the **start of every session**, merging them
into context. Two placement options:

- **User-level (recommended for this file): `~/.claude/CLAUDE.md`** — applies to *every* project on
  your machine. This file is general working-style, so it belongs here.
  - macOS/Linux: `~/.claude/CLAUDE.md`
  - Windows: `C:\Users\<you>\.claude\CLAUDE.md`
- **Project-level: `./CLAUDE.md`** in a repo root — applies only when working in that repo. Use this
  for project-specific context (what the project *is*), not general working style.

If you already have a `~/.claude/CLAUDE.md`, **do not blindly overwrite or append** — see §3.

Verify it loaded: start a new session and run `/memory` (lists the memory/instruction files Claude
has loaded). A running session won't pick up edits — the file is read once at launch, so start a
**fresh session** (or run `/compact`) after any change.

## 2. Adapt before you use it (the ⟨bracketed⟩ spots + taste calls)

- **Expert stance** — fill in the ⟨your primary domain⟩ placeholder with the field you work in, so
  answers come from a practitioner's stance instead of a generic one.
- **Register and tone** — this is the most *taste-dependent* section. It's deliberately terse and
  strips out warmth/reassurance. If you like a warmer assistant, soften or delete it. Don't keep it
  just because it's there.
- **Push, prod, disagree** / **nothing closed unless the user closes it** — strong stances that
  invite pushback and treat your soft preferences as reopenable. Keep only if you actually want to
  be argued with; some people don't.
- **Adversarial self-check** — if you build a custom review slash-command later, wire it into the
  "escalate" line.
- **Hard-won lessons** — these are generic debugging traps. The real value of this section is *your
  own* accreted lessons (see §4). Treat what's here as examples of the format.

## 3. Merge, don't clobber — and keep it lean

The single most important maintenance rule (evidence-backed, not preference): **a long, dense
instruction file measurably degrades how reliably Claude follows any individual rule** — later and
lower-signal rules get dropped first. So:

- If you have an existing `CLAUDE.md`, **merge by hand**: keep the higher-signal version of each
  overlapping rule, don't stack both.
- **Audit test per line:** "would removing this cause a mistake?" If not, cut it. Every low-value
  line dilutes the salience of the load-bearing ones.
- **Front-load the highest-stakes rules** (verify-vs-infer, self-check) — order matters under density.
- Route *sometimes*-relevant material (long playbooks, war-stories, domain history) into on-demand
  docs you point at, not into the always-loaded file.

## 4. How it should grow

- **Add a rule only after you actually observe the failure** — ideally the *second* time it happens,
  not preemptively. A file grown from real failures is high-signal; one grown from imagined ones is bloat.
- **Distill each lesson to a one-liner** in `CLAUDE.md`; if it has a useful backstory, put the full
  narrative in a companion file (e.g. `~/.claude/working-style-lessons.md`) and reference it, so it
  loads on demand instead of every session.
- **Prune rules Claude already follows** without being told — they're just noise.

## 5. Quick start

1. Fastest: open Claude Code in a clone of this repo and follow **`ADAPT-WITH-CLAUDE.md`**.
2. Or manually: copy `CLAUDE.template.md` to `~/.claude/CLAUDE.md` (or merge into your existing one),
   fill the ⟨domain⟩ placeholder, make the tone/pushback taste calls in §2.
3. Start a fresh session; run `/memory` to confirm it loaded.
4. Over the following weeks, add your own one-line lessons as you hit real failures; prune anything
   that isn't earning its place.
