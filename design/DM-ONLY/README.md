> [!CAUTION]
> **DM-ONLY — CAMPAIGN SPOILERS**
>
> This folder holds the canonical design documents for Underleaf: the actual cosmology, the antagonist throughline, the overall campaign arc, and the living reference material the DM consults during prep and play.
>
> If you are or might become a player in this campaign, close this folder now. Players who genuinely want to read up on Underleaf can do so — that's nothing new for tabletop games — but please make a deliberate choice rather than stumbling in by accident.

# Contents

## Locked design foundation (the *what*)

- [`world-truths.md`](world-truths.md) — the actual cosmology of Underleaf: emergent intelligence at every scale, The Quiet, the magic system, the dead-scientist mechanic, the role of AI. **Also** the authoritative *"Precise phrasing — single-timeline discipline"* rubric (❌/✅ table, four drift patterns, house template).
- [`antagonist.md`](antagonist.md) — the campaign's central antagonist arc.
- [`arc.md`](arc.md) — play-mechanics phasing: what mechanics are active when, the magic-discovery beats, the in-medias-res convention.
- [`big-arc.md`](big-arc.md) — canonical story-shape document: three acts, locked invariants, cast, misdirection seed bank, agency choices, two endings. In-game time discipline. "Directors and pawns" framing + held-open-causation reading-list. Cross-references every other DM-ONLY file.
- [`principles.md`](principles.md) — campaign-level authorial principles (*possible future not prophecy* / *engagement layers* / *rationalization is real, work with it*).

## Living campaign-management docs (the *how* + the *cadence*)

- [`episode-outline.md`](episode-outline.md) — session-by-session working horizon for Eps 5-25 (updated after each played session). LIVING DOCUMENT: it holds the *cadence* while `big-arc.md` holds the *shape*. Prevents Act I from ballooning silently; every future episode's prep starts by revisiting this file.
- [`hook-ledger.md`](hook-ledger.md) — cross-campaign rollup of every unresolved narrative hook + fire-status + standing per-session disciplines (S1 flattening beat / S2 Dakota-driver check / S3 Dakota-culprit-frame monitor / S4 ledger-arithmetic audit).
- [`facts-ledger.md`](facts-ledger.md) — cross-campaign facts snapshot: what is TRUE in the world. Consulted during play when a PC surfaces something obscure. Grows each episode.
- [`anchors-cards-ledgers.md`](anchors-cards-ledgers.md) — substrate-mechanics vocabulary: anchors (documentary vs physical), anchor sites, cards, ledgers (L1-L8 assignment table), retro-causal writing.
- [`brainstorm-open-questions.md`](brainstorm-open-questions.md) — pre-canon seeds under active thought (NOT committed design). Refined incrementally; user decides implement or discard.

# Reading order

If you are coming to Underleaf cold, read in this order:

1. `principles.md` — the three authorial principles that shape every other decision.
2. `world-truths.md` — what is actually going on cosmologically. Without this, nothing else makes sense. Includes the phrasing rubric that keeps DM notes precise.
3. `big-arc.md` — the campaign's three-act story shape, locked invariants, and held-open-causation reading-list.
4. `arc.md` — the play-mechanics phasing that runs alongside the story shape.
5. `antagonist.md` — the throughline and its resolution. Builds on the cosmology.
6. `anchors-cards-ledgers.md` — vocabulary you'll need before reading detailed episode DM notes.
7. `episode-outline.md` — the session-by-session horizon. Read after the arc-level docs so the sessions make sense in context.
8. `hook-ledger.md`, `facts-ledger.md`, `brainstorm-open-questions.md` — reference docs. Skim now; you'll return to them during each episode's prep.

# Discipline for episode prep

Before designing any new episode:

1. Skim [`episode-outline.md`](episode-outline.md) — what arc-nodes are due? Which have slipped?
2. Check [`hook-ledger.md`](hook-ledger.md) — anything past its fire-by window that needs to be promoted (into the next episode) or retired (as ambient texture)?
3. Read [`facts-ledger.md`](facts-ledger.md) alphabetical index for any NPCs / locations / artifacts you might touch.
4. Glance at [`brainstorm-open-questions.md`](brainstorm-open-questions.md) — does the current episode open any new angle on an active-brainstorm entry?

Post-session:

1. Fold played record into the episode's `dm/run-guide.md`.
2. Update `hook-ledger.md` fire statuses.
3. Add played facts to `facts-ledger.md` tagged `First established: Ep N (played)`.
4. Re-snapshot `episodes/00N-.../dm/continuity-through-ep-N.md` from the updated master.
5. Update `episode-outline.md` Ep N+1 entry based on what actually happened.
6. Draft player-facing summary + any per-player packages.

# Authoring conventions

When you write a new DM-only document, copy the `> [!CAUTION]` alert block verbatim from the top of any file in this folder. The warning must be the first thing a reader sees if they open the file without context. GitHub renders these alerts as a red-barred warning block; other Markdown renderers degrade them to a regular blockquote, which is still visually distinct.

When you write content that mixes spoiler and non-spoiler material, split the file: public content goes in the non-DM folder, private content goes here. Mixing the two in one file is what leads to accidental leaks.

- [`run-guide-style.md`](run-guide-style.md) — **read before writing or revising any episode run-guide.** The two-phase method: a shorthand-heavy working draft for finding bugs, then a full rewrite as the document the DM actually runs from. Includes the handover checklist.
