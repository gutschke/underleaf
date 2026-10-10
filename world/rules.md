# Rules reference (v0.1)

This is the ruleset that Quire's bundled play app supports out of the box. It is paper-friendly: every mechanic here can be tracked on a character sheet with pencil and dice. The runtime adds convenience (digital sheet, dice helper, magic-tier reasoning aid, audit log) but never gates play on a computer.

The framework is in principle ruleset-agnostic, but only this ruleset is wired into the v0.1 runtime. Other rulesets would require additional code in the play app.

## Design pillars

- **Story over mechanics.** A session with zero dice rolls is valid. The dice are for moments where outcome is genuinely uncertain and the surprise serves the story.
- **Players roll, DM narrates.** Only players roll dice. The DM applies consequences, not random rolls of their own.
- **No farming.** No XP grind, no mana pool, no spell-slot accounting. Progression is milestone-based and capped.
- **DM cognitive load minimized.** A simple core resolution carries most situations.

## Stats

Six stats, each rated **-2 to +3**:

- **STR** — lifting, brawling, physical labor.
- **DEX** — driving, fine motor, dodging, climbing.
- **CON** — endurance, illness resistance, drug or alcohol tolerance, sleep deprivation.
- **INT** — academics, problem-solving, languages, technical knowledge.
- **WIS** — willpower, intent integrity, perception, intuition. This is the stat that modifies uncertain magic rolls — not because magic is stat-gated, but because uncertain casts depend on how cleanly the caster can hold intent.
- **CHA** — talk, presence, lying, reading rooms.

**Fixed starting array (no point-buy):** one +2, three +1s, two 0s. Story-first play discourages min-maxing.

No 7th "Conviction" stat. Adding one would signal that magic is stat-gated, which it is not.

## Resolution

For any uncertain outcome, the player rolls **2d6 + stat**:

| Roll | Result |
|---|---|
| ≤ 6 | **Miss** — fail, or succeed at cost. |
| 7-9 | **Partial** — yes-but, yes-and-cost. |
| 10+ | **Hit** — clean success. |
| 12+ | **Exceptional** — success with bonus. |

Skill modifiers add to the total (see Skills, below). The DM does not roll for the world — they narrate outcomes.

### Wild outcomes

Double 1s and double 6s preserve the dice-as-storyteller role that d20's nat-1 and nat-20 play, at about half the frequency (~5.6% combined vs d20's ~10%).

