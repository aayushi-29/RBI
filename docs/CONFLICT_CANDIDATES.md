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

## Candidate 2: SEBI LODR corporate-governance norms vs. RBI's bank board/committee rules, for an RBI-regulated listed bank, on or after 2021-09-01

This is the strongest candidate found so far — a genuine cross-regulator conflict with a
documented history of its own precedence rule being removed, corroborated by multiple
independent secondary sources (web research done 2026-11-22; primary gazette/circular text
still needs to be pulled and quoted verbatim by a human before any item is drafted, per
D-006/D-009's own standard — nothing below is quoted as clause text yet, only described).

**The shape of it:**
1. SEBI (LODR) Regulations, 2015, Regulation 15(2), carried a proviso to clause (b) giving
   "overriding effect" to a listed entity's "specific statute" where it conflicted with LODR's
   corporate-governance provisions (Regulations 17–27). Secondary-source summary (Vinod Kothari
   & Co., "SEBI notifies substantial amendments in Listing Regulations," May 2021): the
   amendment "provides for deletion of the said proviso effective from September 1, 2021," and
   notes "no rationale seems to have been provided in the agenda."
2. RBI separately regulates bank board/committee composition — e.g. circular RBI/2021-22/24,
   "Corporate Governance in Banks – Appointment of Directors and Constitution of Committees of
   the Board" (DOR.GOV.REC.8/29.67.001/2021-22, 26 April 2021; https://rbi.org.in/Scripts/NotificationUser.aspx?Id=12078),
   later folded into RBI's 2025 Master Direction "Commercial Banks – Governance" (id=13161,
   28 Nov 2025). Independent legal commentary (conventuslaw.com, law.asia) describes this circular
   as imposing a *stricter* independent-director quorum for board/committee meetings than SEBI
   LODR Regulation 18/17 require for the same entities.
3. The same vinodkothari.com source states the consequence directly: for an entity caught
   between the two, "Subsequent to September 1, 2021 these entities will be regarded as
   non-compliant of the provisions of Listing Regulations," potentially "subject to penalty."

**Why this clears D-004's bar better than Candidate 1:** two different regulators (RBI and
SEBI), two different in-force instruments, a documented example of where they actually impose
different requirements on the same entity (bank board/committee composition), and — unlike
Candidate 1's single-instrument ambiguity — a specific, dated event (2021-09-01) where the
stated precedence rule that used to resolve this was deleted with, per the same source, no
replacement rule announced. If that account holds up against the primary gazette text, this is
close to a textbook `Conflict`: in force, contradictory, no documented tie-breaker, dated.

**What is NOT yet done, and must be before this becomes a draft item, let alone gold:**
- Pull the actual 2021 SEBI (LODR) (Amendment) Regulations gazette notification and quote
  Regulation 15(2)(b)'s proviso exactly as it read before deletion, and confirm there is no
  successor precedence clause elsewhere in the current (2026) consolidated LODR text — the
  current indiankanoon.org excerpt of Regulation 15(2)'s *opening* words ("...shall apply to the
  extent that it does not violate their respective statutes and guidelines or directives issued
  by the relevant authorities") looks like it might still carry some general carve-out distinct
  from the deleted 15(2)(b) proviso. **These two things need to be reconciled by someone reading
  the full current regulation text side by side with the pre-2021 text — this document does not
  resolve that, and getting it wrong in either direction would misclassify the item.**
- Identify the exact current RBI clause (2025 Master Direction id=13161, or whichever is live
  when drafted) and the exact current LODR Regulation 17/18 text, both verbatim, both dated.
- Confirm the entity type this actually bites for (a bank that is both RBI-regulated *and* a
  SEBI-listed entity under LODR — e.g. a listed public-sector or private-sector bank) and that
  no other RBI/SEBI circular has since re-introduced a precedence rule between 2021 and now.

## What this branch did and didn't do

**Done:** identified Candidate 1 from data already in the repo; researched and documented
Candidate 2 from external sources with full citations, strong enough to be worth a human's time
to verify against primary text.

**Not done:** no new benchmark item was added for either candidate, and no outcome was asserted
as gold — or even as draft. Both candidates need a human to read the actual gazette/circular/
Master Direction text (not secondary commentary) and write down the verbatim clause text and
dates, the same rigor D-006/D-009 applied to every other obligation in this catalog, before
either can become a real draft item.
