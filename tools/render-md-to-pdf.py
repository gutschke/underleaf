#!/usr/bin/env python3
"""Render a markdown file to a print-friendly PDF via markdown + Chrome headless.

Themes:
- default: single-column serif, minimal color, good general purpose
- guide: color-coded scene headers, callout boxes for read-aloud/body-signal/firewall,
    two-column narrative (tables + pre break out), tag color-coding (STRUCTURE/SCENE-DRIVER/TEXTURE)
- compact: tight typography for shorter docs, per-stance color accents

Usage:
    render-md-to-pdf.py <input.md> <output.pdf> [--title "Doc Title"] [--theme guide]
"""

import argparse
import html
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import markdown as md_lib


# ============================================================
# CSS — base + theme-specific overrides
# ============================================================

THEME_CARD = """
@page { margin: 0.38in 0.42in; }
body { font-size: 8.2pt; line-height: 1.18; }
h1 { font-size: 14pt; border-bottom: 1.5px solid var(--fg); margin-bottom: 0.25em; }
h2 { font-size: 10.5pt; margin: 0.55em 0 0.2em; }
table { font-size: 8pt; margin: 0.3em 0; }
th, td { padding: 1.5px 4px; }
ul, ol { margin: 0.25em 0 0.25em 1.1em; }
li { margin: 0.1em 0; }
p { margin: 0.3em 0; }
blockquote { margin: 0.35em 0; padding: 0.25em 0.6em; }
"""

RUNNING_HEAD_CSS = """
/* Chrome repeats position:fixed elements on every printed page. */
@media print {
  .pagefoot {
    position: fixed; bottom: 0; left: 0; right: 0;
    font: 7.5pt Georgia, serif; color: #555;
    border-top: 0.5pt solid #bbb; padding-top: 2pt;
    justify-content: space-between;
  }
  body { padding-bottom: 22pt; }
}
.pagefoot { display: none; }
"""

CSS_BASE = """
@page { size: letter; margin: 0.55in 0.6in; }
:root {
    --fg: #1a1a1a; --muted: #666; --border: #d0d0d0;
    --code-bg: #f5f5f5; --blockquote-border: #b0b0b0;
    --caution-bg: #fff4e5; --caution-border: #f0ad4e; --caution-fg: #8a5a00;
    --read-aloud-bg: #f0f7ec; --read-aloud-border: #7aa06b;
    --body-signal-bg: #f2eef7; --body-signal-border: #7a5aa8; --body-signal-fg: #4a3070;
    --firewall-bg: #fef3d7; --firewall-border: #c9871c; --firewall-fg: #6a4a10;
    --structure-color: #9c1c1c;
    --scene-driver-color: #1c5c9c;
    --texture-color: #666;
}
body {
    font-family: "Charter", "Georgia", "Palatino Linotype", "Palatino", serif;
    font-size: 10pt;
    line-height: 1.35;
    color: var(--fg);
    margin: 0; padding: 0;
}
h1, h2, h3, h4, h5, h6 {
    font-family: "Helvetica Neue", "Helvetica", "Arial", sans-serif;
    font-weight: 600; line-height: 1.2;
    margin-top: 1.1em; margin-bottom: 0.35em;
    break-after: avoid; page-break-after: avoid;
}
h1 { font-size: 18pt; border-bottom: 2px solid var(--fg); padding-bottom: 0.15em; margin-top: 0; }
h2 { font-size: 14pt; border-bottom: 1px solid var(--border); padding-bottom: 0.1em; }
h3 { font-size: 11pt; color: #333; }
h4 { font-size: 10.5pt; color: #444; }
p, ul, ol, blockquote { margin: 0.4em 0; }
strong { font-weight: 600; }
em { font-style: italic; }
code {
    font-family: "SF Mono", "Menlo", "Consolas", monospace;
    font-size: 9pt; background: var(--code-bg);
    padding: 0.1em 0.3em; border-radius: 3px;
}
pre {
    background: var(--code-bg); padding: 0.5em 0.75em;
    border-radius: 4px; overflow-x: auto;
    font-size: 9pt; page-break-inside: avoid; break-inside: avoid;
}
pre code { background: none; padding: 0; font-size: inherit; }
blockquote {
    border-left: 3px solid var(--blockquote-border);
    padding-left: 0.9em; color: #333; margin-left: 0;
}
table {
    border-collapse: collapse; width: 100%;
    margin: 0.6em 0; font-size: 9pt;
    page-break-inside: avoid; break-inside: avoid;
}
th, td {
    border: 1px solid var(--border);
    padding: 0.3em 0.55em; text-align: left; vertical-align: top;
}
th { background: #f0f0f0; font-weight: 600; }
tr:nth-child(even) td { background: #fafafa; }
hr { border: 0; border-top: 1px solid var(--border); margin: 1em 0; }
a { color: #0057b7; text-decoration: none; }
ul, ol { padding-left: 1.4em; }
li { margin: 0.12em 0; }
li p { margin: 0.2em 0; }
.callout-caution {
    background: var(--caution-bg); border-left: 4px solid var(--caution-border);
    color: var(--caution-fg); padding: 0.55em 0.85em; margin: 0.7em 0;
    border-radius: 3px; page-break-inside: avoid; break-inside: avoid;
}
.callout-caution strong { color: var(--caution-fg); }
.doc-header {
    font-family: "Helvetica Neue", "Helvetica", sans-serif;
    font-size: 8pt; color: var(--muted);
    border-bottom: 1px solid var(--border);
    padding-bottom: 0.35em; margin-bottom: 0.7em;
}
"""

