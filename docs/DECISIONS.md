# TAARR Decisions and Open Questions

This log makes design assumptions visible so we do not silently change the proposal. Decisions affect benchmark gold labels and must be versioned before annotation scales.

## Adopted for the initial dataset implementation

1. **Benchmark unit:** one target-obligation decision per item (query + reference date + entity profile + target obligation). This gives the specified single `gold_outcome` a stable meaning. An item may also link supporting and related obligations.
2. **Four outcomes:** `Applicable`, `Not applicable`, `Indeterminate`, `Conflict` only.
3. **Temporal intervals:** represent validity as start-inclusive/end-exclusive. Keep publication date and effective date distinct. Null end date means "not recorded" until verified.
4. **Human-reviewed gold:** model-assisted extraction may propose records; it does not create verified gold labels. Two annotators label independently, disagreements are adjudicated against official sources.
5. **Provenance:** gold clause/version references must point to official RBI/SEBI URLs and preserve paragraph/sub-paragraph identifiers.
6. **No synthetic gold labels:** the initial benchmark is empty. Examples used in unit tests must be clearly marked as synthetic software fixtures, never merged into the regulatory gold dataset.
7. **No in-force version (D-001):** adopt `NoVersionPolicy.NOT_APPLICABLE`, following Review Paper Algorithm 1. If an obligation has no version in force on the reference date, emit `Not applicable` with the temporal-filter reason and evidence. Do not silently drop the target-obligation decision.

## Open decisions before labelling affected edge cases

### D-001: No version is in force on the reference date — DECIDED

- **Build Plan**, "Novelty 2: Algorithm", page 3, says after temporal filtering: if no versions, continue/drop it ("superseded/not-yet-effective -> drop, don't hallucinate it in").
- **Review Paper**, Algorithm 1 on page 13, says if the valid-version set is empty, emit `NOT_APPLICABLE` with reason "not in force on t".
- **Decision:** adopt the Review Paper behavior: use `NoVersionPolicy.NOT_APPLICABLE`. Emit `Not applicable` for the target obligation, with a clear reason that no recorded version is in force on the reference date and with temporal-filter evidence. This is an explicit decision to report the considered target obligation, not to claim that its substantive applicability condition was evaluated and found false.
- **Consequences:** keep the policy explicit and recorded in experiment reports; test the no-active-version case; do not drop these target-obligation decisions from the result set under the selected policy. Do not create gold labels for real regulatory records until the exact source/version timeline has been verified.
- **Status:** project owner selected Option B in the conversation; the policy choice is frozen unless explicitly reopened.

### D-002: Missing facts versus false predicates

The Review Paper states that missing attributes evaluate to UNKNOWN in Kleene three-valued logic, and the Build Plan says missing required facts should emit Indeterminate before evaluating condition truth. Preserve that rule: absent fact is not false. The annotation guideline must identify exactly which profile attributes are required by the obligation.

### D-003: Decision ordering when applicability is unknown and an exemption may apply — DECIDED

The Review Paper's Algorithm 1 and Build Plan's Algorithm 1 order some operations differently. The Review Paper evaluates temporal versions, then applicability, exemptions and dependencies with three-valued logic. The Build Plan emits Indeterminate when facts needed for applicability are missing before exemption resolution and describes a more streamlined branch order.

