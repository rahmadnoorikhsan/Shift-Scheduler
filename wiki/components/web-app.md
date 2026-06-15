---
type: component
tags: [frontend, html, javascript]
updated: 2026-06-15
sources: [docs/index.html]
---

# `docs/index.html`

The entire front end: a single self-contained HTML file (inline CSS + vanilla JS, no
framework, no build). Served by GitHub Pages — see [[deployment-pipeline]].

## What it renders

From [[state-json]] it draws:
- Two summary cards: active **cycle** and **last reshuffled** date (Indonesian
  locale).
- The **current order** as a ranked list, showing each person's week-1 Monday shift.
- The **full 5-week schedule** table (`Minggu 1–5` × `Senin–Minggu`).
- A **reshuffle history** list (shown only when more than one cycle exists).
- An info box explaining how to trigger a reshuffle.

`Djaloe` and `Aji` are visually highlighted (avatar + bold name) because they are the
constrained members — see [[constraints]] and [[team]].

## How it works

- `PATTERN` (the schedule matrix) is **hard-coded here** as a JS const — ⚠️ a second
  copy of the matrix in [[reshuffle-py]]. They must match. See [[shift-patterns]].
- `loadState()` fetches `state.json` (cache-busted), calls `renderApp(state)`, and is
  re-run every 5 minutes via `setInterval`.
- Person→schedule mapping is by index: row `i` of `order` is rendered against
  `PATTERN[i]`. See [[positions-and-people]].
- Theming via CSS custom properties with a `prefers-color-scheme: dark` block.
- On fetch failure it shows an inline error; while loading it shows "Memuat jadwal…".

## Gotchas

- Because the schedule comes from a static `PATTERN`, the app shows the pattern for
  whatever order is in `state.json`; it never computes shifts itself beyond indexing.
- All user-facing text is Indonesian — keep it that way.
