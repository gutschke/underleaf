# Sessions

This folder accumulates post-session logs as the campaign is played. Each session is a directory `<YYYY-MM-DD>/` containing:

- `events.jsonl` — append-only event log captured during play (by the runtime).
- `snapshot.json` — pointer to the state at session start.
- `summary.md` — DM's narrative summary, written after the session.

Session summaries are *public* — players read them between sessions to remember what happened. DM-private reflections from a session belong in a separate `dm-reflections.md` (or under the episode's `dm/` folder if the reflections are episode-specific).

Initially empty until play begins.