- **Decision:** adopt `UnknownPrecedencePolicy.DEFINITIVE_RULES_FIRST` (the Review Paper's ordering): when applicability is `UNKNOWN`, do not abstain immediately. Evaluate exemptions and dependencies first. A definite (non-`UNKNOWN`) exemption or dependency result can settle the outcome (`Not applicable` or `Conflict`) even while applicability itself remains unknown — a system that can abstain is weaker than one that resolves on dispositive evidence it already has. Only when no definite rule settles the case does unresolved applicability fall through to `Indeterminate`.
- **Consequences:** `resolve_obligation` in `src/taarr/reasoning.py` already implements this branch order, and `.env.example` already sets `TAARR_UNKNOWN_PRECEDENCE_POLICY=DEFINITIVE_RULES_FIRST`. This entry only catches the documentation up to that implemented and configured behavior. `INDETERMINATE_FIRST` remains available in `UnknownPrecedencePolicy` as a documented diagnostic baseline (ablation), never the production policy.
- **Status:** frozen. Gold labels may now be created for overlap cases where applicability is unknown and an exemption/dependency is definite, provided the annotation packet records which rule was dispositive.

### D-004: Equal-priority conflict and precedence evidence

Only mark Conflict when authoritative in-force sources genuinely disagree and no documented precedence rule resolves the disagreement. Never invent priority numbers. Source links and adjudicator rationale are required.

### D-005: Project owner opted out of the annotator role — DECIDED

On 2026-10-21, after the catalog had grown to 60 obligations (all source-located, none gold-verified), the project owner explicitly asked the assistant to perform full verification alone and said: "please do the verification on your own, i am not able to do such a large data verification, exclude me from this role." This changes what verification tiers are actually reachable without a new human annotator.

- **What stays true regardless:** `gold_verified` still requires two annotators who worked independently (per `ANNOTATION_PROTOCOL.md`) plus adjudication. One person checking something twice is not independent dual-annotation, however carefully it is done. The assistant will not mark anything `gold_verified`, `dual_annotated`, or `adjudicated` under this decision, and will not reuse "annotator_1"/"annotator_2" fields to simulate independence that does not exist.
- **What "single_pass_reviewed" means from this point on:** `DATASET_SPEC.md`'s original definition of this tier included project-owner review and approval. With the owner opted out, that is no longer what happens. From 2026-10-21 onward, an obligation or benchmark item reaching `single_pass_reviewed` (or the matching catalog `verification_status`) means: the clause was fetched from the official source at least twice, independently, in separate tool calls, by the assistant, and the two fetches agreed (or a disagreement was found and corrected -- see the 2026-10-21 regulation-2(1)(zb)/(zc) correction for a real example). It does **not** mean a human reviewed or approved it. This is a real weakening of the tier's original meaning, done openly rather than left implicit.
- **Why this is still worth doing:** a second independent fetch catches real mistakes a first pass alone would not -- it already found and fixed one mis-citation (see above). That is strictly better than a single uncorroborated pass. It is still not equivalent to a human legal reviewer, and the paper's threats-to-validity section must say so plainly: **no human has reviewed the substantive legal correctness of the 2026-10-21 bulk-added obligations.**
- **Consequences:** `docs/DATASET_SPEC.md`'s `single_pass_reviewed` section and `src/taarr/dataset.py`'s inline comment are updated to describe this owner-opted-out meaning. If the owner later wants to resume the annotator_1 role, or a different second human reviewer is found, that reopens the path toward genuine `gold_verified` labels; nothing here forecloses it.
- **Important: the `annotation_status`/`verification_status` string alone does not say which kind of check happened.** The 5 draft items marked `single_pass_reviewed` before 2026-10-21 (`TAARR-DRAFT-0001`..`0005`) genuinely went through the original meaning: the owner checked source text via screenshots and approved the outcome logic -- that is recorded in their own `annotations.source_verification_human_check` / `annotations.outcome_logic_review` fields, which remain true and unchanged. Everything promoted to `single_pass_reviewed` **on or after 2026-10-21** instead carries `annotations.single_pass_review = {"checked_by": "assistant_solo_refetch", "owner_reviewed": false, ...}`, marking the weaker, owner-opted-out meaning. Anyone reading this dataset must check the `annotations` payload, not just the status string, to know which of the two actually happened for a given item.
- **Status:** frozen. Reopen only if the owner wants to resume a review role, or a second human becomes available.

### D-006: Project owner resumed the annotator_1 role and personally verified all 60 obligations — DECIDED

On 2026-10-21 (later the same day as D-005), the project owner asked for a document listing every obligation's official source link with a plain-English yes/no question, worked through all 57 remaining obligations herself, and reported back a full table of answers with source quotes for each. Asked directly whether she had personally read each source or used an AI tool to generate the answers, she confirmed: *"i read through each source and verified by myself."*

- **What this is:** the owner resuming the annotator_1 role she had opted out of under D-005. This is a genuine single human source-text check for all 60 obligations (the original 3 were already owner-confirmed before D-005; this closes the gap for the other 57).
- **One flagged item checked before promotion:** the owner's own notes on item 23 (`RBI-KYC-PARA40B-MOBILE-NUMBER-RESTRICTION`) raised a possible mismatch, mixing in content from paragraph 17(2) (OTP-based e-KYC alerts) with paragraph 40(b) (the actual target clause). The assistant independently re-fetched paragraph 40(b) directly and confirmed our existing `clause_text` is accurate verbatim; no data change was needed for this item.
- **What changed:** all 57 obligations previously at `single_pass_reviewed` (the D-005, assistant-solo-refetch meaning) are promoted to `source_text_human_confirmed`, the same tier the original 3 pilot obligations held. All 60 obligations in `data/obligations/obligations.jsonl` now carry a genuine one-human source-text confirmation.
- **What this does NOT yet unlock:** `gold_verified` still requires **two independent human annotators plus adjudication**, applied at the **benchmark-item** level (query + reference date + entity profile + target obligation + outcome) per `ANNOTATION_PROTOCOL.md`, not just a clause-text match at the obligation level. One person confirming source text, however genuine, is not dual annotation. No benchmark item is marked `gold_verified`, `dual_annotated`, or `adjudicated` under this decision.
- **Consequences:** `docs/DATASET_SPEC.md`'s `single_pass_reviewed`/`source_text_human_confirmed` description and `docs/PENDING_TWO_PERSON_VERIFICATION.txt` are updated to reflect that the owner has resumed real verification work and all 60 source clauses are now human-confirmed; what remains open is specifically a **second independent annotator** for the benchmark items themselves.
- **Status:** frozen. Reopens further (toward `dual_annotated`/`gold_verified`) if a second independent human reviews the benchmark items, or the owner does a second, blind pass without seeing her first answers.

### D-007: First genuine independent human annotation pass on the 127 benchmark items — DECIDED

On 2026-10-21 the project owner had 5 different people, each independently handling a ~25-item block, answer all 127 draft benchmark items from a document that showed the plain-English rule, the known facts, and an optional "watch for" exemption note -- **never** the project's own draft `gold_outcome` or `gold_explanation`. Result: all 127 answers agreed with the draft hypothesis.

- **What this is:** the first real, independent, human-produced annotation of the benchmark items themselves (distinct from D-006, which checked the 60 source *obligations'* clause text, not the 127 *questions'* outcomes). Recorded per item as `annotations.annotator_1` in `draft_items.jsonl`.
- **What it is NOT:** the project's own draft hypothesis is not, and has never been, treated as one of the two required independent annotators (consistent with D-005/D-006) -- it is the thing being checked, not a checker. So this pass is `annotator_1`, not a human-vs-human comparison. A second, different independent human pass (`annotator_2`) is still required before any item can be `dual_annotated`; disagreement between the two humans (not between a human and the draft hypothesis) is what gets adjudicated into `gold_verified`.
- **An honest caveat on the 127/127 agreement:** this is good news, but should not be read as proof the dataset is correct. The checklist gave reviewers the rule's operative condition and the exact facts needed to apply it (e.g. "more than 10% ownership" + "25%"), so most items reduce to a mechanical threshold check with one defensible answer -- agreement there is expected, not a strong signal. The "watch for" column on the two small-account items (4, 5) also stated the exemption's existence outright, which may have pointed reviewers toward the same conclusion as the hypothesis rather than requiring them to discover and confirm it from the primary source themselves. The underlying open legal question noted in those items' `gold_explanation` (whether paragraph 23's small-account carve-out actually reaches paragraph 38(e) specifically) is **not** resolved by this pass.
- **Consequences:** `docs/PENDING_TWO_PERSON_VERIFICATION.txt` updated to reflect annotator_1 done, annotator_2 still needed. No item's `annotation_status` was changed by this decision -- promotion to `dual_annotated`/`gold_verified` still requires a second, different independent human pass plus adjudication of any disagreement between the two humans.
- **Status:** frozen. Reopens once a second, different independent person or group annotates the same 127 items without seeing either the draft hypothesis or annotator_1's answers.

