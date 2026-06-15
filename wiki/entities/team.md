---
type: entity
tags: [people, team]
updated: 2026-06-15
sources: [docs/state.json, reshuffle.py, docs/index.html]
---

# Team

The Technical Support team — five people who rotate through the five positions
(see [[positions-and-people]]). Initial order in [[state-json]]:
`Djaloe, Aji, Dimas, Fazri, Faza`. This is the team of the deployed "Shift Weekend
Coverage (5P)" scheme in [[jadwal-xlsx]].

Related schemes in the same workbook use different rosters: the **4P** variant drops
`Faza` (Djaloe, Aji, Dimas, Fazri only), and the 24/7 **6-person** schemes
(`Shift`, `Shift Off 1D`) use generic `Personil 1–6` rather than names. The [[sop]] is
likewise written for a 6-person operation. Only the 5-person scheme is live.

## Members

Whether a person is constrained on a reshuffle depends on their **current seat**, not
their name (see [[constraints]]). In the current order:

| Person | Seat | Ends Sun W5 | Constrained this cycle? |
|---|---|---|---|
| **Djaloe** | 0 | `S2` | ✅ next Monday must be `{S2, LIBUR}`. Highlighted in the UI. |
| **Aji** | 1 | `S1` | ✅ next Monday must be `{S1, LIBUR}`. Highlighted in the UI. |
| **Dimas** | 2 | `LIBUR` | — free |
| **Fazri** | 3 | `LIBUR` | — free |
| **Faza** | 4 | `LIBUR` | — free |

After a reshuffle the constraint follows whoever lands in seats 0 and 1, so the
constrained pair changes each cycle. The exact rule is in [[constraints]]; how it is
applied is in [[reshuffle-algorithm]].

## Roster coupling

The constraint logic is now **name-agnostic** (it targets working-Sunday seats), so no
member is special-cased in code. What *is* still coupled to the roster:

- `order` in [[state-json]] must list exactly the five names; names must be unique
  (the reshuffler uses `list.index`).
- The `PATTERN` is fixed at **5 seats** (see [[shift-patterns]]); adding/removing a
  person means reworking the pattern and `order`. There is no configuration layer yet.
