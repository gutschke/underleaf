> [!CAUTION]
> **DM-ONLY — EPISODE SPOILERS**
>
> Quick-reference for every named NPC in *Unattended Baggage*. If you are or might become a player, close this file now.

# NPCs — Unattended Baggage

Players ask for NPC names at the worst possible moments. This file exists so the DM has an answer.

**None of this is load-bearing.** Every detail below is optional. Use what's helpful; ignore what isn't. The entries exist so that when a player suddenly cares about the second-shift flight attendant or the bored passenger across the aisle, the DM can answer plausibly and move on.

If the PCs become attached to one of these NPCs, **promote them**. Copy the entry into `characters/npcs/<id>.json` (schema in [Quire](https://github.com/gutschke/quire/tree/main/schema/v0)) and flesh them out — they're now a recurring character.

## How to use this file

- **Skim once** before the session. Don't memorize.
- **Pick names** that fit the player table — if you've previously named an NPC "Andrei" and have an Andrei-the-real-person at your table, swap freely.
- **Don't rehearse the details.** Just have them available.

## NPCs by scene

### Cabin crew of Flight 887

**Captain Diane Reeves** — *she/her*, late 50s, pilot in command.
- *Looks like*: heard only, never seen by the PCs. Authoritative voice, light Tennessee underlay.
- *Sounds like*: the practiced "everything is fine" cadence of a senior airline captain. Calm performance even when announcements are tightening.
- *Wants*: to keep her passengers reassured and get the airframe to Taipei without incident.
- *Stats hint*: WIS +2, CHA +1, INT +1. Will not roll in this episode.
- *If recurring*: probably not in this campaign.

**First Officer Marcus Park** — *he/him*, early 40s, co-pilot.
- *Looks like*: heard only via the ACARS/voice channel {{pc:3}} intercepts.
- *Sounds like*: terser than the captain. Says "uh" before technical assessments.
- *Wants*: to do his job right; he's on his second airline after his first one folded.
- *If recurring*: unlikely.

**Yui Tanaka** — *she/her*, mid-30s, flight attendant on upper-deck galley duty.
- *Looks like*: half-Japanese, half-Filipino, born in Daly City. Hair in a tight bun. Tired around the eyes.
- *Sounds like*: efficient, professional, slight clipped quality when tired.
- *Wants tonight*: to finish this rotation without incident. Her toddler is at her mother's; she's been awake since 0400.
- *Disposition toward PCs*: friendly-distant, professional.
- *Stats hint*: CHA +1, WIS +1, otherwise average. No combat. Persuadable on mundane requests.
- *If recurring*: **Yes, in Episode 2's investigation.** Promoted to the canonical record at [`characters/npcs/yui-tanaka.json`](../../../characters/npcs/yui-tanaka.json). See that file for full background (wife Inez, daughter Mei, sourdough hobby, Millbrae home).

**Eli Schwartz** — *they/them*, late 20s, flight attendant on main-deck cabin.
- *Looks like*: tall, lean, Ashkenazi-American from Chicago. Plays in a community theater group on weekends.
- *Sounds like*: theater-kid energy under the customer-service voice.
- *Wants tonight*: not to mess up a sourdough trial they're going to do when they get home Wednesday.
- *Disposition*: friendly, slightly distracted.
- *If recurring*: minor.

**Priya Iyer** — *she/her*, mid-40s, flight attendant in and out of crew rest.
- *Looks like*: Tamil-American, born in San Jose, lives in San Bruno. Greying at the temples; doesn't dye.
- *Sounds like*: warm, the calmest voice in the cabin. The attendant passengers turn to in mild distress.
- *Wants*: her vacation, which is two weeks away.
- *If recurring*: minor.

### Gate area — SFO Terminal G (Scene 7 rewind)

**Reggie Okeke** — *he/him*, late 20s, gate agent for Flight 887.
- *Looks like*: Nigerian-American, grew up in Oakland, lives in Berkeley. Wears the airline polo over a longer black tee. Glasses.
- *Sounds like*: easygoing, soft Bay-Area cadence, calls regular passengers *boss* or *my friend*.
- *Wants tonight*: to clear the last of the boarding cycle and go home. His shift ends at midnight.
- *Disposition toward PCs*: friendly, no reason to remember anyone in particular.
- *Stats hint*: average across the board; CHA +1. Will not roll in Episode 1.
- *If recurring*: **Yes. Reggie is the load-bearing NPC for Episode 2's gate-agent investigation.** Promoted to the canonical record at [`characters/npcs/reggie-okeke.json`](../../../characters/npcs/reggie-okeke.json). See that file for full background (Berkeley roommates, bass-in-a-band, mother in Oakland, sister Ada the ATC at LGB).

**Andrei Sokolov** — *he/him*, late 50s, business-class passenger across the aisle from {{pc:1}}.
- *Looks like*: Russian-American businessman, San Francisco–Moscow regular for two decades. Salt-and-pepper hair, expensive but unfussy suit, reading glasses.
- *Sounds like*: low, faintly amused, English with the soft Russian shape.
- *Wants*: to be left alone tonight; he's tired and on his fourth long-haul this month.
- *Disposition*: observant, not actively hostile. Reads the cabin like a poker game.
- *Stats hint*: INT +2, WIS +1, CHA +1. Notices things others don't. Mechanically could be very useful if the PCs befriend him.
- *If recurring*: possible. He's the kind of NPC who'd remember faces and could re-appear in Episode 4-6 as a coincidence-thread node. Don't promise this; the texture is here.

### Scene 5 distraction NPCs

**Mariam Habibi** — *she/her*, early 30s, mother of the toddler.
- *Looks like*: Iranian-American, lives in San Mateo. Stretched thin and beautiful in the way that only exhausted parents look.
- *Sounds like*: warm but visibly losing patience with the world.
- *Wants*: her son to please go back to sleep.
- *If recurring*: no.

**Naseem Habibi** — toddler, age 2.
- *Wants*: milk and his stuffed lion.
- *Looks like*: cranky.

**Brett Halloran** — *he/him*, mid-40s, the "anxiety attack" passenger.
- *Looks like*: Irish-American, lives in Daly City, works in commercial real estate. Used to be athletic; less so now. Loud aloha shirt over the business-casual underneath.
- *Sounds like*: louder than he thinks, slightly slurred. Has had four whiskies.
- *Wants*: to feel important. Tonight his "anxiety attack" is really turbulence and bad decisions.
- *Disposition*: thinks the world owes him service. Cannot be reasoned with; can be managed.
- *If recurring*: definitely not.

### Background passengers

If a PC asks who's in the cabin generally, the answer is: a Tuesday-night SFO-Taipei mix.
- Business travelers (mostly Asian-American or Asian, tech and finance, in their 30s-50s).
- Some family travelers (younger and older together, lots of duty-free in the carry-ons).
- Occasional vacationers (couples, mostly).
- A few students returning home (younger, with school logos on hoodies).
- One or two senior travelers being shepherded by adult children.

Make up names on the fly if needed. Pull from your usual sources.

## Naming notes

If the PCs end up with strong feelings about an NPC not listed here — the second-shift attendant, the gate gate manager, an immigration officer — invent quickly and write it down in a session log. *That* NPC has become someone, even if you didn't plan it.

The framework principle: the worst-case is the DM stalling because they didn't have a name ready. The second-worst case is the name being inconsistent across sessions. This file solves the first; session logs solve the second.