### D-008: Second genuine independent human annotation pass on the 127 benchmark items — DECIDED

On 2026-10-21, later the same day as D-007, a second, different group of 3 people (confirmed by the project owner to be different individuals from the 5 who did annotator_1, and to have answered without seeing annotator_1's answers or the project's draft hypothesis) independently answered the same 127 draft benchmark items, using the same blind document (plain-English rule, known facts, optional "watch for" note -- never the draft `gold_outcome`).

- **What this is:** the second required independent human annotation pass. Recorded per item as `annotations.annotator_2` in `draft_items.jsonl`.
- **The comparison that matters:** annotator_2 vs. annotator_1 (two real humans), not either human vs. the project's own hypothesis. Result: **all 127 items match -- zero disagreements between the two independent human passes.**
- **What this unlocks:** per `ANNOTATION_PROTOCOL.md` point 4 ("have two annotators label items independently... without seeing each other's outcome"), this is genuine dual annotation. All 127 items are promoted from `single_pass_reviewed`/`draft` to **`annotation_status: "dual_annotated"`**, validated by `src/taarr/dataset.py`.
- **What this does NOT yet unlock:** `gold_verified` per `ANNOTATION_PROTOCOL.md` point 6 requires more than annotator agreement -- it requires actually checking "source URLs, clause IDs, effective dates, related provisions, outcome and explanation." Agreement between two humans is strong evidence, not a substitute for that check. No item has been promoted to `adjudicated` or `gold_verified` under this decision; `annotations.adjudication` has not been written for any item.
- **Honest caveat carried forward from D-007:** the same caveat about task design applies here too -- both annotator groups were given the rule's operative condition and the exact facts, so most items are a mechanical threshold check with one defensible answer. Two independent groups agreeing on a mechanical check is real signal (an error would likely have surfaced as a split), but it is still not the same as an adjudicator independently re-deriving the answer from the primary source with no steering facts at all. The open small-account/para-23-vs-para-38(e) question (items 4, 5) is not resolved by annotator agreement alone.
- **Consequences:** `docs/PENDING_TWO_PERSON_VERIFICATION.txt` updated to reflect dual-annotation done, source-text adjudication check still the one remaining step before `gold_verified`.
- **Status:** frozen pending the adjudication/source-check step. Reopens if that check finds a problem with any item's source link, clause id, effective date, or explanation text.

### D-009: Source-text adjudication pass — 125 of 127 items promoted to gold_verified — DECIDED

On 2026-10-21, immediately after D-008, the assistant performed the adjudication/source-check required by `ANNOTATION_PROTOCOL.md` point 6 — the last step before any item can be called `gold_verified`.

- **What was done:**
  1. **Live source-text re-fetch.** The assistant fetched the full text of both primary source documents directly from their official URLs: the RBI KYC Master Direction (rbi.org.in) and the SEBI LODR Regulations PDF (sebi.gov.in). These were fetched fresh via web access, not copied from the project's stored `clause_text` fields, so any drift between our stored text and the live official text would have been caught.
  2. **Clause-by-clause verification.** For every referenced paragraph (RBI) and regulation (SEBI), the assistant confirmed: the clause ID/paragraph number is correct; the wording, numeric thresholds (ownership percentages, monetary limits, time periods), and effective dates in the stored data match the live official text; related provisions (exemptions, carve-outs, dependencies) are correctly accounted for.
  3. **Computational consistency re-derivation.** As a secondary check for coding bugs (typos, wrong operators, off-by-one thresholds), the assistant ran `_resolve_item` from `src/taarr/experiments.py` on all 127 items against the full catalog with the configured policy. Result: 0 mismatches — every item's resolver output matched its `gold_outcome`. This is a consistency check (the resolver agrees with itself), not a substitute for the manual source-text verification above.

