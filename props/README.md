# Props

## Badges

`make-badges.py` builds four CR80 office badges (2.125 × 3.375in, portrait) —
two per PC, one live and one dead:

| | Badge | State |
|---|---|---|
| **slot 3** | County of San Mateo · Clerk II, Recorder's Office | current |
| | San Francisco State · Graduate Division | **EXPIRED** |
| **slot 1** | Meridian Logic Systems · federal facility credential | **VOID** |
| | Vo & Associates, Oakland · Investigator, Records | issued this month |
| **slot 2** | UCSF Health · Registered Nurse, Intensive Care | current |
| | California BRN · RN licence *(landscape card)* | active |
| | American Heart Association · ACLS Provider *(landscape card)* | current |
| | Samuel Merritt University · BSN clinical placement | **EXPIRED** |

Two card shapes are supported: `kind="id"` is the portrait badge with a photo,
`kind="card"` is a landscape credential card with no photo. **Keep each sheet's
rows uniform** — the set builder sorts portraits before landscape for that
reason, because a mixed row makes the duplex backs look wrong even when they
register correctly.

The Vo badge reuses the photo off the void one, because it was made in an
afternoon by somebody who had a scan already. Meridian Logic Systems is invented;
no real agency, seal or logo is reproduced anywhere, and every back carries
`PROP · NOT A GENUINE CREDENTIAL` in the small print.

    ./make-badges.py --set vega --out badges.pdf        # slots 1 and 3
    ./make-badges.py --set iyer --out badges-priya.pdf   # slot 2's nursing set

**Use `--set`.** Emitting everything on one sheet re-lays-out badges you have
already cut, which is how a good print run gets invalidated.

**Print duplex, flip on the LONG edge, at 100% scale.** Fronts are sheet 1,
backs are sheet 2 with the columns reversed so the pairs land together. The two
grids start at the identical height on both sheets — that is what the fixed
header block is for, so do not let the intro paragraphs change length.
**Everything on a back sits 0.30in inside the edge**, so a cut that wanders by
an eighth of an inch still gives you a badge that looks right.

## Portraits

`badge_photo.py` generates them. **No stock library and no real person** — a lit
head-and-shoulders built from primitives, then aged in layers until the features
stop resolving: optical softening, dye shift, splotching, abrasion, the crease
every lanyard clip leaves, then grain and a holder vignette. The point is that
nobody at the table can make out a face, which is what an ID photo looks like
after a few years anyway.

    ./badge_photo.py     # writes four samples to /tmp
