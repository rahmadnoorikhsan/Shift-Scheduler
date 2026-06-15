---
type: overview
tags: [architecture, synthesis]
updated: 2026-06-15
sources: [reshuffle.py, docs/index.html, docs/state.json, .github/workflows/reshuffle.yml, README.md]
---

# Overview

**Shift Scheduler** is a zero-backend tool that publishes a 5-person Technical
Support team's rotating shift schedule and reshuffles who-sits-where every five
weeks under a fairness constraint. It runs entirely on GitHub primitives: a static
page on GitHub Pages plus a GitHub Actions job — no server, no database, no
dependencies beyond the Python standard library.

The schedule's source of truth is the spreadsheet [[jadwal-xlsx]]; the deployed app
implements its "Shift Weekend Coverage (5P)" sheet (one known one-cell drift — see
[[shift-patterns]]). Day-to-day operations are governed by the [[sop]].

## The mental model in one paragraph

There is a fixed **shift pattern** for five **positions** over a 5-week cycle
(see [[shift-patterns]]). People are assigned to positions by an **order** list
(see [[positions-and-people]]). The web app renders the current order against the
pattern (see [[web-app]]). At the end of a 5-week cycle the **reshuffle** randomizes
the order — subject to a continuity **constraint** for two people — and writes the new
order back to `state.json` (see [[reshuffle-algorithm]], [[constraints]], [[state-json]]).
The page re-reads `state.json` and shows the new rotation (see [[deployment-pipeline]]).

## Data flow

```
                        manual click / Sunday cron
                                   │
                                   ▼
     .github/workflows/reshuffle.yml  ──runs──►  reshuffle.py
     [[workflow]]                                [[reshuffle-algorithm]]
                                   │                     │
                                   │            reads + rewrites
                                   ▼                     ▼
                          git commit + push ───►  docs/state.json
                                                  [[state-json]]
                                                         │
                                          GitHub Pages serves docs/
                                                         ▼
                                          docs/index.html (fetch state.json)
                                          [[web-app]]  ──►  rendered schedule
```

## Components at a glance

| Artifact | Role | Page |
|---|---|---|
| `reshuffle.py` | Reshuffle algorithm + the canonical `PATTERN` | [[reshuffle-py]] |
| `docs/state.json` | Current cycle, order, history, timestamp | [[state-json]] |
| `docs/index.html` | Static viewer (its own copy of `PATTERN`) | [[web-app]] |
| `.github/workflows/reshuffle.yml` | Manual/cron trigger that runs the script | [[workflow]] |

## Key invariants & risks

- **Two copies of `PATTERN`** (Python + JS) must stay identical. Currently in sync and
  matching [[jadwal-xlsx]], but there is no shared source — still the likeliest bug
  source. See [[shift-patterns]].
- **Position, not person, drives shifts.** All fairness reasoning is about which
  position a person lands in after a reshuffle — see [[positions-and-people]].
- **Continuity constraint is seat-based.** It binds whoever occupies a working-Sunday
  seat (today seats 0/1 = `Djaloe`/`Aji`) and follows those seats across reshuffles —
  see [[constraints]] and [[team]].
- `state.json` is **bot-written**; hand edits must keep its fields consistent —
  see [[state-json]].
