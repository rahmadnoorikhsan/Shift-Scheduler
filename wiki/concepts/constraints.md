---
type: concept
tags: [fairness, rules]
updated: 2026-06-15
sources: [reshuffle.py]
---

# Constraints

The reshuffle is not a free-for-all: it preserves **shift continuity** across the
cycle boundary. The intent is to avoid whiplash — ending a cycle on an evening rhythm
and starting the next on a morning shift (or vice versa) without a rest day in between.

The rule is **seat-based, not name-based**: it applies to *whoever* occupies a seat
that still works on Sunday of Week 5. Today those are seats 0 and 1 (held by `Djaloe`
and `Aji`), but after a reshuffle the rule automatically follows whoever lands there.

Enforced inside `reshuffle_with_constraint` / `allowed_monday_shifts` in
[[reshuffle-py]]; consumed by the [[reshuffle-algorithm]].

## The rule

For each person, compare the **last shift of the current cycle** (week-5 Sunday at
their current seat) with the **first shift of the next cycle** (week-1 Monday at their
new seat):

- Ends on `S1` (worked the morning) → next start must be `S1` or `LIBUR`.
- Ends on `S2` (worked the evening) → next start must be `S2` or `LIBUR`.
- Ends on `LIBUR` → **no constraint** (they already rested; free to land anywhere).

`LIBUR` always satisfies the rule because a day off is the rest that makes a shift-type
change acceptable.

In code, the allowed week-1 Monday shifts are computed per person from their *current*
seat, and only working-Sunday seats produce an entry:

```python
WORKING_SHIFTS = {"S1", "S2"}

for seat, person in enumerate(current_order):
    end_shift = week5_sunday_shift(seat)
    if end_shift in WORKING_SHIFTS:
        allowed[person] = {end_shift, "LIBUR"}
```

## Boundary values that drive it

The rule reads two cells per seat (verified — see [[positions-and-people]]):

| Seat (0-indexed) | Week-5 Sun (end) | Week-1 Mon (next start) | Constrained? |
|---|---|---|---|
| 0 | `S2` | `S2` | ✅ ends S2 |
| 1 | `S1` | `S1` | ✅ ends S1 |
| 2 | `LIBUR` | `LIBUR` | — free |
| 3 | `LIBUR` | `S1` | — free |
| 4 | `LIBUR` | `S2` | — free |

Only seats 0 and 1 work on Sunday W5, so only the two people in them are constrained
each cycle. Because every seat's week-1 Monday is `S1`, `S2`, or `LIBUR` and `LIBUR`
satisfies everything, valid permutations always exist — the `RuntimeError` fallback in
[[reshuffle-algorithm]] is defensive only.

## Worked example (current cycle)

With `Djaloe` in seat 0 (ends `S2`) and `Aji` in seat 1 (ends `S1`), the week-1 Monday
of each seat decides where each may go (`Personil N` = `order[N-1]`):

| Seat (1-indexed) | Week-1 Monday | OK for Aji (ends S1) | OK for Djaloe (ends S2) |
|---|---|---|---|
| 1 | `S2` | — | ✅ |
| 2 | `S1` | ✅ | — |
| 3 | `LIBUR` | ✅ | ✅ |
| 4 | `S1` | ✅ | — |
| 5 | `S2` | — | ✅ |

So **Aji** may land in seat **2, 3, or 4**; **Djaloe** in seat **1, 3, or 5**.

```
Before:  1.Djaloe  2.Aji  3.Dimas  4.Fazri  5.Faza
After:   1.Dimas   2.Fazri 3.Faza  4.Aji    5.Djaloe
```
- Aji → seat 4 → week-1 Monday `S1` ✅ (ended on `S1`).
- Djaloe → seat 5 → week-1 Monday `S2` ✅ (ended on `S2`).

## Why seat-based matters (next cycle)

In the example above, the new order puts `Dimas` in seat 0 and `Fazri` in seat 1. So
**next** reshuffle the constrained people are `Dimas` (ends `S2`) and `Fazri`
(ends `S1`) — the rule moved with the seats, with no code change. `Djaloe`/`Aji`, now in
LIBUR-ending seats, are free.

Source for the boundary values: [[jadwal-xlsx]] ("Shift Weekend Coverage (5P)").

## Notes

- The rule is fully **generic**: change the team, the names, or the pattern and the
  constraint still targets exactly the working-Sunday seats. No names are hard-coded.
- If a future pattern made *more* seats work on Sunday W5, all of them would be
  constrained automatically.
