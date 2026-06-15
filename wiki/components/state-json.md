---
type: component
tags: [data, state]
updated: 2026-06-15
sources: [docs/state.json, reshuffle.py, docs/index.html]
---

# `docs/state.json`

The runtime source of truth and the hand-off between [[reshuffle-py]] (writer) and
[[web-app]] (reader). See [[deployment-pipeline]].

## Shape

```json
{
  "cycle": 1,
  "order": ["Djaloe", "Aji", "Dimas", "Fazri", "Faza"],
  "history": [
    { "cycle": 1, "order": ["Djaloe", "Aji", "Dimas", "Fazri", "Faza"] }
  ],
  "last_reshuffled": null
}
```

| Field | Type | Meaning |
|---|---|---|
| `cycle` | int | Current cycle number; incremented on each reshuffle. |
| `order` | string[5] | Person→position mapping; index = position. See [[positions-and-people]]. |
| `history` | object[] | Append-only `{cycle, order}` log of every order. |
| `last_reshuffled` | string\|null | UTC ISO timestamp of the last reshuffle; `null` before the first. |

## Lifecycle

- Written by `main()` in [[reshuffle-py]] with `json.dumps(..., indent=2,
  ensure_ascii=False)`, then committed/pushed by [[workflow]].
- Read by `loadState()` in [[web-app]] via `fetch('state.json?t=' + Date.now())`
  (cache-busting), re-fetched every 5 minutes.

## Editing by hand

Possible but do it carefully — keep the fields mutually consistent:
- `order` must contain exactly the five known names (the constrained ones,
  `Djaloe`/`Aji`, must be present or [[reshuffle-py]] will raise on `.index`).
- After any change to `order`, the matching cycle should also be appended to
  `history`, and `cycle` kept in sync.
- It is normally **bot-written**; manual edits risk being overwritten by the next
  workflow run.