CSS_GUIDE = """
/* Guide theme: color-coded scenes, callout boxes, two-column narrative */
@page { size: letter; margin: 0.5in 0.55in; }
body { font-size: 9.5pt; line-height: 1.32; }

/* Two-column narrative; tables/pre/callouts break out */
main-body { columns: 2; column-gap: 0.5in; column-rule: 1px solid #eee; }
main-body table, main-body pre, main-body .callout,
main-body h1, main-body h2, main-body blockquote.read-aloud {
    column-span: all;
    break-inside: avoid;
}

h1 { font-size: 17pt; margin-top: 0; }
h2 {
    font-size: 13pt; margin-top: 1em;
    padding: 0.3em 0.5em;
    color: white; background: #3a4a5a;
    border-radius: 3px; border-bottom: none;
    break-after: avoid;
}
h2.scene-1 { background: #1c5c9c; }
h2.scene-2 { background: #2c8a5c; }
h2.scene-3 { background: #6a3c8c; }
h2.scene-4 { background: #b06020; }
h2.contents { background: #444; }
h2.snapshot, h2.standing, h2.audit, h2.rolls, h2.contingency,
h2.firewall, h2.workflow { background: #555; }
h3 {
    font-size: 10.5pt; margin-top: 0.9em;
    padding: 0.15em 0; border-bottom: 1.5px solid #aaa;
    break-after: avoid;
}

/* STRUCTURE / SCENE-DRIVER / TEXTURE inline tags */
.tag-structure {
    color: white; background: var(--structure-color);
    padding: 0.05em 0.4em; border-radius: 2px;
    font-family: "Helvetica Neue", sans-serif;
    font-size: 8pt; font-weight: 600;
    text-transform: uppercase; letter-spacing: 0.03em;
}
.tag-scene-driver {
    color: white; background: var(--scene-driver-color);
    padding: 0.05em 0.4em; border-radius: 2px;
    font-family: "Helvetica Neue", sans-serif;
    font-size: 8pt; font-weight: 600;
    text-transform: uppercase; letter-spacing: 0.03em;
}
.tag-texture {
    color: white; background: var(--texture-color);
    padding: 0.05em 0.4em; border-radius: 2px;
    font-family: "Helvetica Neue", sans-serif;
    font-size: 8pt; font-weight: 600;
    text-transform: uppercase; letter-spacing: 0.03em;
}

/* Read-aloud text — distinctive green box */
blockquote.read-aloud {
    background: var(--read-aloud-bg);
    border-left: 4px solid var(--read-aloud-border);
    padding: 0.5em 0.8em 0.5em 1em; margin: 0.6em 0;
    color: #234020; border-radius: 3px;
    page-break-inside: avoid; break-inside: avoid;
    font-family: "Charter", "Georgia", serif;
    font-style: italic;
}
blockquote.read-aloud::before {
    content: "READ ALOUD  ";
    display: block; font-style: normal; font-weight: 600;
    color: var(--read-aloud-border);
    font-family: "Helvetica Neue", sans-serif;
    font-size: 7.5pt; letter-spacing: 0.1em; margin-bottom: 0.2em;
}
blockquote.read-aloud em { color: #234020; font-style: italic; }


/* ---- Speaker-labelled dialogue boxes -------------------------------
   Written as:  > **ROSA:** *"line"*
   The speaker name becomes the box label and picks a stable colour. */
blockquote.speaker {
    padding: 0.45em 0.8em 0.5em 1em; margin: 0.55em 0;
    border-left: 4px solid var(--spk-border);
    background: var(--spk-bg);
    color: var(--spk-fg);
    border-radius: 3px;
    page-break-inside: avoid; break-inside: avoid;
    font-family: "Charter", "Georgia", serif;
}
blockquote.speaker::before {
    content: attr(data-speaker);
    display: block; font-style: normal; font-weight: 700;
    color: var(--spk-border);
    font-family: "Helvetica Neue", sans-serif;
    font-size: 7.5pt; letter-spacing: 0.11em; margin-bottom: 0.2em;
}
blockquote.speaker p { margin: 0.15em 0; }
blockquote.speaker em { font-style: italic; color: var(--spk-fg); }
/* Stable per-speaker palettes */
blockquote.spk-a { --spk-bg:#f2f0fa; --spk-border:#6f5fa8; --spk-fg:#2c2450; }
blockquote.spk-b { --spk-bg:#fdf1ec; --spk-border:#c2673d; --spk-fg:#5a2c14; }
blockquote.spk-c { --spk-bg:#eef5fa; --spk-border:#4a80a8; --spk-fg:#1d3purple; }
blockquote.spk-c { --spk-bg:#eef5fa; --spk-border:#4a80a8; --spk-fg:#1d3a52; }
blockquote.spk-d { --spk-bg:#f3f6ec; --spk-border:#6f8f45; --spk-fg:#2f3f18; }
blockquote.spk-e { --spk-bg:#faf0f4; --spk-border:#a85278; --spk-fg:#521f36; }
blockquote.spk-f { --spk-bg:#f6f2e8; --spk-border:#9a7b3f; --spk-fg:#453212; }
/* Numbered answer lists keep the boxes tight */
ol.answers > li { margin: 0.15em 0; }

/* Body-signal reminders */
.callout-body-signal {
    background: var(--body-signal-bg);
    border-left: 4px solid var(--body-signal-border);
    color: var(--body-signal-fg);
    padding: 0.5em 0.8em; margin: 0.6em 0;
    border-radius: 3px; page-break-inside: avoid; break-inside: avoid;
}
.callout-body-signal strong { color: var(--body-signal-fg); }

/* Firewall reminders */
.callout-firewall {
    background: var(--firewall-bg);
    border-left: 4px solid var(--firewall-border);
    color: var(--firewall-fg);
    padding: 0.5em 0.8em; margin: 0.6em 0;
    border-radius: 3px; page-break-inside: avoid; break-inside: avoid;
}
.callout-firewall strong { color: var(--firewall-fg); }
"""

