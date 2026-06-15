---
type: component
tags: [ci, github-actions, yaml]
updated: 2026-06-15
sources: [.github/workflows/reshuffle.yml]
---

# `.github/workflows/reshuffle.yml`

GitHub Actions workflow "Reshuffle Jadwal Shift" — the CI trigger that runs
[[reshuffle-py]] and pushes the result. See [[deployment-pipeline]].

## Triggers

- `workflow_dispatch` with a required `confirm` input — **manual** run from the
  Actions tab. The recommended interface.
- `schedule: cron: '0 16 * * 0'` — **every Sunday** 16:00 UTC (23:00 WIB).

## Job: `reshuffle` (ubuntu-latest)

Declares `permissions: contents: write` so the bot can push.

1. **Checkout** (`actions/checkout@v4`).
2. **Confirmation gate** (manual runs only): fails unless `inputs.confirm == "reshuffle"`.
3. **Setup Python** 3.12 (`actions/setup-python@v5`).
4. **Run** `python reshuffle.py` (rewrites `docs/state.json`).
5. **Commit & push**: configures the `github-actions[bot]` identity, `git add
   docs/state.json`, commits only if there is a diff, with message
   `chore: reshuffle siklus <N>` (N read back from `state.json`), then pushes.

## ⚠️ Behavior gap

The confirmation gate guards only the **manual** path. The **cron** path runs
`reshuffle.py` directly, and the script has **no end-of-cycle check** (see
[[reshuffle-py]]). So as written, the cron would reshuffle **every Sunday**, not every
5 weeks. Until a cycle check is added to `reshuffle.py`, prefer manual triggering, or
disable/adjust the cron. This is the headline lint item — see [[log]].
