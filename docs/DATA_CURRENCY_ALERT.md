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

## What is NOT yet established (needs more research, flagged honestly rather than assumed)

- **Whether this affects the 127 gold_verified benchmark items' actual correctness.** Most
  benchmark items use `reference_date: 2025-09-01` (87 items) or `2026-08-01` (32 items) — see
  `docs/STRATIFICATION_GAP_ANALYSIS.md`. The 2025-09-01 items predate the 28 Nov 2025 repeal, so
  for *those* items the 2016 Master Direction genuinely was the correct in-force instrument on
  that reference date — **not an error for those items specifically.** The 32 items dated
  2026-08-01 are reference dates *after* the repeal, and so are exactly the ones that should be
  resolving against the 2025 entity-specific successor directions, not the repealed 2016 one —
  this is the group that needs checking first.
- **Whether the entity-specific directions are substantively identical to the 2016 text** for
  the specific clauses the catalog relies on (38(e)'s notice duty, paragraph 2's general
  applicability rule, etc.), beyond the one confirmed paragraph-renumbering example (23 → 28 for
  the small-account carve-out). Not yet checked clause by clause.
- **Which entity-specific direction applies to which obligation.** The catalog's obligations
  mostly use a generic `subject_scope: ["RBI-regulated entity"]` rather than distinguishing
  Commercial Banks / Small Finance Banks / Payments Banks / Rural Co-operative Banks — but the
  2025 successor regime is explicitly split by exactly that distinction. Obligations may need
  entity-specific successor citations rather than one shared one, depending on which entity
  types each is actually meant to cover.

## Recommended next step

Before drafting any more RBI-KYC items (including resuming Candidate 1 or adding stratification
items against this instrument), re-verify the 32 items with `reference_date: 2026-08-01`
against the correct 2025 entity-specific successor direction for their modeled entity type, and
spot-check whether the specific clauses the catalog already relies on (paragraph 2, 23/28,
38(e)) carry over with the same substance under new numbering. This is a one-time catalog
currency sweep, not a redesign — the obligation *content* is probably still substantively
correct, re-citation is the work.
