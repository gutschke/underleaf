---
$schemaVersion: 0.1.0
name: The Gate Agent
summary: The PCs find Reggie Okeke. He denies everything — sincerely, likeably. Treated fairly, he becomes an ally and points them onward. A real fork.
location: SFO Terminal G, or Reggie off-shift in Berkeley.
presentNpcs:
  - Reggie Okeke (gate agent; canonical NPC)
expectedDuration: 15 minutes
mood: Friendly, then a little raw. A wall that is also a person.
rolls:
  - Influence/Insight as the conversation turns. No roll gates the denial; rolls shape the relationship.
---

# The Gate Agent

**Finding him first:** the PCs never got his name in Episode 1. The how-to (default + routes + safety net + the coworker who'll volunteer his name) is in [`../dm/legwork.md`](../dm/legwork.md) §"Finding Reggie." It can't dead-end — they always reach him.

The PCs track down **Reggie Okeke** (full sheet: [`../../../characters/npcs/reggie-okeke.json`](../../../characters/npcs/reggie-okeke.json)). Play this as a conversation, not an interrogation. See [`../dm/npcs.md`](../dm/npcs.md) for his Episode-2 handling.

## The played variant — coincidental SFO intercept + In-N-Out (recommended)

A real table (2026-08-15) played this as **two stages**, which produced a richer scene than the single-location default and is now the recommended shape.

**Setup:** the PCs came to SFO not specifically looking for Reggie but to trace the anti-static bag's chain-of-custody stamps (see [`01-reconvene.md`](01-reconvene.md) §"Bag chain-of-custody"). The frontal approaches at the ticketing counter go nowhere. Reggie is a **coincidence** the PCs run into, not a target they hunt.

**Stage A — SFO intercept (~4 min).** As {{pc:5}} and {{pc:4}} are giving up on the ticketing counter, part of the group spots Reggie walking through the back of the departure hall between boarding cycles. He clocks them. His face changes. He is visibly upset the moment he sees {{pc:4}} (who was holding the anti-static bag on the plane) and MORE upset when Yui's name comes up. He does not want to talk. But he also can't just walk past them:

> *"I— I have to get to G-12, they're pushing back in ten. I can't— " (a beat; he looks at {{pc:4}} in a way he can't explain to himself) "There's an In-N-Out in Daly City, off the freeway. Meet me at eleven. I'm off at ten-thirty. I'll be there. I need to think."*

He gives them the cross street and jogs toward his gate. This is not an evasion — he's genuinely between boardings AND rattled AND cannot say what's rattling him. The PCs get *nothing* here except the meeting time.

**Stage B — In-N-Out, Daly City, 11pm (~12 min).** The scene's real work. Reggie orders a **5×5** (a legacy off-menu build the chain no longer officially makes) and gets it because one of his roommates is the store's manager. He hasn't eaten since 7am. He's very tired.

The In-N-Out setting does load-bearing work the terminal doesn't:
- The financial texture is legible — multiple jobs, roommates, this is where his food comes from, one of his roommates is the manager. He is not condescending about it.
- His guard is down after a long shift. The friendly-wary opening never quite fires; he's too tired to perform.
- The 5×5 order is a natural "you get to know him" beat.
- If the PCs already have the footage (see next), they can show it to him at the table on a laptop or a phone — a physical, quiet reveal.

**Opener at the In-N-Out** (in place of the airline-questions opener):

> *"Alright. So. Tell me the whole thing. I told my roommate I might be late tonight. I've got until they close, which is one."*

## The single-location variant (unchanged)

If the PCs approach Reggie somewhere other than SFO (his home, at a bar someone tipped them off to), the terminal-intercept stage doesn't happen and the single-location denial + fork below runs cleanly. Use the older opener:

**Opener (how it starts):** Reggie clocks the airline questions immediately and goes friendly-wary:

> *"You're asking about a flight? You with the airline, or…?"*

## The wall

Reggie genuinely does not remember approving a passenger's bag being held at the counter — *his memory is anchored to a pre-edit shape in which the bag-hold never happened, and it never updated when the world's shape did.* He is friendly first: easygoing, calls them *boss*, would love to help. As the questions imply he failed at his job (approving a policy violation), he gets defensive — he prides himself on professionalism, and paperwork he's dimly aware of says the bag-hold happened even though he has no memory of it. He is not shifty. He is a sincere man carrying a mismatch he doesn't know is a mismatch — his mind attests one shape; the records attest another. See [`../../001-unattended-baggage/dm/the-cable.md`](../../001-unattended-baggage/dm/the-cable.md) §"record-vs-memory asymmetry" for why his memory stayed anchored to pre-edit rather than updating.

> *"Honestly, boss, I'd remember. We don't let bags sit. That's like the one thing. If I'd done that I'd have heard about it — there's cameras, there's a write-up, the whole thing." (a beat) "...There's no write-up."*

He's right that there's no write-up. That absence will nag the PCs. Let it.

## The fork (real, player-controlled)

- **Treated fairly — they trust his denial, don't accuse him, don't go over his head** → Reggie warms back up and becomes a **casual ally**. He's curious now too. He'll do them a small favor (see the door, below).
- **Escalated — they push, threaten a complaint, demand his supervisor** → Reggie closes. Polite, done, "you'll have to talk to the airline." The door shuts; they'll have to get the footage the hard way in Scene 4.

Make the kind path pay better. It is the campaign's whole thesis in miniature (kindness as the move), and it protects the quieter players from the table's pushier ones.

**Rolls (the fork is driven by approach, but the die colors it):** if a PC rolls **Influence** to win him over — Hit (10+): he warms fully and gives *both* doors below (the footage help *and* the referral). Partial (7–9): one of the two. Miss (≤6): friendly but gives nothing concrete this scene (they'll get the footage another way — [`../dm/legwork.md`](../dm/legwork.md)). **Insight** to read him — Hit: "he's not hiding anything; the hole is in him, not in his story." Escalation/threats override any roll: he closes.

## The door (if treated fairly)

Reggie gives them something — pick what fits:

- He'll quietly pull, or help them request, the gate-area footage from that night (sets up Scene 4's easy acquisition).
- The referral toward the Archivist, dropped offhand:
  > *"You know who you should talk to? Years back, after some other weird gate thing, this insurance lady came around asking about — what'd she call them — 'anomaly reports.' Little old lady, took notes on index cards. I thought she was nuts. Somebody'd have her name."*
- A small human detail that lands the cost: he's had an unaccountable sick-day since, an hour he can't place. He mentions it as a joke. (Do not let any PC connect it to a pattern yet — it's a seed, not a clue.)

## What not to do

- Do **not** let Reggie half-remember to reward investigation. Invariant: no NPC explains the gate edit. Reward investigation with the *referral* and the *relationship*, never with a leak.
- Do **not** make him eerily agreeable. He's warm because he's warm, not because he's been flattened. The flattening is not visible as a pattern yet.

## What this scene is doing

Opening the gate investigation; converting "a weird night" toward "people who were there don't remember it"; banking Reggie as a recurring ally; and handing the PCs the thread that leads to Bea. The denial is a wall; the relationship and the referral are the door.

## What Reggie says about Yui

If the conversation turns to the flight attendant, Reggie's guard drops a second time. He is very fond of Yui — she passes through his gate regularly on the SFO-TPE rotation, and they've developed the kind of coworker friendship where one buys the other coffee wordlessly. When the PCs mention that Yui almost got fired over the bag-hold incident, Reggie becomes visibly agitated:

> *"Almost got — she what? I didn't — she — corporate didn't say anything to me. They couldn't prove she — she wouldn't. She wouldn't do that. That's not who she is." (a beat) "…I didn't even know."*

This is the played variant's version of the flight-attendant beat — Reggie *carries* the human cost so the PCs feel it without Scene 3 having to fire independently. In the compressed 4-scene flow, Scene 3 may end up vestigial (see [`03-the-flight-attendant.md`](03-the-flight-attendant.md) §"Vestigial variant").

## Pacing

**Two-stage variant (recommended):** ~15 minutes total (~3 min SFO intercept + ~12 min In-N-Out). Compressible to 10 by tightening the In-N-Out conversation.

**Single-location variant:** ~15 minutes. If the table is cool toward Reggie or escalates fast, compress and let the footage be harder to get in Scene 4; the referral can also surface via Plant 2 in Scene 5.
