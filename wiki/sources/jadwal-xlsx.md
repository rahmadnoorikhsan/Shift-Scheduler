---
type: source
tags: [source-of-truth, spreadsheet, schedule]
updated: 2026-06-15
sources: [JADWAL SHIFT TS FULL COVERAGE.xlsx]
---

# Source: `JADWAL SHIFT TS FULL COVERAGE.xlsx`

The **authoritative reference** for the team's schedules and operating rules, ingested
2026-06-15. The deployed app implements exactly one of its sheets — "Shift Weekend
Coverage (5P)". The other sheets are planning artifacts / alternative schemes for
different team sizes and coverage models.

## Sheets

| Sheet | Personil | Shifts | Cycle | Relation to the app |
|---|---|---|---|---|
| `SOP Manajemen Shift` | 6 | — | — | Operating procedure (backup, holiday points, swaps). See [[sop]]. |
| `Shift` | 6 (Personil 1–6) | S1/S2/S3, 24/7 | 6 weeks | Pure staggered rotation, weekend-block off. Not deployed. |
| `Shift Off 1D` | 6 (Personil 1–6) | S1/S2/S3, 24/7 | 6 weeks | Same team, single-day-off pattern (offs scattered). Not deployed. |
| `Shift Weekend Coverage (4P)` | 4 (drops Faza) | S1/S2 | 5 weeks | Two-shift weekend-coverage variant. Not deployed. |
| **`Shift Weekend Coverage (5P)`** | **5 (named)** | **S1/S2** | **5 weeks** | **The deployed scheme** — see [[shift-patterns]]. |

## Shift hours differ by scheme

- **24/7 schemes** (`Shift`, `Shift Off 1D`): `S1` 07:00–15:00, `S2` 15:00–23:00,
  `S3` 23:00–07:00, `OFF`.
- **Weekend Coverage** (`4P`, `5P`): `S1` 06:00–14:00, `S2` 13:00–21:00, `LIBUR`.
  These are the hours shown in the deployed [[web-app]].

## The deployed sheet — "Shift Weekend Coverage (5P)"

Named team `Djaloe, Aji, Dimas, Fazri, Faza` (see [[team]]) over a 5-week cycle. It is
a **clean staggered rotation** of five weekly archetypes R1–R5 (see [[shift-patterns]]):
position 0 starts on R5, each subsequent position one week ahead. Week-5 Sunday vs.
week-1 Monday boundaries match the [[constraints]] rule the user described.

## Key finding (resolved 2026-06-15): code vs. source drift

The `PATTERN` in [[reshuffle-py]] and [[web-app]] matched this sheet everywhere except
one cell — position 0 (then Djaloe), Week 1, Selasa: code had `S1`, the xlsx has `S2`.
`PATTERN[0][0][1]` was corrected to `"S2"` in **both** files, so the code now matches
the spreadsheet exactly. The cell never affected the [[constraints]] logic (which uses
only week-1 Monday and week-5 Sunday). See [[log]].