CSS_COMPACT = """
/* Compact theme: tighter typography for shorter reference docs */
@page { size: letter; margin: 0.45in 0.5in; }
body { font-size: 9.5pt; line-height: 1.25; }
h1 { font-size: 16pt; margin-top: 0; }
h2 { font-size: 12pt; margin-top: 0.9em; }
h3 { font-size: 10.5pt; margin-top: 0.7em; }
p, ul, ol, blockquote { margin: 0.3em 0; }
table { font-size: 8.5pt; }
th, td { padding: 0.25em 0.4em; }

/* Per-stance colored headings for single-player handout docs */
h3.stance-focused { color: white; background: #2c5a8a; padding: 0.2em 0.5em; border-radius: 3px; border-bottom: none; }
h3.stance-contrite { color: white; background: #4a8a5c; padding: 0.2em 0.5em; border-radius: 3px; border-bottom: none; }
h3.stance-doubling { color: white; background: #b06020; padding: 0.2em 0.5em; border-radius: 3px; border-bottom: none; }
h3.stance-frightened { color: white; background: #6a3c8c; padding: 0.2em 0.5em; border-radius: 3px; border-bottom: none; }

/* Inline yellow highlight for quick-reference bits during play */
mark, .hi {
    background: #fff08a; color: inherit;
    padding: 0.05em 0.2em; border-radius: 2px;
}

/* Colored callout boxes usable via <div class="..."> in markdown */
.box-party {
    background: #eef4fb; border-left: 4px solid #2c5a8a;
    padding: 0.5em 0.75em; margin: 0.5em 0;
    border-radius: 3px; page-break-inside: avoid; break-inside: avoid;
}
.box-party strong { color: #1a3a5a; }
.box-dakota {
    background: #f7ecdc; border-left: 4px solid #b06020;
    padding: 0.5em 0.75em; margin: 0.5em 0;
    border-radius: 3px; page-break-inside: avoid; break-inside: avoid;
}
.box-dakota strong { color: #6a3c10; }
.box-people {
    background: #f0f2ec; border-left: 4px solid #5a7a3a;
    padding: 0.4em 0.75em; margin: 0.4em 0;
    border-radius: 3px; page-break-inside: avoid; break-inside: avoid;
}
.box-play {
    background: #fbf1d6; border-left: 4px solid #c9871c;
    padding: 0.5em 0.75em; margin: 0.5em 0;
    border-radius: 3px; page-break-inside: avoid; break-inside: avoid;
}
.box-play strong { color: #6a4a10; }
.box-quote {
    background: #f4f0e6; border: 1px solid #c9b17a;
    padding: 0.55em 0.85em; margin: 0.55em 0;
    border-radius: 3px; page-break-inside: avoid; break-inside: avoid;
    font-style: italic; font-family: "Charter", "Georgia", serif;
}
/* Framing/meta block — muted burgundy, distinct from the party/dakota/people palette */
.box-frame {
    background: #f3e8ea; border-left: 4px solid #7a2c3a;
    padding: 0.7em 0.95em; margin: 0.7em 0;
    border-radius: 3px; page-break-inside: avoid; break-inside: avoid;
}
.box-frame strong { color: #4a1620; }
.box-frame em { color: #4a1620; }
"""


