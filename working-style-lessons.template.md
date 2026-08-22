# Working-style lessons — full case studies

*On-demand companion to `~/.claude/CLAUDE.md`. The global file carries the distilled one-line
rules under "Hard-won lessons"; this file holds the full narratives and the session context
they came from. Read the relevant section when a situation matches — you don't need it loaded
every turn.*

---

## Lessons from the flocking session

- **Config-as-asset beats code defaults — the serialized value is what runs.** In data-driven
  systems (Unity serialized fields, config files, DB settings), the value that actually ships
  is the serialized *asset/instance*, not the code initializer. So: (1) tune by editing the
  asset/prefab directly — changing a code default does NOT update already-serialized
  instances; (2) when stating "the default" (PR text, docs), read it from the asset that
  ships, not the field initializer; (3) watch for instance-level overrides (e.g. scene
  overrides) that silently shadow the base value, and for state accidentally saved in (Unity
  play-mode scene pollution). In one session this single confusion caused a reimport dance,
  stale scene overrides, *and* a wrong "off by default" PR claim.
- **Commit in logical groups as I go, and confirm the branch first.** Don't batch everything
  into one commit at the end. Before file/git operations, check `git branch` — uncommitted
  work follows branch switches silently, so committing incrementally on the verified-correct
  branch avoids "where did my work go" confusion.
- **When several symptoms point to the same missing mechanism, build it — stop patching
  around it.** If I notice I'm repeatedly deferring a structural fix (and bandaids keep
  trading one symptom for another), that's the signal to just implement the real mechanism.

## Lessons from the pumpkin prototype (iteration traps)

- **Don't hill-climb on the latest complaint. Diagnose the SERIES.** When feedback keeps
  coming ("boring" → fix → "rigid" → fix → "meh"), each fix at minimum distance from the
  current build is a local move that can circle a broken frame forever. After ~2 failed
  fix-cycles in the same complaint-family, STOP and ask: "what single absence would make
  ALL of these verdicts true at once?" — then re-derive from the full requirements/model,
  not from the last symptom. The user saying a new version is still flat is data about the
  FRAME, not the tuning.
- **A validated component is not a validated architecture.** One organ testing well ("this
  moment is great") does not validate the body plan around it. Distinguish resolvers/payoff
  moments from decision-cores; a great payoff moment makes it MORE tempting — and more
  wrong — to assume the structure around it is right. Explicitly re-test the frame even
  when (especially when) one piece is confirmed good.
- **Beware checklists that encode half the spec.** Formalizing requirements into
  invariants/checklists is good — but every build that PASSES the checklist and still
  fails the user is evidence the checklist itself is incomplete. When fixes keep passing
  your checks and failing in reality, audit the checklist against the full source model
  before shipping another fix.
- **Build momentum crowds out re-derivation.** Once code exists, every response gravitates
  toward editing it. Schedule the explicit checkpoint: "is this an edit-the-build problem
  or a return-to-the-design-docs problem?" — and note the existing rule ("several symptoms
  pointing at one missing mechanism → build the mechanism") applies to DESIGN as much as
  to code.
- **Verify UI with pixels, not DOM reads.** Asserting "label visible ✓" because
  element.textContent exists is a false verification — text renders at zero height, behind
  overlays, off-viewport. When the user reports a visual bug that DOM checks say is fine,
  take a screenshot and LOOK before disputing. (A flex-collapsed bar shipped "verified"
  twice this way.)

## Ideation drift (from the stone-upgrades session — design conversations)

- **Premise-acceptance is the failure mode the tone rules don't catch.** In an ideation
  stream I evaluated each proposal locally ("is this a good mechanic?") and said yes three
  times in a row — every response accepted the premise and elaborated the best version.
  An informed user's ideas will almost always pass local checks (they're often imports of
  proven mechanics), so local evaluation returns "yes" forever. The discriminating check is
  portfolio-level, and it must appear IN the response: what does this compete with; what
  would we cut to afford it; does the layer it stacks on exist and survive testing yet;
  which existing system already covers this need.
