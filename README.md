# Underleaf

Sample campaign for the [Quire](https://github.com/gutschke/quire) TTRPG framework.

> **Status: in development.** Not yet playable. The structure and design are landing; campaign content (episodes, NPCs, bestiary, places) will accumulate over time.

---

## If you are or might become a player — read this first

Underleaf is a story-driven game whose pleasure comes from gradual discovery. Most of what makes the campaign work happens *because the players don't know yet*. The repository is organized so that browsing it casually does not spoil the campaign — but a few folders are deliberately full of spoilers, and they are clearly labeled.

**The short version:**

- **Safe to browse:** this README, [`world/overview.md`](world/overview.md), the `characters/pcs/` folder (these are *your* characters), and any `scenes/` folder *for episodes that you have already played*.
- **Do not browse:** any folder named `dm/`, the [`design/DM-ONLY/`](design/) folder, and any episode's `scenes/` for episodes you have not yet played.
- If you absolutely want to read up on the campaign anyway, that's nothing new for tabletop games and the DM cannot stop you — but please make it a deliberate choice rather than stumbling in by accident. The fun is in the discovery.

Folders that contain spoiler material have prominent warning headers at the top of the README and at the top of every file inside.

## What this is

Underleaf is set in a contemporary-feeling world that looks much like our own. The players are young adults — students, junior professionals, hobbyists, dropouts, the people who *notice things*. The world has surprises in it, but the players will learn about them through play rather than reading ahead.

The system mechanics live in [`world/rules.md`](world/rules.md). Quire is the runtime; Underleaf is the content (including the rules themselves).

## Playing

Once Quire reaches phase 1 of development, this campaign will be playable at:

<https://play.quire.games?campaign=gutschke/underleaf>

Until then, you can read the public files here and follow along.

## Editing

Players and DMs are expected to edit their character sheets and other public records freely. The Quire runtime provides an in-browser editor for every record type — you should rarely need to edit files in this repository directly. When you do edit through Quire, your changes can be exported or committed back to a fork.

If you are editing files directly (rather than through the runtime), the [Quire schemas](https://github.com/gutschke/quire/tree/main/schema/v0) describe the recognized shape of each record type.

## Repository layout

```
README.md                  this file
campaign.json              manifest
world/                     public world overview (PC-eye view)
characters/
  pcs/                     player characters — public, players edit
  npcs/                    non-player characters — see folder README
bestiary/                  threats and creatures
items/                     objects, equipment, focus candidates
spells/                    documented patterns — see folder README
episodes/                  episode arcs
  000-template/            template showing the structure
  001-…/                   actual episodes as they are written
    scenes/                public scenes (no spoilers for played episodes)
    dm/                    ⚠ DM-only spoilers, encrypted in published forks
design/                    design and arc notes
  DM-ONLY/                 ⚠ DM-only — campaign spoilers
sessions/                  post-session summaries (the past is shareable)
```

## Forking

You can fork Underleaf to build your own campaign:

1. **Just change the content.** Copy this repo, swap in your own NPCs, places, episodes. Players visit `play.quire.games?campaign=your-name/your-fork`.
2. **Run your own runtime, too.** See [Quire's architecture doc](https://github.com/gutschke/quire/blob/main/design/architecture.md#three-forking-modes) for the self-host path.

When you fork, the DM-only files come along — the encryption tooling that protects them at rest will land in phase 1 of Quire.

## License

Content: CC-BY-SA 4.0 (see [LICENSE](LICENSE)).
Any code or tooling in this repo: MIT.
