# Sessions

This folder accumulates post-session logs as the campaign is played. Each session is a directory `<YYYY-MM-DD>/` containing:

- `session.json` — the structured session log, validated against the
  `session-log` schema (`quire/schema/v0/session-log.schema.json`). Run
  `quire lint .` at the campaign root to check it.
- `events.jsonl` — append-only event log captured during play (by the runtime).
- `snapshot.json` — pointer to the state at session start.
- `summary.md` — DM's narrative summary, written after the session.

`session.json` is the durable record; the schema is intentionally permissive
(`additionalProperties: true`), so extra fields such as `scenesNotReached`,
`playedHighlights`, `carriedForward`, `partyStateAtEnd` and `durationMinutes`
are welcome and are used by the existing logs.

Session summaries are *public* — players read them between sessions to remember what happened. DM-private reflections from a session belong in a separate `dm-reflections.md` (or under the episode's `dm/` folder if the reflections are episode-specific).

## Backlog

Eps 1 and 2 have no session log yet — their real-world play dates were not
recorded anywhere in the repo. Add `sessions/<date>/session.json` for each once
the dates are confirmed.

Advancement marks (`rules.md` §Advancement) were not collected at the end of
Ep 4. The post-session workflow in each episode's `dm/run-guide.md` should
prompt for them; the `marks` field exists for this.
