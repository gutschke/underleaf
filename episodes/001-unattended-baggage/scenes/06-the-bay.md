---
$schemaVersion: 0.1.0
name: The Bay
summary: PCs find the fault — a cracked ARINC connector — and discover they cannot fix it. Dead end.
location: 747 E&E (Electrical & Electronics) bay, beneath the cockpit.
presentNpcs:
  - none (PCs alone in the bay)
expectedDuration: 15 minutes
mood: Cold, focused, then deflated.
rolls:
  - Tech check (find the fault). Default success — the fault is observable.
  - Craft check (attempt the repair). Default success — they get it diagnosed.
  - No roll for resolving it: the part isn't available. Mechanical dead end.
---

# The Bay

One or two PCs descend the ladder. The other PCs hold the panel and the cover from above.

## Optional: a secured inner hatch

> **DM (optional — see [`../dm/the-lock.md`](../dm/the-lock.md)).** If you are running the combination-lock coincidence, the bottom of the ladder ends at a secured inner hatch with a small four-wheel combination lock (gym-locker hardware). Set its code equal to a number a PC has spoken aloud earlier (a luggage combo, a TSA-lock code) and don't say so. Wait — don't prompt. If a player tries that number, it opens first try; narrate it as nothing and continue into the read-aloud below. If they don't, it's picked or left open. Skip entirely if you're not seeding the coincidence.

## DM read-aloud (the bay)

> *Down the ladder: a corridor maybe seven feet high, four feet wide. Steel grating underfoot. The walls are racks of black-anodized boxes, each labeled with a code: SAARU, FMC-L, FMC-R, ADIRU, IRS-1. The labels mean nothing to most people; the racks themselves are the point. Each is held in place by quick-release clamps; each connects to the next through bundles of shielded cable in clipped conduits. Some of the cable bundles have ribbons of color-coded tape at the ends. Some are unlabeled. The bay is cold — about ten degrees Celsius — and the air smells faintly of ozone and the warm-plastic smell of a server room.*
>
> *Three of the LEDs are amber. Most are steady green. One — on the unit labeled `BUS COUPLER 2A` — is flickering.*

## Finding the fault

The tech-comfortable PC (the one who descended) examines the BUS COUPLER 2A. They follow the cable from it down to a connector at the next rack.

The connector is an **ARINC 600** — large, multi-pin, with a metal locking ring that rotates to clamp the cable in place. (See [`dm/avionics-realism.md`](../dm/avionics-realism.md) for the technical context.) The locking ring has **cracked**. The cable hangs in place by friction; whenever the airframe vibrates, the connector micro-shifts and the signal is lost for a few milliseconds.

The PC reseats it. The flickering amber LED goes green. They watch for thirty seconds. The plane shudders — turbulence, or just the airframe — and the LED flickers amber again.

The PC tries to tighten the ring. It will not catch. The pawl is broken; the threads beneath it are intact but cannot be locked.

Diagnosis: this needs a replacement connector. Reseating works for seconds, not for the next eight hours.

## The dead end

The PC scans the bay for a spare. There are spare cables in a small parts locker (real on many widebodies, though spotty in inventory). There are no spare connectors. ARINC 600s are not consumable; they're not stocked the way ethernet jacks are stocked. Outside of a maintenance hangar, finding one in flight is improbable. Outside of a maintenance hangar at 38,000 feet, it is essentially impossible.

The PCs cannot fix this. They climb back up the ladder.

## Returning to the cabin

> *You re-emerge into the galley. The attendant who was on duty has rotated; a new one is preparing for the next service round. The cover story holds. You return to your seats. {{pc:3}}, you check the laptop: the maintenance ACARS messages are continuing. The captain is still planning the Tokyo stop.*
>
> *You sit. The plane drones on. Three of you are looking at each other. The other two are looking out the window.*

End the scene here. Let the deflation hang for a beat.

## What this scene is doing

Demonstrating mundane realism. The fix is identifiable and small in the abstract; the part is mundane in the abstract; the situation is intractable for the PCs' specific circumstances. This makes the eventual resolution in Scene 7 land hard.

## DM note

Resist the temptation to make the bay more dramatic than it is. It is a small dim utility space, not a sci-fi engine room. The drama is in the cracked plastic locking ring of a sixty-dollar industrial connector, and the unbridgeable gap between "we know what's wrong" and "we can fix it."

The next scene is the load-bearing one of the entire episode. See [`dm/the-gate.md`](../dm/the-gate.md) before running [`07-the-gate.md`](07-the-gate.md).
