> [!CAUTION]
> **DM-ONLY — EPISODE SPOILERS**

# The footage — DM script

For Scene 4. The footage is **forensically pristine and corroborates the played-out gate scene.** It is NOT blank and NOT erased — blanking instrumented data is the most expensive thing the Quiet can do and the opposite of how it works (see [`../../001-unattended-baggage/dm/the-cable.md`](../../001-unattended-baggage/dm/the-cable.md) §"The anchors — and where the cost lands"). Read "security footage is clean" as *forensically clean — no tampering — not blank.*

## What the footage shows

The full window plays normally. The bag comes off {{pc:1}}'s shoulder; Yui is right there; Reggie is at his counter. Timecode continuous, hashes verify, chain of custody intact. The PCs are **vindicated** — they did not imagine it.

The one impossible instant — the connector's appearance inside the bag — is hidden behind an utterly ordinary occlusion. Pick one and stay consistent:

- Yui half-turns and her shoulder/torso fills the frame for ~1 second;
- a catering or service cart crosses the foreground;
- the auto-iris blooms against jet-bridge window glare and washes the frame.

Before the occlusion: bag on shoulder. After: bag on the counter. Nobody is seen doing anything, because — on camera — nobody did.

## Acquisition

- **Reggie-ally (recommended):** he quietly pulls or facilitates it. Acquisition = relationship payoff, one clean scene.
- **Light caper:** records request, friendly contact, social engineering. Let the tech/Subterfuge PCs win. Mundane friction is fine (retention windows, airline liability caginess — a passenger left a bag with an attendant, which the airline doesn't want documented); keep that friction *mundane*, never a cover-up.

Either way, **they get the file.** Don't stonewall the caper; the payload is the content.

## What a forensic examination finds (the hacker WILL do this)

Real gate CCTV has a rich *natural* anomaly floor — low frame rate (often 5–15 fps), long-GOP H.264/H.265 compression (smear/macroblocking on motion is normal), auto-iris/WDR hunting and bloom, multiplexed-encoder micro-stutter, DVR clock drift, retention limits. A competent examiner expects these.

Under examination they find:

- File structurally intact: monotonic frame index, normal GOP structure, consistent container metadata, **no missing frames, no re-encode signature on the original, hashes verify.** Nothing says "tampered."
- At the critical window: a perfectly ordinary occlusion (torso / cart / glare). The bag is visible before and after; the handoff is half-seen; the connector instant is simply not in frame.
- Professional conclusion: **"authentic, occluded, inconclusive."**

For a skilled hacker, *that is the anomaly:* a real recording of an impossible event with no manipulation → it happened **in the world, not in the file.** Let the hacker generate their own dread by exhausting the deniable explanations. You keep answering, truthfully, "the analysis is clean." Do not let forensics turn up tampering — a smoking gun would validate the conspiracy misread and point away from the truth.

**But pair the void with a real win (important — this is the table's best investigator).** Their signature skill must produce a *positive deliverable*, not only the elegant absence. The deliverable: they can **definitively establish authenticity** — intact frame index, verifying hashes, unbroken chain of custody, no re-encode signature. *"This is real, and I can prove it's real"* is a hard, found-by-skill accomplishment only they could land. Give it to them explicitly, as a win they keep, alongside the dread of what it implies. Without this, the hacker's whole session is "my one skill produced nothing" — which is precisely "investigation with no win" for the PC most equipped to investigate.

> Player option (don't volunteer): if they run error-level analysis, sensor-noise fingerprinting, etc., the noise floor is *normal* — which a suspicious mind can read either way ("too clean = laundered" vs. "clean = untouched"). The truth stays deniable in both directions. That is the design, not a bug.

## The cost-gradient (leave half-legible — and keep it a thread, not a rubric)

Put all three (or four) facts plainly on the table (memory gone / phone gapped / camera immaculate / [lock matched]). **Priority:** the scene's job is the *corroboration* and the *"backwards" unease*, NOT getting the cost-rule assembled. A table that never connects them has lost nothing. Do **not** state the rule. If a player assembles it (*"the harder it is to fake, the less it's touched — that's backwards"*), **treat a correct connection exactly like a wrong one** — *"could be, could not be"* — and bounce to action. Early assembly earns a *chill and a thread to pull in sessions 3–5*, never a confirmed answer. The cost-gradient is the *mechanism of magic* rendered legible; handing it over confirmed in session 2 spends the realization beat early.

## Footage-as-mirror is a deliberate dial

Showing the footage to Yui *before* her interview (she watches herself hold a bag she can't remember) is a strong, sad beat — but it's the densest concentration of realization-seed in the episode (the edited person confronting the instrumented record of her own edit, right as you're planting "the hole is in the edited, not the witness"). Use it for a table you're *content* to have theorizing hard between sessions; skip it for a table where you want sessions 3–5 to do that work. Make it a conscious choice, not an incidental scene-order accident.

## The phone gap

{{pc:1}}'s phone has a small gap in location/photo timeline for those minutes. Cheap to leave: personal device, weak anchor, gaps are its natural state (airplane mode, terminal GPS multipath, app backgrounding). It corroborates the missing-time without being suspicious in itself.

## The lock branch (player-initiated; mundane corroboration)

If the lock fired in Episode 1 and a PC digs the maintenance *paperwork*, they find a handwritten turnaround-sheet note that the forward E&E hatch was opened and re-secured that night with no discrepancy — corroborating that it came open, confirming nothing about how. Mundane, loose, dead-ending; a good *positive find* for the hacker. Full text and the reframe (do **not** use an ACARS/sensor "tamper log" — a mechanical lock can't produce one, and it would mis-file the lock as an expensive anchor) are in [the-lock-callback.md](the-lock-callback.md). Player-initiated only; never volunteered.

## Hold the ambiguity

Present the footage **flatly** — "here's the gate, here's the bag, here's where you can't quite see" — and let the PCs supply the meaning, same discipline as the gate scene. The pristine-corroboration tilts toward neither "it always happened" nor "it became true through play"; that's correct. Both readings survive.
