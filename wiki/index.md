---
type: index
tags: [meta, navigation]
updated: 2026-06-15
sources: []
---

# Wiki Index

Catalog of every page in this wiki. Read this first when answering a question:
find the relevant pages here, then drill into them. Keep one-line summaries
current on every ingest.

See [[overview]] for the big picture and [[log]] for the chronological record.

## Overview
- [[overview]] — what the system is and how its parts fit together end to end.

## Sources — raw inputs (source of truth)
- [[jadwal-xlsx]] — `JADWAL SHIFT TS FULL COVERAGE.xlsx`: authoritative schedules + SOP.

## Concepts — how it works
- [[shift-patterns]] — the `S1/S2/LIBUR` shift types and the 5×5×7 `PATTERN` rotation matrix.
- [[positions-and-people]] — why the schedule is keyed by position (0–4), not by person.
- [[reshuffle-algorithm]] — random-shuffle-until-valid algorithm that rotates the order.
- [[constraints]] — the seat-based shift-continuity rule enforced on reshuffle.
- [[deployment-pipeline]] — Pages + Actions + `state.json` flow that ships changes.
- [[sop]] — operating procedure (backup, holiday points, shift swaps) from the xlsx.

## Components — one page per artifact
- [[reshuffle-py]] — `reshuffle.py`, the reshuffle entry point and pattern source.
- [[state-json]] — `docs/state.json`, the runtime source of truth.
- [[web-app]] — `docs/index.html`, the static viewer.
- [[workflow]] — `.github/workflows/reshuffle.yml`, the CI trigger.

## Entities
- [[team]] — the five Technical Support staff and their roles in the rules.

## Conventions
- Pages carry YAML frontmatter (`type`, `tags`, `updated`, `sources`).
- Links use Obsidian wikilinks by filename: `[[reshuffle-algorithm]]`.
- The schema and workflows live in [`/CLAUDE.md`](../CLAUDE.md), not here.
