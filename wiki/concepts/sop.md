---
type: concept
tags: [operations, sop, policy]
updated: 2026-06-15
sources: [JADWAL SHIFT TS FULL COVERAGE.xlsx]
---

# SOP — Shift Management

Operating procedure from the `SOP Manajemen Shift` sheet of [[jadwal-xlsx]]
(v1.0, Februari 2026). Written for a **6-person, 24/7** operation, so it is broader
than the deployed 5-person weekend-coverage [[web-app]] — treat it as the team's
governing policy, not as something the code enforces. None of this is implemented in
code today; it is human process.

## A. Backup (sick / sudden leave)
- Report **≥ 4 hours** before shift to the Lead via the official WhatsApp group.
- Replacement priority: (a) someone OFF that day, (b) someone who just finished a shift
  (min 8-hour gap), (c) someone from the next working day (shift swapped).
- Wed–Fri (double coverage) gaps may be covered by split-shift / overtime.
- Every substitution is logged (Date, Absentee, Reason, Replacement, Shift, Lead
  approval).
- Compensation: 1 replacement OFF day **or** overtime pay per company policy.

## B. Fair rotation on national holidays
- National OFF days follow the normal rotation — no automatic change.
- Working a public holiday earns **+1 "OFF Nasional" point** per red-date worked.
- Accumulated points set priority for extra leave/OFF (highest points choose first).
- Points are tallied each quarter by the Lead and shared with the team.
- Ties broken by: (a) who last got a holiday OFF, (b) open draw if still tied.

## C. Shift-swap rules
- Allowed only between staff with **written consent** of both parties + Lead approval.
- Request **≥ 3 days (H-3)** ahead.
- Prohibited if it makes anyone work **>2 consecutive shifts (>16h)** without an
  8-hour break.
- Submitted via a Shift-Swap form (Date, From shift, To shift, Requester, Swap partner,
  Reason, digital signature).
- Lead may reject a swap that unbalances per-shift competency (e.g. two juniors, no
  senior).

## D. General provisions
- Every member must read and sign the SOP.
- Violations are logged and reviewed monthly; **3 violations = warning letter**.
- SOP reviewed every 6 months or whenever headcount / shift pattern changes.

## Relation to the rest of the wiki
- The automatic [[reshuffle-algorithm]] and its [[constraints]] are about *generating*
  the rotation; this SOP is about *running* it day-to-day (absences, swaps, holidays).
- The "6 personil" framing here hints at a future/parallel scheme; the deployed app is
  5-person — see [[team]] and [[jadwal-xlsx]].