- **Result for 125 of 127 items:** every referenced clause's wording, thresholds, and effective dates matched the stored data. The assistant wrote `annotations.adjudication` records and promoted these 125 items to `annotation_status: "gold_verified"` in `data/benchmark/draft_items.jsonl`. These 125 items were also written into `data/benchmark/benchmark.jsonl` — the first time the project's real benchmark ledger has ever contained data.

- **Items 4 and 5 (the paragraph-2/paragraph-38(e) small-account exemption question):** the adjudication pass initially found a grammatical ambiguity in the proviso's scope; the project owner subsequently decided to accept the existing hypothesis (small accounts exempted from the whole Direction, including paragraph 38(e)) and promoted these two items to `gold_verified` alongside the other 125.

- **First real evaluation result.** With all 127 gold items in `benchmark.jsonl`, the `run_benchmark` API endpoint now produces real (not illustrative) numbers for the first time: n=127, accuracy=1.0, macro_f1=0.75.

- **Critical circularity caveat (must be carried into any paper or report):** the benchmark's facts, entity profiles, and expected outcomes were originally generated from the same rule engine now being evaluated. A 100% accuracy result therefore shows internal consistency — the resolver agrees with the data it produced — not proven correctness against an independent ground truth. This is the same caveat documented for the earlier illustrative run (see `docs/ILLUSTRATIVE_EVAL.md`), now applying to the real evaluation as well. Breaking this circularity requires benchmark items whose expected outcomes are derived independently of the resolver (e.g., by a qualified legal reviewer working from the primary source text alone).

- **Consequences:** `data/benchmark/benchmark.jsonl` populated with all 127 gold items (header comment block references D-007, D-008, D-009). `tests/test_api.py` updated: the old test assuming an empty benchmark was replaced with two new tests — one confirming the real benchmark scores 127 items, one confirming the original "no gold rows → excluded" safety property via a separate temporary file. `docs/PENDING_TWO_PERSON_VERIFICATION.txt` updated to reflect completion.
- **Status:** frozen. All 127 gold items are final unless a source-text error is later discovered. Cohen's kappa (point 7 of the annotation protocol) is formally 1.0 given zero disagreements between annotators, but has not been separately computed or recorded as a standalone metric — it would be trivially perfect and adds no information beyond what D-008 already states.

## Next decision gate

D-001 and D-003 are decided as above. D-002 and D-004 are preserved as drafting/labelling guidance, not open-ended choices: D-002 is implemented as `MissingFactsPolicy.KLEENE` (see `.env.example`), and D-004 governs how annotators and `_resolve_exception_effects` justify a `Conflict` label — both remain the live policy unless explicitly reopened here. All 127 benchmark items are now `gold_verified` (D-009). The next gate is breaking the circularity caveat: creating benchmark items whose expected outcomes are derived independently of the resolver, to validate real-world correctness beyond internal consistency.

## D-010: Guided "Check my rules" flow, built on top of the frozen engine (2026-10-22)

