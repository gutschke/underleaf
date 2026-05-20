# Episodes

> **Player note:** scenes inside an episode you have not yet played are spoilers. Each episode's `dm/` subfolder is always spoilers and is marked accordingly. If you have already played an episode, its `scenes/` are safe to revisit.

Each episode is a directory under this folder, named `<NNN>-<slug>/`. Inside:

```
episode.json           manifest (public summary, scene order, in-game date)
scenes/                public scenes — revealed to players during play
dm/                    ⚠ DM-only: twists, hidden NPCs, encounter design
maps/                  (optional) hand-drawn maps with fog regions (v2 feature)
```

The numeric prefix is just for ordering. Episodes do not need to be played in numeric order; the `prerequisites` field in `episode.json` describes any actual dependencies.

[`000-template/`](000-template/) is a template showing the structure. It is not a playable episode.
