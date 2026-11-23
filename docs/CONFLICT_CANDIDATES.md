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

**Research update (2026-11-22, assistant self-verification against primary RBI text — not a
substitute for the two-person gold process, same tier as D-005's "assistant_solo_refetch"):**
fetched the actual KYC Master Direction text rather than relying on the obligation record's own
paraphrase. Confirmed:
- Paragraph 2(a)'s actual text: *"The provisions of these Directions shall apply to every
  entity regulated by Reserve Bank of India... except where specifically mentioned otherwise."*
  No proviso attached directly to paragraph 2 itself in the current consolidated text found.
- The small-account carve-out is real and verified: *"Provided this rule shall not apply to
  'small accounts' referred to in Section 23 of Chapter VI"* — found in RBI circular text
  (NotificationUser.aspx?Id=11261) discussing the general applicability rule, consistent with
  the catalog's framing.
- Substantively, "Small Accounts" exist under the PMLA Rules specifically as a *relaxed-KYC*
  category (no OVD required, capped balances/turnover, 12-month initial validity) — a different
  renewal mechanism from ordinary periodic KYC updation. That supports reading outcome **1**
  above (the carve-out genuinely exempts small accounts from the ordinary periodic-update notice
  duty, because small accounts are on their own separate renewal track) as more likely correct
  than outcome 3 (genuine Conflict) — but this is the assistant's own reasoned interpretation of
  the primary text, not a legal-reviewer's adjudication, and is explicitly not gold-equivalent.
- **This research also surfaced something bigger than the Candidate 1 question itself:** the
  2016 KYC Master Direction these paragraph numbers refer to has been repealed effective 28
  November 2025 and replaced by separate entity-specific 2025 KYC Directions with renumbered
  paragraphs (confirmed: the small-account carve-out is now "paragraph 28," not paragraph 23, in
  the Small Finance Banks and Payments Banks successor directions). See the new
  `docs/DATA_CURRENCY_ALERT.md` — this affects re-verifying Candidate 1 against the *correct*,
  currently-live instrument, not just the question of which paragraph governs which.

**Verdict on Candidate 1 as of 2026-11-22 (earlier in the day):** leaned toward outcome 1 (genuine
exemption, not Conflict) based on the substantive reading above — flagged as needing re-check
against the 2025 successor direction before finalizing, per `docs/DATA_CURRENCY_ALERT.md`.

**REOPENED (2026-11-22, later same day) — the promised re-check against the 2025 successor
found a real structural discrepancy, not just a renumbering.** Fetched the live Reserve Bank of
India (Commercial Banks – KYC) Directions, 2025 (`id=13141`) directly, specifically the
Applicability section and the small-accounts clause, to re-check outcome 1 against the
currently-live text rather than the repealed 2016 text. Findings (via WebFetch; the tool's
125-character verbatim-quote limit means these are paraphrases of live text, not pasted
quotations — **flagged for primary-text confirmation**, same caveat applied throughout this
document):
- The 2016 Direction's "paragraph 2" (general applicability clause, "applies to every entity...
  except where specifically mentioned otherwise") does not have a direct successor carrying a
  general small-account proviso. In the 2025 Commercial Banks Direction, the main domestic
  applicability clause is now paragraph 3, and **paragraph 3 contains no mention of small
  accounts and no proviso of any kind.** The only small-account proviso left in the Applicability
  section (Chapter I.B) is on paragraph 4, which extends the Direction to a bank's *foreign
  branches and subsidiaries* — a narrower, different clause than 2016's general-scope paragraph 2.
- Paragraph 28 of Chapter VI (successor to 2016's paragraph 23, "Small Accounts") opens with
  *"Notwithstanding anything contained in paragraph 23 and as an alternative thereto"* — i.e. its
  own stated exemption scope is narrow: an alternative to paragraph 23's *document/identity*
  requirements specifically, not a blanket carve-out from the whole Direction.
- Paragraph 42(7) ("Due Notices for Periodic Updation of KYC," successor to 2016's paragraph
  38(e)) does not itself mention small accounts or any exemption.
- **What this means for Candidate 1:** if this reading is correct, the 2025 successor direction
  does not contain a general, Direction-wide small-account exemption at all — only a narrow one
  limited to paragraph 23's own CDD-document requirements. That would mean a small account is
  **not** exempt from the periodic due-notices duty (paragraph 42(7)) under the *current* RBI
  instrument, which is the opposite of this document's earlier (same-day) leaning toward outcome
  1. The catalog's `RBI-KYC-PARA2-SMALL-ACCOUNT-PROVISO` exemption relation and `TAARR-DRAFT-0005`
  (currently `Indeterminate`, modeled as exempt-if-small-account) were both built against the
  *repealed* 2016 text's paragraph 2, whose own general proviso this session has not yet found a
  surviving equivalent for in the 2025 successor.
- **Status: reopened, not resolved either way.** This is exactly the kind of finding that
  deserves a human legal reviewer's eyes, not a same-session self-reversal treated as final: it
  rests on an AI-paraphrased fetch of a 155,000-character live government page, not a verified
  primary-text excerpt pasted and cross-checked the way D-012/D-013 were for Candidate 2. Before
  any conclusion, the recommended next step is to pull the actual PDF of RBI/DOR/2025-26's
  Commercial Banks KYC Direction and verbatim-confirm (a) paragraph 3's full text has no proviso,
  (b) paragraph 4's proviso text, and (c) paragraph 28's opening "notwithstanding" clause — the
  same primary-source-pull standard used to confirm Candidate 2's text in D-012/D-013.
- See `docs/DECISIONS.md` D-018 for the formal log entry.

## Candidate 2: CLOSED — not a genuine Conflict (owner-confirmed 2026-11-22)

**Verdict: this candidate does not clear D-004's bar.** The project owner confirmed that the
current RBI governance clause and the current SEBI LODR Regulation 17/18 text impose **the same
requirement** — i.e. the two sides don't actually disagree today, whatever the removed proviso's
history. D-004 requires authoritative sources to *genuinely disagree*; converging substantive
requirements means there is nothing to adjudicate, regardless of whether a general precedence
rule still exists on paper. The rest of this section is kept as a record of the research and
why it looked promising, not as a live candidate — **do not draft a benchmark item from this.**

The earlier framing below is preserved for the research trail, with the verdict above standing
as the final word.

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

**Why this is now closed rather than left open:** the proviso-removal history above is real and
well-sourced, and made this *look* like a strong candidate — but D-004 asks whether the sources
actually disagree, not whether a rule that used to prevent disagreement was removed. The owner's
confirmation that RBI's current clause and LODR Regulation 17/18 give the same answer settles
that question directly: there's no disagreement to adjudicate. This is itself a useful negative
result — it shows the Candidate-2-style search (look for a removed precedence rule) can surface
things that look promising on paper but resolve cleanly once the current substantive text is
actually compared, which is exactly why D-004 and D-006's rigor insist on checking current text
before drafting, not just amendment history.

**Current status of the Conflict gap:** back to zero confirmed candidates (Candidate 1 is still
open per its own three-way branch above; Candidate 2 is closed). The benchmark's zero-Conflict
gap (`docs/STRATIFICATION_GAP_ANALYSIS.md`) remains unresolved and needs either Candidate 1's
resolution or a new Candidate 3.

## What this branch did and didn't do

**Done:** identified Candidate 1 from data already in the repo; researched and documented
Candidate 2 from external sources with full citations, strong enough to be worth a human's time
to verify against primary text.

**Not done:** no new benchmark item was added for either candidate, and no outcome was asserted
as gold — or even as draft. Both candidates need a human to read the actual gazette/circular/
Master Direction text (not secondary commentary) and write down the verbatim clause text and
dates, the same rigor D-006/D-009 applied to every other obligation in this catalog, before
either can become a real draft item.

## Candidate 3 (checked, not found): paragraph 40(e)/44(5) first-transaction rule vs. paragraph 44(a)/48 foreign-student remittance cap

**Checked 2026-11-22, closed as a negative result, same session as D-020.** The lead: RBI KYC's
non-face-to-face onboarding rule requires an account's *first* transaction to be a domestic
KYC-complied credit (paragraph 40(e) in the 2016 Direction; confirmed renumbered to **paragraph
44(5)** in the 2025 Commercial Banks successor, same substance: *"First transaction in such
accounts shall be a credit from existing KYC-complied bank account of the customer."*). Separately,
the foreign-students clause (old paragraph 44(a), confirmed renumbered to **paragraph 48(1)/(3)**)
*permits* a foreign student's account to receive foreign remittances up to USD 1,000 pending
local-address verification. If a foreign student's first-ever transaction were a foreign
remittance, these would appear to clash.

**Why it's not a Conflict, on the text actually found:**
- Paragraph 48's foreign-remittance allowance is permissive ("may receive"), not a requirement
  that the first transaction specifically be a foreign remittance — the two rules can coexist
  (first transaction = domestic credit as required by 44(5); subsequently, capped foreign
  remittances are also allowed during the 30-day window).
- Paragraph 48 describes a bank-run procedure for opening a foreign student's account, which
  reads as a different (likelier in-person) onboarding path than the "non-face-to-face" trigger
  condition that activates paragraph 44(5) in the first place — so the two clauses' trigger
  conditions may not even overlap in the typical case.
- Checked for a stated cross-reference either direction in the live Commercial Banks 2025 text:
  none found.
- **Caveat:** this check used `id=13141` (the correct current source, not the dead `id=11566`
  found in D-020) via WebFetch, so same AI-paraphrase caveat as D-018 applies — not a verbatim
  primary-text pull.

Kept here as a worked, closed lead (same convention as Candidate 2) so the next research pass
doesn't re-tread it.

## Candidate 4 (checked, not found): RBI NBFC related-party loan sanction vs. SEBI LODR Reg 23 audit-committee approval

**Checked 2026-11-23, following an explicit owner instruction to find a real Conflict.** The
lead: a listed NBFC making a loan to a related party is simultaneously subject to RBI's
prudential lending rules and SEBI's listed-entity governance rules — two different regulators,
same transaction, same entity, which is exactly the shape a genuine Conflict needs.

**What was actually found, from primary/near-primary sources via WebSearch:**
- RBI finalized "Amendment Directions on Lending to Related Parties by Regulated Entities"
  (RBI/2025-26/179, DOR.CRE.REC.380/07-02-008/2025-26, dated 5 Jan 2026), amending the NBFC
  Credit Risk Management Directions, 2025 (`id=12954`). The live text (paragraph 13I): *"All
  loans above the prescribed materiality threshold shall be sanctioned by the Board of the
  NBFC."* — a **Board-sanction** duty, triggered only **above a materiality threshold** the RBI
  Directions set.
- SEBI LODR Regulation 23(2): *"All related party transactions shall require prior approval of
  the audit committee"* — an **Audit Committee approval** duty, applying to **all** RPTs
  irrespective of value (with shareholder approval added on top for transactions material under
  SEBI's own, separate threshold test).

**Why it's not a Conflict, on the text found:** nothing in either source says its own approval
body is the *exclusive* one, or that the other regulator's approval requirement is displaced.
A listed NBFC can satisfy both: Board sanction for loans above the RBI threshold, and Audit
Committee (plus shareholder, if material) approval for the same transaction under LODR Reg 23 —
cumulative, overlapping compliance obligations, not a contradiction where satisfying one duty
would violate the other. This is the same shape as Candidates 2 and 3: two regulators layering
requirements on the same fact pattern, not genuinely disagreeing about what the entity may or
must do.

**Caveat:** sourced via WebSearch snippets of the RBI notification and several SEBI circulars
referencing Regulation 23(2)-(4), not a single pasted primary-text read of either full
instrument — same single-pass research caveat as D-018/D-022/D-023. The RBI Related-Party
Lending Directions were themselves only finalized 5 Jan 2026 (previously a draft open for
comment, closed 31 Oct 2025), so this is also a very recent provision with limited secondary
commentary to cross-check against.

**Running pattern worth naming explicitly:** four candidates have now been checked across two
research sessions (Candidates 1-4); none is a genuine Conflict on the primary/secondary text
found so far. The recurring shape is that RBI and SEBI (and RBI's own instruments against each
other) tend to add cumulative, non-exclusive requirements rather than issue directly
contradictory ones — which is itself a modest, honest finding about this regulatory domain, not
a failure of the search. It does not prove no genuine Conflict exists anywhere in RBI/SEBI law;
it means none has turned up yet in the areas searched (KYC onboarding rules, foreign-student
remittances, NBFC/listed-entity board governance, and now NBFC/listed-entity related-party
approval authority).

## Candidate 5 (checked, not found): RBI KYC/PMLA record-retention duty vs. DPDP Act erasure principle

**Checked 2026-11-23, explicitly prompted by the owner naming Conflict as important for project
approval.** The lead: RBI's KYC Master Direction and the PMLA (Maintenance of Records) Rules,
2005 require banks to retain customer identification records for 5+ years after a relationship
ends; the 2025 Digital Personal Data Protection (DPDP) Act's data-minimisation/erasure principle
appears, on a surface reading, to require the opposite. This is a real, publicly debated tension
in Indian legal commentary — not an obscure lead.

**What was actually found:** DPDP Act **Section 8(7)** itself carries the resolution. Its
parent clause opens with "unless retention is necessary for compliance with any law for the time
being in force" — the erasure duties in 8(7)(a)/(b) are subject to that carve-out, so where PMLA
or RBI's own Direction requires retention, no erasure duty arises at all. The Act's own
**Illustration II** addresses banks directly: a customer closing a savings account, where the
bank "shall retain" personal data for as long as the governing law (PMLA Rules) requires.

**Why it's not a Conflict, on the text found:** this is the clearest-cut case yet, precisely
*because* the statute anticipated the tension and wrote its own precedence rule — exactly what
D-004 excludes from Conflict. Source: a legal-commentary analysis
(unifiedchambers.com/blog/rbi-dpdp-retention-reconciliation) arguing the popular "conflict" thesis
quotes only 8(7)(a) in isolation and omits both the parent clause and Illustration II. The
article flags one real residual case — data kept only on *consent* (e.g. marketing profiles, no
statutory retention basis) — but that is a different, non-overlapping fact pattern from KYC/AML
retention, not a conflict within it.

**Caveat:** sourced via a single secondary legal-commentary analysis plus the statutory text it
quotes, not a primary read of DPDP Section 8(7) and its illustrations by this project. The
underlying legal reasoning (carve-out clauses resolving apparent retention/erasure tensions) is
well-established doctrine, not a novel claim, but this specific analysis has not been
independently cross-checked against a second source.

**Running pattern, updated:** five candidates across two sessions, zero genuine Conflicts. Two
of the five (this one and Candidate 4) turned out to have an *explicit* textual precedence rule
resolving them, which is the strongest possible form of "not a Conflict" under D-004 — not an
absence of evidence, but a documented resolution. Per `docs/DATASET_SPEC.md` rule 8 and
`README.md`'s explicit instruction not to invent Conflict examples, this pattern is reported
as-is rather than papered over.
