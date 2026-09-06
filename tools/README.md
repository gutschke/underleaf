# tools

`render-md-to-pdf.py` — renders the repo's markdown (run-guides, clock cards,
handouts) to print-ready PDF via Python-Markdown and headless Chrome.

    ./render-md-to-pdf.py IN.md OUT.pdf --theme guide|default|compact|card

`guide` is for run-guides, `card` for one-page clock cards. It renders
speaker-labelled dialogue boxes from `> **NAME:** *"line"*`.

**Resolve `{{pc:N}}` tokens before rendering** if you want real names on the
DM's copy; the tokens themselves render literally.

`build-pc-sheets.py` — renders the player character sheets from
`characters/pcs/*.json`. **The sheets are no longer a hand-maintained HTML
file**; everything on them comes from the sanitized public record, so they can be
rebuilt from scratch if a working directory is ever lost.

    ./build-pc-sheets.py --out sheets.html --pdf sheets.pdf \
        --session "Session 7 — The Fourth Birthday"

Add `--map <private.json>` to substitute real player names; without it the sheets
print `{{pc:N}}'s player`, per the repo's token convention. **The map is the only
part that cannot be public.** Slot order is `characters.pcs` in `campaign.json`,
skipping the example character.

**It refuses to build if DM guidance has drifted into a player-facing field.**
That is not hypothetical — the first run caught a bond carrying `DM note: …` that
would have printed on a sheet and been handed to that player. Put guidance in
`dmNotes`.

Two fields exist purely for the sheet and are safe to edit: `sheetMotif` (the
inline SVG in the header) and `sheetWriteIn` (a blank table the player fills in —
rendered last, so if the sheet overflows the spill page is a clean worksheet
rather than a stub).

## Guards — run these before every commit and before handing anything over

**These live here, in version control, deliberately.** They spent weeks in an
untracked scratch directory, which meant the things protecting the repo were the
things most likely to be lost — and one of them was quietly broken the whole time.

`check-no-player-names.sh` — the repo carries CHARACTER names freely and must
never carry PLAYER names. **It is case-insensitive, and that is load-bearing:**
until 2026-09-06 it was case-sensitive and passed a lowercase player name sitting
inside a filename reference, for weeks, while reporting "clean". Do not remove
the `-i`.

    UNDERLEAF_PARTY_MAP=~/path/party-mapping.json tools/check-no-player-names.sh .

`check-player-firewall.sh <file.pdf>…` — player-facing PDFs must not carry DM
vocabulary (cast, caster, magic, substrate, The Quiet, realization, dmNotes…).
No PC has `knowsTheyCanCast` set; the sheets say *focus* and *anchor*.

`check-episode-consistency.py <episode-dir>` — duplicate headings, dangling scene
cross-references, placeholders, conflicting numeric claims, deck-size
disagreements, references to cut components. **Partial edits are the commonest
defect in this repo**; a single find-and-replace that hits the first of two
identical headings has cost real work more than once. Skips generated
`continuity-through-*.md` snapshots, where repeated headings are the structure.

`resolve-pc-tokens.py IN.md OUT.md` — substitutes real names for `{{pc:N}}` for
the DM's own copy. **The map is private and never committed**; point at it with
`UNDERLEAF_PARTY_MAP`. `tokenize-pc-names.py` goes the other way, for sanitizing
a document before it is committed.

`build-dm-sheets.py` — extends the generated player sheets with `dmNotes`. Paths
come from the environment (`UNDERLEAF_BASE_SHEETS`, `UNDERLEAF_DM_HTML`,
`UNDERLEAF_DM_PDF`, `UNDERLEAF_PARTY_MAP`). **DM sections render in a single
column on purpose** — Chrome silently clips multicol content across a page break,
and the DM loses notes with nothing on the page to show it.
