# The Underleaf party

**Underleaf ships with a specific, canonical five-PC party** — the characters the published episodes are written around. They are recommended, not required; a table can freely substitute their own PCs (see "Adapting" below) but should expect to also adapt the campaign material when they do.

Quire couples PCs to story more tightly than a typical D&D module. Ep 3 §1 hardcodes an 1878 mining-crew ledger with the party's four surnames (Reyes / Iyer / Sun / Whitmore / Faraone; the fifth is deliberately smudged). Ep 4 introduces an NPC (Vivian Loewe) who reads Dakota's specific shape at her door and asks each PC one small personal question. Substituting your own party works — but where the campaign's DM notes reference these PCs by name or role, you'll need to remap or rewrite. That's the cost of the tighter coupling; the payoff is scenes that land specifically rather than generically.

## The five PCs (in slot order)

Full sheets in this directory as one JSON per PC. Summary here:

| Slot | Name | Handle | Archetype | Focus | Domain | Alignment (start) |
|---|---|---|---|---|---|---|
| S1 | **Morgan Reyes** | "coredump" | Hacker | Flipper Zero | systems / information | Chaotic Good |
| S2 | **Priya Iyer** | — | Caregiver | The bag (canvas messenger) | body / care | Chaotic Neutral |
| S3 | **Mira Sun** | — | Outsider (memory-loss backstory) | The note (brother's letter in a locket) | memory / identity | Chaotic Good |
| S4 | **Dakota Whitmore** | — | Control-seeker (political-history undergrad) | Mahogany pipe | speech / presence | Lawful Evil (personal-code framing) |
| S5 | **Marcus "Mars" Faraone** | "Mars" | Operator (aggrieved) | 9mm SIG P365 (concealed-carry) + keychain holster clip fallback | posture / presence | Chaotic Neutral |

Files:
- [morgan-reyes.json](morgan-reyes.json)
- [priya-iyer.json](priya-iyer.json)
- [mira-sun.json](mira-sun.json)
- [dakota-whitmore.json](dakota-whitmore.json)
- [mars-faraone.json](mars-faraone.json)

## Load-bearing party dynamics

Published DM notes assume these:

- **Morgan + Mars** are the only pre-flight PC pair — they know each other, they trust each other. Give them scenes where their bond is a strength.
- **Dakota ↔ Mira** is the load-bearing dramatic irony. Dakota has decided Mira is his follower; Mira is quietly watching him. If Mira ever contradicts him openly, that's an act break for Dakota's arc.
- **Priya** is the emotional center whether she chose to be or not. She's the person the others check with when they need to feel like a person.

## Load-bearing surnames

Ep 3 §1's 1878 mining-crew ledger names four of the party's surnames as historical miners at Bodie's Standard Mill (Reyes / Sun / Whitmore / Faraone). Iyer is the deliberately-smudged fifth entry (a "physician") whose surname can't be verified. **If you substitute PCs, the surname name-match beat can either be rewritten around your PCs' surnames OR the scene will lose its central hook.** See Ep 3 §1 answers doc for the mechanism (cheap-shape cost-gradient; the substrate routed through the cheapest available anchor).

## Adapting the party

**If you keep all five recommended PCs:** run the campaign as published; per-PC DM notes will line up.

**If you swap ONE PC:** most likely to be safe if you preserve the archetype (a different Hacker for Morgan, a different Caregiver for Priya, etc.) and keep the surname where possible. Rewrite the ONE character's backstory to fit your new PC; leave the others intact. Ep 3 §1's smudged-fifth-entry (Iyer) is the most-substitutable slot; the four historical names are the hardest to swap without rewriting Ep 3.

**If you swap MULTIPLE PCs or change archetypes:** you're now running "Underleaf with your own party." The world-canon (Bea, Vivian, the annex, the network, Companion) still works. But most per-PC DM notes ("hand the lead to the Caregiver here"; "the Control-seeker will try to seize this scene") will need remapping. See [`archetypes.md`](archetypes.md) for the archetype-to-role mapping the notes key on.

**If a role isn't represented at all** (say, no Control-seeker at your table): skip DM notes tagged for that role. The three-act shape survives; the specific scenes may need trimming.

**Portable-mode alternative:** if you want to run Underleaf with a purely generic party (all invented PCs, ignore the recommended set), a role-based portable-party guidance version of this file lives in this repo's history as prior versions of `example-party.md`. Recover it from git if that's your preference.

## PC-sheet schema notes

Each PC JSON follows the schema in [`example-character.json`](example-character.json), extended with:
- `focus` (name / domain / description; the object that anchors the PC's magic-adjacent moments)
- `bonds` (array of PC or NPC relationships)
- `age`, `archetype`, `temperament`, `bayAreaRelation`, `neighborhood` (chargen-question answers)
- `handle` (optional nickname)
- `dmNotes` (an object with magicPhase, castDomain, alignmentDriftWatch, focusNotes, and any character-specific DM guidance like `substrateSensitivity` for Priya or `personaDropCanon` for Dakota)

DM-only fields (in the `dmNotes` object) contain spoilers and behind-the-scenes character-arc guidance. Players who intend to actually play a character should ask the DM for a sanitized player-facing sheet, or skim the top-level fields only.

## Session state — starts at zero

Committed sheets show `harm: 0`, `stress: 0`, `marks: 0`, `advancements: 0`. Actual per-session play state (marks earned, harm/stress marked, advancements taken) is managed by the Quire runtime OR the DM's session notes OR the player's own tracking — not committed here. When importing a recommended PC into a Quire session, expect to layer session-state on top of the committed baseline.

## Why this exists

- The published Underleaf episodes reference PCs by name in a way that doesn't fully generalize to arbitrary parties. Rather than pretend otherwise, we ship the party the episodes are written for.
- New DMs can start playing with zero chargen overhead by using the recommended PCs.
- Adapting DMs get an editable starting point that's cleaner than a from-scratch chargen.
- The tight PC-to-story coupling is a deliberate design choice per Quire's principles (see the Quire authoring conventions repo). Underleaf leans into it.
