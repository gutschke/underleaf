#!/usr/bin/env python3
"""Synthetic, heavily-worn ID-badge portraits.

**These are generated, not photographs.** No stock library, no real person, no
likeness — a lit head-and-shoulders built from primitives and then aged until
the features stop resolving, which is exactly what an ID photo looks like after
a few years in a badge holder. The point is that nobody at the table can make
out a face, so nobody is being depicted.

The degradation is layered the way real wear arrives: optical softening first,
then dye shift and splotching, then abrasion, then the crease from a lanyard
clip, then the surface haze of a scratched laminate.
"""
import math, random
from PIL import Image, ImageDraw, ImageFilter, ImageChops
import numpy as np


def _lerp(a, b, t):
    return tuple(int(round(x + (y - x) * t)) for x, y in zip(a, b))


def _base_portrait(rng, w, h, skin, hair, shirt, backdrop):
    """A studio head-and-shoulders. Deliberately soft — no crisp features."""
    im = Image.new("RGB", (w, h), backdrop[0])
    d = ImageDraw.Draw(im)

    # Backdrop: the usual flat wall with a slight lighting falloff to one side.
    for y in range(h):
        d.line([(0, y), (w, y)], fill=_lerp(backdrop[0], backdrop[1], y / h))
    glow = Image.new("L", (w, h), 0)
    ImageDraw.Draw(glow).ellipse(
        [-w * 0.3, -h * 0.2, w * 0.9, h * 0.9], fill=60)
    im = Image.composite(Image.new("RGB", (w, h), backdrop[1]), im,
                         glow.filter(ImageFilter.GaussianBlur(w * 0.25)))
    d = ImageDraw.Draw(im)

    cx = w * (0.5 + rng.uniform(-0.03, 0.03))
    head_w = w * rng.uniform(0.40, 0.46)
    head_h = head_w * rng.uniform(1.24, 1.34)
    head_cy = h * rng.uniform(0.40, 0.44)

    # Shoulders and collar — a dark mass that anchors the head.
    sh_top = head_cy + head_h * 0.72
    d.ellipse([cx - w * 0.62, sh_top, cx + w * 0.62, h * 1.5], fill=shirt)
    # Collar opening, slightly off-centre so it does not read as symmetrical.
    d.polygon([(cx - w * 0.10, sh_top + h * 0.02),
               (cx + w * 0.11, sh_top + h * 0.02),
               (cx + w * 0.02, sh_top + h * 0.16)], fill=_lerp(skin, shirt, 0.45))

    # Neck.
    d.rounded_rectangle([cx - head_w * 0.24, head_cy + head_h * 0.28,
                         cx + head_w * 0.24, sh_top + h * 0.03],
                        radius=int(head_w * 0.18), fill=_lerp(skin, (0, 0, 0), 0.18))

    # Hair mass behind the head.
    d.ellipse([cx - head_w * 0.60, head_cy - head_h * 0.66,
               cx + head_w * 0.60, head_cy + head_h * 0.34], fill=hair)
    # Face.
    d.ellipse([cx - head_w / 2, head_cy - head_h / 2,
               cx + head_w / 2, head_cy + head_h / 2], fill=skin)
    # Fringe / hairline across the top of the face.
    d.chord([cx - head_w * 0.54, head_cy - head_h * 0.62,
             cx + head_w * 0.54, head_cy + head_h * 0.10],
            180, 360, fill=hair)

    # Feature hints only. These get blurred into suggestion, never detail.
    eye_y = head_cy - head_h * 0.04
    for s in (-1, 1):
        d.ellipse([cx + s * head_w * 0.22 - head_w * 0.10, eye_y - head_h * 0.035,
                   cx + s * head_w * 0.22 + head_w * 0.10, eye_y + head_h * 0.035],
                  fill=_lerp(skin, hair, 0.55))
    d.ellipse([cx - head_w * 0.07, head_cy + head_h * 0.10,
               cx + head_w * 0.07, head_cy + head_h * 0.20],
              fill=_lerp(skin, (90, 60, 55), 0.30))
    d.ellipse([cx - head_w * 0.13, head_cy + head_h * 0.27,
               cx + head_w * 0.13, head_cy + head_h * 0.35],
              fill=_lerp(skin, (120, 70, 70), 0.40))
    # Modelling: light from one side.
    shade = Image.new("L", (w, h), 0)
    ImageDraw.Draw(shade).ellipse(
        [cx - head_w * 0.10, head_cy - head_h * 0.5,
         cx + head_w * 0.75, head_cy + head_h * 0.6], fill=70)
    im = Image.composite(Image.new("RGB", (w, h), _lerp(skin, (0, 0, 0), 0.35)),
                         im, shade.filter(ImageFilter.GaussianBlur(w * 0.10)))
    return im


