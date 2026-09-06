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
import argparse, html, json, pathlib, re, shutil, subprocess, sys, tempfile

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
    skills = [f'{s} {"<strong>+2</strong>" if lv.get(s, 1) >= 2 else "+1"}' for s in d.get("skills", [])]
    handle = (f' <span style="font-size:12pt;color:#666;font-weight:400;">'
              f'(&ldquo;{E(d["handle"])}&rdquo;)</span>') if d.get("handle") else ""
    player = E(SLOTS[str(slot)]["player"]) if SLOTS else f"{{{{pc:{slot}}}}}&rsquo;s player"
    pr = (d.get("pronouns") or "they/them").split("/")[0]
    poss = {"he": "His place", "she": "Her place"}.get(pr, "Their place")
    inv = d.get("inventory", {})
    marks, adv = d.get("marks", 0), d.get("advancements", 0)
    focus = d.get("focus", {})
    parts = [f'<article class="sheet" id="pc{slot}">', f"""  <header class="header">
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
    if d.get("backstory"):
        parts.append(f'  <section class="backstory"><h2>Backstory</h2>\n{paras(E(d["backstory"]))}</section>')
    if inv:
        carries = " &middot; ".join(md(E(c)) for c in inv.get("carries", []))
        parts.append(f'  <section><h2>Inventory</h2>\n'
                     f'    <p><strong>Vehicle:</strong> {md(E(inv.get("vehicle","")))}</p>\n'
                     f'    <p><strong>Carries:</strong> {carries}</p></section>')
    if d.get("bonds"):
        parts.append(f'  <section><h2>Bonds</h2>{bonds(d["bonds"])}</section>')
    # A write-in table goes LAST. If the sheet overflows, the spill page is then a
    # clean worksheet rather than a stub carrying two orphaned lines.
    if d.get("sheetWriteIn"):
        parts.append(write_in(d["sheetWriteIn"], d["name"]))
    dots = "●" * marks + "○" * max(0, 5 - marks)
    pending = " &mdash; <strong>advancement PENDING</strong>" if marks >= 5 else ""
    parts.append(f"""  <footer>
    <span>Marks: <strong>{marks} / 5</strong>{pending} ({adv} taken; cap 8) &middot; {dots}</span>
    <span>Slot {slot} &middot; {E(session)}</span>
  </footer>
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
out = f"""<!doctype html><html><head><meta charset="utf-8">
<title>Underleaf — character sheets</title>
<style>{CSS}</style></head><body>
<main>
{body}
</main>
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
                    "--no-pdf-header-footer", f"--print-to-pdf={args.pdf.resolve()}",
                    f"file://{args.out.resolve()}"], check=True, capture_output=True)
    print(f"Wrote {args.pdf} ({args.pdf.stat().st_size // 1024} KB)")
