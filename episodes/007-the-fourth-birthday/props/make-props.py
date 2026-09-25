#!/usr/bin/env python3
"""Build the Ep 7 props sheet: private slips, the cake card, three contact cards.

Print SINGLE-SIDED and cut apart. Everything here is player-facing; run
tools/check-player-firewall.sh on the output before printing.

    ./make-props.py --out ep7-props.pdf                      # {{pc:N}} tokens
    ./make-props.py --map party-mapping.json --out ep7-props.pdf

The intermediate HTML is written next to the PDF (never to the system /tmp).
"""
import argparse, html, json, pathlib, shutil, subprocess, sys

ap = argparse.ArgumentParser(description="Build the Ep 7 props sheet.")
ap.add_argument("--map", type=pathlib.Path, default=None,
                help="private slot->PC map; without it the sheet prints {{pc:N}}")
ap.add_argument("--out", type=pathlib.Path, required=True)
args = ap.parse_args()

if args.map:
    SLOTS = json.loads(args.map.read_text())["slots"]
    PC = {i: SLOTS[str(i)]["pc"] for i in range(1, 6)}
else:
    PC = {i: "{{pc:%d}}" % i for i in range(1, 6)}

E = html.escape

# (recipient slot, when, text). Handed over in silence at the moment named.
SLIPS = [
    (5, "At the piñata",
     "You haven't said a word to them. You're just holding a rope. They keep coming back anyway."),
    (3, "At the photo board",
     "A dull headache starts behind your eyes."),
    (2, "After cake",
     "Mei is making no sound. Her hands are at her throat. Nobody else has noticed."),
    (2, "Afterwards",
     "It was out before your hands had finished moving. You are sure what you saw."),
    (2, "Afterwards &mdash; <i>only if someone else got there first</i>",
     "You were already moving."),
    (2, "Later, with Yui",
     "The pain stepped down. You weren't doing anything. You were listening to Yui."),
    (2, "Later, with Yui &mdash; <i>only if you said &ldquo;I just want&rdquo;</i>",
     "It stopped when you said it. You didn't push."),
]

# (owner slot, name, what they are, good for, a line of theirs)
CONTACTS = [
    (4, "Detective Camila Ortiz", "SFPD Missing Persons",
     "police procedure &middot; records &middot; what the law actually says &middot; knowing who to ask",
     "Any chance you can stop by my office? Some paperwork I want to walk you through in person."),
    (2, "Alaia Vega", "State park ranger, Bodie; works emergencies at the other end of the state",
     "emergencies &middot; the outdoors &middot; staying calm and getting somewhere fast",
     "Sometime soon, at your convenience. I owe you a coffee."),
    (1, "Trina Vo", "Corporate investigations, Oakland",
     "finding people and companies in databases &mdash; the legitimate ones, and the others",
     "That's a two-hour pull. What do you actually need out of it?"),
]

def slip(slot, when, text):
    return (f'<div class="slip"><div class="to">For {E(PC[slot])}</div>'
            f'<div class="when">{when}</div><div class="txt">{E(text)}</div>'
            f'<div class="foot">Read it. Keep it to yourself.</div></div>')

def contact(slot, name, what, good, line):
    return (f'<div class="contact"><div class="owner">{E(PC[slot])}&rsquo;s contact</div>'
            f'<div class="name">{E(name)}</div><div class="what">{what}</div>'
            f'<div class="good"><b>Good for:</b> {good}</div>'
            f'<div class="line">&ldquo;{E(line)}&rdquo;</div>'
            f'<div class="call">Say <b>&ldquo;I call {E(name.split()[-1] if name.startswith("Detective") else name.split()[0])}&rdquo;</b> any time. They pick up.</div></div>')

CSS = """
@page { size: letter; margin: 0.45in; }
body { font-family: Georgia, serif; color: #1a1a1a; margin: 0; }
h1 { font-size: 11pt; margin: 0 0 6pt; font-weight: normal; color: #555; }
.grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0; }
.slip, .contact { border: 1.2px dashed #888; padding: 12pt 14pt; min-height: 1.55in;
  break-inside: avoid; box-sizing: border-box; }
.to { font: bold 9pt Helvetica, Arial, sans-serif; letter-spacing: .08em; text-transform: uppercase; }
.when { font: italic 9pt Georgia, serif; color: #666; margin: 2pt 0 8pt; }
.txt { font-size: 15pt; line-height: 1.3; }
.foot { font: 7.5pt Helvetica, Arial, sans-serif; color: #888; margin-top: 10pt; }
.page2 { break-before: page; }
.cake { border: 1.2px dashed #888; height: 3.6in; display: flex; flex-direction: column;
  align-items: center; justify-content: center; background: #fff7fb; margin-bottom: 0.2in; }
.cake .top { font: bold 46pt "Comic Sans MS", "Chalkboard SE", cursive; color: #2a6fdb;
  text-align: center; line-height: 1.1; }
.cake .under { font: 9pt Helvetica, Arial, sans-serif; color: #999; margin-top: 16pt; }
.owner { font: bold 8.5pt Helvetica, Arial, sans-serif; letter-spacing: .08em; text-transform: uppercase; color: #666; }
.name { font-size: 17pt; font-weight: bold; margin-top: 4pt; }
.what { font-style: italic; font-size: 10pt; margin-bottom: 6pt; }
.good { font-size: 10pt; margin-bottom: 6pt; }
.line { font-size: 11pt; font-style: italic; margin-bottom: 8pt; }
.call { font: 10pt Helvetica, Arial, sans-serif; border-top: 1px solid #ccc; padding-top: 5pt; }
"""

body = ['<h1>Ep 7 &middot; private slips &mdash; cut along the dashes &middot; hand each over in silence</h1>',
        '<div class="grid">'] + [slip(*s) for s in SLIPS] + ['</div>']
body += ['<div class="page2"><h1>Ep 7 &middot; the cake &mdash; put it in front of '
         f'{E(PC[1])} with a marker</h1>',
         '<div class="cake"><div class="top">HAPPY 3rd<br>BIRTHDAY MEI</div>'
         '</div>',
         '<h1>Contact cards &mdash; one to each owner, and post them in the group chat</h1>',
         '<div class="grid">'] + [contact(*c) for c in CONTACTS] + ['</div></div>']

HTML = f"<!doctype html><html><head><meta charset='utf-8'><title>Ep 7 props</title><style>{CSS}</style></head><body>{''.join(body)}</body></html>"

out_pdf = args.out.resolve()
out_html = out_pdf.with_suffix(".html")
out_html.write_text(HTML, encoding="utf-8")
chrome = next((c for c in ("google-chrome", "chromium", "chromium-browser",
                           "google-chrome-stable") if shutil.which(c)), None)
if chrome is None:
    sys.exit("no Chrome/Chromium on PATH — needed to render the PDF")
subprocess.run([chrome, "--headless", "--disable-gpu", "--no-sandbox",
                "--no-pdf-header-footer", f"--print-to-pdf={out_pdf}", f"file://{out_html}"],
               check=True, capture_output=True)
print(f"Wrote {out_pdf} ({out_pdf.stat().st_size // 1024} KB) — {len(SLIPS)} slips, 1 cake, {len(CONTACTS)} contacts")