def _damage(im, rng, severity):
    """Age it. severity 0..1 — 1 is 'this badge is older than the job'."""
    w, h = im.size
    s = severity

    # 1 · Optical: the laminate has gone cloudy and the print was never sharp.
    im = im.filter(ImageFilter.GaussianBlur(w * (0.006 + 0.022 * s)))

    a = np.asarray(im).astype(np.float32)

    # 2 · Dye shift: cheap dye-sub fades unevenly — magenta goes first, then cyan.
    a[..., 0] *= 1.0 + 0.10 * s
    a[..., 1] *= 1.0 - 0.03 * s
    a[..., 2] *= 1.0 - 0.14 * s
    # Global contrast loss toward a warm grey.
    a = a * (1 - 0.34 * s) + np.array([176, 168, 156]) * (0.34 * s)

    # 3 · Splotching: low-frequency blotches of over- and under-development.
    small = rng.randint(6, 9)
    blot = np.array(Image.fromarray(
        (np.random.RandomState(rng.randrange(1 << 30)).rand(small, small) * 255
         ).astype(np.uint8)).resize((w, h), Image.BICUBIC), dtype=np.float32)
    blot = (blot - blot.mean()) / 128.0
    a += blot[..., None] * (30 * s)
    # A second, tighter blotch field with a colour cast.
    small2 = rng.randint(14, 20)
    blot2 = np.array(Image.fromarray(
        (np.random.RandomState(rng.randrange(1 << 30)).rand(small2, small2) * 255
         ).astype(np.uint8)).resize((w, h), Image.BICUBIC), dtype=np.float32)
    blot2 = (blot2 - blot2.mean()) / 128.0
    a[..., 0] += blot2 * (18 * s)
    a[..., 2] -= blot2 * (12 * s)

    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))

    # 4 · Abrasion: fine scuffs, mostly along the axis the badge swings on.
    scuff = Image.new("L", (w, h), 0)
    ds = ImageDraw.Draw(scuff)
    for _ in range(int(14 + 34 * s)):
        x0 = rng.uniform(0, w); y0 = rng.uniform(0, h)
        ang = rng.gauss(math.pi / 2, 0.35)
        ln = rng.uniform(h * 0.03, h * 0.30)
        ds.line([x0, y0, x0 + math.cos(ang) * ln, y0 + math.sin(ang) * ln],
                fill=rng.randint(8, 30), width=1)
    scuff = scuff.filter(ImageFilter.GaussianBlur(1.1))
    im = ImageChops.screen(im, Image.merge("RGB", (scuff, scuff, scuff)))

    # 5 · The crease. Every badge that lives on a clip gets one.
    crease = Image.new("L", (w, h), 0)
    dc = ImageDraw.Draw(crease)
    cy = h * rng.uniform(0.18, 0.30)
    pts = [(x, cy + math.sin(x / w * 3.0 + rng.random()) * h * 0.012)
           for x in range(0, w + 1, 8)]
    dc.line(pts, fill=int(70 * s), width=max(1, int(w * 0.012)))
    crease = crease.filter(ImageFilter.GaussianBlur(w * 0.010))
    im = ImageChops.screen(im, Image.merge("RGB", (crease, crease, crease)))

    # 6 · Grain, then a vignette from the holder's window.
    g = np.random.RandomState(rng.randrange(1 << 30)).normal(0, 4.5 * s, (h, w, 1))
    im = Image.fromarray(np.clip(np.asarray(im).astype(np.float32) + g, 0, 255
                                 ).astype(np.uint8))
    vig = Image.new("L", (w, h), 0)
    ImageDraw.Draw(vig).rounded_rectangle(
        [w * 0.04, h * 0.03, w * 0.96, h * 0.97],
        radius=int(w * 0.10), fill=255)
    vig = vig.filter(ImageFilter.GaussianBlur(w * 0.13))
    im = Image.composite(im, Image.new("RGB", (w, h), (150, 146, 138)), vig)
    return im


PALETTES = {
    # Warm mid tones and black hair; everything is a suggestion after the aging.
    "a": dict(skin=(226, 192, 164), hair=(38, 30, 30), shirt=(58, 66, 84),
              backdrop=((208, 214, 216), (176, 186, 192))),
    "b": dict(skin=(222, 186, 158), hair=(30, 26, 28), shirt=(74, 68, 62),
              backdrop=((214, 210, 200), (184, 180, 172))),
    "c": dict(skin=(232, 198, 170), hair=(42, 34, 32), shirt=(46, 52, 60),
              backdrop=((198, 206, 212), (170, 180, 188))),
    "d": dict(skin=(218, 184, 156), hair=(34, 28, 30), shirt=(86, 84, 80),
              backdrop=((206, 202, 196), (178, 176, 170))),
}


def make(seed, palette="a", severity=0.75, size=(300, 380)):
    rng = random.Random(seed)
    w, h = size
    im = _base_portrait(rng, w, h, **PALETTES[palette])
    return _damage(im, rng, severity)


if __name__ == "__main__":
    for i, p in enumerate("abcd"):
        make(f"demo-{p}", p, 0.7 + 0.1 * i).save(f"/tmp/badge-photo-{p}.png")
    print("wrote /tmp/badge-photo-{a,b,c,d}.png")
