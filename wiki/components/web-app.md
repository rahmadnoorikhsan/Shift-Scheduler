---
type: component
tags: [frontend, html, javascript]
updated: 2026-06-15
sources: [docs/index.html]
---

# `docs/index.html`

The entire front end: a single self-contained HTML file (inline CSS + vanilla JS, no
framework, no build). Served by GitHub Pages — see [[deployment-pipeline]]. As of
2026-06-15 it is styled as a **spreadsheet replica** of the "Shift Weekend Coverage
(5P)" sheet in [[jadwal-xlsx]] — the web page is meant to fully replace the Excel file.

## What it renders

From [[state-json]] it draws:
- A **title banner** + a meta line (active **cycle**, current **order**, last
  reshuffled date in Indonesian locale).
- A **color legend**: `S1 · 06:00–14:00`, `S2 · 13:00–21:00`, `LIBUR · OFF`.
- **One table per week** (`Minggu 1`–`Minggu 5`), each with columns
  `Personil | Sen | Sel | Rab | Kam | Jum | Sab | Min | Hari Kerja`. The `Hari Kerja`
  cell shows the count of non-`LIBUR` days (always `5 hari` for this pattern).
- A **reshuffle history** list (only when more than one cycle exists) and an info box
  on how to trigger a reshuffle.

## Excel-faithful colors

Cell fills match the spreadsheet's conditional formatting exactly (CSS variables):

| Value | Color | Hex |
|---|---|---|
| `S1` | green | `#C6E0B4` |
| `S2` | yellow | `#FFE699` |
| `LIBUR` | orange | `#F4B084` |
| `Hari Kerja` ("5 hari") | blue | `#B4C7E7` |

Header rows use `#D9D9D9`, "Minggu N" bands use `#44546A`, the title bar `#305496` —
a light, Excel-like theme (no dark mode, to keep the colors faithful).

## How it works

- `PATTERN` (the schedule matrix) is **hard-coded here** as a JS const — ⚠️ a second
  copy of the matrix in [[reshuffle-py]]. They must match. See [[shift-patterns]].
- `loadState()` fetches `state.json` (cache-busted), calls `render(state)`, and is
  re-run every 5 minutes via `setInterval`.
- Person→schedule mapping is by index: row `i` of `order` is rendered against
  `PATTERN[i]`. So after a reshuffle, refreshing the page re-maps the new names onto
  the fixed seat patterns automatically. See [[positions-and-people]].
- On fetch failure it shows an inline error; while loading it shows "Memuat jadwal…".

## Gotchas

- Because the schedule comes from a static `PATTERN`, the app shows the pattern for
  whatever order is in `state.json`; it never computes shifts itself beyond indexing.
- All user-facing text is Indonesian — keep it that way.
- Local preview: `python3 -m http.server -d docs` (or the `.claude/launch.json`
  config) so `index.html` and `state.json` are served together.
