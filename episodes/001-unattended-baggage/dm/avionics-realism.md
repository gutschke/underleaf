> [!CAUTION]
> **DM-ONLY — EPISODE SPOILERS**
>
> 747 avionics realism notes. Useful for answering player questions; mostly not needed at the table. If you are or might become a player, close this file now.

# Avionics realism

## What's real

### The 747 E&E bay location

The Boeing 747 has its **Electrical and Electronics (E&E) bay** in the **forward lower fuselage, directly beneath the cockpit**. On a 747 the cockpit is on the upper deck (the famous "hump"), so the E&E bay is below the cockpit and accessible from various points depending on the variant. (Sources at the end.)

### Access points

The 747 has multiple paths to the E&E bay:

- **The forward wheel well bulkhead door** — exterior maintenance access, used by ground crews. Not relevant in flight.
- **A floor panel in the main-deck forward galley** — interior service access for the cockpit and forward crew. This is the path the PCs use.

The internal-access vulnerability has been written about publicly (see the Runway Girl article on the 777, similar mechanism on the 747). It is *not* unique to the 747; the 767 and 777 have similar arrangements. The user-facing point: the bay is reachable from inside the aircraft, by anyone who knows where to look and is willing to risk being caught.

### What's in the bay

A confined corridor lined with **Line-Replaceable Units (LRUs)** — black-anodized boxes mounted in standard racks, each providing a specific avionics function:

- **SAARU** — Secondary Attitude and Air Data Reference Unit.
- **FMC** — Flight Management Computers (typically two, L and R).
- **ADIRU** — Air Data Inertial Reference Unit.
- **IRS** — Inertial Reference Systems.
- **Various bus couplers, power distribution units, and communication boxes.**

The LRUs talk to each other over **ARINC 429** (an old, slow, robust digital serial bus) and increasingly **AFDX / ARINC 664** (Ethernet-based). For a 747-400 most of the buses are ARINC 429.

### ARINC 600 connectors

The **ARINC 600** is a real industry-standard connector used for LRU racking — large rectangular multi-pin connectors with a metal locking mechanism. They are designed for thousands of mating cycles, for vibration resistance, for environmental sealing. They are not consumer parts and they are not in any general parts catalog. A working aerospace mechanic can identify one on sight; a competent electronics hobbyist can recognize it as "obviously aerospace" but might not know the standard by name.

ARINC 600 connectors have **rotating locking rings** that secure the connector to the rack. The locking ring is a known wear part; cracked locking rings are a documented failure mode that produces exactly the intermittent-contact symptom described in the episode.

### Why the PCs can't fix it

Aircraft maintenance organizations stock spare ARINC 600 connectors in their hangars but not on the airframe itself. The bay carries some spare cables, fuses, and a few common LRUs (depending on the operator's policy); it does not carry connector spares. The fault would be addressable in three minutes by a ground engineer with the right parts bin. In flight, with no parts on board, it is not addressable at all.

### ACARS realism

**ACARS** (Aircraft Communications Addressing and Reporting System) is real. It carries short messages between the aircraft and ground stations — telemetry, weather requests, position reports, maintenance flags. Many of these messages are transmitted in the clear and can be received by a software-defined radio with the right decoder. The hobbyist community is small but real; ACARS decoding has been a hobbyist activity for at least twenty years.

What PC3 is doing in Scene 3 is **passive reception**, which is legal. No transmissions; no spoofing; no interference. The closest thing to a legal concern would be if PC3 broadcasted what they overheard — but they don't.

## What's artistic liberty

### The bay's accessibility from a passenger 747

The exterior bulkhead door is real. The interior floor-panel-access is real on cargo and some passenger variants. The specific scenario of a passenger plausibly opening the panel during a meal-service rotation and getting away with it for the time the PCs need is *plausible* but should not be played as easy. Most airlines have crew procedures that would make this hard. The PCs are getting away with it partly through luck and partly because they're good at improvising covers.

If a player is an aviation enthusiast and wants to argue the realism, the DM can acknowledge: *"You're right, this is unlikely. Run with it."* Don't try to win the argument; just acknowledge and move on.

### The connector appearing in PC1's bag

Not realistic. That's the point. This is the moment of magic, dressed up as logistics. The realistic detail (the connector is a genuine part with a manufacturing trail) makes the unrealistic detail (its sudden appearance in a sealed bag with no manufacturing trail) land harder.

If a PC inspects the connector after the flight, they will find:
- The part is genuine ARINC 600, correct revision for a 747-400's BUS COUPLER 2A.
- The packaging is generic anti-static, no manufacturer or distributor markings.
- There is no shipping label, no SKU, no part lot, no purchase receipt.
- If they look up the part number, they will find catalogue entries from aerospace distributors at $40-$120 USD; they would normally be ordered with a 1-4 week lead time.
- If they try to trace where *this specific* part came from, they will hit a wall.

## When players ask realism questions

- **"Could this actually happen?"** — "Mostly yes. A few details are nudged for story; I'm happy to talk about which after the session."
- **"Wouldn't they detect us in the bay?"** — "Maybe. The crew is busy; the bay is small; you got lucky."
- **"How do I know this connector is the right one?"** — "Your tech-comfortable PC recognizes the standard. They've seen one in a video, or worked with industrial cousins of it, or recognize the form factor."
- **"Why doesn't the flight crew just override the fault?"** — "They can route around individual bus errors, and that's what they're doing. The fault is below the threshold for emergency; it's at the threshold for 'we want it looked at on the ground before continuing.' That's why the diversion makes sense."

## Sources

- [Avionics bay — Wikipedia](https://en.wikipedia.org/wiki/Avionics_bay)
- [Avionics Bay Access and Pressurization — Airliners.net thread](https://www.airliners.net/forum/viewtopic.php?t=1469593)
- [Will industry address vulnerability beneath the carpet of the 777? — Runway Girl Network](https://runwaygirlnetwork.com/2014/07/will-industry-address-vulnerability-beneath-the-carpet-of-the-777/)
- [Inside a Boeing 747 freighter — Allplane](https://allplane.tv/blog/2020/4/28/inside-a-boeing-747-freighter)

The DM does not need to cite these at the table. They are here so that if a player who works in aerospace asks "where did you get this?", the DM can point them to the references and have the conversation between sessions.
