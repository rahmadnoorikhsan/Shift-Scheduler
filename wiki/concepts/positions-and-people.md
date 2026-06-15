---
type: concept
tags: [data-model, fairness]
updated: 2026-06-15
sources: [reshuffle.py, docs/state.json, docs/index.html]
---

# Positions and People

The single most important idea in this project: **the schedule is keyed by position,
not by person.**

- The shift `PATTERN` is indexed by **position** `0–4` (see [[shift-patterns]]).
- Who works each position is decided by the **`order`** list in [[state-json]], e.g.
  `["Djaloe", "Aji", "Dimas", "Fazri", "Faza"]`.
- A person's index in `order` *is* their position. `order[0]` works position 0,
  `order[1]` works position 1, and so on.

So a person's entire 5-week schedule is determined purely by where they sit in
`order`. The web app makes this explicit: it maps each person to `PATTERN[i]` by
their index `i` (see [[web-app]]).

## Why this matters

Reshuffling is just **permuting `order`** — nobody's pattern changes, only which
person is attached to each position. This is what makes fairness tractable: you reason
about the five fixed positions, then shuffle people across them. See
[[reshuffle-algorithm]].

## Per-position boundary shifts (verified)

The [[constraints]] depend on two boundary cells per position: the last day of the
current cycle and the first day of the next. Computed from the matrix:

| Position | Week-5 Sunday (cycle end) | Week-1 Monday (next cycle start) |
|---|---|---|
| 0 | `S2` | `S2` |
| 1 | `S1` | `S1` |
| 2 | `LIBUR` | `LIBUR` |
| 3 | `LIBUR` | `S1` |
| 4 | `LIBUR` | `S2` |

These map to the helpers `week5_sunday_shift(position)` and
`week1_monday_shift(position)` in [[reshuffle-py]], and are exactly the values the
continuity rule checks. See [[constraints]].
