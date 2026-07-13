# Adapt this template using your own Claude Code

You don't have to hand-edit the template — let Claude Code do the adaptation as a short
interview. Most of the work is *taste calls* (your domain, how terse you want the tone, whether
you want to be argued with), and Claude can draw those out of you instead of you editing markdown.

## Flow

1. Clone this repo (or download `CLAUDE.template.md` and `README.md` into a folder). The template
   is named `CLAUDE.template.md` — not `CLAUDE.md` — precisely so Claude Code doesn't auto-load it
   as your active config while you're still editing it.
2. Open Claude Code in that folder.
3. Paste the prompt below.
4. Answer its questions. Review the result it shows you. Approve. It installs to `~/.claude/CLAUDE.md`.
5. Start a **fresh session** (or run `/compact`) so the new config takes effect — a running session
   won't pick up the file, since it's read once at launch.

## Paste this prompt

> I want to set up a personal working-style config for you (a `~/.claude/CLAUDE.md`). There's a
> starter template at `./CLAUDE.template.md` and its guide at `./README.md` — read both first.
>
> This template came from someone else, so adapt it to me rather than installing it as-is.
> **Before writing anything, interview me** — ask these as questions and wait for my answers;
> do not guess the taste calls:
> 1. My primary domain(s) of work, so the "Expert stance" section names them.
> 2. Whether I want the terse, no-warmth tone in "Register and tone" as written, softened, or dropped.
> 3. Whether I want the "push, prod, disagree / treat my preferences as reopenable" stance, or something gentler.
> 4. What kind of work I do day to day, so you keep the debugging lessons that apply (e.g. the
>    UI/pixels one) and drop the ones that don't.
> 5. Whether I already have a `~/.claude/CLAUDE.md`. If I do, read it and **merge** — keep the
>    higher-signal version of each overlapping rule, don't stack both.
>
> Then apply the file's own maintenance discipline from the README: keep it lean (drop any line
> whose removal wouldn't cause a mistake), front-load the highest-stakes rules (verify-vs-infer,
> self-check), and don't add anything I didn't ask for.
>
> Show me the adapted file and a short list of what you changed and why. Only after I approve,
> write it to `~/.claude/CLAUDE.md`. Then remind me to start a fresh session or run `/compact`.

## Why interview-first matters

The whole point of this config is calibrated, non-sycophantic reasoning. If Claude *guessed* your
tone and pushback preferences to be agreeable, it would be committing the exact failure the file
is trying to prevent. Making it ask — and making you approve the result before it touches your
real config — keeps you in control of a file that will shape every future session.
