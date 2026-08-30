# {{pc:4}} — phase gates

*DM and author facing. **{{pc:4}}'s player must not see this.** Written
2026-08-29, after Ep 5, because the existing documentation conflated two
different gates and one of them was never defined at all.*

---

## The defect: realization and release are not the same thing

`world/rules.md` defines a sequence:

1. **Phase 1 — Accidental.** The caster does not know. *(Where he is now.)*
2. **Phase 2 — Realization.** Per-PC, private, sessions 3–6. The caster notices
   the pattern. **Never a table beat, never group-ratified.**
3. **The trying-too-hard tax.** −2, applied once they know.
4. **The moment of release.** One quiet, unforced moment. **Drops the tax to 0.**

**His sheet defines step 4 and calls it "his true Phase-2 release moment":**

> *"he has to earn it by dropping the persona in a scene where the persona would
> have gotten him what he wanted."*

**That is a release condition and it is a good one. Keep it.**

**But the episode outline and the Ep 5 run-guide both call the same sentence his
"Phase-2 realization."** It is not. It is step 4 being used as step 2.

> **So the actual answer to "what does {{pc:4}} need to do to advance to the next
> phase" is: nothing is written. His realization gate has never been defined.**
> Everything on file describes a release he cannot reach yet, because he has not
> realized.

---

## Why his realization is genuinely harder than anyone else's

**His cover story is airtight, and he built it himself.** His domain is
speech/presence: a room turns to him, a hostile crowd cools, an official
reconsiders. **He believes he is simply charismatic.** So every effect that
lands is *confirmation of his self-model*, not an anomaly.

Compare the others: {{pc:3}} reads absences that are not there to read.
{{pc:2}} produced firewood in a locked hall. Those are hard to explain away.
**{{pc:4}} can explain every one of his away, and does, automatically.**

**This is a feature, not a problem to engineer around.** But it means the ordinary
realization move — show him something the party missed — will not work. He will
absorb it.

---

## Proposed realization gate — the DM's call

**The gate must be an effect his charisma cannot account for.** Three shapes that
work, in rough order of preference:

**(a) It lands while he is not performing.** He is silent, or across the room, or
has already given up on the person. **The room turns anyway.** Charisma requires
a performance; there wasn't one. *This is the cleanest and it costs one scene.*

**(b) It lands on someone who could not perceive him.** Through glass, on a call
with the mic muted, someone facing away, someone who does not share a language.
**Strong, but stage it carefully** — it edges toward spectacle, and this campaign
does not do spectacle.

**(c) It lands when he was actively trying for the opposite.** He needs to be
ignored — to slip past, to not be the one remembered — and he cannot manage it.
**Thematically the richest**, because the thing he has organised his life around
turns out not to be under his control, and it is the one he would find
frightening rather than flattering.

> **Recommendation: (c), with (a) as the cheaper fallback.** (c) is the only one
> that threatens the self-model instead of feeding it, which is what realization
> has to do for this character.

**He also has no body cost-tell**, which every other caster has ({{pc:2}}'s
migraine, {{pc:5}}'s neck-flare). **That is a gap and it is the other half of the
fix** — a cost is something charisma cannot explain either. Suggested, matching a
man who talks for a living: **his voice goes. Not dramatically — it thins, and
catches, for an hour or two afterwards.** He would notice, and he would hate it,
and he would have no story for it.

---

## The player-preference conflict — decide deliberately, do not drift

**The player's stated want** *(from a simulated read; confirm with him before
relying on it)*: a {{pc:4}} who **notices but never concludes** — *"a man who has
been given every piece and declines to assemble them."*

**That is compatible with realization and incompatible with release.**

- **Realization** is noticing. It can land and be rationalised away *for the
  persona*, while still flipping `knowsTheyCanCast`.
- **Release** requires him to genuinely drop the persona at a cost. **If the
  player never wants that, {{pc:4}} stays at −2 indefinitely.**

> **A permanently-taxed caster is a legitimate and interesting outcome** — the man
> whose conviction costs him the thing the conviction is for, forever. **But it
> must be chosen, not discovered at Ep 11 when his moment of release is due.**

**Decide before Ep 11.** Options: run the release as written and let him decline
it; substitute a release that does not require a persona drop; or accept the
permanent tax as his arc.

---

## What to log when it happens

- **Realization:** flip `knowsTheyCanCast` to true, apply the −2 tax, note the
  scene. **Do not announce it at the table.**
- **Release:** clear the tax to 0, note what it cost him.
- **Keep the persona thread out of both entries.** His social arc and his casting
  arc are separate and must not be run through each other — see
  `characters/pcs/dakota-whitmore.json` → `dmNotes.castDomain`.
