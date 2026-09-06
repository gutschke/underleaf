#!/usr/bin/env bash
# Guard: fail if any real player's first name appears in this public repo.
#
# The repo carries CHARACTER names freely; it must never carry PLAYER names.
# The slot->player map is private and is not committed — point at it with
# UNDERLEAF_PARTY_MAP, or pass it as the second argument.
#
#   ./check-no-player-names.sh [repo-dir] [party-mapping.json]
#
# CASE-INSENSITIVE, and that matters: this guard was case-sensitive until
# 2026-09-06 and silently passed a lowercase player name sitting inside a
# filename reference for weeks. Do not "optimise" the -i away.
set -u
REPO="${1:-$(dirname "$0")/..}"
MAP="${2:-${UNDERLEAF_PARTY_MAP:-$(dirname "$0")/party-mapping.json}}"
if [ ! -f "$MAP" ]; then
  echo "no slot->player map at $MAP — set UNDERLEAF_PARTY_MAP or pass one." >&2
  exit 2
fi
NAMES=$(python3 -c "
import json,sys
print('|'.join(s['player'] for s in json.load(open(sys.argv[1]))['slots'].values()))" "$MAP")
HITS=$(grep -rInEi "\b($NAMES)\b" --include='*.md' --include='*.json' --include='*.html' \
        --include='*.py' --include='*.sh' "$REPO" 2>/dev/null)
if [ -n "$HITS" ]; then
  echo "LEAK — player names found in the public repo:"
  echo "$HITS"
  exit 1
fi
echo "clean — no player names in $REPO"