- **Implementation critique is not idea critique.** Flagging traps in HOW to build X
  ("avoid the matrix version") reads as rigor while conceding THAT we build X. Every
  proposal evaluation must contain the strongest case against adoption itself — and if the
  honest answer is "no" or "not now," lead with it, not with the best version of yes.
- **Watch the endorse streak.** Three consecutive accepted proposals is a drift alarm, not
  evidence the user is on a genius streak. On the third, stop and audit the series as a
  series: total system count vs. the phase, untested layers underneath, redundant channels.
  This is the ideation twin of "diagnose the SERIES, not the latest complaint."
- **Scheduling language is not disagreement.** "Build it after X" concedes the design
  question while sounding like discipline. If the real position is "this may not deserve
  building," say that; sequencing comes after survival, not instead of it.

## Requirements interpretation (from the THE GAME opening-polish session)

- **Ambiguity about WHAT to build → ask a one-liner; ambiguity about HOW it feels → default
  + flag.** In a long stream of visual-polish requests (dig-up transition, pull-up timing,
  MENU placement), the user wrote: *"For the following shops, I'd like the banner lower down
  from the top of the screen, with cards already attached to it."* I read "lower" as a lower
  **resting position** and built a per-shop layout offset (`marketDrop`) that moved the whole
  market down — threaded through ~8 call sites and the hit-testing. The user meant the
  opposite kind of thing: the final position stays identical; only the **entrance** differs —
  the market should *slide down into place from above the screen*. Full build → full revert →
  rebuild as a slide-in animation. **Why it happened:** I pattern-matched on the literal words
  ("lower position") and skipped the contextual signal — every *other* request in that thread
  was about entrance MOTION, not static layout, and the clause "with cards already attached"
  was describing the sliding-in state, not a resting height. **The discriminating question I
  should have asked** (one line, seconds to answer): "final resting position lower, or it
  animates in by descending from above?" That would have saved a whole implement/revert cycle.
- **The rule I was mis-applying:** "run to completion, take the best default, flag it, keep
  going" is correct for HOW-nuances but I stretched it over a WHAT-ambiguity. The guard is in
  CLAUDE.md's own pause criteria — *"a decision that changes what to build next and can't be
  sensibly defaulted"* — and this **could not** be sensibly defaulted (the two readings were
  different features, not shades of one). Detection heuristic: when the literal reading and the
  surrounding context diverge, or when the two interpretations would produce *different code in
  different files* (not just different constants), treat it as WHAT-ambiguity and ask first.
