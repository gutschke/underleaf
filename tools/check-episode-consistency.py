#!/usr/bin/env python3
"""Catch the stale-text defects that repeated manual read-throughs kept missing.

Every check here exists because the same class of bug shipped at least once:
an edit landed in one document and not its mirror, or a `replace` matched the
first of two identical headings and left the second behind.

    ./check-episode-consistency.py underleaf/episodes/006-eight-twenty-sharp

Exit 1 on any finding, so it chains with && before a commit.
"""
import re, sys, pathlib, collections

# Always checked, in every episode.
BAD_PHRASES = [
    (r"used to (?:read|say)|an earlier (?:version|draft)|previously,", "authoring changelog voice"),
    (r"\bTODO\b|\bTKTK\b|\bXXX\b", "placeholder left in"),
    (r"\bsee (?:the )?(?:section|lookup) below\b", "vague cross-reference; name the scene"),
]

# Components an episode CUT during design. A reference to one is stale text left
# behind by a partial edit -- the single commonest defect in this repo.
# Pass with --cut, e.g.  --cut board,meeples,dice
CUT_PATTERNS = {
    "board":   (r"\bthe board\b(?! game)", "references a board that was cut"),
    "meeples": (r"\bmeeples?\b", "references meeples, which were cut"),
    "dice":    (r"\b2d6\b|\bsnake eyes\b|\bboxcars\b", "references dice, which were cut"),
    "strip":   (r"\bthe strip\b", "references a strip that was cut"),
}

def heading_dupes(text):
    heads = [l.strip() for l in text.splitlines() if l.startswith("#")]
    return [h for h, c in collections.Counter(heads).items() if c > 1]

def dangling_refs(text):
    """A cross-reference to a Scene that has no heading."""
    have = set(re.findall(r"^##+\s*(Scene \d+)", text, re.M))
    want = set(re.findall(r"\bsee (Scene \d+)|\b(Scene \d+)\b(?=[^\n]*\bbelow\b)", text, re.I))
    want = {a or b for a, b in want}
    return sorted(w for w in want if w and w not in have)

NEGATED = re.compile(r"(never|not|no longer|rather than|instead of|drop to|fall back)\W*$", re.I)

def numeric_claims(text):
    """Flag a value stated two different ways.

    Skips negated forms - "four rounds, never five" is one claim, not two -
    and skips a value that only ever appears as a fallback.
    """
    pats = {
        "round count": r"\b(three|four|five) rounds\b",
        "round cost": r"(?<!run )\b(five to six|seven to nine|ninety seconds)\b",
        "slip count": r"\b(four|five) (?:blank )?slips\b",
        "session total": r"\b(2h50|3h10|three hours and ten)\b",
    }
    out = {}
    for name, pat in pats.items():
        vals = set()
        for m in re.finditer(pat, text, re.I):
            before = text[max(0, m.start() - 30):m.start()]
            if NEGATED.search(before):
                continue
            # a numbered fallback line is allowed to name a smaller number
            line_start = text.rfind("\n", 0, m.start()) + 1
            if re.match(r"\s*\d+\.\s", text[line_start:m.start()] or ""):
                continue
            vals.add(m.group(1).lower())
        if len(vals) > 1:
            out[name] = sorted(vals)
    return out

def deck_counts(text):
    return {m.group(1): int(m.group(2))
            for m in re.finditer(r"\*\*([A-Z][A-Z ]+)\*\*\s*\((\d+)", text)}

def check_npc_date_conflicts(root):
    """Contradictory dates inside a SINGLE character file.

    Partial edits are this repo's commonest defect, and JSON was a blind spot:
    Rosa's husband died in 2007 in one field and 2016 in another, in adjacent
    fields, introduced and missed on the same day.
    """
    import json as _json
    bad = []
    for f in sorted(root.rglob("characters/**/*.json")):
        try:
            blob = _json.dumps(_json.loads(f.read_text()), ensure_ascii=False)
        except Exception:
            continue
        # Only relationship words that can refer to ONE person within one file.
        # "died"/"deceased" are too noisy — a single NPC file legitimately
        # mentions several deaths — and a check that cries wolf gets ignored.
        for subject in ("husband", "wife"):
            years = set()
            # (?!-) skips ISO date stamps like "corrected 2026-09-05"
            for m in re.finditer(rf"{subject}[^.\"]{{0,80}}?((?:19|20)\d\d)(?!-)", blob, re.I):
                years.add(m.group(1))
            if len(years) > 1:
                bad.append(f"{f.name}: '{subject}' has conflicting years {sorted(years)}")
    return bad


def main(root, cut=()):
    root = pathlib.Path(root)
    checks = list(BAD_PHRASES) + [CUT_PATTERNS[c] for c in cut if c in CUT_PATTERNS]
    # Skip generated snapshots. continuity-through-*.md is a verbatim copy of the
    # facts ledger, so its repeated section headings and its cross-references into
    # other episodes are expected structure, not partial-edit damage.
    docs = [d for d in sorted(root.rglob("*.md"))
            if not d.name.startswith("continuity-through-")]
    if not docs:
        print(f"no markdown under {root}"); return 1
    bad = 0
    for line in check_npc_date_conflicts(root):
        print(f"  {line}"); bad += 1
    for d in docs:
        t = d.read_text()
        for pat, why in checks:
            for m in re.finditer(pat, t, re.I):
                line = t[:m.start()].count("\n") + 1
                print(f"{d}:{line}: {why} — {m.group(0)!r}"); bad += 1
        for h in heading_dupes(t):
            print(f"{d}: DUPLICATE HEADING {h!r} — an edit will silently hit only the first"); bad += 1
        for r in dangling_refs(t):
            print(f"{d}: cross-reference to {r!r} but no such heading"); bad += 1
        for name, vals in numeric_claims(t).items():
            print(f"{d}: conflicting {name}: {vals}"); bad += 1
    # deck counts must agree across every document that states them
    seen = {}
    for d in docs:
        for deck, n in deck_counts(d.read_text()).items():
            if deck in seen and seen[deck][1] != n:
                print(f"deck {deck!r}: {seen[deck][0].name} says {seen[deck][1]}, {d.name} says {n}"); bad += 1
            seen.setdefault(deck, (d, n))
    print("clean" if not bad else f"{bad} finding(s)")
    return 1 if bad else 0

if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    cut = []
    for a in sys.argv[1:]:
        if a.startswith("--cut"):
            cut = a.split("=", 1)[1].split(",") if "=" in a else []
    sys.exit(main(args[0] if args else ".", cut))
