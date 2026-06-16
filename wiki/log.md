---
type: log
tags: [meta, history]
updated: 2026-06-15
sources: []
---

# Wiki Log

Append-only, chronological record of work on this wiki — ingests, queries, and lint
passes. Newest at the bottom. Each entry starts with `## [YYYY-MM-DD]` so the log
stays greppable:

```bash
grep "^## \[" wiki/log.md | tail -5
```

---

## [2026-06-15] ingest | Initialize wiki from the codebase
- Bootstrapped the LLM Wiki (Karpathy pattern) for the Shift Scheduler project.
- Read all raw sources: `reshuffle.py`, `docs/index.html`, `docs/state.json`,
  `.github/workflows/reshuffle.yml`, `README.md`.
- Created the schema [`/CLAUDE.md`](../CLAUDE.md) and the initial wiki structure
  (`concepts/`, `components/`, `entities/`, plus `index.md`, `log.md`, `overview.md`).
- Derived and verified the per-position shift boundaries (week-5 Sunday end vs.
  week-1 Monday start) that the [[constraints]] depend on; recorded them in
  [[positions-and-people]] and [[constraints]].
- Documented the duplicated `PATTERN` (in `reshuffle.py` and `index.html`) as a
  standing drift risk — see [[shift-patterns]].
- Noted a stray empty directory `{.github` from a botched `mkdir` as safe to delete.
- Pages touched: [[index]], [[overview]], [[shift-patterns]], [[positions-and-people]],
  [[reshuffle-algorithm]], [[constraints]], [[deployment-pipeline]], [[reshuffle-py]],
  [[state-json]], [[web-app]], [[workflow]], [[team]].

## [2026-06-15] ingest | Spreadsheet JADWAL SHIFT TS FULL COVERAGE.xlsx
- Ingested the authoritative source workbook (5 sheets: SOP, `Shift`, `Shift Off 1D`,
  Weekend Coverage `4P`, Weekend Coverage `5P`). Created [[jadwal-xlsx]] and [[sop]].
- Confirmed the deployed app implements the **5P** sheet; recorded the divergent shift
  hours of the 24/7 schemes (S1 07–15 / S2 15–23 / S3 23–07) vs. weekend coverage
  (S1 06–14 / S2 13–21).
- Captured the user's constraint rule + worked example (Aji→seats 2/3/4, Djaloe→seats
  1/3/5); verified it matches the code and the 5P data. Updated [[constraints]] and
  [[reshuffle-algorithm]].
- Corrected [[shift-patterns]]: the authoritative matrix is a clean R1–R5 rotation
  (pos 0 starts on R5); the "R0" in code is a one-cell typo of R5.
- **FINDING (open):** code `PATTERN[0][0][1]` = `S1` but xlsx = `S2` (pos 0 / Week 1 /
  Tuesday). Present in both `reshuffle.py` and `index.html`; does not affect constraint
  logic. Fix = set that cell to `"S2"` in both files. Awaiting user go-ahead.
- **QUESTION (open):** constraint anchors by name (`Djaloe`/`Aji`) vs. by working-shift
  seat (0/1). Matches intent for cycle 1; may diverge after reshuffles. See [[constraints]].
- Pages touched: [[index]], [[overview]], [[shift-patterns]], [[constraints]],
  [[reshuffle-algorithm]], [[team]], [[jadwal-xlsx]], [[sop]].

## [2026-06-15] ingest | Code change — fix cell + seat-based constraint
- (a) Fixed the one-cell drift: `PATTERN[0][0][1]` `S1`→`S2` in **both** `reshuffle.py`
  and `docs/index.html`. Both copies now match [[jadwal-xlsx]] (verified equal).
- (b) Reworked the constraint to be **seat-based, not name-based**. Added
  `WORKING_SHIFTS` and `allowed_monday_shifts(order)` in `reshuffle.py`; removed all
  `Djaloe`/`Aji` literals from the logic. Anyone in a working-Sunday-W5 seat keeps
  their shift family (or `LIBUR`) on Monday W1; the rule follows the seats each cycle.
- Verified: constraint held across **4800 reshuffles over all 120 start orders**;
  output always a changed permutation; user's example accepted; cycle-2 demo shows the
  constrained pair shift from Djaloe/Aji to Dimas/Fazri automatically.
- Updated [[constraints]], [[reshuffle-algorithm]], [[reshuffle-py]], [[team]],
  [[overview]], [[shift-patterns]], [[jadwal-xlsx]], [[index]], `/CLAUDE.md`, and the
  Indonesian `README.md` constraint section.
- Resolved the two open items from the previous entry (display drift; name-vs-seat).
- Not committed; `docs/state.json` not mutated (no reshuffle run).

## [2026-06-15] ingest | Web dashboard rebuilt as a spreadsheet replica
- Rewrote `docs/index.html` to look and act like the Excel "Shift Weekend Coverage
  (5P)" sheet: title banner, color legend, one table per week with columns
  `Personil | Sen…Min | Hari Kerja`. Goal: the web page replaces the .xlsx.
- Extracted the spreadsheet's true conditional-formatting colors and matched them
  exactly: S1 `#C6E0B4`, S2 `#FFE699`, LIBUR `#F4B084`, Hari Kerja `#B4C7E7`.
- Kept the dynamic engine: fetch `state.json` (cache-busted, 5-min auto-refresh) and
  map `order[i] → PATTERN[i]`, so a refresh after reshuffle re-renders the whole sheet.
- Verified in a headless preview: PATTERN parity with `reshuffle.py` holds, computed
  cell colors are byte-exact, and a simulated reshuffled order re-maps names onto the
  seat patterns correctly.
- Added `.claude/launch.json` (local static-server preview helper; not committed yet).
- Pages touched: [[web-app]], [[index]] (no summary change needed), [[jadwal-xlsx]].
