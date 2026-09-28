#!/usr/bin/env bash
# Player-facing PDFs must not carry DM vocabulary.
#
# Two tiers (changed 2026-09-27, when the DM ruled that Ep 8 reveals the players'
# abilities plainly — facts-ledger §50):
#   ALWAYS banned: the secret cosmology and DM machinery (substrate, The Quiet,
#     phase / realization labels, dmNotes, DM-only).
#   Banned only with --pre-reveal: cast / magic / spell. Before Ep 8 the sheets
#     said "focus" and "anchor" and never "cast"; from Ep 8 on the handout itself
#     says "aimed cast" and "supported casts", so these are player vocabulary.
# Usage: check-player-firewall.sh [--pre-reveal] <file.pdf> [more.pdf ...]
set -u
ALWAYS='substrate|The Quiet|Phase 1|Phase 2|realization|dmNotes|DM NOTES|DM-only'
PRE='cast|casts|casting|caster|magic|magical|spell'
BAD="\\b($ALWAYS)\\b"
if [[ "${1:-}" == "--pre-reveal" ]]; then BAD="\\b($ALWAYS|$PRE)\\b"; shift; fi
issues=0
for f in "$@"; do
  hits=$(pdftotext "$f" - 2>/dev/null | grep -inE "$BAD" || true)
  if [[ -n "$hits" ]]; then
    echo "  ⚠  $(basename "$f"):"; echo "$hits" | sed 's/^/       /'; issues=$((issues+1))
  fi
done
if (( issues == 0 )); then echo "player firewall: clean"; else
  echo "player firewall: $issues file(s) carry DM vocabulary — DO NOT HAND OVER"; exit 1; fi
