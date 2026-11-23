# Stratification gap analysis — branch `1st-Round-of-Changes`

Purpose: quantify, from the actual data (not estimates), how far `data/benchmark/benchmark.jsonl`
is from the 100–200 item stratified target in `docs/DATASET_SPEC.md` / `docs/RESEARCH_EVALUATION.md`,
and what adding real items would require. This is a gap report, not new gold data — closing
these gaps means new `draft` items going through the same D-007–D-009 two-annotator +
adjudication process, which needs real human annotators (see D-005's rejection of simulated
independence).

## 1. Current coverage (measured 2026-11-22, n=127, all gold_verified)

**By outcome:**

| Outcome | Count | Share |
|---|---|---|
| Not applicable | 61 | 48.0% |
| Applicable | 60 | 47.2% |
| Indeterminate | 6 | 4.7% |
| **Conflict** | **0** | **0.0%** |

**By regulation area (scenario_tags):**

| Tag | Count |
|---|---|
| rbi_kyc | 90 |
| sebi_lodr | 37 |

No other instrument is represented at all — the whole benchmark is two regulation families.

**By mechanism tested (scenario_tags), the dimensions the spec says to stratify on:**

| Dimension | Count | Note |
|---|---|---|
| applicability_positive | 59 | well covered |
| applicability_negative | 58 | well covered |
| missing_entity_fact / abstention | 6 each | thin |
| numeric_threshold | 6 | thin |
| amendment_sensitive | 1 | **near-zero** — temporal/version reasoning (the engine's headline feature) is tested once |
| exemption_positive | 2 | thin |
| exemption_unknown | 1 | thin |
| pep, vcip, risk_categorization, unconditional_duty | 2 each | thin, single-topic |
| entity_scope_positive / negative | 1 each | thin |
| small_account, pan_form60, balance_cap | 1–3 each | thin |

**By obligation:** 60 distinct `target_obligation_id` values across 127 items — i.e. every item
maps to a different obligation on average ~2.1x, so there is close to no repeated-obligation
testing under different entity profiles for most obligations, and no held-out obligation set at
all (train/test are the same 60 obligations).

**By reference date:** 87 of 127 items (68%) use `2025-09-01`; another 32 use `2026-08-01`. Only
8 items (6%) use any other date. Amendment-sensitive temporal reasoning needs date diversity
*around specific amendment effective dates*, not just two bulk dates.

## 2. What the spec actually asks for

`docs/RESEARCH_EVALUATION.md` says to stratify 100–200 items across:
- pre-amendment and post-amendment dates (we have 1 amendment_sensitive item — far short)
- distinct entity types and condition thresholds (concentrated in 2 instruments)
- true and false applicability predicates (met — 59/58 is balanced)
- intentionally missing required facts → Indeterminate (6 items — thin but present)
- source-grounded exemptions and dependencies (3 items total — thin)
- **genuine unresolved conflicts, only where official evidence supports them** (0 items)

## 3. Concrete gaps, ranked by priority

1. **Zero Conflict examples.** This is the single biggest gap — one whole outcome class
   untested, and (per D-011 on this branch) the reason macro-F1 reads 0.75 instead of 1.0.
   See `docs/CONFLICT_CANDIDATES.md` (added on this branch) for real candidate scenarios
   worth a human adjudicator's attention under D-004's rule. **Update (2026-11-23, D-025):**
   four candidates have now been checked across two sessions (KYC small-account proviso,
   bank-vs-LODR board governance, KYC onboarding rules, and NBFC/SEBI related-party approval
   authority) — none is a genuine Conflict on the text found. The pattern so far is that RBI
   and SEBI tend to layer cumulative requirements rather than contradict each other outright.
   Still genuinely open: either a wider search turns up a real one, or this outcome stays
   untested in the gold benchmark.
2. **Regulatory scope was two instruments.** RBI KYC Master Direction and SEBI LODR only.
   The project's own novelty claim is about RBI *and* SEBI applicability reasoning generally;
   a reviewer will reasonably ask whether the engine generalizes beyond KYC/LODR. **Update
   (2026-11-22, D-019 and D-022):** two more instruments are now in the catalog —
   `RBI-NBFC-PARA12-LOAN-APP-ACKNOWLEDGEMENT` (RBI NBFC Responsible Business Conduct
   Directions, 2025) and `RBI-FEMA-FCGPR-REPORTING-TIMELINE` (FEMA/NDI Rules, via the Master
   Direction – Foreign Investment in India) — both single-pass research leads
   (`verification_status` tiers below the catalog's `"source_text_human_confirmed"` norm,
   D-022 lower still since its exact paragraph number isn't confirmed), not yet human-verified,
   and no benchmark item is built from either yet. **Update (2026-11-23, D-023):** a second
   SEBI instrument is now in the catalog too — `SEBI-PIT-REG7-2A-CONTINUAL-DISCLOSURE` (SEBI
   Prohibition of Insider Trading Regulations, 2015), chosen over the originally-suggested
   Mutual Funds/ICDR candidates for a well-corroborated, differently-shaped (numeric
   threshold + fixed deadline) obligation. Same `"assistant_single_pass_webfetch"` tier as
   D-019 — the live primary PDF itself was fetched and quoted, not just a cover page — but
   still not independently human-verified. **5 instruments total now, 2 of them SEBI** — gap #2
   as originally scoped (a second SEBI instrument) is closed at the catalog level. **Update
   (2026-11-23, D-026/D-027):** 17 `draft` benchmark items (not gold) now exist across the 3
   newer instruments — 4 on RBI-NBFC, 6 on RBI-FEMA, 7 on SEBI-PIT — covering Applicable,
   Not-applicable (via each condition in a multi-condition `all_of` block in isolation),
   Indeterminate (missing-fact abstention on each condition), amendment-sensitivity (reference
   date before `effective_from`), and a numeric boundary case (exactly-at-threshold,
   confirming `gt` is not `gte`). Every expected outcome was confirmed by running the actual
   resolver; none is `gold_verified` — that needs the real two-annotator pipeline (D-007–D-009).
   The *gold* benchmark is still 90 `rbi_kyc` / 37 `sebi_lodr` / 0 on anything else; only the
   draft layer now reflects the catalog's full instrument range, with meaningfully more depth
   than a single Applicable/Not-applicable pair per instrument. **Update (2026-11-23, D-024):**
   at the owner's
   explicit instruction, the `verification_status` field on D-019, D-022, and D-023 was set to
   `"source_text_human_confirmed"` *without* an actual human source-text check — a documented
   owner override, not a genuine D-006-style pass (see D-024 for the full record). None of the
   three has actually had its `clause_text` independently checked against the primary PDF by a
   human; that real check, plus the same for the 2025 KYC renumbering in D-021, is still the
   outstanding work before any of them should be trusted at face value, regardless of what the
   field now says.
3. **Amendment-sensitive reasoning is tested once in the gold benchmark.** For a project whose
   algorithmic novelty claim is explicitly "temporal validity" and "which version of a clause
   applied," 1/127 items actually exercising a pre/post-amendment date split is a real weakness
   a reviewer will flag before worrying about raw item count. **Update (2026-11-22, D-017):** a
   second item, `TAARR-DRAFT-0135`, is now drafted (status `draft`, in `draft_items.jsonl`,
   not yet gold) as the pre-amendment negative companion to the existing `TAARR-DRAFT-0001` —
   same obligation, reference date before the amendment instead of after. Still needs the full
   annotation pipeline before it counts toward the gold benchmark's coverage.
4. **Exemptions/dependencies are tested on 3 items.** The "exemptions, dependencies" novelty
   claim needs more than 2–3 examples to look like a tested mechanism rather than a demo.
5. **Item count itself (127) is already inside the 100–200 target range** — so the priority is
   not "add more of the same," it's fixing the stratification shape above. Padding with more
   rbi_kyc applicability_positive/negative items would make the number bigger without closing
   any of the gaps a reviewer would actually probe.
6. **Not urgent after all, but worth knowing:** the 2016 KYC Master Direction was repealed
   effective 28 Nov 2025 (see `docs/DATA_CURRENCY_ALERT.md`). Checked directly: every one of the
   90 `rbi_kyc` items uses a reference date before the repeal, so none of the current 127 gold
   items are affected. Relevant for two things instead: (a) any *new* RBI-KYC item must cite the
   right 2025 entity-specific successor, not the repealed 2016 text; (b) a reference date
   straddling 27–28 Nov 2025 against an `rbi_kyc` obligation is a real, source-grounded
   amendment-sensitive item — directly closes gap #3 (only 1 such item exists) with genuine
   regulatory history instead of a constructed example.

## 4. What this branch does and doesn't do about it

**Done on this branch:** this gap analysis, and `docs/CONFLICT_CANDIDATES.md` identifying
candidate Conflict scenarios for human review.

**Not done, and why:** drafting and gold-verifying new items for gaps 2–4 requires (a) sourcing
and D-006-style human verification of new obligations from instruments not yet in the catalog,
and (b) the full D-007–D-009 two-independent-annotator + adjudication pipeline for any new
benchmark item. Both need real people and real source documents, not something this session can
simulate without repeating the exact shortcut (D-005) this project already rejected. The
actionable next step is: pick one gap above (Conflict is the highest-leverage one — see the
candidates doc), source 3–5 real obligations/items for it, and run them through the same process
D-007–D-009 used.
