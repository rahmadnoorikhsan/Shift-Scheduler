---
type: concept
tags: [schedule, data-model, pattern]
updated: 2026-06-15
sources: [reshuffle.py, docs/index.html]
---

# Shift Patterns

The authoritative definition of this schedule is the "Shift Weekend Coverage (5P)"
sheet of [[jadwal-xlsx]]. The `PATTERN` in code is a copy of it (with one known
discrepancy — see below).

## Shift types

| Code | Meaning | Hours |
|---|---|---|
| `S1` | Morning shift | 06:00–14:00 |
| `S2` | Evening shift | 13:00–21:00 |
| `LIBUR` | Day off | — |

`S1` and `S2` overlap 13:00–14:00, giving "full coverage" 06:00–21:00 (the subtitle
in [[web-app]]).

## The `PATTERN` matrix

The schedule is a fixed 3-D array indexed `PATTERN[position][week][day]`:

- **position**: `0–4` — a seat in the rotation, not a person. See [[positions-and-people]].
- **week**: `0–4` — the five weeks of a cycle (UI labels "Minggu 1–5").
- **day**: `0–6` — `Senin`(Mon) … `Minggu`(Sun).

Each cell is one of `S1` / `S2` / `LIBUR`. Position 0 starts as:

```python
["S2","S1","S2","LIBUR","S1","LIBUR","S1"]   # pos 0, week 0 (Mon..Sun)
```

## Structure: a clean staggered rotation

The authoritative matrix ([[jadwal-xlsx]]) is a **pure rotation** of five reusable
**weekly archetypes** R1–R5. Each position runs all five, phase-shifted by one week;
position 0 simply starts at R5.

| Archetype | Mon–Sun |
|---|---|
| R1 | `S1 S1 S1 S1 LIBUR S2 LIBUR` |
| R2 | `LIBUR S1 S1 S1 S1 S1 LIBUR` |
| R3 | `S1 LIBUR S2 S2 S2 S2 LIBUR` |
| R4 | `S2 S2 LIBUR S2 S2 LIBUR S2` |
| R5 | `S2 S2 S2 LIBUR S1 LIBUR S1` |

Per-position week sequence:

| Position | wk0 | wk1 | wk2 | wk3 | wk4 |
|---|---|---|---|---|---|
| 0 | R5 | R1 | R2 | R3 | R4 |
| 1 | R1 | R2 | R3 | R4 | R5 |
| 2 | R2 | R3 | R4 | R5 | R1 |
| 3 | R3 | R4 | R5 | R1 | R2 |
| 4 | R4 | R5 | R1 | R2 | R3 |

The effect: across a cycle each position works a balanced mix of morning, evening,
and off weeks, and the team collectively covers every day. The reshuffle then rotates
*which person* gets which position next cycle — see [[reshuffle-algorithm]].

> **History (resolved 2026-06-15).** `reshuffle.py` and `index.html` previously encoded
> position 0, week 1 as `S2 S1 S2 LIBUR S1 LIBUR S1` — R5 with Tuesday wrongly set to
> `S1`. That one cell was corrected to `S2` in both files, so the code now matches R5
> and [[jadwal-xlsx]]. There is no real "R0" archetype.

## ⚠️ `PATTERN` is duplicated

The matrix is hard-coded in two places, with **no shared source**:

- `reshuffle.py` (lines ~10–51) — used to compute the [[constraints]].
- `docs/index.html` (the `PATTERN` const, ~line 107) — used to render the table.

As of 2026-06-15 the two copies agree with **each other** and with the authoritative
[[jadwal-xlsx]] (the old one-cell drift at position 0 / week 1 / Tuesday is fixed). But
the duplication itself remains: **if you edit the pattern, edit both copies**, or they
will silently diverge again. This is the standing lint item — see [[log]].