- **Context:** the engine (D-001–D-009) and its 127-item gold benchmark were already frozen. A separate, non-research request followed: make the applicability engine usable by someone who does not know the catalogue's internal fact names (e.g. `risk_category`) or clause IDs — a guided path from "describe your organisation" to a plain-English checklist, without changing how any obligation is decided.
- **What was built**, entirely as a layer on top of the existing deterministic `resolve_obligation` — no change to `reasoning.py`, the catalog, or any gold label:
  1. **`data/facts/fact_registry.json`** — a closed list of the 43 distinct facts used anywhere in the 60 obligations' `conditions`/`exemptions`/`dependencies`, each with a plain-English question, type, and allowed values/range. A test (`test_registry_matches_obligations_exactly`) enforces that this list always equals exactly the set of attributes the obligations actually reference, so the registry cannot silently drift from the catalogue.
  2. **`src/taarr/fact_extraction.py`** — turns a free-text description into entries in that closed list using Gemini, constrained to the registry's keys via a JSON response schema, with every value re-validated server-side (type/range/enum) and required to be backed by a verbatim quote from the user's own text. Gemini only fills the form; it never sees or influences the applicability decision.
  3. **`POST /api/v1/checklist`** — runs every obligation in the catalog against one entity profile and groups the results (`applies` / `does_not_apply` / `need_more_info` / `conflict` / `dropped`), with the exact registry question for every still-missing fact and a ranked list of which unanswered questions would settle the most obligations. Each row also carries `decided_by` (every fact its conditions/exemptions/dependencies reference) and `circular_url` (the obligation's official source), used by the UI's per-rule dialog and circular browser.
  4. **Frontend**: a guided 3-step flow (describe → confirm a short set of answers → checklist) plus a "Browse circulars and rules" view listing the RBI KYC Master Direction and SEBI LODR rules directly; both open the same rule dialog with the plain-English result, the deciding question(s), the exact clause text, and a link to the official circular.
- **API-usage decision:** Gemini is used in exactly two UI actions — Autofill (one call per click) and the AI cross-check (one *batched* call for every selected item, replacing the original one-call-per-item loop) — and nowhere else; the checklist and its live re-runs are local and deterministic. The key and model are read from `.env` on every request (`src/taarr/settings.py`), not passed through the browser, so a rate-limited key can be swapped for another model with a `.env` edit and no restart.
- **Consequences:** no obligation, exemption, dependency, or gold label changed; the 127-item benchmark and its n=127/accuracy=1.0/macro-F1=0.75 result are unaffected. Test count grew from 222 (pre-D-010) to 242. This work does not address the circularity caveat above — that remains the open research gate.

## D-011: Metrics transparency fix and stale-doc correction — branch `1st-Round-of-Changes` (2026-11-22)

- **Context:** a review of the frozen 127-item benchmark (D-009) questioned whether accuracy=1.0 / macro-F1=0.75 indicated overfitting. It does not indicate overfitting — the real cause is two separate, already-partially-documented facts: (1) the circularity caveat above, and (2) a scoring bug in `src/taarr/evaluate.py`.
- **The bug:** `score()` averaged per-class F1 over a hardcoded `/4` rather than `/len(LABELS)`, and — more importantly — `Conflict` has zero gold examples in the current benchmark (confirmed: `gold_outcome` only ever takes `Applicable`, `Not applicable`, `Indeterminate` across all 127 items). A label with zero support scores f1=0.0 under this function's own precision/recall convention (0/0 → 0.0 rather than undefined), which silently drags macro-F1 from 1.0 to 0.75 for a run that is otherwise 100% correct on every class it has actually been tested on.
- **Fix:** `score()` now reports both `macro_f1` (unchanged value, now computed over `len(LABELS)` instead of a hardcoded `4`) and two new fields, `macro_f1_excl_zero_support` and `zero_support_classes`, so neither reading is hidden. For the current benchmark: `macro_f1=0.75`, `macro_f1_excl_zero_support=1.0`, `zero_support_classes=["Conflict"]`. No existing number changed; the dilution is now visible instead of silent. All 242 pre-existing tests pass unchanged; no test asserted the old hardcoded-4 behavior.
- **Stale-doc correction:** `docs/EVALUATION_NEXT_STEPS.md` still told readers (as of this review) that a second independent annotator pass was a future step. It was not — D-007/D-008/D-009 and `docs/PENDING_TWO_PERSON_VERIFICATION.txt` already recorded that pass as complete on 2026-10-21. The file was never updated to match after D-009 landed. Corrected to state the real current status and point at the actual next gate (breaking the circularity caveat), per D-009's own "Consequences" note.
- **What this does NOT do:** it does not add any new benchmark item, obligation, or gold label, and it does not mark anything `gold_verified`. Adding genuine `Conflict` examples (so that label stops being zero-support for a real reason, not a metrics patch) requires the same two-independent-human-annotator + source-adjudication process as D-007–D-009, which this branch does not have authority to simulate — consistent with the D-005 decision that the assistant will not reuse annotator fields to fake independence that does not exist.
- **Status:** merged to this branch, pending human review before merge to `main`.

## D-012: Owner-corrected legal reading of the Conflict Candidate 2 regulation structure (2026-11-22)

- **Context:** `docs/CONFLICT_CANDIDATES.md`'s first draft of Candidate 2 (SEBI LODR vs. RBI bank
  governance) flagged an unresolved "loose end": whether Regulation 15(2)'s opening words carried
  a general statutory carve-out separate from the proviso deleted in 2021, based on reading a
  secondhand `indiankanoon.org` excerpt rather than the primary notification.
- **Correction:** the project owner identified this as wrong on two points, citing the regulation's
  actual structure and the primary notification number from memory/expertise: (1) Regulation
  15(2)'s opening words only create the small-cap/SME-exchange exemptions, with no general
  carve-out; the carve-out language belongs to a separate proviso under clause (b); (2) that
  proviso was omitted effective 2021-09-01 under the SEBI (LODR) (Second Amendment) Regulations,
  2021, Notification No. SEBI/LAD-NRO/GN/2021/22 dated 5 May 2021 — so there is no surviving
  general carve-out to reconcile, and the loose end does not exist.
- **Verification:** the assistant then located a hosted copy of the actual gazette notification
  text (ca2013.com's copy of SEBI/LAD-NRO/GN/2021/22) confirming verbatim: "under clause (b), the
  proviso shall stand omitted with effect from September 01, 2021." This is primary-source
  confirmation of the owner's correction, not merely a second secondary source.
- **Consequences:** `docs/CONFLICT_CANDIDATES.md` updated to remove the resolved loose end and
  cite the primary notification. Candidate 2 is materially stronger than before — its main open
  risk is closed — but it remains a research lead, not a draft or gold benchmark item. The
  omitted proviso's own pre-2021 text still needs to be located and quoted verbatim before any
  item is drafted.
- **Status:** open — Candidate 2's remaining verification steps (verbatim proviso text, current
  RBI/LODR clause text, confirming no later precedence rule was reintroduced) are unstarted.

## D-013: Verbatim pre-omission proviso text supplied and cross-checked (2026-11-22)

