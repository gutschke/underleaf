#!/usr/bin/env python3
"""Inverse of resolve-pc-tokens.py: turn real names into {{pc:N}} tokens.

Used once when promoting a DM doc written with real names into the public
repo.  Order matters: "PC (Player)" pairs collapse first, then bare player
names become "{{pc:N}}'s player", then bare PC names become "{{pc:N}}".

  ./tokenize-pc-names.py IN.md OUT.md
"""
import json, re, sys, pathlib

HERE = pathlib.Path(__file__).parent
SLOTS = json.load(open(HERE / "party-mapping.json"))["slots"]


def tokenize(text: str) -> str:
    for n, s in SLOTS.items():
        tok = "{{pc:%s}}" % n
        pc, player = s["pc"], s["player"]
        # 1. "Morgan (Player)" and "Player (Morgan)" -> token
        text = re.sub(rf"\b{re.escape(pc)}\s*\(\s*{re.escape(player)}\s*\)", tok, text)
        text = re.sub(rf"\b{re.escape(player)}\s*\(\s*{re.escape(pc)}\s*\)", tok, text)
        # 2. bare player name -> "{{pc:N}}'s player" (possessive-aware)
        text = re.sub(rf"\b{re.escape(player)}'s\b", tok + "'s player's", text)
        text = re.sub(rf"\b{re.escape(player)}\b", tok + "'s player", text)
        # 3. bare PC name -> token
        text = re.sub(rf"\b{re.escape(pc)}\b", tok, text)
        # 4. full PC name, if it survived
        text = re.sub(rf"\b{re.escape(s['pcFull'])}\b", tok, text)
    return text


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__); return 2
    src, dst = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
    out = tokenize(src.read_text())
    dst.write_text(out)
    leaked = []
    for s in SLOTS.values():
        if re.search(rf"\b{re.escape(s['player'])}\b", out):
            leaked.append(s["player"])
    print(f"{src.name} -> {dst.name}: {'CLEAN' if not leaked else 'LEAKED ' + ','.join(leaked)}")
    return 1 if leaked else 0


if __name__ == "__main__":
    sys.exit(main())