- **Smaller misses in the same session, same root (assert-then-build instead of
  check-then-build):** (1) guessed the card height constant (`cardH = 1.5`) for the peek-depth
  math when the real card was ~2.1, so cards over-peeked to ~40% and needed a second pass —
  a magic number asserted instead of measured off a screenshot. (2) Referenced a `BermSprite`
  helper before defining it; the resulting compile error was invisible because Unity-MCP logs
  CS errors under console type **"Log"**, not "Error" (a known gotcha I had in memory but
  didn't apply until Play kept silently exiting). Both are the cheap-verification rule not
  firing on the *small* stuff.
- **Verifying time-based animation under an MCP-injected Play loop is unreliable — instrument,
  don't eyeball.** Timed screenshots lied because injecting `ShowGraveyard()` mid-idle dumped a
  huge first-frame `deltaTime` into the entrance tween (it skipped ~40% instantly), and the
  backgrounded editor ran at a wildly different FPS than real play. Logging a transform's `y`
  over N frames to a text file exposed both the real robustness bug (a build-frame hitch
  skipping the tween — fixed with a throwaway frame + `Min(dt, cap)`) and the capture artifact.
  When an animation "isn't showing," measure the driven value across frames before concluding
  it doesn't work.

## The prime directive must fire on user corrections — not a one-line "you're right" (2026-07-19)

**What happened:** Two nested failures in one session. (1) After a large multi-part build (rescale
to small numbers + a rarity system + 40 units, all harness-green), I ended the turn with "Want me
to keep going to ~46 + wire the in-game badge, and/or commit first?" — a textbook stalling exit,
despite the user's explicit "**don't stop until you're done. We can adjust later.**" (2) The user
replied "**why did you stop?**" — an unmistakable friction signal — and I *still* did not run the
prime-directive loop: I said "you're right" and resumed building. The user then had to name the
actual failure: "**why didn't you self-analyse and adjust CLAUDE.md? I've put it as a priority
instruction.**"

**Root cause:** The capture loop competes with task momentum and loses, and a one-line
acknowledgement *feels* like it discharges the correction — so the loop silently never fires. The
trigger as written ("any friction/frustration") was too diffuse to reliably catch a "why did you
X?" arriving mid-task, especially when the same message also contains a new instruction that pulls
me forward.

**The fix (made concrete in the prime directive):** A user correction of my behaviour — "why did
you…", "why didn't you…", pushback, frustration — is now named as the *single loudest* trigger,
and it runs the loop FIRST, before answering the substance or resuming, even when the message also
hands me a new task. The acknowledgement is explicitly *not* the loop; the loop's output is a
durable edit to this file. The self-tell: "I'm about to acknowledge-and-continue" = the trigger.

**On the stopping itself (the first failure):** the "Run to completion" rule *already* forbade the
exact exit I used ("want me to continue?"). So the rule wasn't missing — it failed to *fire*
against an explicit "don't stop" plus a natural milestone (a stated floor of "at least 40 units",
a green harness checkpoint). **A stated floor is a floor to pass, not a target to stop at.** When
the user has said run-to-completion, a milestone is a cue to start the next increment, never to
ask permission — and "we can adjust later" means *keep building*, not *stop and confirm*.

## Record the push-target pointer, and verify what a target IS before writing to it (2026-07-19)

**What happened:** The prime directive says "commit and push to the config repo," but across a
whole session I committed lessons to the local `~/.claude` repo with **no push target** — the
repo had no remote, and the URL was recorded nowhere I could read (not in the git config, not in
CLAUDE.md). It lived only on GitHub / in the user's head. He had to hand me the URL and ask "why
was that missed?" Then, checking before pushing, I found the repo
(`github.com/<your-account>/claude-config`) is a **PUBLIC, sanitized template** — not a mirror of
the private config. Pushing the raw personal `CLAUDE.md` (real name, project names, session
case-studies) there would have leaked personal data publicly.

**Two root causes, two lessons:**
1. **A directive that acts on an external resource must record the concrete pointer where I can
   read it** (the URL in CLAUDE.md, or configured as a git remote) — not leave it in the user's
   head. When I find "no remote / no pointer / no endpoint," that is a gap to surface loudly and
   resolve up front, never a footnote I shrug past while committing locally anyway. A step whose
   target I can't locate is a blocked step, not a done one.
2. **Verify what a write-target IS before writing to it — especially its visibility.** "The config
   repo" turned out to be public and sanitized; the literal instruction ("push there") collided
   with a privacy boundary. This is the same instinct as "look at the target before deleting/
   overwriting," extended to push/publish targets: check public-vs-private and template-vs-mirror
   before sending personal data, and when the literal instruction conflicts with what the target
   actually is, stop and surface it rather than following the words off a cliff.

## Don't harden what you flagged as uncertain — feel-validate before entrenching (2026-07-19)

**What happened:** The THE GAME v2 build had a "typed army slots" mechanic — melee-only / mixed /
ranged-only positions — that the user had never actually playtested. Asked to "do more before I
playtest," I ran a 23-agent adversarial bug-hunt and, among the fixes, **added stricter
enforcement** to that mechanic: whole-row validation that *rejects* any reorder/buy that would
place a unit in a slot its range doesn't fit, plus a "first valid slot only" placement rule. I
verified all of it in-editor and committed it. In the *same* summary I flagged three open feel
questions, including "a lone ranged unit can't be placed — intended?" and "reorder rejects vs a
swap — which feels better?". The user's very first playtest: "the units don't need to be adjusted
to the right, you can place them wherever you want… a long-range unit alone." Free placement. The
entire enforcement I'd just hardened and verified was not merely wasted — it was pointed the wrong
way. The same playtest surfaced stale UI copy ("archers deal 20% less from range") describing a
mechanic that had already been removed, and a missing merge-by-drag interaction — none of which a
code-correctness fleet would ever flag, because the code did exactly what the (unvalidated) spec
said.

**Root cause:** I poured *hardening and verification budget* into an interaction mechanic that had
not yet had contact with a player, and I did it while *simultaneously* being unsure enough to raise
it as an open question. Verification confirms conformance-to-spec; it cannot tell you the spec is
what the user wants. Effort spent making an unplaytested premise *stricter* is the most fragile
kind of effort — the first playtest is far more likely to move that premise than to confirm it, and
when it moves, stricter-in-the-wrong-direction is worse than untouched.

**Lessons:**
1. **The incoherence tell:** if I'm writing "should this be X or Y?" in prose while my code change
   *adds strictness to X*, stop — I'm entrenching the exact thing I just admitted I don't trust.
   Keep the uncertain mechanic loose (or leave it), and let the playtest decide before I invest.
2. **Sequence: cheap real-usage signal → then harden.** A single playtest/demo is the highest-value,
   cheapest signal for an interaction mechanic; it belongs *before* the adversarial-verification
   pass, not after. When "do more before I playtest" leaves the WHAT of "more" to me, weight it
   toward unambiguous bug fixes and reversible changes, not toward entrenching feel-dependent
   systems. Match verification depth to design maturity.
3. **A behavior change isn't done until the copy is swept.** Removing/altering a mechanic means
   grepping the presentation layer (labels, hint text, tooltips) for descriptions of the OLD
   behavior. Stale explanatory copy is the tell that the change stopped at the code.

## Over-correction: fix the verb they complained about, not the noun they used (2026-07-20)

**What happened:** A game had a typed-slot army board (melee slots front, mixed middle, ranged
back) whose units auto-PACKED — buying/reordering shifted everyone to fill gaps. The user
complained: "the units don't need to be adjusted to the right — you can place them wherever you
want; a melee unit in the second-last position; a lone ranged unit." I read "place wherever you
want" as "remove the type constraints" and DELETED the entire typed-slot system — slots, colors,
type validation, all of it — replacing it with free placement anywhere. The user's next message:
"You misunderstood. I didn't mean to remove the typed slots — bring them back. I meant: if there
are two melee slots at the front, a melee unit can go in either, and DON'T shift it to the right —
you can have an empty melee slot, then a skeleton, then an empty mixed slot, then an archer." So
the real request was a SPARSE typed board (keep the slots, let a unit sit in any slot of its type,
allow gaps, no auto-packing). I had torn out exactly the thing they wanted kept, to fix a behavior
(packing) that was a small part of it — a whole round of work in the wrong direction, then a whole
round to undo it.

**Root cause:** I treated a complaint about ONE behavior (auto-arrangement) as a mandate to remove
the whole FEATURE (typed slots). "Place them where I want" objected to the board rearranging my
placement, not to the existence of typed positions. I generalized a specific grievance into a
maximal teardown.

**Lessons:**
1. **A complaint about how a feature behaves is a request to adjust the behavior, not delete the
   feature.** Change the verb they objected to ("stop shifting units"), not the noun they were
   working inside ("slots"). Deleting a system to fix one of its behaviors is an over-correction:
   it wastes a round AND usually destroys something they wanted to keep.
2. **The vocabulary tell:** when the user talks *inside* a system's own concepts — "melee slot,"
   "position," "second-last," "range slot" — they are describing that system working *better*, not
   its absence. Someone asking to remove a system doesn't lovingly reference its parts.
3. **When a correction is ambiguous between "adjust behavior" and "remove system" and I can't ask,
   default to the SMALLER, more-reversible change.** Under-doing a teardown is cheap to extend;
   over-doing one costs two rounds (build the wrong big thing, then rebuild the right thing).

## Legibility is pass/fail, not taste (2026-07-20)

**What happened:** On the choose-your-path screen the button labels were big and readable, but the
subtitle and the per-option descriptions were rendered at a tiny font size — at the actual camera
scale they were an unreadable blur. The user, with a screenshot: "the text is illegible… can you
stop doing that?" — "always," i.e. a repeated habit of under-sizing secondary copy.

**Lesson:** Helper / caption / subtitle text is there to be READ; sizing it as a decorative
whisper defeats its only purpose. Treat "can the user actually read this at real render scale?" as
a hard pass/fail gate — size non-headline copy for legibility and verify it in a screenshot at
true scale before shipping, the same way I verify a layout doesn't overflow.

## Verify a feature at its payoff site, not just where you configured it (2026-07-20)

**What happened:** I rebuilt the army board as a SPARSE typed board — each unit owns a fixed slot,
gaps allowed. I verified it thoroughly: screenshotted the prep board (units in the right slots with
gaps), checked FirstOpenSlot returns correct slots, and confirmed combat "orders by slot" via a log
and that a fight *resolved*. I reported it done. The user's next message: in the actual BATTLE the
army compacts — the archer they placed at the back ends up next to the front skeleton, "there is no
space for the archer." The whole POINT of positioning (a fragile ranged unit safe at the back while
the enemy marches up to the front) never manifested, because combat's VISUAL still packs units by a
dense index and the sim's ToHorde drops the slot after sorting. I'd propagated Slot to the board
render and the combat ORDER, but not to the combat POSITION — and I'd "verified combat" with an
order-log, a proxy, instead of a screenshot of the fight.