# ============================================================
# Preprocessors
# ============================================================

CAUTION_BLOCK_RE = re.compile(
    r"^> \[!CAUTION\]\n((?:> .*\n?)+)",
    re.MULTILINE,
)


def preprocess_gfm_callouts(md_text: str) -> str:
    """Convert `> [!CAUTION]` blocks into HTML divs."""
    def replace(match):
        body_lines = match.group(1).strip().splitlines()
        stripped = "\n".join(line.lstrip("> ").rstrip() for line in body_lines)
        inner_html = md_lib.markdown(stripped, extensions=["extra"])
        return f'<div class="callout-caution">{inner_html}</div>\n'
    return CAUTION_BLOCK_RE.sub(replace, md_text)


# Stable speaker -> palette class. Recurring NPCs get fixed slots so a given
# character is always the same colour across every document.
SPEAKER_SLOTS = {
    "ROSA": "spk-a", "NIA": "spk-b", "BEA": "spk-c", "ORTIZ": "spk-d",
    "ALAIA": "spk-e", "VIVIAN": "spk-f", "ELENA": "spk-c", "CALLER": "spk-d",
    "THE ROOM": "spk-d", "REGGIE": "spk-e",
}
_SPK_CYCLE = ["spk-a", "spk-b", "spk-c", "spk-d", "spk-e", "spk-f"]

SPEAKER_P_RE = re.compile(
    r'<p>\s*<strong>([A-Z][A-Z0-9 .\'\u2019-]{1,24}):</strong>\s*'
)
BLOCKQUOTE_RE = re.compile(r'<blockquote>(.*?)</blockquote>', re.S)
PARA_RE = re.compile(r'<p>.*?</p>', re.S)


def _speaker_class(name):
    """Colour is keyed to the CHARACTER, not the label.

    A numbered label like `ROSA 7` (used for ordered answer lists) must render in
    Rosa's colour, not a seventh one -- otherwise a single speaker turns into a
    rainbow and the whole point of a stable per-character colour is lost.
    """
    base = re.sub(r"\s*\d+$", "", name).strip() or name
    cls = SPEAKER_SLOTS.get(base)
    if cls is None:
        cls = _SPK_CYCLE[sum(map(ord, base)) % len(_SPK_CYCLE)]
    return cls


