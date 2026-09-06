#!/usr/bin/env python3
"""Build the DM master sheets by extending the generated player sheets with dmNotes.

Input is whatever `tools/build-pc-sheets.py` produced. Paths come from the
environment so nothing is hardcoded to one machine:
  UNDERLEAF_BASE_SHEETS  the player-sheets.html to extend
  UNDERLEAF_DM_HTML / UNDERLEAF_DM_PDF   outputs
  UNDERLEAF_PARTY_MAP    private slot->player map, for {{pc:N}} resolution

DM-only sections are laid out in a SINGLE column on purpose - Chrome silently
clips multicol content that spans a page break, and the DM loses notes with
nothing on the page to show it.

Original notes follow.


Reads:
- player-sheets.html (base layout)
- underleaf/characters/pcs/{morgan-reyes,priya-iyer,mira-sun,dakota-whitmore,mars-faraone}.json (dmNotes)

Writes:
- dm-master-sheets.html (extended)

Then renders to PDF via Chrome headless.
"""

import os
import html
import json
import re
import subprocess
import tempfile
from pathlib import Path

BASE_HTML = Path(os.environ.get("UNDERLEAF_BASE_SHEETS", "player-sheets.html"))
PCS_DIR = Path(__file__).resolve().parent.parent / "characters" / "pcs"
MAP = Path(os.environ.get("UNDERLEAF_PARTY_MAP",
                          Path(__file__).resolve().parent / "party-mapping.json"))

# The DM sheet is the resolved copy: {{pc:N}} is unreadable mid-session.
_SLOTS = json.loads(MAP.read_text())["slots"] if MAP.exists() else {}
_PC_RE = re.compile(r"\{\{pc:([1-9])\}\}")

def resolve_pcs(text):
    if not isinstance(text, str) or not _SLOTS:
        return text
    return _PC_RE.sub(lambda m: _SLOTS[m.group(1)]["pc"], text)
OUT_HTML = Path(os.environ.get("UNDERLEAF_DM_HTML", "dm-master-sheets.html"))
OUT_PDF = Path(os.environ.get("UNDERLEAF_DM_PDF", "dm-master-character-sheets.pdf"))

# Article ids come from tools/build-pc-sheets.py, which numbers them by slot.
PC_ORDER = [
    ("pc1", "morgan-reyes.json"),
    ("pc2", "priya-iyer.json"),
    ("pc3", "mira-sun.json"),
    ("pc4", "dakota-whitmore.json"),
    ("pc5", "mars-faraone.json"),
]

