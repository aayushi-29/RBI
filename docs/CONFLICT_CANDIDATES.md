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

**Loose end from the first draft of this document — now resolved, by the project owner's own
review (2026-11-22), the same role she played in D-006:** the first version of this document
flagged uncertainty about whether Regulation 15(2)'s *opening* words carried a general
statutory/regulator carve-out distinct from the deleted 15(2)(b) proviso, based on an
`indiankanoon.org` excerpt. That was wrong on both counts, and the owner corrected it with the
exact regulation structure:
- Regulation 15(2)'s opening words only create the small-cap (≤₹10 crore paid-up equity /
  ≤₹25 crore net worth) and SME-exchange exemptions — **no general statutory carve-out at all.**
  The "...shall apply to the extent that it does not violate their respective statutes..."
  language the first draft quoted belongs to the separate proviso under clause (b), not the
  opening words.
- That clause-(b) proviso is exactly what was omitted, effective 2021-09-01, under the
  **Securities and Exchange Board of India (Listing Obligations and Disclosure Requirements)
  (Second Amendment) Regulations, 2021** (Notification No. SEBI/LAD-NRO/GN/2021/22, dated
  5 May 2021). Primary-source confirmation (gazette notification text, not secondary commentary):
  *"under clause (b), the proviso shall stand omitted with effect from September 01, 2021."*
  (hosted at ca2013.com's copy of the notification). This matches, and upgrades to primary-source
  status, the vinodkothari.com secondary-source account already cited above.
- So there is no surviving general carve-out in Regulation 15(2) for private-sector banks today
  — the specific reconciliation provisos that do remain (e.g. Regulation 17(1C)'s
  shareholder-approval proviso, or provisos retained for public-sector banks specifically) are
  narrower and don't cover this case. Both LODR and RBI's governance regime apply concurrently,
  with no general tie-breaker.

**Verbatim pre-omission proviso text, supplied by the project owner (2026-11-22) and
independently cross-checked against a hosted mirror of the consolidated LODR text
(`ca2013.com/lodr-regulation-15/`), which preserves the same wording with strikethrough
formatting against the live regulation:**

> "Provided that for other listed entities which are not companies, but body corporate or are
> subject to regulations under other statutes, the provisions of corporate governance
> provisions as specified in regulation 17, [17A,] 18, 19, 20, 21, 22, 23, 24, [24A,] 25, 26,
> 27 and clauses (b) to (i) of sub-regulation (2) of regulation 46 and para C, D and E of
> Schedule V shall apply to the extent that it does not violate their respective statutes and
> guidelines or directives issued by the relevant authorities."

Citation chain (all per the owner, cross-checked where notable below):
- Inserted into the proviso: `17A` and `24A`, by the SEBI (LODR) (Amendment) Regulations, 2018,
  Notification No. SEBI/LAD-NRO/GN/2018/10, dated 9 May 2018, w.e.f. 1 April 2019 (the owner
  notes some consolidated footnotes carry a typographical slip of "w.e.f. 2.9.2015" for this —
  worth independently confirming before citing a date from a footnote rather than the
  notification itself).
- Omitted in full: by the SEBI (LODR) (Second Amendment) Regulations, 2021, Notification No.
  SEBI/LAD-NRO/GN/2021/22, dated 5 May 2021, w.e.f. 1 September 2021, Regulation 3(V) — matches
  the primary-source confirmation already found above.
- Baseline (pre-2018, no 17A/24A): Notification No. SEBI/LAD-NRO/GN/2015-16/013, published
  2 September 2015, effective 1 December 2015, Chapter IV, Regulation 15(2)(b).
- **Cross-check note:** `ca2013.com/lodr-regulation-15/`'s own footnote gives the omission date
  as "w.e.f 01.09.2019" against the same 05.05.2021 notification — internally inconsistent (the
  notification postdates that claimed effective date by over a year), i.e. that specific mirror
  has a typo. The owner's 1 September **2021** date is the one consistent with the notification
  date and with every other source checked (vinodkothari.com, the primary gazette-hosted PDF).
  Flagging this so whoever drafts the final item cites 2021, not the mirror's 2019 typo.
- Other mirrors named by the owner, not yet independently fetched in this session:
  `indiankanoon.org/doc/89681788/` (pre-2021 text archived inline) and the official SEBI
  consolidated LODR PDF under Legal → Regulations on sebi.gov.in.

**What is still NOT done, and must be before this becomes a draft item, let alone gold:**
- Pull the exact current RBI clause (2025 Master Direction id=13161, or whichever is live when
  drafted) and the exact current LODR Regulation 17/18 text, both verbatim, both dated — the
  pieces that actually conflict, now that the missing precedence-proviso side is fully sourced.
- Confirm the entity type this actually bites for (a private-sector bank that is both
  RBI-regulated *and* SEBI-listed under LODR) and that no other RBI/SEBI circular has since
  reintroduced a precedence rule between 2021 and now.
- This candidate's sourcing is now essentially complete on the "what used to resolve this, and
  when did it stop" side. What remains is verbatim-quoting the two sides that actually conflict.

## What this branch did and didn't do

**Done:** identified Candidate 1 from data already in the repo; researched and documented
Candidate 2 from external sources with full citations, strong enough to be worth a human's time
to verify against primary text.

**Not done:** no new benchmark item was added for either candidate, and no outcome was asserted
as gold — or even as draft. Both candidates need a human to read the actual gazette/circular/
Master Direction text (not secondary commentary) and write down the verbatim clause text and
dates, the same rigor D-006/D-009 applied to every other obligation in this catalog, before
either can become a real draft item.