def apply_speaker_boxes(html_text: str) -> str:
    """`> **ROSA:** *"line"*` becomes a colour-coded, speaker-labelled box.

    Python-markdown merges blockquotes separated only by a blank line into a
    SINGLE blockquote. Left alone that silently files several characters' lines
    under whichever name came first -- the exact failure a DM hunting for a cue
    cannot afford. So split any blockquote that holds more than one speaker
    paragraph into one box per speaker.
    """
    def split_bq(m):
        inner = m.group(1)
        paras = PARA_RE.findall(inner)
        # Only intervene when the block is entirely paragraphs and at least one
        # of them opens with a speaker label; otherwise leave it untouched.
        # Anything other than paragraphs (lists, nested quotes) -> leave alone.
        if not paras or PARA_RE.sub("", inner).strip():
            return m.group(0)
        if not any(SPEAKER_P_RE.match(par) for par in paras):
            return m.group(0)
        out = []
        for par in paras:
            sm = SPEAKER_P_RE.match(par)
            if sm:
                name = sm.group(1).strip()
                body = par[sm.end():]
                if not body.startswith("<p"):
                    body = "<p>" + body
                out.append(
                    f'<blockquote class="speaker {_speaker_class(name)}" '
                    f'data-speaker="{name}">{body}</blockquote>'
                )
            else:
                out.append(f'<blockquote>{par}</blockquote>')
        return "".join(out)

    return BLOCKQUOTE_RE.sub(split_bq, html_text)


def postprocess_guide_theme(html_text: str) -> str:
    """Add classes to scene headers, tag spans, callout paragraphs, read-aloud blockquotes."""
    # Speaker boxes first, so the generic read-aloud rules below skip them.
    html_text = apply_speaker_boxes(html_text)
    # Scene N headers → class="scene-N"
    def scene_h2(m):
        num = m.group(1)
        return f'<h2 class="scene-{num}">{m.group(2)}</h2>'
    html_text = re.sub(
        r'<h2>Scene (\d+)([^<]*)</h2>',
        scene_h2,
        html_text,
    )

    # Categorize other h2s
    h2_class_map = {
        "Contents": "contents",
        "Session snapshot": "snapshot",
        "Standing DM knowledge": "standing",
        "Per-PC engagement": "audit",
        "Optional consequential rolls": "rolls",
        "Contingency handling": "contingency",
        "Firewall discipline": "firewall",
        "Post-session workflow": "workflow",
    }
    for prefix, cls in h2_class_map.items():
        html_text = re.sub(
            rf'<h2>({re.escape(prefix)}[^<]*)</h2>',
            rf'<h2 class="{cls}">\1</h2>',
            html_text,
        )

    # Inline STRUCTURE / SCENE-DRIVER / TEXTURE tags
    # Match [STRUCTURE ...], [SCENE-DRIVER ...], [TEXTURE ...] with optional trailing detail
    def tag_replace(m):
        raw = m.group(1).upper()
        if raw.startswith("STRUCTURE"):
            cls = "tag-structure"
        elif raw.startswith("SCENE-DRIVER"):
            cls = "tag-scene-driver"
        elif raw.startswith("TEXTURE"):
            cls = "tag-texture"
        else:
            return m.group(0)
        # Truncate long descriptor after the tag
        short = raw.split("—")[0].split("-")[0].strip() if raw.startswith("TEXTURE") else raw.split("—")[0].strip()
        # For STRUCTURE and SCENE-DRIVER, keep the base tag word only for the pill
        if cls == "tag-structure":
            short = "STRUCTURE"
        elif cls == "tag-scene-driver":
            short = "SCENE-DRIVER"
        else:
            short = "TEXTURE"
        return f'<span class="{cls}">{short}</span>'
    html_text = re.sub(
        r'\[(STRUCTURE[^\]]*|SCENE-DRIVER[^\]]*|TEXTURE[^\]]*)\]',
        tag_replace,
        html_text,
    )

    # Body-signal reminder paragraphs → callout box
    html_text = re.sub(
        r'<p><strong>Body-signal reminder:',
        r'<p class="callout-body-signal"><strong>Body-signal reminder:',
        html_text,
    )

    # Firewall reminder paragraphs (specific patterns)
    html_text = re.sub(
        r'<p><strong>(Firewall note|Firewall discipline)',
        r'<p class="callout-firewall"><strong>\1',
        html_text,
    )

    # Read-aloud blockquotes: a blockquote whose PREVIOUS sibling is a paragraph
    # containing "Read-aloud" or "Read the transcript aloud" or DM voice cue
    # This is done by matching the pattern with lookbehind in HTML
    html_text = re.sub(
        r'(<p>[^<]*(?:Read-aloud|read the transcript aloud|DM voice|DM narrates? directly|Read-aloud text|deliver on speakerphone|Deliver Elena.*line before the cast)[^<]*(?:<[^>]+>[^<]*)*</p>\s*)(<blockquote>)',
        r'\1<blockquote class="read-aloud">',
        html_text,
        flags=re.IGNORECASE,
    )

    # Also: any blockquote that starts with an italic (typical "*read-aloud*" pattern)
    # gets marked as read-aloud
    html_text = re.sub(
        r'<blockquote>\s*<p>\s*<em>&ldquo;',
        r'<blockquote class="read-aloud"><p><em>&ldquo;',
        html_text,
    )
    html_text = re.sub(
        r'<blockquote>\s*<p>\s*<em>&quot;',
        r'<blockquote class="read-aloud"><p><em>&quot;',
        html_text,
    )
    # Handle straight quotes too (markdown may not always convert)
    html_text = re.sub(
        r'<blockquote>\s*<p>\s*<em>"',
        r'<blockquote class="read-aloud"><p><em>"',
        html_text,
    )
    html_text = re.sub(
        r"<blockquote>\s*<p>\s*<em>\*",
        r'<blockquote class="read-aloud"><p><em>*',
        html_text,
    )

    return html_text


