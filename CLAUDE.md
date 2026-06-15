# CLAUDE.md

Guidance for Claude Code (and any LLM agent) working in this repo. This file is
the **schema** in the [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
sense: it is loaded every session and tells you what this project is, how to work
on it, and how the companion wiki under [`wiki/`](wiki/) is organized and maintained.

Keep this file short and scannable. Depth lives in the wiki; point to it, don't
duplicate it here.

---

## 1. What this project is

**Shift Scheduler — Technical Support.** A tiny, zero-backend web app that shows a
5-person support team's rotating shift schedule and reshuffles the rotation every
5 weeks under fairness constraints.

- **Static site** (`docs/index.html`) served by **GitHub Pages**, reading state from
  `docs/state.json` at runtime.
- **Reshuffle logic** (`reshuffle.py`) run by a **GitHub Actions** workflow
  (`.github/workflows/reshuffle.yml`), which commits the updated `state.json` back.
- No build step, no dependencies beyond the Python standard library, no server.

The team and UI strings are in **Indonesian**; keep that language for user-facing
copy. Shifts: **S1** = 06:00–14:00 (morning), **S2** = 13:00–21:00 (evening),
**LIBUR** = day off.

## 2. Repo map

```
reshuffle.py                     # Reshuffle algorithm + fairness constraint (entry point)
docs/
  index.html                     # The web app (vanilla JS, no framework)
  state.json                     # Source of truth for current cycle + order + history
.github/workflows/reshuffle.yml  # Manual/cron workflow that runs reshuffle.py
README.md                        # Human-facing setup + operations guide (Indonesian)
wiki/                            # LLM-maintained knowledge base (see §4)
```

> Note: a stray directory literally named `{.github` (containing `workflows,docs}`)
> exists from a botched `mkdir -p {.github/workflows,docs}` that did not brace-expand.
> It is empty and unused — safe to delete. Do not add files to it.

## 3. Working on the code

There is no test suite and nothing to install.

```bash
python3 reshuffle.py            # Run a reshuffle locally (mutates docs/state.json)
python3 -m http.server -d docs  # Preview the web app at http://localhost:8000
```

Conventions and gotchas (full detail in the wiki):

- **`PATTERN` is duplicated** in both `reshuffle.py` and `docs/index.html` (currently in
  sync with the source spreadsheet). If you change the shift pattern, change it in
  **both** places or they will disagree. See [[shift-patterns]] and [[jadwal-xlsx]].
- The schedule is keyed by **position (0–4), not by person.** A person's shifts are
  determined entirely by their index in `state.json["order"]`. See [[positions-and-people]].
- Reshuffle preserves a **seat-based shift-continuity constraint**: whoever sits in a
  seat that works Sunday of Week 5 keeps their shift family (or gets `LIBUR`) on Monday
  of Week 1. No names are hard-coded. See [[constraints]] and [[reshuffle-algorithm]].
- `state.json` is **machine-written** by the Actions bot; edit it by hand only with
  care and keep `cycle`, `order`, `history`, and `last_reshuffled` consistent. See
  [[state-json]].

Before changing behavior, read the relevant wiki page; after changing behavior,
update that page and append to [[log]] (see §5).

## 4. The wiki

[`wiki/`](wiki/) is a persistent, interlinked knowledge base **you maintain** — the
human curates and asks; you do the bookkeeping. It is Obsidian-compatible.

**Layers**
- **Raw sources** = the code and config in this repo (`reshuffle.py`, `docs/*`, the
  workflow, `README.md`). Treat these as the source of truth; the wiki summarizes and
  synthesizes them, it never replaces them.
- **The wiki** = `wiki/**.md`, owned entirely by the agent.
- **The schema** = this file.

**Structure**
```
wiki/
  index.md                # Catalog of every page (content-oriented). Read this first.
  log.md                  # Append-only chronological record (ingest/query/lint).
  overview.md             # Top-level synthesis of the whole system.
  concepts/               # How things work (algorithms, rules, data shapes).
  components/             # One page per code/config artifact.
  entities/               # The people / team.
```

**Page conventions**
- Each page starts with YAML frontmatter: `type`, `tags`, `updated` (ISO date),
  and `sources` (the raw files it derives from).
- Link between pages with Obsidian wikilinks by **filename, no path or extension**:
  `[[reshuffle-algorithm]]`. Link liberally — a link to a page that does not exist
  yet is a valid TODO marker.
- Keep each page focused on one entity/concept/component. Prefer updating an existing
  page over creating a near-duplicate.
- Cite the source file (and line if useful) for non-obvious claims.

## 5. Workflows

Run these on request; they keep the wiki a compounding asset rather than stale notes.

**Ingest** — when code/config changes or a new source is added:
1. Read the changed source.
2. Update the relevant `components/` and `concepts/` pages (and `overview.md` if the
   big picture moved).
3. Update [[index]] if pages were added/removed or summaries changed.
4. Append a dated entry to [[log]].

**Query** — when asked a question about the project:
1. Read [[index]] to locate relevant pages, then drill in.
2. Answer with citations to wiki pages and/or source files.
3. If the answer is reusable (a comparison, a derived table, a discovered
   connection), file it back as a new/updated wiki page so it compounds.

**Lint** — on request, health-check the wiki:
- Contradictions between pages, or claims the code has since superseded.
- Orphan pages (no inbound links) and missing cross-references.
- Concepts referenced but lacking their own page.
- Drift between the two copies of `PATTERN` (a recurring risk here).
Report findings and fix what is safe to fix.

**Log entry format** (keeps `log.md` greppable):
```
## [YYYY-MM-DD] <ingest|query|lint> | <short title>
- what changed / what was asked
- pages touched: [[a]], [[b]]
```
Find recent activity with: `grep "^## \[" wiki/log.md | tail -5`

## 6. House rules

- User-facing strings stay **Indonesian**; code identifiers and the wiki are English.
- Don't introduce dependencies or a build step without being asked — the zero-infra
  property is a feature.
- Commit or push only when the user asks.
- Today's date for new `updated:`/log stamps: use the real current date.