# DM-section CSS to inject into the <head>
# Aggressive single-page compression: everything for one PC fits on one letter sheet.
# Typography is small but legible; backstory goes 2-column; DM notes go 3-column.
DM_CSS = """
/* DM-only master sheet: single-page-per-PC discipline */
@page { size: letter; margin: 0.3in; }
@media print {
    body { font-size: 9pt; line-height: 1.28; }
    .sheet {
        page-break-after: always !important;
        break-after: page !important;
        padding: 0 !important;
        margin: 0 !important;
        min-height: unset !important;
    }
    .sheet:last-child { page-break-after: auto !important; }

    /* Header — smaller PC name, tighter quick-facts */
    .sheet header {
        padding-bottom: 5px !important;
        margin-bottom: 6px !important;
        gap: 4px 12px !important;
    }
    .sheet .pc-name { font-size: 17pt !important; }
    .sheet .player-line { font-size: 8.5pt !important; margin-top: 2px !important; }
    .sheet .quick-facts { font-size: 8pt !important; line-height: 1.22 !important; }
    .sheet .motif { width: 34px !important; height: 34px !important; }

    /* Stat block — tighter */
    .sheet .stat-row { margin: 5px 0 !important; gap: 3px !important; }
    .sheet .stat { padding: 3px 2px !important; }
    .sheet .stat .label { font-size: 7.5pt !important; }
    .sheet .stat .value { font-size: 13pt !important; margin-top: 1px !important; }

    /* Tracks — inline-tight */
    .sheet .tracks { margin: 3px 0 6px !important; font-size: 8.5pt !important; }
    .sheet .box { width: 10px !important; height: 10px !important; }

    /* Sections — pull margins down */
    .sheet section { margin: 4px 0 !important; }
    .sheet h2 { margin: 0 0 2px !important; font-size: 9pt !important; padding-bottom: 1px !important; }
    .sheet .chip { font-size: 8pt !important; padding: 1px 6px !important; }
    .sheet .two-col { gap: 10px !important; }

    /* Focus + intention — keep readable, trim padding */
    .sheet .focus-box { padding: 4px 8px !important; font-size: 8.5pt !important; line-height: 1.28 !important; }
    .sheet .intention { padding: 4px 8px !important; font-size: 8.5pt !important; line-height: 1.28 !important; }
    .sheet .intention p { margin: 2px 0 !important; }

    /* Backstory: 2 columns, small type, tight lines */
    .sheet .backstory { margin: 3px 0 !important; columns: 2; column-gap: 14px; column-rule: 1px dotted #d8d1bf; }
    .sheet .backstory h2 { column-span: all; }
    .sheet .backstory p {
        font-size: 7.3pt !important;
        line-height: 1.22 !important;
        margin: 0 0 3px !important;
        text-align: justify;
        hyphens: auto;
    }

    /* Bonds — compact list */
    .sheet section ul { margin: 2px 0 2px 16px !important; }
    .sheet section li { margin: 1px 0 !important; font-size: 8.5pt !important; line-height: 1.28 !important; }

    /* Footer — minimal */
    .sheet footer { margin-top: 4px !important; padding-top: 3px !important; font-size: 7.5pt !important; }
}
.dm-notes {
    margin-top: 5px;
    padding: 5px 8px;
    background: #fff4e0;
    border-left: 3px solid #c9871c;
    border-radius: 3px;
    /* Long DM-note blocks (Dakota's especially) must flow onto a second page.
       column-fill:auto is load-bearing: with the default balanced fill, Chrome
       silently CLIPS whatever does not fit instead of carrying it over, and the
       DM loses notes with no visible sign that anything is missing. */
    page-break-inside: auto;
    break-inside: auto;
    font-size: 6.9pt;
    line-height: 1.16;
    /* SINGLE COLUMN, deliberately. Chrome's multicol fragmentation silently
       CLIPS whatever does not fit when a block spans a page break, and the DM
       loses notes with nothing on the page to show it. Multicol also scrambles
       pdftotext output, which is what the completeness check reads. */
    columns: 1;
    column-gap: 8px;
}
.dm-notes h2 {
    column-span: all;
    color: #8a5a10 !important;
    margin: 0 0 3px !important;
    font-size: 8.5pt !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
    border: none !important;
    padding: 0 !important;
}
.dm-notes .dm-note {
    margin: 0 0 4px 0;
    /* allow notes to break across columns so they never force overflow */
}
.dm-notes .dm-note strong { color: #6a4008; }
.dm-notes .dm-note p { margin: 0 0 3px; }
.dm-notes .dmq { border-left: 2px solid #c9871c; padding-left: 5px; margin: 3px 0; color: #6a4008; }
.dm-notes ul { margin: 2px 0 2px 1.1em; padding: 0; }
.dm-notes li { margin: 1px 0; }
"""



def _md(text):
    """DM notes are authored in light markdown. Render **bold**, *italic*,
    `code`, > quotes and blank-line paragraphs — otherwise the asterisks print
    literally on the DM's sheet."""
    import re as _re
    out = []
    for block in _re.split(r"\n\s*\n", str(text).strip()):
        block = block.strip()
        if not block:
            continue
        quote = all(l.lstrip().startswith(">") for l in block.splitlines())
        if quote:
            block = "\n".join(_re.sub(r"^\s*>\s?", "", l) for l in block.splitlines())
        b = html.escape(block).replace("\n", "<br>")
        b = _re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", b, flags=_re.S)
        b = _re.sub(r"(?<!\*)\*([^*]+?)\*(?!\*)", r"<em>\1</em>", b, flags=_re.S)
        b = _re.sub(r"`(.+?)`", r"<code>\1</code>", b, flags=_re.S)
        out.append(f'<div class="dmq">{b}</div>' if quote else f"<p>{b}</p>")
    return "".join(out)


