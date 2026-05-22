---
$schemaVersion: 0.1.0
name: The Hack
summary: {{pc:3}} (radio hobbyist) notices the plane's avionics health is degrading. They share with the table.
location: Upper-deck business class, ongoing.
presentNpcs:
  - cabin crew (background)
  - flight crew (heard, not seen — voice/ACARS only)
expectedDuration: 15 minutes
mood: Curiosity tipping into concern.
rolls:
  - Tech check, if you want a roll for the hack itself. Default success — {{pc:3}} is in their element.
---

# The Hack

{{pc:3}} has been doing what {{pc:3}} quietly does on long flights.

## What {{pc:3}} is actually doing

{{pc:3}} carries a small SDR (software-defined radio) — a USB-stick-sized receiver — and runs an open-source decoder on their laptop. It picks up:

- **ATC voice** on VHF (only when over land or within range of coastal stations; mostly silent over the open Pacific).
- **ACARS** — Aircraft Communications Addressing and Reporting System — short text messages between the aircraft and its airline's operations center. Engine telemetry, weather requests, position reports, maintenance flags.
- **ARINC/SATCOM background chatter** if the plane is transmitting on those bands.

This is **passive radio interception**. No transmissions. No criminality. It is a niche hobby — search "ACARS decoder" and you'll find a small enthusiastic community. {{pc:3}} has done it on a dozen previous flights for fun; tonight is no different.

Until it is.

## DM read-aloud

> *{{pc:3}}, you've been half-watching the ACARS stream for hours, mostly maintenance pings and position reports. Then, over the last twenty minutes, the pattern thickens. Routine telemetry is interrupted by what looks like a fault report. Then another. Then a confirmation that maintenance flags have escalated. The codes mean nothing to most people. To you, they're recognizable — `EICAS` warnings, the avionics-bus health channel reporting intermittent ARINC 429 errors, the kind of nuisance message that a cockpit crew normally clears with a button press.*
>
> *Except the message keeps coming back.*

## What {{pc:3}} finds

If the player engages, {{pc:3}} can piece together:

- Several **ARINC 429 bus error** messages — a digital communication bus widely used in commercial avionics. Intermittent errors usually mean a loose connector, a cracked cable, or a degraded shielded pair.
- A **maintenance ACARS message** to the airline's ops center asking for a diagnostic recommendation.
- **Pilot voice channel** (briefly audible if {{pc:3}} catches the right frequency window): the captain in a calm, professional tone discussing options. "We're showing intermittent on the secondary bus. No safety implication. Recommend continuing to TPE with the redundant path." The dispatcher answers. Discussion. "Yeah, okay, we'll plan for a precautionary stop in NRT."

## Bringing it to the table

{{pc:3}} has a choice: keep this to themselves, or share. Most PCs will share — the others' open curiosity in Scene 2 has already established the table as people who want to know things.

When {{pc:3}} shares, the other PCs ask what it means. {{pc:3}} explains in plain language: *the plane has a minor electrical fault, the crew has noticed, they're talking about an unscheduled stop in Tokyo to have it looked at.*

The PCs absorb this. Some are unconcerned (a delay is a delay). Some are already calculating connections.

## DM cues for the other PCs

- The non-tech PCs ask what ACARS even is. Let {{pc:3}} explain. This is a good moment to give the radio-hobbyist player some screen time and the other players a chance to ask in-character questions.
- One of the other PCs may push for more: *"Are we in danger?"* — {{pc:3}} should reassure. "Not the way you mean. It's like a check-engine light. They don't fly planes that are unsafe."
- The plain reading: *we'll have a long delay in Tokyo*. Move into Scene 4.

## What this scene is doing

Giving the radio-hobbyist PC their first plot moment. Establishing the technical fault in plain language. Setting up the stakes scene by making the delay concrete.

## Sample ACARS line for color

The DM can read this aloud if it helps the table picture the data:

> ```
> .H1 887 PHM2 1342Z FAULT EICAS BUS-A INTERMIT
> .OPS REQ DIAG RECOMMEND
> ```

The codes are flavor. {{pc:3}} reads them and *understands*; the others read them and ask.
