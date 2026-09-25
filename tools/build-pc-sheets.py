#!/usr/bin/env python3
"""Render the player character sheets from the PC JSON files.

**This exists so the sheets stop being a hand-maintained HTML file.** Everything
on a sheet now comes from `characters/pcs/*.json`, which is the sanitized public
record — so the generator can live in the public repo, and the sheets can be
rebuilt from scratch if the working directory is ever lost.

The ONE thing that is not public is the mapping from slot to the real player's
name. Pass it with `--map`; without it the sheets print `{{pc:N}}'s player`,
which is the repo's normal token convention.

    ./build-pc-sheets.py --out sheets.html
    ./build-pc-sheets.py --map ../../party-mapping.json --out sheets.html --pdf sheets.pdf

Slot order is the order of `characters.pcs` in campaign.json, skipping the
example character. The output is structurally compatible with the DM master-sheet
builder, which extends this HTML with a dmNotes block.
"""
import argparse, html, json, os, pathlib, re, shutil, subprocess, sys, tempfile

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent

ap = argparse.ArgumentParser()
ap.add_argument("--out", type=pathlib.Path, default=HERE / "pc-sheets.html")
ap.add_argument("--pdf", type=pathlib.Path, default=None,
                help="also render to PDF (needs Chrome/Chromium on PATH)")
ap.add_argument("--map", type=pathlib.Path, default=None,
                help="private slot->player-name JSON; omit to keep {{pc:N}} tokens")
ap.add_argument("--session", default=None,
                help='footer session label, e.g. "Session 7 — The Fourth Birthday"')
args = ap.parse_args()

SLOTS = json.loads(args.map.read_text())["slots"] if args.map else {}
CSS = (HERE / "pc-sheet.css").read_text()

# --- build-time firewall -----------------------------------------------------
# Player-facing fields are printed and handed to a player. DM guidance that has
# drifted into one of them will otherwise be discovered at the table. This has
# already happened once (a bond carrying "DM note: ..." printed on slot 4's
# sheet, caught 2026-09-06 the first time these were generated).
DM_MARKERS = re.compile(r"DM note|DM-note|\(DM\b|do not tell|never tell the player"
                        r"|the player must not|NOT PLAYER", re.I)
PLAYER_FIELDS = ("name", "handle", "pronouns", "age", "alignment", "archetype",
                 "temperament", "bayAreaRelation", "specificPlace", "skills", "tags",
                 "focus", "intentionUnderPressure", "backstory", "inventory", "bonds")


def firewall(d, slug):
    bad = []
    for k in PLAYER_FIELDS:
        v = d.get(k)
        blobs = ([v] if isinstance(v, str)
                 else [json.dumps(v, ensure_ascii=False)] if isinstance(v, dict)
                 else [x if isinstance(x, str) else json.dumps(x, ensure_ascii=False)
                       for x in v] if isinstance(v, list) else [])
        for b in blobs:
            m = DM_MARKERS.search(b)
            if m:
                bad.append(f"  {slug}.{k}: …{b[max(0, m.start()-60):m.start()+100]}…")
    return bad


campaign = json.loads((REPO / "campaign.json").read_text())
slugs = [s for s in campaign["characters"]["pcs"] if s != "example-character"]

E = lambda t: html.escape(str(t))


def paras(text):
    return "\n".join(f"<p>{md(p.strip())}</p>" for p in re.split(r"\n\s*\n", text.strip()) if p.strip())


def md(t):
    """The JSON carries light markdown; the sheets have always rendered it."""
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", t)
    return t


def stat_row(stats):
    top = max(stats.values())
    out = []
    for k in ("str", "dex", "con", "int", "wis", "cha"):
        v = stats.get(k, 0)
        cls = "stat emphasis" if v == top and v > 0 else "stat"
        out.append(f'<div class="{cls}"><div class="label">{k.upper()}</div>'
                   f'<div class="value">{"+" if v > 0 else ""}{v}</div></div>')
    return f'<div class="stat-row">{"".join(out)}</div>'