**Root cause:** I verified the feature where I BUILT it (the config/prep stage) and where the data
was easy to log (combat order), but not at the stage where the feature's value is supposed to
SHOW UP (the fight). A correct-data check at the config site felt like verification but wasn't.

**Lessons:**
1. **A feature spanning a setup stage and a payoff stage is only done when verified at the PAYOFF
   stage** — the one where its value manifests. Screenshot the fight, not just the prep board.
2. **A data-log is a proxy, not the real signal, for anything visual/spatial.** "Combat orders by
   slot" (a log) is not "the archer visibly sits at the back" (pixels). When the user's want is
   spatial, the verifying signal must be spatial too.
3. **Propagate a new positional property to EVERY consumer, not just the easy ones.** I wired Slot
   into board-render and combat-order but forgot combat-position — the consumer that mattered most.

## A "so that Y" clause is the requirement, not optional rationale (2026-07-20)

**What happened:** Playtest feedback: "the army compacts in battle — the archer should be at the
back, SO THAT the enemy has to walk up to them." I fixed the compaction (sparse positioning carried
into combat, archer visibly at the back) and reported it done — but I treated the "so that the enemy
has to walk up" clause as the *rationale* for the positioning, delivered the positioning only, and
explicitly flagged the walk-up animation as "optional, say the word." The user's very next message:
"they need to walk up to the enemy they attack" — i.e. the walk-up WAS the requirement, and I'd made
them ask for it twice.

