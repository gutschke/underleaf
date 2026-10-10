#!/usr/bin/env python3
"""Build the Ep 8 props: five "What Nia told you" slips (one per page), two "Later. Just us." slips,
and the phone-screen card for the printer scene.

Print SINGLE-SIDED and cut apart. Everything here is player-facing; run
tools/check-player-firewall.sh on the output before printing.

    ./make-props.py --out ep8-props.pdf                      # {{pc:N}} tokens
    ./make-props.py --map party-mapping.json --out ep8-props.pdf

The slip text is read from what-nia-told-you.md next to this script, so the
markdown stays the one place to edit it. The intermediate HTML is written next to
the PDF (never to the system /tmp).
"""
import argparse, html, json, pathlib, re, shutil, subprocess, sys

ap = argparse.ArgumentParser(description="Build the Ep 8 props.")
ap.add_argument("--map", type=pathlib.Path, default=None,
                help="private slot->PC map; without it the props print {{pc:N}}")
ap.add_argument("--out", type=pathlib.Path, required=True)
args = ap.parse_args()

if args.map:
    SLOTS = json.loads(args.map.read_text())["slots"]
    PC = {i: SLOTS[str(i)]["pc"] for i in range(1, 6)}
else:
    PC = {i: "{{pc:%d}}" % i for i in range(1, 6)}

src = (pathlib.Path(__file__).parent / "what-nia-told-you.md").read_text(encoding="utf-8")
src = re.sub(r"\{\{pc:(\d)\}\}", lambda m: PC[int(m.group(1))], src)


def inline(t):
    t = html.escape(t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    return re.sub(r"\*(.+?)\*", r"<i>\1</i>", t)


# Split on "## " headings; the first chunk is the file title.
sections = {}
for chunk in re.split(r"^## ", src, flags=re.M)[1:]:
    head, _, body = chunk.partition("\n")
    paras = [p.strip().replace("\n", " ") for p in body.split("\n\n")]
    sections[head.strip()] = [p for p in paras if p and p != "---"]

shared = sections.pop("For all five")
later = sections.pop("Later. Just us.")
if len(sections) != 5:
    sys.exit(f"expected five PC slips, found {len(sections)}: {list(sections)}")


def is_intro(p):
    return p.startswith(">")


def paras_html(paras):
    return "".join(f"<p>{inline(p)}</p>" for p in paras)


def slip(name, paras):
    # Plain-language intro first (the "> " paragraphs), then the reference block.
    intro = [p.lstrip("> ") for p in paras + shared if is_intro(p)]
    mine = [p for p in paras if not is_intro(p)]
    rest = [p for p in shared if not is_intro(p)]
    # A reach can't be backed, so the backing rule would contradict the slip.
    if any(p.startswith("**Always alone.**") for p in mine):
        backing = [p for p in rest if p.startswith("**Trying on purpose costs more**")]
        if len(backing) != 1:
            sys.exit("expected exactly one backing paragraph in 'For all five'")
        rest.remove(backing[0])
    return (f'<div class="slip"><div class="to">What Nia told you &middot; {html.escape(name)}</div>'
            f'<div class="intro">{paras_html(intro)}</div>'
            f'<div class="ref">The details</div>{paras_html(mine + rest)}'
            f'<div class="foot">Yours to keep.</div></div>')


def later_slip():
    return (f'<div class="later"><div class="big">Later. Just us.</div>'
            f'<div class="sub">{inline(later[0])}</div></div>')


CSS = """
@page { size: letter; margin: 0.45in; }
body { font-family: Georgia, serif; color: #1a1a1a; margin: 0; }
h1 { font: 9pt Helvetica, Arial, sans-serif; color: #777; margin: 0 0 4pt; }
.slip { border: 1.2px dashed #888; padding: 16pt 20pt; box-sizing: border-box;
  break-inside: avoid; }
.slip p { font-size: 12pt; line-height: 1.32; margin: 0 0 7pt; }
.intro { background: #eef3f7; border-left: 4px solid #4a7a9c; padding: 10pt 12pt 3pt; margin-bottom: 12pt; }
.intro p { font-size: 13pt; }
.ref { font: bold 8.5pt Helvetica, Arial, sans-serif; letter-spacing: .08em; text-transform: uppercase;
  color: #777; border-top: 1px solid #ccc; padding-top: 6pt; margin-bottom: 6pt; }
.to { font: bold 9.5pt Helvetica, Arial, sans-serif; letter-spacing: .08em; text-transform: uppercase;
  margin-bottom: 9pt; }
.foot { font: 7.5pt Helvetica, Arial, sans-serif; color: #888; }
.page { break-before: page; }
.later { border: 1.2px dashed #888; height: 1.8in; display: flex; flex-direction: column;
  align-items: center; justify-content: center; margin-bottom: 0.2in; }
.later .big { font: italic 30pt Georgia, serif; }
.later .sub { font: 9pt Helvetica, Arial, sans-serif; color: #888; margin-top: 10pt; }
.phone { border: 1.2px dashed #888; height: 2.3in; display: flex; flex-direction: column;
  align-items: center; justify-content: center; background: #f4f6f8; margin-bottom: 0.2in; }
.phone .app { font: 10pt Helvetica, Arial, sans-serif; color: #666; }
.phone .msg { font: bold 26pt Helvetica, Arial, sans-serif; margin-top: 8pt; text-align: center; }
"""

names = list(sections)
body = []
for i, n in enumerate(names):
    if i:
        body.append('<div class="page"></div>')
    body.append('<h1>Ep 8 &middot; hand all five over together after the game &middot; cut along the dashes</h1>')
    body.append(slip(n, sections[n]))
# The later-slips page names no one: it may be handled in view of the players.
body.append('<div class="page"><h1>Later slips &mdash; the run-guide says when. Hand one over in silence.</h1></div>')
body += [later_slip(), later_slip()]
# The phone cards get a page of their own: they're held up in front of everyone in
# Scene 2, so nothing else (least of all a hint about a private slip) may share it.
body.append('<div class="page"><h1>The printer &mdash; Nia\'s phone screen. Show the first card; swap to the second after the cast.</h1></div>')
body.append('<div class="phone"><div class="app">HP Smart</div><div class="msg">Paper jam.<br>0 of 6 printed</div></div>')
body.append('<div class="phone"><div class="app">HP Smart</div><div class="msg">5 of 6 printed.<br>Paper jam on page 6</div></div>')

HTML = ("<!doctype html><html><head><meta charset='utf-8'><title>Ep 8 props</title>"
        f"<style>{CSS}</style></head><body>{''.join(body)}</body></html>")

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
# One slip per page, then a page of later-slips, then a page of phone cards. A slip that
# outgrows its page spills silently, so count the pages and refuse.
pages = int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", str(out_pdf)],
            capture_output=True, text=True, check=True).stdout).group(1))
if pages != len(names) + 2:
    sys.exit(f"{out_pdf}: {pages} pages, expected {len(names) + 2} — a slip no longer fits its page")
print(f"Wrote {out_pdf} ({out_pdf.stat().st_size // 1024} KB) — {len(names)} slips, 2 later-slips, phone card")
