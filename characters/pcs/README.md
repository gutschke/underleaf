# Player characters

This folder is for *your* characters. Players edit freely. The Quire runtime gives you an in-browser sheet — you should rarely need to touch the files directly.

## Creating a character

The PC schema is documented in [Quire's schema docs](https://github.com/gutschke/quire/tree/main/schema/v0). At minimum a PC needs a `name`; everything else is optional. A typical starting PC has:

- A name and pronouns.
- An alignment (one of nine — Lawful/Neutral/Chaotic crossed with Good/Neutral/Evil). Binding, but it can evolve through play.
- A stat block (STR/DEX/CON/INT/WIS/CHA, default array: one +2, three +1s, two 0s).
- A skill category they're good at, plus 3-5 free-text tags from their background.
- A backstory in Markdown.

## A note on backstory

There is a specific question your backstory should answer, even if obliquely:

> **What in your life taught you to hold an intention against pressure?**

It might be a quiet thing — a parent who taught you to think before agreeing, a year of homesickness that made you find what you actually wanted, a job where standing firm mattered. It might be loud — adversity, betrayal, an experience of being right when everyone else was wrong. It doesn't have to be dramatic. It does have to be specific.

You will not know why this question matters at the start. Trust that it does.

## In-medias-res convention

Underleaf episodes typically open with the PCs already in a scene together, not converging on one. You will not be asked to explain how you all met before play starts. Your backstory exists; your party formation will emerge through play. This is intentional.

## Example

[`example-character.json`](example-character.json) shows a complete PC record at v0.1.0. It is a template, not a canonical NPC.
