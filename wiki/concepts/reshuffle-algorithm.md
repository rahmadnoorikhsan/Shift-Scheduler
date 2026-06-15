---
type: concept
tags: [algorithm, fairness]
updated: 2026-06-15
sources: [reshuffle.py]
---

# Reshuffle Algorithm

Every 5-week cycle the team rotates who works which position. This is implemented as
**rejection sampling**: shuffle the `order` randomly, keep the first permutation that
satisfies the [[constraints]].

Defined in `reshuffle_with_constraint(current_order)` in [[reshuffle-py]].

## Steps

1. `allowed_monday_shifts(current_order)`: for each **seat** whose week-5 Sunday is a
   working shift (`S1`/`S2`), record the person there and their allowed next-cycle
   week-1 Monday = `{that shift, LIBUR}`. Seats that end on `LIBUR` add no entry. This
   is seat-based — no names are hard-coded. See [[constraints]].
2. Up to **10,000** times: `random.shuffle` a copy of `order`.
   - Skip a shuffle that equals the current order (the rotation must actually change).
   - Accept the first shuffle where **every** constrained person's new seat gives an
     allowed week-1 Monday shift (`all(...)` over the `allowed` dict).
3. If no valid permutation is found in 10,000 tries, raise
   `RuntimeError("Tidak ditemukan urutan valid ...")`.

## Worked example

```
Before:  1.Djaloe  2.Aji  3.Dimas  4.Fazri  5.Faza
After:   1.Dimas   2.Fazri 3.Faza  4.Aji    5.Djaloe
```
Aji (ended `S1`) lands in seat 4 → Monday `S1` ✅; Djaloe (ended `S2`) lands in seat 5
→ Monday `S2` ✅. See the full slot table in [[constraints]].

## Notes & caveats

- Only the people in **working-Sunday seats** (currently seats 0 and 1 → `Djaloe`,
  `Aji`) are constrained; everyone ending on `LIBUR` can land anywhere. Who is
  constrained moves with the seats each cycle. See [[constraints]] and [[team]].
- With 5 people there are only `5! − 1 = 119` non-identity permutations, so 10,000
  tries is vastly more than enough as long as *some* valid permutation exists. The
  retry cap is a safety net, not a tuning parameter.
- Acceptance is **uniform over valid permutations only in expectation** — it returns
  the first random hit, which is fine for fairness here but is not a guaranteed-uniform
  draw.
- The function is pure: it takes `current_order` and returns a new list. Persistence
  (cycle bump, history append, timestamp, file write) happens in `main()` — see
  [[state-json]] and [[reshuffle-py]].

The whole thing is driven by [[workflow]] and its output is consumed by [[web-app]];
see [[deployment-pipeline]].
