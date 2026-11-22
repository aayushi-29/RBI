# Data currency alert: the RBI KYC Master Direction (2016) has been repealed

**Severity: high. Affects the source instrument for the majority of the benchmark (the
`rbi_kyc` scenario tag covers 90 of 127 items — see `docs/STRATIFICATION_GAP_ANALYSIS.md`).**

Researched and self-verified 2026-11-22 against primary RBI sources (not secondary commentary
alone) while investigating Conflict Candidate 1. This is a new finding, not something flagged
in any existing doc, and it's significant enough that it shouldn't sit buried in a research
log — hence its own file.

## The finding

Every `RBI-KYC-*` obligation in `data/obligations/obligations.jsonl` cites, as its source
instrument, the **Master Direction – Know Your Customer (KYC) Direction, 2016**
(DBR.AML.BC.No.81/14.01.001/2015-16, 25 February 2016), via `source_url`
`https://www.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=11566` or equivalent.

**That instrument has been repealed.** Primary-source confirmation: RBI notification
RBI/2025-26/101 (CO.DPSS.POLC.No.S-955/02-30-010/2025-26), dated 28 November 2025, addressed to
all Payment System Providers and Participants, states directly: *"The Reserve Bank has, today,
repealed the RBI Master Direction DBR.AML.BC.No.81/14.01.001/2015-16 dated February 25, 2016 (as
updated from time to time) with immediate effect."* Independent secondary confirmation
(taxguru.in, 2025): *"The Reserve Bank of India has repealed the 2016 Master Direction on KYC
and replaced it with the new 'Reserve Bank of India (Commercial Banks – Know Your Customer)
Directions, 2025', effective immediately."*

**What replaced it is not one direction, but several, split by entity type** — each with its
own notification number, dated 28 November 2025, each with a "Chapter XI – Repeal and Other
Provisions" section:
- Reserve Bank of India (Commercial Banks – Know Your Customer) Directions, 2025
  (RBI/DOR/2025-26/169, DOR.AML.REC.No.88/14.01.002/2025-26)
- Reserve Bank of India (Small Finance Banks – Know Your Customer) Directions, 2025
  (RBI/DOR/2025-26/200, DOR.AML.REC.No.119/14.01.007/2025-26)
- Reserve Bank of India (Payments Banks – Know Your Customer) Directions, 2025
- Reserve Bank of India (Rural Co-operative Banks – Know Your Customer) Directions, 2025
- (likely others — Local Area Banks at minimum; this list is not yet exhaustively confirmed)

**Paragraph numbering has shifted between the old and new instruments.** The 2016 Master
Direction's small-account carve-out referenced "paragraph 23 of Chapter VI" (matches the
catalog's own `RBI-KYC-PARA2-SMALL-ACCOUNT-PROVISO` relation and `TAARR-DRAFT-0005`). The new
2025 entity-specific directions (checked: Small Finance Banks id=13109, Payments Banks id=13090)
instead say *"Provided that this rule shall not apply to 'small accounts' referred to in
**paragraph 28** of Chapter VI."* Same substantive carve-out, different paragraph number. Every
`clause_id` in the catalog that cites a specific paragraph number against the 2016 Master
Direction is at risk of this same drift once checked against its entity-specific 2025
successor.

## Why this matters for TAARR specifically

TAARR's own novelty claim is clause/version-level provenance and *temporal validity* — "which
version of a clause applied on a reference date." A repealed source instrument, cited as
currently authoritative for 90 benchmark items without any `effective_to` date reflecting the
repeal, is exactly the kind of staleness the engine is supposed to catch and didn't, because
the catalog itself was never updated to reflect it. This is a genuine temporal-validity gap in
the data, not the engine — the engine would resolve these items correctly *against the data as
given*; the data no longer reflects reality as of 28 November 2025.

## Correction (2026-11-22, same day): the current 127 gold items are NOT affected

The first draft of this document assumed, without checking, that the 32 items dated
`reference_date: 2026-08-01` were `rbi_kyc` items and therefore the group needing re-checking
against the repeal. **That assumption was wrong, and checking it directly reverses the
conclusion:**

```
rbi_kyc items:   90, date distribution: {'2025-09-01': 87, '2025-07-01': 3}
sebi_lodr items: 37, date distribution: {'2026-08-01': 32, '2025-06-01': 3, '2023-05-01': 2}
```

**All 32 items dated `2026-08-01` are `sebi_lodr` items, not `rbi_kyc`.** Every single one of
the 90 `rbi_kyc` items uses `2025-09-01` or `2025-07-01` — both before the 28 November 2025
repeal. So **none of the current 127 gold_verified benchmark items are affected by this repeal
at all.** The 2016 Master Direction genuinely was the correct, in-force instrument on every
reference date any existing RBI-KYC item actually uses. No gold label needs revisiting on this
account.

This is still a real and useful finding, just not an urgent one for the existing benchmark:

- **It matters for any *future* RBI-KYC item.** Any new draft item (for stratification, or for
  resolving/replacing Candidate 1) with a reference date on or after 2025-11-28 must cite the
  correct 2025 entity-specific successor direction, not the repealed 2016 one — and must pick
  the right successor for its modeled entity type (Commercial Banks / Small Finance Banks /
  Payments Banks / Rural Co-operative Banks), which the current catalog's generic
  `"RBI-regulated entity"` subject_scope doesn't distinguish.
- **Whether the entity-specific directions are substantively identical to the 2016 text** for
  the specific clauses the catalog relies on (38(e)'s notice duty, paragraph 2's general
  applicability rule, etc.), beyond the one confirmed paragraph-renumbering example (23 → 28 for
  the small-account carve-out), is still not checked clause by clause.
- It's also a legitimate stratification opportunity in its own right: a benchmark item with a
  reference date straddling 27–28 November 2025 against an `rbi_kyc` obligation would be a
  genuine, real amendment-sensitive temporal test — closing gap #3 in
  `docs/STRATIFICATION_GAP_ANALYSIS.md` (only 1 amendment-sensitive item exists today) with real
  regulatory history instead of a constructed example.

## Recommended next step

Not urgent for the existing gold benchmark. For any new RBI-KYC drafting (Candidate 1's
resolution, or new stratification items), cite the correct 2025 entity-specific successor
instead of the repealed 2016 original, and spot-check whether the specific clauses the catalog
already relies on (paragraph 2, 23/28, 38(e)) carry over with the same substance under the new
numbering. This is a one-time catalog currency sweep for new items, not a redesign of existing
ones — the obligation *content* is probably still substantively
correct, re-citation is the work.