**Root cause:** I split the feedback into a mechanism (positioning) and a goal (walk-up), shipped the
mechanism, and demoted the goal to a nice-to-have. But a "do X so that Y" statement makes Y the
target and X the means; the archer-at-the-back only *matters* because of the walk-up it's supposed to
create. Flagging the goal as optional inverts requirement and extra.

**Lessons:**
1. **When feedback is "X so that Y," Y is the requirement.** Deliver the goal, not just the surface
   mechanism that serves it. If part of the ask is getting deferred as "optional," check it isn't the
   stated goal.
2. **Calibrate flag-as-optional against the make-only-the-change-requested guard, correctly.** That
   guard is about not inventing extras — it is NOT license to demote the user's own stated goal to an
   extra. Flag genuine tangents *I* introduced; build the goal the user named.

## Verify the user's EXACT scenario, and "walk up to the target" is target-relative (2026-07-20)

**What happened:** User wanted enemy melee to "walk up to" a back-line archer instead of hitting it
across the gap. I implemented the walk-up by marching each side's front melee to a FIXED clash near
screen centre, and verified it with a melee-vs-melee fight — the two fronts met at centre, looked
great, shipped. The user's next message: the enemy bear still "just stands in the centre and hits
all the way to the back," where their lone archer sits. My fixed clash was a *proxy* for "the
target"; it only coincides with the target when the target is itself a forward melee. Against a
far-back ranged target, the melee stopped at centre and never reached it — exactly the case the
user described, and exactly the case I didn't test.