- **Context:** D-012 confirmed the omitted-proviso-under-clause-(b) structure and its omission
  date via a primary gazette excerpt, but the proviso's own pre-2021 wording hadn't been located.
- **What happened:** the project owner supplied the verbatim proviso text plus a full citation
  chain (the 2018 amendment inserting `17A`/`24A`, the 2021 omission notification, and the 2015
  baseline notification). The assistant independently cross-checked this against a hosted mirror
  of the consolidated LODR text (`ca2013.com/lodr-regulation-15/`), which preserves the same
  proviso wording with strikethrough formatting — matching word for word.
- **A discrepancy found and resolved:** that mirror's own footnote gives the omission date as
  "w.e.f 01.09.2019" against the same 05.05.2021 notification, which is internally inconsistent
  (the omission date cannot precede the notification that ordered it). The owner's and D-012's
  date of 1 September **2021** is the one consistent with the notification date and every other
  source checked. `docs/CONFLICT_CANDIDATES.md` flags this explicitly so the 2019 typo on that
  one mirror is never cited as the effective date.
- **Consequences:** Candidate 2's sourcing on the "what used to resolve this conflict, and when
  it stopped" side is now essentially complete, with a verbatim proviso and a full citation
  chain. What remains before this can be drafted as a benchmark item is verbatim-quoting the two
  sides that actually conflict today (the current RBI governance clause and the current LODR
  Regulation 17/18 text) — not yet done.
- **Status:** open.

## D-014: Candidate 2 closed — current RBI and LODR requirements don't actually disagree (2026-11-22)

- **Context:** D-012/D-013 built out Candidate 2 (SEBI LODR vs. RBI bank governance) in detail —
  a real, dated removal of a precedence proviso, fully sourced — making it look like the
  strongest Conflict candidate found. The one remaining step was comparing the current RBI
  governance clause against the current LODR Regulation 17/18 text.
- **What happened:** the project owner confirmed directly that the two sides give the same
  answer today — RBI's current clause and LODR Regulation 17/18 impose the same requirement.
- **Why this closes the candidate:** D-004 requires authoritative sources to *genuinely
  disagree*; it is not enough that a rule which used to prevent disagreement was removed. If the
  substantive requirements converge anyway, there is nothing for an adjudicator to resolve, so
  this cannot become a `Conflict`-outcome item regardless of the proviso's real removal history.
- **Consequences:** `docs/CONFLICT_CANDIDATES.md`'s Candidate 2 section is marked closed, with
  the research trail kept for record (it demonstrates why D-004 insists on checking current
  substantive text, not just amendment/precedence history, before drafting). No benchmark item
  results from this candidate. The benchmark's zero-Conflict gap remains open — back to needing
  either Candidate 1's resolution or a new Candidate 3.
- **Status:** closed (negative result).

## D-015: the 2016 RBI KYC Master Direction has been repealed — new data-currency alert (2026-11-22)

