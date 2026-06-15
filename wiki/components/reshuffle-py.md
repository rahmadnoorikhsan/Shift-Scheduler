---
type: component
tags: [python, entry-point]
updated: 2026-06-15
sources: [reshuffle.py]
---

# `reshuffle.py`

The reshuffle entry point. Run by [[workflow]]; can also be run locally with
`python3 reshuffle.py` (it mutates `docs/state.json` in place).

## Responsibilities

1. Holds the canonical `PATTERN` matrix (see [[shift-patterns]]) — ⚠️ duplicated in
   [[web-app]].
2. Computes shift boundaries via helpers:
   - `get_shift(position, week, day)` → a cell of `PATTERN`.
   - `week5_sunday_shift(position)` → `PATTERN[position][4][6]` (cycle end).
   - `week1_monday_shift(position)` → `PATTERN[position][0][0]` (next cycle start).
3. `allowed_monday_shifts(current_order)` → maps each person in a working-Sunday seat
   to their allowed week-1 Monday shifts (`{end_shift, "LIBUR"}`). Seat-based; the
   `WORKING_SHIFTS = {"S1","S2"}` constant defines "working". See [[constraints]].
4. `reshuffle_with_constraint(current_order)` → returns a new permutation satisfying
   the [[constraints]] (the [[reshuffle-algorithm]]). Pure; no I/O.
5. `main()` → loads `state.json`, calls the reshuffler, then bumps `cycle`, sets
   `order`, sets `last_reshuffled` (UTC ISO), appends to `history`, writes the file
   (`indent=2, ensure_ascii=False`), and prints a summary.

## Key facts

- Reads/writes a single file: `STATE_FILE = Path("docs/state.json")` — relative to the
  current working directory, so run it from the repo root. See [[state-json]].
- Standard library only (`json`, `random`, `datetime`, `pathlib`). No dependencies.
- **No names are hard-coded.** The constraint targets working-Sunday *seats*, so it
  adapts to any roster automatically. See [[constraints]] and [[team]].

## Known gaps

- **No "is it end of cycle?" check.** `main()` reshuffles unconditionally whenever it
  runs. The cron in [[workflow]] fires every Sunday, so relying on the schedule would
  reshuffle weekly, not every 5 weeks. The README acknowledges this logic is
  "to be added." Treat manual triggering as the real interface for now.
- No tests.
