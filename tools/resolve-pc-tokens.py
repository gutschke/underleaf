#!/usr/bin/env python3
"""Resolve {{pc:N}} tokens in Underleaf DM docs into human-readable names.

The public repo (gutschke/underleaf) keeps player identities out of committed
files by writing PCs as {{pc:N}} and players as "{{pc:N}}'s player".  The DM
runs at the table off a resolved copy, because thinking in slot numbers mid-
session is hopeless.

  ./resolve-pc-tokens.py IN.md OUT.md [--style both|pc]

  both  (default)  {{pc:1}} -> "Morgan (Player)" on first use in a section,
                   then "Morgan" thereafter; "{{pc:1}}'s player" -> "Player"
  pc               {{pc:1}} -> "Morgan" everywhere (matches the Ep 4 copies)

The mapping is PRIVATE and is never committed. Point at it with the
UNDERLEAF_PARTY_MAP environment variable, or drop it beside this script.
"""
import os, sys, pathlib
import json, re, sys, pathlib

HERE = pathlib.Path(__file__).parent
MAP = pathlib.Path(os.environ.get("UNDERLEAF_PARTY_MAP", HERE / "party-mapping.json"))
if not MAP.exists():
    sys.exit("no slot->player map. Set UNDERLEAF_PARTY_MAP to your private "
             "party-mapping.json, or place one beside this script. It is "
             "deliberately NOT in this repository.")
SLOTS = json.loads(MAP.read_text())["slots"]

# "{{pc:4}}'s player" / "{{pc:4}}'s player's" -> the player's name.
PLAYER_RE = re.compile(r"\{\{pc:([1-9])\}\}'s player(?P<poss>'s)?")
PC_RE = re.compile(r"\{\{pc:([1-9])\}\}")


def resolve(text: str, style: str = "both") -> str:
    def player_sub(m):
        s = SLOTS[m.group(1)]
        return s["player"] + (m.group("poss") or "")

    text = PLAYER_RE.sub(player_sub, text)

    seen: set[str] = set()

    def pc_sub(m):
        n = m.group(1)
        s = SLOTS[n]
        # A possessive immediately after would read "Morgan (Player)'s father",
        # which is unspeakable.  Use the bare PC name and let the next plain
        # mention in this section carry the player name instead.
        possessive = m.string[m.end():m.end() + 2] == "'s"
        if style == "pc" or n in seen or possessive:
            return s["pc"]
        seen.add(n)
        # First mention gets both names, per the show-both-names rule.
        return f'{s["pc"]} ({s["player"]})'

    # Reset the "first mention" set at each heading so a DM scanning to one
    # scene mid-session still sees both names there.
    out = []
    for line in text.split("\n"):
        if line.startswith("#"):
            seen.clear()
        # Read-aloud and in-fiction blocks are blockquotes.  A player name said
        # out loud in an NPC's mouth is exactly the mix the naming rule forbids,
        # so inside a blockquote we always resolve to the character name alone.
        if line.lstrip().startswith(">"):
            out.append(PC_RE.sub(lambda m: SLOTS[m.group(1)]["pc"], line))
        else:
            out.append(PC_RE.sub(pc_sub, line))
    return "\n".join(out)


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    style = "pc" if "--style=pc" in sys.argv or "pc" in sys.argv[3:4] else "both"
    if len(args) < 2:
        print(__doc__)
        return 2
    src, dst = pathlib.Path(args[0]), pathlib.Path(args[1])
    body = resolve(src.read_text(), style)
    banner = (
        "<!-- RESOLVED COPY — contains player identities. Keep in tmp/, never "
        "commit to the public repo. Regenerate with resolve-pc-tokens.py. -->\n\n"
    )
    dst.write_text(banner + body)
    left = len(PC_RE.findall(body))
    print(f"{src.name} -> {dst} ({'clean' if not left else str(left)+' UNRESOLVED'})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