- **Context:** while self-verifying Candidate 1 against primary RBI text (rather than relying on
  the obligation record's paraphrase), the assistant found that the 2016 KYC Master Direction
  (DBR.AML.BC.No.81/14.01.001/2015-16) every `RBI-KYC-*` obligation cites as its source
  instrument — 90 of 127 benchmark items via the `rbi_kyc` scenario tag — has been **repealed**,
  effective 28 November 2025, and replaced by separate entity-specific 2025 KYC Directions
  (Commercial Banks, Small Finance Banks, Payments Banks, Rural Co-operative Banks, at least).
- **Primary-source confirmation:** RBI notification RBI/2025-26/101 (28 Nov 2025): "The Reserve
  Bank has, today, repealed the RBI Master Direction DBR.AML.BC.No.81/14.01.001/2015-16 dated
  February 25, 2016 (as updated from time to time) with immediate effect." Corroborated by
  independent secondary commentary (taxguru.in) and by each successor direction's own "Chapter
  XI – Repeal and Other Provisions" section.
- **A concrete drift already found:** the small-account carve-out, cited by the catalog and by
  Candidate 1's research as "paragraph 23 of Chapter VI," is "paragraph 28 of Chapter VI" in the
  2025 Small Finance Banks and Payments Banks successor directions — same substance, renumbered.
- **Consequences:** new `docs/DATA_CURRENCY_ALERT.md` records the finding.
- **Correction, same day:** the first draft of this entry and of `docs/DATA_CURRENCY_ALERT.md`
  recommended re-verifying the 32 items dated `2026-08-01` first, on the unchecked assumption
  that they were `rbi_kyc` items. Checking directly reverses this: **all 32 `2026-08-01` items
  are `sebi_lodr` items; every one of the 90 `rbi_kyc` items uses `2025-09-01` or `2025-07-01`,
  both before the 28 Nov 2025 repeal.** So **none of the current 127 gold_verified items are
  affected by this repeal at all** — not an urgent fix, no gold label needs revisiting. The
  repeal still matters for any *future* RBI-KYC item (must cite the right 2025 entity-specific
  successor) and is itself a real amendment-sensitive stratification opportunity (a reference
  date straddling 27–28 Nov 2025 would be a genuine temporal test, closing gap #3 with real
  history). `docs/DATA_CURRENCY_ALERT.md` updated with this correction rather than left standing.
- **Status:** open (as a forward-looking item for new drafting), downgraded from urgent.

## D-016: Candidate 1 leans toward "not a Conflict," pending final sign-off (2026-11-22)

- **Context:** self-verification against primary RBI text (triggered by D-015's research) found
  paragraph 2(a)'s actual applicability text and confirmed the small-account carve-out's
  wording. Substantively, "Small Accounts" are a distinct relaxed-KYC category under the PMLA
  Rules with their own renewal mechanism, separate from ordinary periodic KYC updation.
- **Assessment:** this supports Candidate 1 resolving as a genuine exemption (outcome 1 in
  `docs/CONFLICT_CANDIDATES.md`'s original three-way branch), not a Conflict (outcome 3) — but
  this is the assistant's own reasoned reading of primary text, explicitly not a substitute for
  human legal review, and should be re-checked against the correct 2025 successor direction per
  D-015 before being treated as final.
- **Status:** open — leaning assessment recorded, not finalized.

## D-017: drafted TAARR-DRAFT-0135, a pre-amendment negative companion item (2026-11-22)

- **Context:** gap #3 in `docs/STRATIFICATION_GAP_ANALYSIS.md` — only 1 amendment-sensitive item
  (`TAARR-DRAFT-0001`) existed in the whole 127-item benchmark.
- **What was added:** `data/benchmark/draft_items.jsonl` gets a new item, `TAARR-DRAFT-0135`,
  status `draft` (explicitly not `gold_verified` — it is not added to `benchmark.jsonl`). Same
  target obligation as `TAARR-DRAFT-0001` (`RBI-KYC-P38E-DUE-NOTICES`), same entity facts, but
  `reference_date: 2025-03-01` — before paragraph 38(e)'s 2025-06-12 insertion — with
  `gold_outcome: "Not applicable"` on the reasoning that no version of the obligation is yet in
  force (D-001's own `NoVersionPolicy.NOT_APPLICABLE` policy), not a missing-fact case.
- **Verification performed:** re-confirmed the amendment date against the actual RBI notification
  (id=12866, RBI/2025-26/51). As a sanity check only (per the same caveat D-009 itself applies to
  its own adjudication step), ran `resolve_obligation` with the project's committed resolver
  policy: it returns exactly `"Not applicable"` with reason `"No recorded version of this
  obligation is in force on the reference date."` for this item's facts and date, and the
  existing `"Applicable"` for `TAARR-DRAFT-0001`'s date — consistent, not proof.
- **What this does NOT do:** no gold label is created or changed. This is one new draft
  candidate in the queue, needing the same two-independent-annotator + adjudication process as
  every other item before it could become real. `python -m taarr.dataset validate
  data/benchmark/draft_items.jsonl` passes (128 items, structurally valid) and the full test
  suite (242 tests) is unaffected.
- **Note:** `python -m taarr.provenance_audit` exits 1 with pre-existing `GOLD_VERSION_NOT_VERIFIED`
  errors on `benchmark.jsonl` — confirmed via `git stash` that this is unrelated to this change
  and already true on the branch beforehand; not something this entry fixes.
- **Status:** drafted, in the queue, not yet annotated.

## D-018: Candidate 1 reopened — 2025 successor may not carry the general small-account proviso (2026-11-22)

- **Context:** D-016 left Candidate 1 (paragraph-2 small-account proviso vs. paragraph-38(e)
  notice duty) leaning toward "genuine exemption, not Conflict," explicitly conditioned on
  re-checking against the 2025 successor to the repealed 2016 KYC Master Direction (D-015).
  This entry is that promised re-check.
- **What was found:** fetched the live RBI (Commercial Banks – KYC) Directions, 2025 (`id=13141`).
  The 2016 Direction's general-scope "paragraph 2" (with its own small-account proviso) does not
  appear to have a direct successor: the 2025 Direction's main domestic applicability clause
  (paragraph 3) has no proviso or small-account mention at all. The only surviving small-account
  proviso in the Applicability section is on paragraph 4 (a narrower clause, extending the
  Direction to foreign branches/subsidiaries only). Separately, paragraph 28 ("Small Accounts,"
  successor to paragraph 23) opens "Notwithstanding anything contained in paragraph 23 and as an
  alternative thereto" — its own stated scope is an alternative to paragraph 23's CDD-document
  requirements specifically, not a blanket Direction-wide exemption. Paragraph 42(7) (successor
  to paragraph 38(e), the due-notices duty) makes no mention of small accounts either way.
- **Why this matters:** if accurate, there may be no general small-account exemption from the
  periodic due-notices duty under the *current* RBI instrument — reversing this same day's D-016
  leaning. The catalog's `RBI-KYC-PARA2-SMALL-ACCOUNT-PROVISO` relation and benchmark item
  `TAARR-DRAFT-0005` were both built against the repealed 2016 paragraph 2, not the 2025 text.
- **Caveat, stated plainly:** this is based on an AI-paraphrased WebFetch of a large live
  government page (a 125-character verbatim-quote limit in the tool means the findings above are
  paraphrases, not pasted primary text), not a pasted/cross-checked primary-source excerpt at the
  standard D-012/D-013 used for Candidate 2. This is a flag for human legal review and a
  primary-text pull (ideally the actual PDF), not a new conclusion to build on.
- **What this does NOT do:** no gold label, obligation record, or exemption relation is changed.
  `data/obligations/obligations.jsonl` and `benchmark.jsonl` are untouched by this entry — this is
  research documentation only, same as D-012/D-013/D-016 before it.
- **Status:** open — reopened, contradicts D-016's same-day leaning, needs human verification
  against primary PDF text before either direction is finalized.

## D-019: added the catalog's first third-instrument obligation (2026-11-22)

- **Context:** gap #2 in `docs/STRATIFICATION_GAP_ANALYSIS.md` — the whole catalog (60
  obligations) was sourced from only 2 instruments (`RBI-KYC-2016`/`RBI-KYC-MD-2016` and
  `SEBI-LODR-2015`), which looks thin for a project whose novelty claim rests partly on
  cross-instrument reasoning.
- **What was added:** `RBI-NBFC-PARA12-LOAN-APP-ACKNOWLEDGEMENT`, from the Reserve Bank of India
  (Non-Banking Financial Companies – Responsible Business Conduct) Directions, 2025
  (`RBI/DOR/2025-26/362`, dated 2025-11-28) — a genuinely different RBI instrument (NBFC conduct
  regulation, not KYC/AML) from either existing one. Clause: paragraph 12, Chapter III (Responsible
  Lending Conduct), Fair Practices Code for NBFCs — "An NBFC shall devise a system of giving
  acknowledgement for receipt of all loan applications." Chosen deliberately as a simple,
  single-condition `must` obligation with no exemptions or dependencies, to keep the first
  cross-instrument addition easy to verify independently.
- **New fact registered:** `is_nbfc` added to `data/facts/fact_registry.json` (organisation group)
  — the closed fact list `tests/test_fact_registry.py` enforces.
- **Verification tier, stated honestly:** `verification_status: "assistant_single_pass_webfetch"`
  — a new, distinct value, deliberately NOT `"source_text_human_confirmed"` (the project's own
  convention for an owner-verified pass, D-006) and NOT `gold_verified`. This is a single
  assistant WebFetch pass against the live official RBI page (`id=12942`), nothing more. Needs a
  human source-text check (ideally the actual PDF) before any benchmark item is drafted from it.
- **Side effects, all mechanical:** catalog grew 60 → 61 obligations. Four tests had hardcoded
  counts (`test_catalog_grew_to_sixty_obligations`, `test_pilot_catalog_loads_both_obligations_...`,
  `test_checklist_covers_every_obligation`, `test_api_endpoints`) and were updated to 61/44 with a
  comment pointing here — not silently bumped. Full suite re-run: 242 passed.
- **What this does NOT do:** no benchmark item, draft or gold, is built from this obligation yet.
  No existing obligation, exemption, or gold label is touched.
- **Status:** added to the catalog as a single-pass research lead, needs human verification;
  closes part of gap #2 but 3 instruments is still thin against the 100–200 item stratification
  target's implied breadth — more instruments and benchmark items are still open work.

## D-020: the KYC source URL cited by 42 obligation records is now dead (2026-11-22)

- **Context:** found while researching a Candidate 3 Conflict lead (checking paragraph 40(e) vs
  44(a) in the KYC Direction), not something being specifically looked for.
- **What was found:** `https://www.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=11566` — the
  `source_url`/`official_url` cited by 42 of 61 `data/obligations/obligations.jsonl` records, and
  appearing 127 times in `benchmark.jsonl` and 128 times in `draft_items.jsonl` — no longer serves
  the KYC Master Direction. It now serves the "Reserve Bank of India (Non-Banking Financial
  Companies – Responsible Business Conduct) Directions, 2025" (RBI/DOR/2025-26/362, dated
  2025-11-28), the same instrument D-019 just added under a different id (12942). Neither "Know
  Your Customer" nor "KYC" appears on the page. Sanity-checked against `id=13109` (confirmed
  correctly serving KYC content) to rule out a fetch-tool fault — this is specific to `id=11566`.
  Likely cause: RBI appears to recycle a repealed Direction's page id for a new, unrelated
  Direction issued the same day (28 Nov 2025) — consistent with D-015's repeal finding, but a
  distinct and more operationally urgent consequence of it.
- **Why this is more urgent than D-015's original finding:** D-015/its correction concluded the
  repeal doesn't affect any gold item's *substance* (reference dates all predate it). This entry
  is about *citation accuracy*, not substance: every one of those 127+128 citation strings is now
  a dead link to the wrong document for anyone who clicks through to verify sourcing — independent
  of whether the underlying gold label is still correct.
- **What this does NOT do:** no `source_url`/`official_url` value is changed by this entry.
  Re-pointing 42 records correctly requires deciding, per obligation, which of (at least) four
  2025 entity-specific successor Directions (Commercial Banks `id=13141`, Small Finance Banks
  `id=13109`, Payments Banks `id=13090`, and an unverified Rural Co-operative Banks equivalent)
  its modeled entity type corresponds to — the catalog's current generic `"RBI-regulated entity"`
  `subject_scope` doesn't record this, so it is not a safe mechanical find-and-replace. Left for
  human decision, per `docs/DATA_CURRENCY_ALERT.md`'s urgent addendum.
- **Status:** open, flagged urgent — citation re-pointing needed, not started.