def render_dm_notes(pc_data: dict) -> str:
    """Render the dmNotes block for one PC as an HTML section."""
    dm = pc_data.get("dmNotes", {})
    if not dm:
        return ""

    # Ordered display of known fields, then anything else alphabetically
    ordered_keys = [
        "magicPhase",
        "intentionUnderPressureNote",
        "cosmologyPrecision",
        "castDomain",
        "personaDropCanon",
        "loadBearingIrony",
        "substrateSensitivity",
        "costTellPolicy",
        "controlSeekerHook",
        "bringAGunWatch",
        "personalStakesLever",
        "alignmentDriftWatch",
        "focusNotes",
        "openThreads",
    ]
    seen = set()

    def label_for(key: str) -> str:
        # camelCase → Title Case
        result = re.sub(r"([A-Z])", r" \1", key).strip().title()
        return result

    parts = ['<section class="dm-notes">']
    parts.append('<h2>DM notes</h2>')

    for key in ordered_keys:
        if key not in dm:
            continue
        seen.add(key)
        val = dm[key]
        label = label_for(key)
        if isinstance(val, list):
            parts.append(f'<div class="dm-note"><strong>{html.escape(label)}:</strong>')
            parts.append('<ul>')
            for item in val:
                parts.append(f'<li>{_md(resolve_pcs(item))}</li>')
            parts.append('</ul></div>')
        else:
            parts.append(
                f'<div class="dm-note"><strong>{html.escape(label)}:</strong> '
                f'{_md(resolve_pcs(val))}</div>'
            )

    # Any remaining keys (defensive)
    for key in sorted(dm.keys()):
        if key in seen:
            continue
        val = dm[key]
        label = label_for(key)
        if isinstance(val, list):
            parts.append(f'<div class="dm-note"><strong>{html.escape(label)}:</strong>')
            parts.append('<ul>')
            for item in val:
                parts.append(f'<li>{_md(resolve_pcs(item))}</li>')
            parts.append('</ul></div>')
        else:
            parts.append(
                f'<div class="dm-note"><strong>{html.escape(label)}:</strong> '
                f'{_md(resolve_pcs(val))}</div>'
            )

    parts.append('</section>')
    return "\n".join(parts)


def main():
    base = BASE_HTML.read_text()

    # Add DM_CSS before </style>
    base = base.replace("</style>", DM_CSS + "</style>", 1)

    # Update title + main headings/instructions
    base = base.replace(
        "<title>Underleaf — Player Character Sheets — Session 4 — The Sacramento Visit</title>",
        "<title>Underleaf — DM Master Character Sheets — Ep 4 prep</title>",
    )
    # Update any h1 heading (the top-of-page one)
    base = re.sub(
        r'<h1[^>]*>Underleaf[^<]*Character Sheets[^<]*</h1>',
        '<h1>Underleaf — DM Master Character Sheets</h1>',
        base,
    )
    # Remove the "To print:" player-facing instructional block (keeps the doc clean for DM use)
    base = re.sub(
        r'<p[^>]*><strong>To print:</strong>[\s\S]*?</p>',
        '<p><strong>DM copy.</strong> Includes DM-only notes per PC (amber section at the bottom of each page). Each PC prints on its own page.</p>',
        base,
    )

    # Add "DM COPY" badge next to each PC name
    base = re.sub(
        r'(<h1 class="pc-name">)',
        r'\1',  # unchanged for now, we could add badge but let's keep h1 clean
        base,
    )

    # Inject DM notes section before each PC's <footer>
    for pc_id, json_file in PC_ORDER:
        pc_data = json.loads((PCS_DIR / json_file).read_text())
        dm_section = render_dm_notes(pc_data)
        if not dm_section:
            continue

        # Find the article for this PC, insert dm_section before its footer
        # The pattern is: <article ... id="{pc_id}">...<footer>...
        pattern = rf'(<article[^>]*id="{pc_id}"[\s\S]*?)(<footer>)'
        replacement = rf'\1{dm_section}\n  \2'
        # Use non-greedy match within the article
        new_base = re.sub(pattern, replacement, base, count=1)
        if new_base == base:
            print(f"WARN: no substitution for {pc_id}")
        base = new_base

    OUT_HTML.write_text(base)
    print(f"Wrote {OUT_HTML}")

    # Render to PDF
    subprocess.run(
        [
            "google-chrome",
            "--headless",
            "--disable-gpu",
            "--no-sandbox",
            "--no-pdf-header-footer",
            f"--print-to-pdf={OUT_PDF}",
            f"file://{OUT_HTML}",
        ],
        check=True,
        capture_output=True,
    )
    size_kb = OUT_PDF.stat().st_size // 1024
    print(f"Wrote {OUT_PDF} ({size_kb} KB)")


if __name__ == "__main__":
    main()
