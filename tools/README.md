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