- **Double 6s** — exceptional success regardless of the underlying math; **the player narrates** an unexpected positive fictional detail they had not asked for.
- **Double 1s** — the mechanical result resolves normally with modifier (so high-stat PCs don't whiff just because the dice did), **but the DM introduces** an unexpected fictional complication or twist independent of success or failure.

## Skills

**Categories** (small fixed list, +1 each when relevant):

- **Action** — physical violence, athletics, brute force.
- **Subterfuge** — stealth, lying, manipulation, theft.
- **Knowledge** — academic recall, research, analysis.
- **Insight** — perception, reading people, noticing patterns.
- **Influence** — persuasion, performance, leadership.
- **Tech** — computers, devices, networks, code.
- **Craft** — making, fixing, building.
- **Medic** — first aid, treatment, diagnostics.

**Tags** (open free-text, +1 each when fiction-relevant):

A tag is a specific bit of expertise the PC owns — "ICU nurse," "competition climber," "fluent in Mandarin," "raised by a beekeeper." 3-5 at character creation; more through advancement.

**Modifier cap:** +2 from skills (one category plus one tag, or two stacking tags). Plus stat modifier. A typical roll is 2d6 + stat + 0-2 from skills.

## Harm and Stress

Two parallel **4-box tracks** replace HP.

### Harm

| Box | Description |
|---|---|
| 1 | **Bruised** — winded, scuffed, minor cuts. No mechanical penalty. |
| 2 | **Wounded** — meaningful injury. -1 to physical rolls. |
| 3 | **Serious** — bleeding, broken, concussed. -1 to all rolls; needs medical attention soon. |
| 4 | **Critical** — out of action. Dying or unconscious. DM and player decide together what "out" means for this PC and situation. |

Healing is mostly fictional. Box 1 clears with rest. Box 2 needs days. Box 3 needs medical attention. Box 4 needs significant intervention; can be fatal without it.

### Stress

| Box | Description |
|---|---|
| 1 | **Tense** — wound up. No penalty. |
| 2 | **Shaken** — -1 to WIS-modified rolls (magic, perception, willpower). *(Was "Strained" until 2026-10-10; renamed so it can't be confused with the thread-debt ladder's Strained.)* |
| 3 | **Frayed** — -2 to WIS rolls; thread debt accumulates faster from any cast. |
| 4 | **Broken** — cannot cast at all. -1 to all rolls until reduced. |

**Triggers:** see the magic tier table below for casting-related triggers. Other stress sources include witnessing distressing events, holding intent against intense social pressure, and direct contact with the world's deeper mechanics.

**Recovery:** one box per full night's real sleep; one box per meaningful conversation, art, or human connection (DM judgment); never clears in-scene; drugs and alcohol suppress stress temporarily with their own consequences.

## Combat

Theater of the mind. No initiative tracker by default.

The DM goes around the table naturally; "what do you do?" rhythm. When stakes spike — an ambush, the opening moments of a fight — the DM may call for an Insight check; high rolls act first.

**Moves available to anyone:**

- **Attack** — Action vs target. Hit deals harm. Partial deals harm + you take harm too.
- **Defend** — DEX or Action against incoming harm. Hit avoids. Partial reduces.
- **Maneuver** — change position, create advantage. Hit gives an ally +1 to their next roll.
- **Aid** — help another's action directly. Hit gives +1.
- **Press** — force someone to reveal or give up something. Influence-based.
- **Withdraw** — disengage. Hit clean exits. Partial exits at cost.

Combat is rare and lethal. PCs are mostly civilians.

## Magic

> [!CAUTION]
> **THIS FILE IS NOT PLAYER-SAFE AND MUST NEVER BE HANDED OUT.** The sections
> below name **specific PCs' cast domains**, a PC's signature intent-phrase, a
> named substrate-sensitive NPC (hook A2), the DM's realization technique, and
> **The Quiet** — which locked invariant 1 forbids naming before Act III.
>
> **The player handout is [`player-handout-magic.md`](player-handout-magic.md).**
> That file is firewall-checked. Hand out that one.

For the world rationale (The Quiet, plausibility, foci as cognitive anchors), see the campaign's design docs. The framework's mechanical interface is:

### Pricing a cast — what the DM does at the table *(DM, 2026-10-10)*

Say the price **before** anything happens. Asking the price is always free and is never aiming.

1. **Is it this PC's kind of problem?** If not, **"No."** (see the last row below).
2. **How plausible is it?** That gives the tier. **The focus is already built in**: every PC carries theirs. Without it, the price is one step dearer.
3. **Add one step for each of:** aiming alone before their release (two others backing with their own reasons cancel this one) · no focus on them · the caster is Strained. **Hard is the cap** — stacking never turns a price into "No". Seized makes Hard the minimum.

Watched records, anchor sites and strain relief are part of the step-2 judgement, not extra steps. **Roll first, then mark stress:** stress from this cast never penalises this cast's roll. Then pay:

| Tier | Roll? | What happens | What it costs the caster |
|---|---|---|---|
| **Free** | No | It turns out to have been so. | Nothing. |
| **Cheap** | No | It works. | Their **body cost** (below). |
| **Costly** | 2d6 + WIS | **10+** works · **7–9** works only partly (default; or the DM picks: the body cost lasts until tomorrow, or someone remarks on it — a tally tick) · **≤6** nothing changes. | Body cost + **1 stress**, whatever the roll. |
| **Hard** | 2d6 + WIS − 1 | **10+** works · **7–9** partly · **≤6** nothing changes, and one everyday thing the caster didn't want turns out to be so (+ a tally tick). The focus cracking, fading or changing can be that thing. | Body cost + **2 stress**, whatever the roll. |
| **No** | — | Only for what magic can't do: off-domain, minds and persuasion, landing on a person, time travel. **Anything merely implausible is "Hard. You can try."** — a "No" must never tell the player *why* something is impossible. | — |

**Body cost** = how the cast feels in this PC's body: pins and needles, a hoarse voice, a headache, lost sleep or appetite, a sore neck. It's on each PC's slip. **It never changes a roll and never stops stress clearing** — a bad night from a body cost still clears a box. Backers pay nothing.

**Double dice on casts.** On a Hard roll, double 1s *is* the unwanted thing (not a second one). Double 6s on a Costly or Hard roll is a clean success — except where a rule says nothing comes back on any roll (an unreachable person). **They still roll, exactly like a famous person would** — skipping the roll would tell them which kind of Hard it was — and double 6s changes nothing there.

**Rolls are WIS only** — skills don't add. **No "check for show"**: a roll that can't fail teaches nothing. Where precision matters, the cast is the price and a normal Insight roll reads the result.

*(Changed 2026-10-10, DM: the body cost became the Cheap tier's price, matching what Ep 8 already did; the focus moved into the quoted price; Hard became a flat −1 with the standard bands (an expert pass found "12+ to work" on top of the −1 made a clean Hard cast 1 in 36 at WIS +1); "Prohibited" narrowed to "No" for what magic can't do; "WIS check for show" deleted. Earlier: Cheap = "minimal thread debt", Hard −1 to −2 with 10+ partial only.)*

**Thread debt** is a soft narrative meter — not a number. The DM tracks the caster's current state on a five-step ladder and **narrates the state in fiction** so the player can perceive where they stand without referring to a sheet:

| State | What the table sees |
|---|---|
| **Settled** | Nothing notable. Few edits around the caster, and they settle without friction. |
| **Noticed** | Small comments from NPCs about "lucky timing." The edits around the caster begin to show in what people notice. |
| **Watched** | Odd luck piles up around the caster and gets written down: a bank flag, a friend's question, a photo. Each record is another fixed point, so casts nearby cost more. |
| **Strained** | Friction. More and more often, the cheapest consistent outcome includes the cast not happening: an interruption, a witness, the caster's own reluctance. **It looks like resistance; nobody is resisting.** Casts in this state are harder than their tier alone suggests. |
| **Seized** | (Very rare; only after sustained overreach.) So much is fixed around the caster that not casting is almost always cheaper. They often can't, or won't. |

*Renamed 2026-10-09 (DM): "Pushing Back" became **Strained** and "Hunted" became **Seized**. The old names implied someone pushing and someone hunting. Nobody is: edits strain a block that has no past or future, and releasing that strain can look like the world noticing or resisting. The cheapest edit is sometimes the cast never happening.*

> **Strain runs both ways.** Where the block is already strained, a well-aimed cast can relieve it and cost less than its tier, even nothing. One cast, anywhere in the block, can make another easier. **All prices are heuristics**: nobody sees the whole block.

The DM advances and retreats the state aloud in fiction, never by number: *"You're starting to feel watched."* *"Things have eased; nobody's mentioned your luck in a while."* The Skeptic player needs to see the cost; the Wonder Chaser needs the state to feel like part of the world. The ladder serves both.

**How it moves — a private DM tally, never spoken** *(DM, 2026-10-10)*. One tick per Costly or Hard cast, and per backed cast, **for everyone in it** — but backing that doesn't change the price isn't backing, and ticks nobody. **While Frayed, Cheap casts tick too.** **Three ticks = one step up. A quiet session (no ticks) = one step down** (faster with deliberate withdrawal, letting the records around them go stale). **Strained makes every cast a step dearer; Seized makes Hard the minimum.** The players only ever hear the step, in the fiction.

*(Changed 2026-10-10: the first step was "Quiet", too close to The Quiet; it is **Settled**, as the player handout already said. Before the tally the ladder had no rate, so it never moved at the table and backing was effectively free.)*

**Foci** shift the plausibility tier of an in-domain cast down by one (Costly → Cheap, Hard → Costly; "No" stays "No"). **The DM quotes prices with the focus already included** (above); it only shows up when it's missing. Foci have a domain (emotion, systems/information, identity, motion, knowledge, etc.) and only apply within it. Foci can break, fade, corrupt, or transform when spent on Hard-tier casts.

**Casts outside a PC's own kind of problem do not work** *(ruled 2026-10-09; facts-ledger §18, §50)*. An off-domain cast is not merely missing the focus discount: there is no effect, like a spell a character doesn't have. The DM may bend this creatively in an extraordinary moment.

**Free / Cheap casting in rapid succession** triggers a stress check from the 3rd in a single scene (AI assist available). Roll 2d6 + WIS; miss marks a stress box. This is what limits cast-spamming organically.

The runtime AI prompt bar serves as the DM's adjudication aid: the player describes a desired effect, the AI proposes a tier and the narrative threads that would make the change consistent, and the DM accepts, modifies, or overrides in seconds. The AI is *not* required — DMs running paper-only games adjudicate themselves.

## Advancement

No XP. No leveling treadmill.

**At session end**, each player may mark up to one of:

- ☐ Resolved a hard moment by acting in line with alignment.
- ☐ Learned something true about The Quiet, the world, or another character.
- ☐ Took a meaningful risk for someone else.
- ☐ Acted against your own short-term interest because the story demanded it.
- ☐ Took on a complication or scar that will matter later.

**Every 5 marks**, the PC may take one advancement:

- +1 to a stat (max +3 per stat; max two stats at +3).
- A category mastery: a +1 category becomes +2.
- A new tag.
- A new focus (a personally-meaningful casting anchor).
- A relationship with an NPC who now appears when called for. *(The campaign keeps this promise: an NPC bought this way does not betray the PC. Their worst case is declining a specific ask — "let's pretend I didn't hear that" — never turning on them. No NPC solves the arc for the party either.)*
- Access to a resource: safe house, contact, equipment.

**Cap: 8 advancements per character.** Past that, growth is narrative.

## Alignment

Standard 9-grid: Lawful/Neutral/Chaotic crossed with Good/Neutral/Evil. Chosen at creation. Binding — characters act in accord with their alignment even when it is short-term costly.

**Drift tracker.** The DM privately notes actions that pulled the PC toward a different quadrant. Around 5 drift marks toward the same destination triggers a realignment conversation between DM and player. Realignment has story consequences: old vows feel wrong, old allies notice.

## Discovering magic (Underleaf-specific arc)

For the sample campaign, PCs *can* cast from session one but do not know it. The three-phase arc:

1. **Accidental** (sessions 1-3): players have no cast action on their sheets; the DM may silently grant Free or Cheap effects to strong intent, attributed in fiction to luck. Tracked in a DM-private out-of-session log.
2. **Realization** (per-PC, sessions 3-6, private): the DM shows the caster something the party missed. See "Realization mechanics" below for how this differs from a scripted table beat.
3. **Aiming costs a tier** (from realization onward): a cast the PC is deliberately *aiming* resolves **one plausibility tier worse** (Free → Cheap, Cheap → Costly, Costly → Hard; Hard stays Hard). Unaimed casts are unaffected.

   **Aiming = reaching for magic, rather than acting for its own sake** *(DM, 2026-10-10)*. Asking the price is never aiming. Acting on instinct for someone in trouble is not aiming: Mars stepping in with the pistol holstered, Priya grabbing someone who's choking. Drawing the pistol is. **Mars's step-in is instinctive by construction** (DM, 2026-10-10): even a step-in he chooses ahead of time is unaimed while the pistol stays holstered — the strength is in not needing it. When in doubt, it's aiming if the player is choosing to *use magic*.

The cost is framed in-fiction: *"Now that you know magic exists, you're trying. Trying breaks intent."* The end-condition is concrete and player-perceivable: the PC must experience **one quiet moment of release** — a calming conversation, an emotional acceptance, an unforced spontaneous cast they didn't aim for.

*(Changed 2026-08-30. This replaces a flat **-2** on intentional casts. A flat penalty made aiming feel merely unlucky; a tier bump makes it feel* expensive*, which is the same lesson in the currency the rest of the system already uses.)*

### Supported casts

**Count the reasons** *(ruled 2026-10-09; the player handout says it in plain words — "Trying on purpose costs a step more — unless two of the others back you…" — and every other document links here instead of restating it)*:

> **Aiming costs a tier — unless two of the others back you, each saying what *they* get out of it. Three reasons, not three voices. "Me too" isn't a reason.**

An aimed cast made with at least two other PCs present and backing it, each giving their own reason, is **not bumped**: it resolves at its natural tier. **Alone, aiming still costs a tier.**

**Definitions, because they will be tested:**

- **Present** = in the scene, able to see or hear what is happening, and able to
  act in it. **A phone call is not present. Another room is not present.** If a PC
  could not be given a roll in that moment, they are not present.
- **Backing it** = giving a reason and meaning it. **A PC may decline**, and
  declining is never a penalty to anyone. With four other PCs available, one
  refusal is survivable — this is deliberately not a veto, and **must never be
  played as one.** If it starts becoming a lever between players, drop the rule
  and go back to a flat tier bump; **no mechanic is worth that at this table.**
- **A reason, not an echo.** Each backer says what *their* PC gets out of this
  cast. If a backer only repeats the caster ("yeah, make it work"), the DM asks
  **once**: *"What do you get out of this?"* (about this cast only, never about
  the PC's wants in general), **then accepts whatever comes.** The DM never grades
  the reasons, never refuses a second answer, and never turns this into a puzzle
  with a right answer. Reasons may overlap; they only have to be each person's own.
- **Backers are PCs.** NPCs never count.
- **Dakota's reach is never backed**: his trigger is reaching alone (below).

**The cost, which is not a dice cost.** Casting together is cheap *and* the group
registers as a group: **a supported cast advances thread debt for every
participant, not just the caster.** That is the whole price.

*(Changed 2026-10-09. Earlier copies of this rule disagreed with each other: one
said "if three players give the same sentence, let it work", another that the
sentences "should not" agree. That let the number of backers, not their reasons,
decide, and it taught the opposite of the campaign's thesis. The DM ruled for
reasons; see `design/DM-ONLY/facts-ledger.md` §44.)*

> **This removes a penalty; it never grants a discount.** A supported cast is never *cheaper* than the same cast made without aiming, so it cannot stack with a focus into free Hard-tier effects and needs no cap.

**Moments of release are beats, not gates.** A PC who has not had theirs is not blocked from anything; release simply retires the aiming cost for that PC. Each PC gets there on their own schedule, and the DM does not steer.

Each PC realizes on their own schedule. The moment of release is itself the cue for the act break in Underleaf's three-act structure.

### Realization mechanics — party rationalization vs. per-PC private scenes

Early drafts assumed Phase-2 realization was a scripted TABLE beat: DM picks a player and a moment, names the pattern, everyone at the table watches the reveal land. Play established that this doesn't work when the party has settled into a *rationalization posture* — the collective response *"it was just luck / it was because [PC-X] did [Y] / weather is weird"* absorbs any single reveal and defers realization for everyone at once.

**When the party rationalizes, do NOT force examination at the table.** Instead:

- Construct a **per-PC private scene** the next session — a 5-10 minute one-on-one moment (over a coffee-shop table between other beats; on the phone during a drive; in the hallway after another scene) where the DM shows the caster something the party missed. Their outline-vision reads a face that shouldn't be legible. Their intuition lands on a fact that couldn't have been guessed.
- Realization lands PRIVATELY. The party doesn't have to agree with the caster's new theory; the caster's own recognition is what matters. Group ratification is a bonus, not a requirement.
- Party consensus about "what happened" and the individual caster's *knowledge of what they can do* are decoupled. Each PC realizes on their own schedule; the whole party never realizes at once.

The party's rationalization posture is not a failure mode — it's the cognitive-immune-system a rational adult population has against magic. Working with it is Underleaf's Phase-2 discipline.

### Signature intent-phrases

Some casters develop signature phrases that crystallize their intent under pressure — a syntactic shape they return to at the moment of casting. Example established Ep 3: Priya's *"I just want [X]"* pattern.

When a player produces the same syntactic shape under coherent pressure in later sessions, treat it as an intent-crystallization cue: the caster is reaching for the pattern that has worked before. This can trigger a Free grant of a matching-tier effect (DM judgment) even for a caster still in Phase-1 or under trying-too-hard tax, provided the fiction supports it. It's not a rules bypass — it's the player showing the DM which anchor the character has learned to use.

### Substrate-sensitive pings

Some non-casting people are body-level sensitive to nearby casting or substrate-crisis events. Established example: Reggie Okeke feels the pattern without casting (Ep 3 played record). **Casters can be too: Priya's sensing is part of her body/care domain** *(ruled 2026-10-09; facts-ledger §30, §50)*. Ep 4 running example: Vivian's syncope that morning correlates with Priya's threshold-release migraine.

**Mechanic:** DM narrates the ping in the sensitive person's body — a migraine, a nausea, a sudden vertigo, an unaccountable exhaustion. Fires ~1-2 times per act at most. **It tells her THAT something nearby was edited, never WHAT or WHO.** Her own casts and tiny (Free) edits don't register. Reggie: reactive only, never voiced (A2). **Priya: told plainly in Ep 8.**

**Priya may also cast it on purpose**, like a *detect magic* spell: an ordinary in-domain cast, priced as usual. It is primarily passive, though. If she felt no passive cue, an active scan usually finds nothing. That's not invalid, just often pointless. It still answers only THAT, never WHAT or WHO.

### Anchor-site tier discount

Cast tier is **contextual, not intrinsic**. The same effect can be Free at an anchor site and Hard elsewhere — because anchor-site permeability + witness-locality + focus-restoration bonuses drop the tier by one or two for the same fictional outcome. See [`../design/DM-ONLY/anchors-cards-ledgers.md`](../design/DM-ONLY/anchors-cards-ledgers.md) §Anchor sites + §Recent damage is cheap to undo. Consult that doc when a player attempts a casting the tier-table alone would price at Costly or higher.

### Focus restoration during in-domain casts

When a caster performs an in-domain cast during a scene in which their focus was damaged or destroyed, the substrate has a mild preference for restoring the focus as part of the cast. Cost is effectively zero on top of the primary effect. This is not a rules bypass — it falls out of the recent-damage-cheap-to-undo mechanic plus the substrate's preference for maintaining the caster's future casting capacity in-domain. See the Priya-canvas-satchel worked example in `anchors-cards-ledgers.md`.

### Domain-specific casting triggers

Not every domain fires the same way. Body/care, memory/identity, and systems/information domains cast from *strong intent under pressure* directly — an accidental fire, an outline-vision, a shoe-size intuition. **Posture/protection (Mars) fires when he physically steps between** someone and something coming at them. **Speech/reach (Dakota) fires when he reaches for one named person** — alone, their full name aloud. Document domain-specific triggers on individual PC files (see `characters/pcs/*.json` dmNotes.castDomain for the party's canonical triggers).

**Persuasion is never magic** *(ruled 2026-09-27, facts-ledger §50)*. Talking a person round is a CHA / Influence roll, for every PC. **Magic is what charm cannot explain.** Each PC owns a *kind of problem* the table can recognise: a body in trouble, and feeling nearby edits in her own body (Priya) · something erased or a record that's wrong (Mira) · a lock, machine, signal or system (Morgan) · something coming at someone (Mars) · a specific person you can't get hold of (Dakota). *(This retires the earlier "presence/posture domains need stance AND intent" trigger, which existed because two domains were indistinguishable from charisma.)*

**Unreachable people (Dakota's domain) are always quoted "Hard. You can try."** — never "No", because the quote itself would say which kind of unreachable they are. **His reach prices already include his aiming** (he always reaches alone, on purpose); after his release each is a step cheaper, except "Hard. You can try." Fixed 2 stress, unaffected by focus; the result is nothing on any roll, and a failure carries no fiction. Dead, gone, unwilling and never-was must be indistinguishable. Full ruling in facts-ledger §50.

This arc is specific to Underleaf and would not apply to a Quire campaign with different cosmology.