def track(label, filled, total=4):
    boxes = "".join(f'<span class="box{" filled" if i < filled else ""}"></span>' for i in range(total))
    mark = f' <span class="label">[{filled} marked]</span>' if filled else ""
    return f'<div class="track"><span class="label">{label}</span>{mark}<span class="boxes">{boxes}</span></div>'


def chips(items):
    return '<div class="chips">' + "".join(f'<span class="chip">{md(E(i))}</span>' for i in items) + "</div>"


def bonds(bs):
    out = []
    for b in bs:
        if isinstance(b, dict):
            n, t, d = b.get("name", ""), b.get("type", ""), b.get("description", "")
            t = f' <em>({E(t)})</em>' if t else ""
            out.append(f"<li><strong>{E(n)}</strong>{t} &mdash; {md(E(d))}</li>")
        else:
            out.append(f"<li>{md(b)}</li>")
    return "<ul>" + "".join(out) + "</ul>"


def write_in(w, pc_name):
    cols = "".join(
        f'<th style="text-align:left;border-bottom:1px solid #a89e83;padding:2px 4px'
        f'{";width:" + wd if wd else ""}">{c}</th>' for c, wd in w["columns"])
    cell = '<td style="border-bottom:1px solid #ddd6c2;height:17px"></td>'
    rows = "".join("<tr>" + cell * len(w["columns"]) + "</tr>" for _ in range(w["rows"]))
    intro = w["intro"].replace("NAME", E(pc_name.split()[0]))
    return f"""  <section>
    <h2>{E(w['title'])}</h2>
    <p style="margin-bottom:5px;font-size:9pt">{intro}</p>
    <table style="width:100%;border-collapse:collapse;font-size:9pt">
      <tr>{cols}</tr>{rows}
    </table>
    <p style="font-size:8.5pt;color:#6b6b6b;margin-top:5px">{w['footnote']}</p>
  </section>
"""