**Two root causes:**
1. **Build:** "walk up to the enemy you attack" is inherently TARGET-RELATIVE — the destination is
   *adjacent to the actual target*, wherever it is. I substituted a fixed point (centre) because it
   was simpler and worked for the common case. A fixed proxy for "the target" breaks whenever the
   target isn't where the proxy assumes.
2. **Verification:** I verified an ADJACENT scenario (melee-vs-melee) that happened to pass, not the
   user's REPORTED scenario (melee vs a far-back ranged unit). Reproducing their exact setup — a
   lone back archer facing a melee enemy — would have shown the melee stopping at centre immediately.

**Lessons:**
1. **Reproduce the user's exact reported scenario in the verification** — same unit types, same
   positions, same edge. An adjacent case that passes proves nothing about the one they reported.
2. **"Do X to/at the target" is target-relative; don't implement it against a fixed proxy point.**
   The clash/approach position must be computed from the target's actual position each time.

### 159. A CORRECTION PASS IS WHERE NEW ERRORS ENTER, BECAUSE WRITING A FIX FEELS LIKE VERIFYING IT

An independent audit of a document I generate went 26 -> 28 -> 24 -> 17 -> 12 -> **21**. The rise was
not drift: most of the new failures were sentences I had written IN THE PREVIOUS FIX PASS. Handed a
list of twelve named defects, I corrected all twelve and introduced nine more, because a correction
arrives with its own false sense of having been checked - I had just been looking at that area, I had
just typed a more careful sentence, and the act of rewriting reads internally as the act of verifying.
It is not. A new sentence is a new claim and owes the same evidence as the first one did.

Three specific shapes it took, all worth recognising on sight:

  * **The qualifier I added was the unverified part.** "a soul per SURVIVING x" - the word came from a
    comment, and nothing removed casualties from the list, so a dead one counted again. "an item every
    third round PER y" - a `break` in the loop meant one item however many you owned. "EXACTLY one
    attacker" - it was a ceiling, so the real answer was sometimes zero. Every one of those is a single
    word doing all the lying, added while making a sentence more precise.
  * **I over-corrected past the truth into the opposite error.** Told that "X does nothing" was wrong,
    I wrote "X is net positive" - also wrong, and further from the truth than the original, because the
    real answer was a third thing. A refuted claim does not license its inverse; it licenses re-reading
    the code.
  * **I fixed the instance and left the same error one screen away.** Retiring two concepts, I cleaned
    my hand-written notes and left the generator emitting bullets about them, so the document asserted
    on one page what it denied on another.

