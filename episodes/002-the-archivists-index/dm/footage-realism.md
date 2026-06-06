> [!CAUTION]
> **DM-ONLY — EPISODE SPOILERS**
>
> Reference doc for the footage scene's technical realism — so a player who knows video/security can't catch you flat. The Episode-2 analog to Ep1's `avionics-realism.md`. If you are or might become a player, close this file.

# Footage realism — answering the hacker

The footage scene rests on one claim: **the file is authentic and untampered, the impossible instant is hidden behind an ordinary occlusion, and a forensic exam comes back "real, occluded, inconclusive."** This doc lets you hold that against a player who actually knows CCTV/forensics. Mechanics and the cost-gradient are in [the-footage.md](the-footage.md); this is the "is that *plausible*?" backup.

## What an airport gate camera actually is

- **Low frame rate.** Retention-channel CCTV commonly records ~5–15 fps, sometimes lower on older/multiplexed NVRs. A "one-second" event is only a handful of frames; motion is already jumpy.
- **Heavy compression, long GOPs.** H.264/H.265, mostly P-frames (deltas) between sparse I-frames (full frames). Fast motion (a turning torso, a passing cart) produces macroblocking, smearing, and ghosting *as normal behavior* — not signs of tampering.
- **Auto-iris / WDR.** Gate areas have brutal dynamic range (window glare vs. jet-bridge shadow). The iris hunts; wide-dynamic-range processing blooms and washes out for fractions of a second when light shifts (a tug or catering truck moves outside). A glare bloom at the critical instant is textbook.
- **Multiplexing + clock drift.** Several cameras time-slice shared encoders/storage, producing uneven inter-frame timing and single-camera micro-stutters. DVR clocks drift; sub-second to multi-second offsets from "true" time are a known real-investigation headache.
- **Retention.** Footage from weeks prior may be near or past the retention window (often 30–90 days); pulling it at all may require it to still exist, and export re-encodes to a playable container (introducing *its own* artifacts).

## What a competent exam finds here

- **Integrity:** file structurally intact — monotonic frame index, normal GOP structure, consistent container metadata, **no missing frames, no re-encode signature on the original, hashes verify** against the export manifest. Nothing says "tampered."
- **The window:** an ordinary occlusion (torso / cart / glare bloom) covers the bag for ~1 second; bag visible before and after; the connector instant simply isn't in frame.
- **Professional conclusion:** *authentic, occluded, inconclusive.*

The key insight to internalize: a competent examiner does **not** expect a clean file to be artifact-*free* — real footage is full of compression smear, iris hunt, multiplex stutter, clock drift. A file with *none* of those would itself be suspicious (signs of laundering/re-encode). This footage is "clean" precisely because it carries the **normal quota of natural artifacts and no anomaly that points at editing.** The hacker can work it all night and find only the noise floor. The truth stays deniable in both directions — which is exactly the gate scene's ambiguity preserved.

## If the hacker pushes (Q&A)

- **"Can I prove it's authentic?"** — *Yes.* Hash integrity, intact frame index, no re-encode, chain of custody. Give them this as a real win (per [the-footage.md](the-footage.md)): "this is real, and I can prove it's real."
- **"Error Level Analysis will show the splice."** — ELA is for *recompressed still JPEGs* and is notoriously unreliable even there (false positives on textured/edge regions; not court-grade). On long-GOP H.264/H.265 video it tells you essentially nothing. A knowledgeable PC *knows* ELA is junk here; let them say so — it reinforces "there's nothing to find."
- **"Sensor-noise / PRNU fingerprint?"** — The PRNU matches the camera that's supposed to have shot it. Consistent with authentic. (If anything, it *confirms* the file came from that camera.)
- **"The occlusion is too convenient."** — Correct instinct, no proof. Cameras get blocked constantly; you can't distinguish "unlucky framing" from "suspiciously lucky framing" forensically. This is the right unease with no payoff — let it sit.
- **"Then someone deepfaked a *clean* file."** — Unfalsifiable and exactly the misread you want: the absence of manipulation reads, to a suspicious mind, as *sophisticated* manipulation. Never confirm; never deny. (Feeds the AI/conspiracy theory — see [the-cable.md](../../001-unattended-baggage/dm/the-cable.md).)

## Don't let forensics find tampering

A smoking gun (a dropout, a hash mismatch, an injected frame) would validate the conspiracy misread and point *away* from the truth. The file is real; there is nothing to find. The hacker's reward is the *vertigo* of a real recording of an impossible event — plus the genuine, keepable win of having proven its authenticity.

## Sources (for the DM who wants grounding)

- **SWGDE**, *Best Practices for Image Authentication* and *Best Practices for the Examination of Digital and Multimedia Evidence* — on what authentication can and can't establish, and chain of custody. (swgde.org)
- **NIST** digital/multimedia forensics materials — integrity hashing, examination workflow. (nist.gov)
- On **Error Level Analysis** being unreliable / false-positive-prone and unsuitable as proof — widely documented in the forensics community (originating critiques around Neal Krawetz's ELA demos); treat any "ELA proves it" claim as folk-forensics.
- **H.264/H.265 GOP structure** (I/P/B-frames) and CCTV frame-rate/WDR behavior — standard codec/surveillance references; the practical upshot is that motion artifacts and brief occlusions are the *norm*, not anomalies.
