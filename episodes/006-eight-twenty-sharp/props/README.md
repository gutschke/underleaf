# The Duck Has You — Ep 6 prop set

The dance in Scene 4 is run as a small board game. `make-dance-game.py` builds
the whole thing: a two-page rules sheet, then 92 cards across ten decks, ten to
a printed page, cut along the dashes.

**At the table you need the cards, a rubber duck, five blank slips and a pen.**
There is no board, and there are no meeples or dice — all three were cut after
playtesting, because the cards and the duck already carried the session.

## Build

    ./make-dance-game.py                       # cards print {{pc:N}} tokens
    ./make-dance-game.py --map ../../../../party-mapping.json --out dance-game.pdf

The map is `{"slots": {"1": {"pc": "Firstname"}, …}}`. **It is deliberately not
in this repository** — see the repo's PC-token convention. Needs Chrome or
Chromium on `PATH`.

## Four decks are in a fixed order and must never be shuffled

**ROSA** (four, in order) · **ROUND** (five stacks by name, numbered) · **ALAIA/WINNIE**
(one interleaved stack, 1–6: a story, then the return that answers it) ·
**GM ONLY** (three cards, held in hand, never in any deck).

Every card in those four prints its own position, so a mixed stack can always be
rebuilt. Everything else — the other eleven CALLER, DUCK, QUESTION, ADOPTED,
BONUS — shuffles freely.

## Why four players have five cards and one has four

The dance runs **four rounds**. Each player's ROUND stack is a small arc whose
**fifth card is a coda that does not get dealt** — that is correct and nothing
is missing. Three codas can stay in the box; slot 1's is his payoff, so hand it
over at the end of the dance rather than losing it.

**Slot 2's stack has four.** Her fifth card is the stumble — GM ONLY 1 of 3,
held all morning and played in silence in Scene 5, with no call, no shout and no
countdown. It was never a round card; **the machinery going quiet for her is the
beat.** That is also why the ROUND deck is 24 and not 25.