def postprocess_compact_theme(html_text: str) -> str:
    """Stance-color coding for single-player handout docs."""
    stance_map = [
        ("Focused", "stance-focused"),
        ("Contrite", "stance-contrite"),
        ("Doubling-down", "stance-doubling"),
        ("Frightened", "stance-frightened"),
    ]
    for name, cls in stance_map:
        html_text = re.sub(
            rf'<h3(?:\s+[^>]*)?>Stance \d+ — {re.escape(name)}([^<]*)</h3>',
            rf'<h3 class="{cls}">Stance — {name}\1</h3>',
            html_text,
        )
    return html_text


# ============================================================
# Renderer
# ============================================================

THEME_CSS = {
    "default": CSS_BASE + RUNNING_HEAD_CSS,
    "guide": CSS_BASE + CSS_GUIDE + RUNNING_HEAD_CSS,
    "compact": CSS_BASE + CSS_COMPACT + RUNNING_HEAD_CSS,
    "card": CSS_BASE + CSS_COMPACT + THEME_CARD + RUNNING_HEAD_CSS,
}

THEME_POSTPROCESS = {
    "default": lambda x: x,
    "guide": postprocess_guide_theme,
    "compact": postprocess_compact_theme,
    "card": postprocess_compact_theme,
}


def render(md_path: Path, pdf_path: Path, title: str, theme: str) -> None:
    text = md_path.read_text()
    text = preprocess_gfm_callouts(text)

    body_html = md_lib.markdown(
        text,
        extensions=[
            "tables", "fenced_code", "toc", "attr_list",
            "sane_lists", "extra",
        ],
        extension_configs={"toc": {"anchorlink": False, "permalink": False}},
    )

    body_html = THEME_POSTPROCESS[theme](body_html)

    css = THEME_CSS[theme]

    # Wrap the main body in a <main-body> element so guide theme can apply
    # column layout to it while keeping the doc-header outside
    body_wrapper_open = '<main-body>' if theme == "guide" else '<div>'
    body_wrapper_close = '</main-body>' if theme == "guide" else '</div>'

    page_html = f"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>{html.escape(title)}</title>
<style>{css}</style>
</head>
<body>
<div class="doc-header">{html.escape(title)}</div>
{body_wrapper_open}
{body_html}
{body_wrapper_close}
</body>
</html>
"""

    with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False) as f:
        f.write(page_html)
        tmp_html = Path(f.name)

    try:
        subprocess.run(
            [
                "google-chrome", "--headless",
                "--disable-gpu", "--no-sandbox",
                "--no-pdf-header-footer",
                f"--print-to-pdf={pdf_path}",
                f"file://{tmp_html}",
            ],
            check=True, capture_output=True,
        )
    finally:
        tmp_html.unlink(missing_ok=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input", type=Path)
    ap.add_argument("output", type=Path)
    ap.add_argument("--title", default=None)
    ap.add_argument("--theme", choices=["default", "guide", "compact", "card"], default="default")
    args = ap.parse_args()

    title = args.title or args.input.stem
    render(args.input, args.output, title, args.theme)
    size_kb = args.output.stat().st_size // 1024
    print(f"Wrote {args.output} ({size_kb} KB, theme={args.theme})")


if __name__ == "__main__":
    main()