def sheet(d, slot, session):
    lv = d.get("skillLevels", {})
    # Markdown, not HTML: chips() escapes its input and then renders **bold**.
    # Raw <strong> here printed literally on the sheets through Eps 6-7 prep.
    skills = [f'{s} {"**+2**" if lv.get(s, 1) >= 2 else "+1"}' for s in d.get("skills", [])]
    handle = (f' <span style="font-size:12pt;color:#666;font-weight:400;">'
              f'(&ldquo;{E(d["handle"])}&rdquo;)</span>') if d.get("handle") else ""
    player = E(SLOTS[str(slot)]["player"]) if SLOTS else f"{{{{pc:{slot}}}}}&rsquo;s player"
    pr = (d.get("pronouns") or "they/them").split("/")[0]
    poss = {"he": "His place", "she": "Her place"}.get(pr, "Their place")
    inv = d.get("inventory", {})
    marks, adv = d.get("marks", 0), d.get("advancements", 0)
    focus = d.get("focus", {})
    first = E(d['name'].split()[0].lower())
    parts = [f'<article class="sheet pc-{first}" id="pc{slot}">', '<div class="page front">', f"""  <header class="header">
    <div>
      <h1 class="pc-name">{E(d['name'])}{handle}</h1>
      <div class="player-line">Player: <strong>{player}</strong> &middot; {E(d.get('pronouns',''))}
        &middot; {E(d.get('age',''))} &middot; {E(d.get('alignment','').replace('-',' ').title())}</div>
    </div>
    <div class="quick-facts">
      <div><span class="label">Archetype:</span> {E(d.get('archetype','')).title()}</div>
      <div><span class="label">Under pressure:</span> {E(d.get('temperament',''))}</div>
      <div><span class="label">Bay Area:</span> {E(d.get('bayAreaRelation',''))}</div>
      <div><span class="label">{poss}:</span> {md(E(d.get('specificPlace','')))}</div>
    </div>
    <div class="motif" aria-hidden="true">{d.get('sheetMotif','')}</div>
  </header>""",
      stat_row(d.get("stats", {})),
      f'<div class="tracks">{track("Harm", d.get("harm",0))}{track("Stress", d.get("stress",0))}</div>',
      f'  <div class="two-col">\n    <section><h2>Skills</h2>{chips(skills)}</section>\n'
      f'    <section><h2>Tags</h2>{chips(d.get("tags",[]))}</section>\n  </div>']
    if focus:
        parts.append(f"""  <section><h2>Focus</h2>
    <div class="focus-box"><span class="focus-name">{E(focus.get('name',''))}</span>
      &middot; <span class="focus-domain">domain: {E(focus.get('domain',''))}</span><br>
      {md(E(focus.get('description','')))}
    </div></section>""")
    if d.get("intentionUnderPressure"):
        parts.append(f'  <section><h2>Intention under pressure</h2>\n'
                     f'    <div class="intention">{paras(E(d["intentionUnderPressure"]))}</div></section>')
    # Bonds (including the people they can call) and inventory are table-use, so
    # they sit on the front with the stats.
    if inv:
        carries = " &middot; ".join(md(E(c)) for c in inv.get("carries", []))
        parts.append(f'  <section><h2>Inventory</h2>\n'
                     f'    <p><strong>Vehicle:</strong> {md(E(inv.get("vehicle","")))}</p>\n'
                     f'    <p><strong>Carries:</strong> {carries}</p></section>')
    if d.get("bonds"):
        parts.append(f'  <section><h2>Bonds</h2>{bonds(d["bonds"])}</section>')
    # FRONT ends here: everything the player uses at the table. Duplex puts the
    # story on the back of the same sheet, so each player holds exactly one sheet.
    parts.append(f'  <footer><span>{E(d["name"])} &middot; Slot {slot} &middot; {E(session)}</span>'
                 f'<span>story &amp; notes overleaf &rsaquo;</span></footer>\n</div>')
    parts.append(f'<div class="page back">\n  <header class="back-header"><span class="pc-name-sm">{E(d["name"])}</span>'
                 f'<span class="back-label">story &middot; notes</span></header>')
    if d.get("backstory"):
        parts.append(f'  <section class="backstory"><h2>Backstory</h2>\n{paras(E(d["backstory"]))}</section>')
    # A write-in table goes LAST. If the sheet overflows, the spill page is then a
    # clean worksheet rather than a stub carrying two orphaned lines.
    if d.get("sheetWriteIn"):
        parts.append(write_in(d["sheetWriteIn"], d["name"]))
    # Ruled notes fill whatever the back has left, so every back page ends level.
    parts.append('  <section class="notes"><h2>Notes</h2><div class="ruled"></div></section>')
    dots = "●" * marks + "○" * max(0, 5 - marks)
    pending = " &mdash; <strong>advancement PENDING</strong>" if marks >= 5 else ""
    parts.append(f"""  <footer>
    <span>Marks: <strong>{marks} / 5</strong>{pending} ({adv} taken; cap 8) &middot; {dots}</span>
    <span>Slot {slot} &middot; {E(session)}</span>
  </footer>
</div>
<!--DM-NOTES-->
</article>""")
    return "\n".join(parts)


session = args.session or "Underleaf"
pcs = [(i, s, json.loads((REPO / "characters" / "pcs" / f"{s}.json").read_text()))
       for i, s in enumerate(slugs, 1)]
leaks = [line for _, s, d in pcs for line in firewall(d, s)]
if leaks:
    sys.exit("REFUSING TO BUILD — DM guidance found in player-facing fields:\n"
             + "\n".join(leaks)
             + "\n\nMove it into dmNotes. These sheets get handed to players.")

