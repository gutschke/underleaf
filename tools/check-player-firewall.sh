#!/usr/bin/env bash
# Player-facing PDFs must not carry DM vocabulary. No PC has knowsTheyCanCast set:
# the sheets say "focus" and "anchor" and must never say cast/magic/The Quiet.
# Usage: check-player-firewall.sh <file.pdf> [more.pdf ...]
set -u
BAD='\b(cast|casts|casting|caster|magic|magical|spell|substrate|The Quiet|Phase 1|Phase 2|realization|dmNotes|DM NOTES|DM-only)\b'
issues=0
for f in "$@"; do
  hits=$(pdftotext "$f" - 2>/dev/null | grep -inE "$BAD" || true)
  if [[ -n "$hits" ]]; then
    echo "  ⚠  $(basename "$f"):"; echo "$hits" | sed 's/^/       /'; issues=$((issues+1))
  fi
done
if (( issues == 0 )); then echo "player firewall: clean"; else
  echo "player firewall: $issues file(s) carry DM vocabulary — DO NOT HAND OVER"; exit 1; fi
