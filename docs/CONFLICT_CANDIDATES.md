# Conflict-outcome candidates — branch `1st-Round-of-Changes`

Purpose: the benchmark has zero `Conflict`-outcome items (see `docs/STRATIFICATION_GAP_ANALYSIS.md`).
This document identifies candidates worth a human adjudicator's attention, under D-004's rule:

> Only mark Conflict when authoritative in-force sources genuinely disagree and no documented
> precedence rule resolves the disagreement. Never invent priority numbers. Source links and
> adjudicator rationale are required.

**No item below is a benchmark row and none is gold. These are research leads for a human
annotator to take through the real D-007–D-009 process — drafting or labeling one from this
document, by the assistant, would be exactly the simulated-independence shortcut D-005 rejects.**

## Candidate 1: the paragraph-2 small-account proviso vs. paragraph-38(e) notice duty

Already present in `data/obligations/obligations.jsonl` as an `EXEMPT` relation on
`RBI-KYC-P38E-DUE-NOTICES` (relation `RBI-KYC-PARA2-SMALL-ACCOUNT-PROVISO`), and already
surfaced once in the benchmark as `TAARR-DRAFT-0005` — but resolved there as `Indeterminate`
(missing fact `is_small_account`), not `Conflict`.

**Why it's a candidate, not a confirmed Conflict:** the obligation's own `notes` field (written
2026-10-21, source-text-human-confirmed tier) says plainly: *"The exact boundary between this
general Direction-wide proviso and paragraph 38(e)'s specific notice duty still needs
confirmation before gold verification."* That is an open question about which clause actually
governs, which is closer to D-004's bar than a routine missing-fact case — but it is explicitly
flagged as unconfirmed, so this document is not asserting it resolves to Conflict. It could
resolve three ways once confirmed:
1. The proviso clearly exempts small accounts from 38(e) → stays `Indeterminate`/`Not applicable`
   depending on the fact, as currently modeled. Not a conflict.
2. The proviso and 38(e) are read by RBI practice as both applying with the proviso taking
   precedence (standard general-vs-specific-clause construction) → still not a conflict, just
   needs an explicit precedence/dependency relation added instead of leaving it ambiguous.
3. If primary-source research finds the two clauses were amended at different times such that
   there's a real window where both are in force with no stated precedence → genuine `Conflict`,
   dated to that window only.

**Next step for a human annotator:** read paragraph 2's proviso and paragraph 38(e) directly in
the current consolidated RBI KYC Master Direction (URL already in the obligation record) and
settle which of the three outcomes above applies. This closes a real open question already
flagged in the data — it isn't inventing a new one.

## Candidate 2 (not yet found): a genuine cross-amendment transition-window conflict

A textbook `Conflict` case for a *temporal*-reasoning engine is a transition window: regulator
issues amendment B effective from date X, but amendment A (still formally in force until some
later repeal/consolidation date) was never explicitly superseded for the same clause, so for a
window both are simultaneously "in force" with different requirements and no stated precedence.

A scan of the current 60 obligations' `effective_from`/`effective_to`/`amendment_lineage` fields
did not surface an existing pair like this (most obligations here share one `effective_from` of
`2025-08-14` from the same bulk consolidation pass, which is why none show an overlap). Finding
a real instance requires reading actual amendment histories (RBI circulars superseding or
partially amending prior circulars) rather than the already-consolidated Master Direction text
this catalog mostly draws from — consolidation pages tend to already resolve these transitions
before publishing, which is exactly why none show up here. SEBI LODR's own amendment history
(it has been amended via several SEBI (LODR) (Amendment) Regulations over the years) is a
plausible place to look for a real, source-grounded transition conflict, but this has not been
researched yet on this branch.

## What this branch did and didn't do

**Done:** identified Candidate 1 from data already in the repo and explained precisely why it is
not yet confirmed as Conflict. Documented what finding Candidate 2 would require.

**Not done:** no new benchmark item was added, and no outcome was asserted as gold. Resolving
Candidate 1 or finding Candidate 2 needs a human reading primary source text directly — that's
the next concrete, scoped task for whoever does the next annotation round.