body = "\n\n".join(sheet(d, i, session) for i, _, d in pcs)
# Each character is exactly two fixed-height pages. Fixed height is what lets the
# notes fill the back and keeps duplex aligned; its danger is that Chrome CLIPS
# overflow silently. So the page measures itself before printing and stamps a
# visible marker on any page that overflows, and this script refuses the PDF if
# the marker appears. UNDERLEAF_SHEET_PAGE_HEIGHT exists to prove the refusal.
PAGE_H = os.environ.get("UNDERLEAF_SHEET_PAGE_HEIGHT", "11.7in")   # 10in printable / zoom 0.85
PAGE_CSS = f"""
/* Page geometry applies in EVERY medium, not just print: the overflow probe runs
   on load under screen styles, and it can only measure what print will do if the
   two agree. Width = 7.5in printable / zoom 0.85. */
body {{ zoom: 0.85; background: white; }}
main {{ max-width: none; padding: 0; margin: 0; }}
.sheet {{ border: none; box-shadow: none; padding: 0; margin: 0; width: 8.82in; }}
.page {{ height: {PAGE_H}; width: 8.82in; display: flex; flex-direction: column; overflow: hidden;
        break-after: page; page-break-after: always; }}
@media print {{
  body {{ zoom: 0.85 !important; }}
  .sheet {{ page-break-after: auto !important; break-after: auto !important; }}
  .sheet:last-of-type .page.back {{ break-after: auto; page-break-after: auto; }}
}}
.page.back .back-header {{ display: flex; justify-content: space-between; align-items: baseline;
  border-bottom: 2px solid var(--accent, #1a1a1a); padding-bottom: 4px; margin-bottom: 10px; }}
.pc-name-sm {{ font-family: "Optima", "Trebuchet MS", sans-serif; font-weight: 600; font-size: 15pt; }}
.back-label {{ font-size: 9pt; letter-spacing: .12em; text-transform: uppercase; color: var(--accent, #666); }}
.page .notes {{ flex: 1; display: flex; flex-direction: column; min-height: 0.9in; margin-top: 6px; }}
.page .notes .ruled {{ flex: 1; background-image: repeating-linear-gradient(to bottom, transparent 0, transparent 26px, #d8d1bf 26px, #d8d1bf 27px); }}
.page.front footer, .page.back footer {{ margin-top: auto; }}
.overflow-flag {{ background: #c00; color: #fff; font: bold 14pt sans-serif; padding: 6px; }}
"""
PROBE = """<script>
window.addEventListener('load', () => {
  document.querySelectorAll('.page').forEach(p => {
    if (p.scrollHeight > p.clientHeight + 2) {
      const f = document.createElement('div'); f.className = 'overflow-flag';
      f.textContent = 'SHEET OVERFLOW: ' + p.closest('.sheet').id + ' ' + (p.classList.contains('front') ? 'front' : 'back');
      p.prepend(f);
    }
  });
});
</script>"""
out = f"""<!doctype html><html><head><meta charset="utf-8">
<title>Underleaf — character sheets</title>
<style>{CSS}{PAGE_CSS}</style></head><body>
<main>
{body}
</main>
{PROBE}
</body></html>
"""
args.out.write_text(out)
print(f"Wrote {args.out} — {len(slugs)} sheets")

if args.pdf:
    chrome = next((c for c in ("google-chrome", "chromium", "chromium-browser",
                               "google-chrome-stable") if shutil.which(c)), None)
    if chrome is None:
        sys.exit("no Chrome/Chromium on PATH")
    subprocess.run([chrome, "--headless", "--disable-gpu", "--no-sandbox",
                    "--virtual-time-budget=3000",
                    "--no-pdf-header-footer", f"--print-to-pdf={args.pdf.resolve()}",
                    f"file://{args.out.resolve()}"], check=True, capture_output=True)
    text = subprocess.run(["pdftotext", str(args.pdf), "-"], capture_output=True, text=True).stdout
    over = sorted(set(re.findall(r"SHEET OVERFLOW: \S+ \S+", text)))
    if over:
        sys.exit("REFUSING: content does not fit its page and Chrome would clip it:\n  "
                 + "\n  ".join(over) + "\nShorten the field, or move a section to the back.")
    print(f"Wrote {args.pdf} ({args.pdf.stat().st_size // 1024} KB)")
