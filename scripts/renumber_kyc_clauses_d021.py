"""D-021: update clause_id values for the 42 RBI-KYC-CB-2025 records to the confirmed
paragraph numbers in the live Commercial Banks 2025 KYC Direction (id=13141), following
D-020's URL re-pointing. Every mapping below was checked against the live document via
WebFetch this session and cross-checked against this catalog's own recorded clause_text
for substance match (not just number lookup) -- see docs/DECISIONS.md D-021 for the full
research trail and the AI-paraphrase caveat that applies throughout.

Old clause_id (2016 numbering, as currently stored) -> new clause_id (2025 Commercial
Banks numbering, confirmed this session).
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Keyed by obligation_id, since several obligations share an old clause_id string
# (e.g. five different obligations were all tagged "paragraph-38") but map to distinct
# new sub-clauses.
MAPPING = {
    "RBI-KYC-P38E-DUE-NOTICES": "paragraph-42(7)",
    "RBI-KYC-PARA39-PAN-FORM60": "paragraph-43",
    "RBI-KYC-PARA17-OTP-EKYC-BALANCE-CAP": "paragraph-25",
    "RBI-KYC-PARA13-WALKIN-THRESHOLD": "paragraph-21(5)-(6)",
    "RBI-KYC-PARA41A-PEP-APPROVAL": "paragraph-45(1)(iii)",
    "RBI-KYC-PARA18C-VCIP-DATA-LOCALIZATION": "paragraph-27(3)(i)",
    "RBI-KYC-PARA40F-NONFACETOFACE-HIGHRISK": "paragraph-44(6)",
    "RBI-KYC-PARA46A-RECORD-RETENTION": "paragraph-50(1)",
    "RBI-KYC-PARA10-1-ANONYMOUS-ACCOUNT-PROHIBITION": "paragraph-17(1)",
    "RBI-KYC-PARA10-2-CDD-INCOMPLETE-BAR": "paragraph-17(3)",
    "RBI-KYC-PARA3-BO-COMPANY-THRESHOLD": "paragraph-5(1)(iv)(a)",
    "RBI-KYC-PARA3-BO-UNINCORPORATED-THRESHOLD": "paragraph-5(1)(iv)(c)",
    "RBI-KYC-PARA3-BO-TRUST-THRESHOLD": "paragraph-5(1)(iv)(d)",
    "RBI-KYC-PARA16B-INDIVIDUAL-PAN-FORM60": "paragraph-23(5)",
    "RBI-KYC-PARA30-COMPANY-PAN": "paragraph-33(3)",
    "RBI-KYC-PARA32-TRUST-PAN-FORM60": "paragraph-35(3)",
    "RBI-KYC-PARA5A-RISK-METHODOLOGY-ANNUAL-REVIEW": "paragraph-10(2)",
    "RBI-KYC-PARA37A-RISK-REVIEW-PERIODICITY": "paragraph-41(1)",
    "RBI-KYC-PARA12-4-RISK-RATING-CONFIDENTIALITY": "paragraph-20(4)",
    "RBI-KYC-PARA38-HIGHRISK-REKYC-2YEARS": "paragraph-42(1)",
    "RBI-KYC-PARA38-MEDIUMRISK-REKYC-8YEARS": "paragraph-42(1)",
    "RBI-KYC-PARA38-LOWRISK-REKYC-10YEARS": "paragraph-42(1)",
    "RBI-KYC-PARA38-ADDRESS-CHANGE-VERIFICATION": "paragraph-42(3)(ii)",
    "RBI-KYC-PARA38-ADVANCE-INTIMATION-COUNT": "paragraph-42(7)",
    "RBI-KYC-PARA39-CESSATION-ON-NONCOMPLIANCE": "paragraph-43",
    "RBI-KYC-PARA40B-MOBILE-NUMBER-RESTRICTION": "paragraph-44(2)",
    "RBI-KYC-PARA40C-ADDRESS-VERIFICATION-BEFORE-OPERATIONS": "paragraph-44(3)",
    "RBI-KYC-PARA40E-FIRST-TRANSACTION-SOURCE": "paragraph-44(5)",
    "RBI-KYC-PARA43-SHG-MEMBER-CDD-RELIEF": "paragraph-47(1)",
    "RBI-KYC-PARA44A-LOCAL-ADDRESS-DECLARATION": "paragraph-48(1)",
    "RBI-KYC-PARA44A-REMITTANCE-CAP-PENDING-VERIFICATION": "paragraph-48(1)-(2)",
    "RBI-KYC-PARA44C-PAKISTANI-STUDENT-APPROVAL": "paragraph-48(3)",
    "RBI-KYC-PARA46B-IDENTIFICATION-RECORD-RETENTION": "paragraph-50(2)",
    "RBI-KYC-PARA6D-DESIGNATED-DIRECTOR-SEPARATION": "paragraph-14(3)",
    "RBI-KYC-PARA42-6-ULTIMATE-RESPONSIBILITY": "paragraph-46(6)",
    "RBI-KYC-PARA11A-STR-IN-LIEU-OF-CDD": "paragraph-19",
    "RBI-KYC-PARA13-2-INTL-TRANSFER-CDD": "paragraph-21(2)",
    "RBI-KYC-PARA18B-IV-VCIP-PROMPTING-REJECTION": "paragraph-27(2)(iv)",
    "RBI-KYC-PARA18B-XII-VCIP-CONCURRENT-AUDIT": "paragraph-27(2)(xv)",
    "RBI-KYC-PARA18B-VI-AADHAAR-FRESHNESS": "paragraph-27(2)(viii)-(ix)",
    "RBI-KYC-PARA14-4-THIRD-PARTY-JURISDICTION-RESTRICTION": "paragraph-22(4)",
    "RBI-KYC-PARA49-NO-RESTRICTION-ON-STR-FILING": "paragraph-54",
}

NOTE_TEMPLATE = (
    "2026-11-22 (D-021): clause_id updated from the old 2016-numbering value {old!r} to "
    "{new!r}, the confirmed paragraph in the live Commercial Banks 2025 KYC Direction "
    "(id=13141, re-pointed in D-020). Confirmed via WebFetch this session by matching this "
    "record's own clause_text/clause_summary against the live document's substance, not by "
    "number lookup alone. Same AI-paraphrase caveat as D-018/D-020 applies: this is a single "
    "assistant research pass, not a pasted/human-verified primary-text excerpt. The old "
    "clause_id is preserved here, in this note, for traceability."
)


def fix_obligations():
    path = ROOT / "data/obligations/obligations.jsonl"
    lines = path.read_text(encoding="utf-8").splitlines()
    out = []
    changed = 0
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            out.append(line)
            continue
        rec = json.loads(stripped)
        new_clause = MAPPING.get(rec.get("obligation_id"))
        if new_clause and rec.get("instrument_id") == "RBI-KYC-CB-2025":
            old_clause = rec["clause_id"]
            rec["clause_id"] = new_clause
            note = NOTE_TEMPLATE.format(old=old_clause, new=new_clause)
            existing_notes = rec.get("notes", "")
            rec["notes"] = (existing_notes + " " if existing_notes else "") + note
            changed += 1
        out.append(json.dumps(rec))
    path.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"obligations.jsonl: {changed} clause_id values updated")


def fix_benchmark_style_file(relative_path):
    path = ROOT / relative_path
    lines = path.read_text(encoding="utf-8").splitlines()
    out = []
    changed_items = 0
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            out.append(line)
            continue
        item = json.loads(stripped)
        touched = False
        for obligation in item.get("gold_obligations", []):
            new_clause = MAPPING.get(obligation.get("obligation_id"))
            if new_clause and obligation.get("instrument_id") == "RBI-KYC-CB-2025":
                obligation["clause_id"] = new_clause
                touched = True
        if touched:
            changed_items += 1
        out.append(json.dumps(item))
    path.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"{relative_path}: {changed_items} items updated")


if __name__ == "__main__":
    fix_obligations()
    fix_benchmark_style_file("data/benchmark/benchmark.jsonl")
    fix_benchmark_style_file("data/benchmark/draft_items.jsonl")
