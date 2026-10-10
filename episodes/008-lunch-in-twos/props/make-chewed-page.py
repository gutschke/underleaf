#!/usr/bin/env python3
"""Make the "chewed" page for the Ep 8 printer scene: page 1 of the player handout,
as an inkjet would leave it after jamming on it.

    ./make-chewed-page.py <handout.pdf> <out.pdf> [--seed N]

What it simulates, top to bottom (an inkjet jam, not a laser jam):
  1. the first third prints, but the sheet fed in a little crooked;
  2. the paper stalls while the head keeps going: several lines overprint into one
     dark, smeared band;
  3. the paper bunches: the next lines come out stretched and dragged;
  4. printing stops; what remains is blank paper with the star-wheel tracks inkjets
     leave, a grey roller scuff, and a smudge where a finger pulled it out.

The physical part (crumple, tear, flatten) is in the run-guide's prep notes.
Needs pdftoppm (poppler) and Pillow + numpy. Intermediates go next to the output.
"""
import argparse, pathlib, subprocess
import numpy as np
from PIL import Image, ImageFilter, ImageChops

ap = argparse.ArgumentParser()
ap.add_argument("handout", type=pathlib.Path)
ap.add_argument("out", type=pathlib.Path)
ap.add_argument("--seed", type=int, default=8)
args = ap.parse_args()
rng = np.random.default_rng(args.seed)

DPI = 200
work = args.out.resolve().parent
base_png = work / "chewed-base"
subprocess.run(["pdftoppm", "-f", "1", "-l", "1", "-r", str(DPI), "-gray", "-png",
                str(args.handout), str(base_png)], check=True)
src = Image.open(f"{base_png}-1.png").convert("L")
W, H = src.size
ink = 255 - np.asarray(src, dtype=np.float32)          # 0 = paper, 255 = full ink

out = np.zeros_like(ink)
# Only real ink smears. Light table shading stacked into the jam looks like a grey box,
# which no printer makes, so the jam and drag use text ink only.
text = np.where(ink > 80, ink, 0).astype(np.float32)

# 1. Clean top third.
clean_end = int(H * 0.34)
out[:clean_end] = ink[:clean_end]

# 2. The stall: the next ~12% of the page printed into a ~3% band, overlapping.
band_src = text[clean_end:int(H * 0.46)]
band_h = int(H * 0.03)
band = np.zeros((band_h, W), np.float32)
step = max(1, band_src.shape[0] // 14)
for k in range(0, band_src.shape[0] - band_h, step):
    jitter = int(rng.integers(-6, 7))
    band += np.roll(band_src[k:k + band_h], jitter, axis=1) * 0.55
band = np.asarray(Image.fromarray(np.clip(band, 0, 255).astype(np.uint8))
                  .filter(ImageFilter.GaussianBlur(1.2)), np.float32)
band = np.clip(band * 1.25, 0, 240)
out[clean_end:clean_end + band_h] = np.maximum(out[clean_end:clean_end + band_h], band)

# 3. Bunched: the next lines stretched vertically and dragged downwards.
drag_src = text[int(H * 0.46):int(H * 0.54)]
drag_h = int(H * 0.16)
drag = np.asarray(Image.fromarray(drag_src.astype(np.uint8)).resize((W, drag_h), Image.BICUBIC),
                  np.float32)
drag_img = Image.fromarray(drag.astype(np.uint8)).filter(ImageFilter.BoxBlur(2))
drag = np.asarray(drag_img, np.float32)
# the paper wobbled sideways as it bunched
drag = np.stack([np.roll(row, int(rng.integers(-4, 5))) for row in drag])
drag = np.asarray(Image.fromarray(drag.astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.6)),
                  np.float32)
# vertical smear: each row picks up some ink from the rows above
for _ in range(3):
    drag = np.maximum(drag, np.roll(drag, int(rng.integers(6, 16)), axis=0) * 0.6)
fade = np.linspace(0.95, 0.15, drag_h)[:, None]
d0 = clean_end + band_h
out[d0:d0 + drag_h] = np.maximum(out[d0:d0 + drag_h], drag * fade)

# 4a. Star-wheel tracks: two columns of tiny dotted marks down the rest of the sheet.
for x in (int(W * 0.27), int(W * 0.71)):
    y = d0
    while y < H - 20:
        r = int(rng.integers(1, 3))
        out[y:y + r, x - r:x + r] = np.maximum(out[y:y + r, x - r:x + r], 90)
        y += int(rng.integers(9, 13))

# 4b. Roller scuff: a faint grey streak, wider at the jam.
scuff_x = int(W * 0.48)
for y in range(clean_end, H):
    w = int(30 * max(0.15, 1 - (y - clean_end) / (H - clean_end)))
    out[y, scuff_x - w:scuff_x + w] = np.maximum(out[y, scuff_x - w:scuff_x + w],
                                                 18 + rng.random(2 * w) * 10)

# 4c. A thumb smudge near the bottom edge, where it was pulled out.
yy, xx = np.mgrid[0:H, 0:W]
cy, cx = int(H * 0.9), int(W * 0.62)
smudge = np.exp(-(((xx - cx) / 120) ** 2 + ((yy - cy) / 55) ** 2)) * 70
out = np.maximum(out, smudge)

# Whole sheet: fed crooked, and a light grey rub along the left edge.
img = Image.fromarray(np.clip(255 - out, 0, 255).astype(np.uint8))
img = img.rotate(1.3, resample=Image.BICUBIC, fillcolor=255)
edge = np.asarray(img, np.float32)
edge[:, :18] -= np.linspace(40, 0, 18)[None, :]
img = Image.fromarray(np.clip(edge, 0, 255).astype(np.uint8))

img.save(args.out, "PDF", resolution=DPI)
print(f"Wrote {args.out}")