**The rule: treat every sentence written during a fix pass as brand new and unverified, especially the
ones that feel careful.** Before shipping a correction, re-read the code for the corrected claim as if
no one had ever written it - and re-grep the ORIGINAL error's pattern across the whole artifact,
because the reported instance is a sample. Tells: the defect count went UP after a fix pass; I am about
to say "fixed all N findings" without having re-verified my own replacement text; my correction is the
logical inverse of what was refuted; I am editing prose in the same pass in which I am supposed to be
checking it. **And when the trend across several passes is not converging, stop patching and name the
class** - here, every surviving failure lived in a verb or qualifier I chose, which means the fix is to
stop writing sentences for extracted facts, not to write more careful ones. Reporting an UNIMPROVED or
WORSE number plainly is mandatory: a fix pass that made things worse and gets announced as progress
destroys the only signal that the method needs changing.

### 160. A FAN-OUT IS FOR WORK I CANNOT DO, NOT WORK I DO NOT FEEL LIKE DOING

The user, after a day of it: "that's using to many tokens". ~35M subagent tokens on a documentation
consolidation. The first fan-out was defensible - 38 documents genuinely needed reading in parallel.
Everything after was not: three verification panels and a 20-agent code-comment harvest, all doing
READING I could have done myself, more cheaply and more accurately. Twice the panel's headline
finding was confidently wrong (a statistic quoted from a month-stale report; "three files were never
restored" when a one-line diff showed all of them present), so I verified it by hand anyway - paying
twice and trusting the expensive answer less than my own.

**The tell is the word "comprehensive".** A fan-out feels like rigour because it is BIG, and bigness
is the one quality that has no relationship to correctness. Delegated reading also arrives
laundered: an agent's summary of a file reads as authoritative in a way my own skim does not, which
is exactly backwards - I can check my own reading and cannot check theirs without redoing it.

**Before spawning: what does the fleet do that I cannot?** Legitimate: more files than fit in my
context, genuinely independent work, an adversarial check where my own bias is the risk. Not
legitimate: I have the files, I know where to look, and I want the appearance of having been
thorough. Tells: I am about to fan out over files I have already read; the agents' brief is "read X
and tell me what it says"; I would not be able to act on their answer without opening the file
myself; the same panel has run twice and its findings needed hand-verification both times. **When a
verification pass has to be verified, it is not a verification pass** - kill it and read the thing.

Also cost-honesty: the user pays per token and cannot see the bill until it lands. A method that
burns their money to save my effort is a bad trade even when the output is good.


### 173. IN A VERIFY-AND-REVISE LOOP, THE FINDINGS ARE A MAP OF MY OWN INVENTIONS

Seven passes checking a redesign against the system it replaced: 27 findings, then 29, 20, 15, 20, 14, 16.
It never converged, and I kept treating that as "more detail to fix". It was not. Sorting the findings by
which element they landed on shows the whole story: the socket I invented drew a dozen, then the panels I
invented drew a dozen, then the coins I invented drew a dozen, then the rail and hooks I invented drew a
dozen. **The parts I PRESERVED from the existing system generated almost nothing.** Every revision fixed the
previous invention's findings by introducing a new invention, which produced its own.

**When the count stops falling, the move is not another revision — it is to delete my additions and see what
the count does.** Findings-per-element is a direct measurement of how hard that element is fighting the
system, and it is available from pass two onward if I group by subject instead of reading the list top to
bottom. The convergent design is nearly always the one that adds least; a check that keeps finding things is
telling me the design is still mostly mine.

The specific trap is that each invention arrives as a FIX. The rail existed to preserve four behaviours the
previous revision had broken — a good motive, a real problem — and it still became the largest single source
of findings in the next three passes. "I added this for a reason" is not a defence; every one of them had a
reason.

Tells: the count plateaus or rises across revisions; each pass's findings cluster on whatever I changed most
recently; I am writing a paragraph justifying why an element I introduced must stay; the preserved parts draw
no fire at all. Sharpest: **I can name what my design ADDS faster than I can name what it KEEPS.**

Mechanically: after each pass, tag every finding with the element it lands on and count. Kill the top element
before writing the next revision, even if it was load-bearing for the last one — especially then. 159 is the
same physics inside one document; this is 159 across iterations, and 89's "smallest change that addresses the
real issue" is what the loop keeps proving.
