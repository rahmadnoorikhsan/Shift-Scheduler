---
type: concept
tags: [infrastructure, ci, github]
updated: 2026-06-15
sources: [.github/workflows/reshuffle.yml, docs/index.html, docs/state.json, README.md]
---

# Deployment Pipeline

The whole system runs on two free GitHub primitives and one JSON file. There is no
server and no build step.

## The pieces

- **GitHub Pages** serves the `docs/` folder of `main` as a static site. `index.html`
  is the app; `state.json` is fetched at runtime. See [[web-app]].
- **GitHub Actions** (`.github/workflows/reshuffle.yml`) runs `reshuffle.py`, then
  commits and pushes the updated `state.json` back to `main`. See [[workflow]].
- **`docs/state.json`** is the hand-off between them — written by the action, read by
  the page. See [[state-json]].

## Flow

```
trigger (manual "Run workflow" / Sunday 23:00 WIB cron)
   └─► Actions: checkout → setup Python 3.12 → python reshuffle.py
          └─► reshuffle.py rewrites docs/state.json   (see [[reshuffle-algorithm]])
                 └─► bot commits "chore: reshuffle siklus N" and pushes to main
                        └─► Pages redeploys docs/
                               └─► index.html fetch('state.json') shows new order
```

The page also auto-refreshes `state.json` every 5 minutes, so a tab left open updates
itself shortly after a workflow run completes.

## One-time setup (per README)

1. **Settings → Pages**: deploy from branch `main`, folder `/docs`.
2. **Settings → Actions → General → Workflow permissions**: "Read and write
   permissions" (so the bot can push `state.json`). The workflow also declares
   `permissions: contents: write`.

## Triggers

- **Manual** (recommended): Actions tab → "Reshuffle Jadwal Shift" → Run workflow →
  type `reshuffle` to confirm. The confirmation gate lives in the workflow.
- **Cron**: `0 16 * * 0` (Sunday 16:00 UTC = 23:00 WIB). ⚠️ As written this fires
  **every** Sunday, not every 5th week — the "only at end of cycle" check described in
  comments/README does **not** exist in `reshuffle.py` yet. See [[workflow]] and
  [[reshuffle-py]] for this gap.
