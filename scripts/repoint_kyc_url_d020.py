"""One-off script for D-020 / D-021: re-point the dead id=11566 KYC citation to the
live Commercial Banks 2025 successor (id=13141), per owner instruction (2026-11-22):
assume all existing generic "RBI-regulated entity" obligations are modeled on Commercial
Banks specifically.

Scope, deliberately narrow: this changes source_url / consolidated_source_url / official_url
and instrument_id / instrument_title wherever the old id=11566 URL appears. It does NOT
renumber clause_id / paragraph references except the ones already confirmed in this
session (38(e)->42(7), 40(e)->44(5), 23->28) -- those stay as recorded by prior commits.
Every other clause_id in the catalog still reflects 2016 numbering and is flagged with a
note, not silently assumed correct against the new document.

Run once; not meant to be part of the normal pipeline.
"""
import json
from pathlib import Path

OLD_URL = "https://www.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=11566"
NEW_URL = "https://www.rbi.org.in/scripts/BS_ViewMasDirections.aspx?id=13141"
NEW_INSTRUMENT_ID = "RBI-KYC-CB-2025"
NEW_INSTRUMENT_TITLE = (
    "Reserve Bank of India (Commercial Banks – Know Your Customer) Directions, 2025"
)
NOTE = (
    "2026-11-22 (D-020/repoint): source_url/official_url re-pointed from the now-dead "
    f"{OLD_URL} (confirmed by this project to no longer serve KYC content -- see "
    "docs/DECISIONS.md D-020) to the live 2025 Commercial Banks KYC successor, "
    f"{NEW_URL}, per explicit owner instruction to assume all existing generic "
    "'RBI-regulated entity' obligations are modeled on Commercial Banks specifically. "
    "This fixes the citation link only. clause_id/paragraph numbers in this record have "
    "NOT been individually re-verified against the new document's numbering, except "
    "where a separate commit already confirmed the mapping (38(e)->42(7), 40(e)->44(5), "
    "23->28). Treat any other clause_id here as still reflecting 2016 numbering until "
    "checked."
)

ROOT = Path(__file__).resolve().parent.parent


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
        touched = False
        if rec.get("source_url") == OLD_URL:
            rec["source_url"] = NEW_URL
            touched = True
        if rec.get("consolidated_source_url") == OLD_URL:
            rec["consolidated_source_url"] = NEW_URL
            touched = True
        for exemption in rec.get("exemptions", []):
            if exemption.get("official_url") == OLD_URL:
                exemption["official_url"] = NEW_URL
                touched = True
        for dependency in rec.get("dependencies", []):
            if dependency.get("official_url") == OLD_URL:
                dependency["official_url"] = NEW_URL
                touched = True
        if touched:
            if rec.get("instrument_id") in ("RBI-KYC-2016", "RBI-KYC-MD-2016"):
                rec["instrument_id"] = NEW_INSTRUMENT_ID
            rec["instrument_title"] = NEW_INSTRUMENT_TITLE
            existing_notes = rec.get("notes", "")
            rec["notes"] = (existing_notes + " " if existing_notes else "") + NOTE
            changed += 1
        out.append(json.dumps(rec))
    path.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"obligations.jsonl: {changed} records updated")


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
            if obligation.get("official_url") == OLD_URL:
                obligation["official_url"] = NEW_URL
                touched = True
            if obligation.get("instrument_id") in ("RBI-KYC-2016", "RBI-KYC-MD-2016"):
                obligation["instrument_id"] = NEW_INSTRUMENT_ID
                touched = True
        for relation in item.get("exemptions_dependencies", []):
            if relation.get("official_url") == OLD_URL:
                relation["official_url"] = NEW_URL
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
