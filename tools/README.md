# tools

`render-md-to-pdf.py` — renders the repo's markdown (run-guides, clock cards,
handouts) to print-ready PDF via Python-Markdown and headless Chrome.

    ./render-md-to-pdf.py IN.md OUT.pdf --theme guide|default|compact|card

`guide` is for run-guides, `card` for one-page clock cards. It renders
speaker-labelled dialogue boxes from `> **NAME:** *"line"*`.

**Resolve `{{pc:N}}` tokens before rendering** if you want real names on the
DM's copy; the tokens themselves render literally.
