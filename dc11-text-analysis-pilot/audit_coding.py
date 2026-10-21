
from pathlib import Path
import pandas as pd
import re

# Locate the project folder and input files.
project_dir = Path(__file__).resolve().parent
coding_path = project_dir / "qualitative_coding.csv"
texts_dir = project_dir / "texts"

coding = pd.read_csv(coding_path)

required_columns = [
    "doc_id",
    "section_reference",
    "excerpt",
    "initial_code",
    "broader_theme",
    "interpretation_note",
]

missing_columns = [
    col for col in required_columns
    if col not in coding.columns
]

if missing_columns:
    raise ValueError(
        f"Missing columns: {missing_columns}"
    )

# Normalise whitespace and capitalisation for comparison.
def normalise(text):
    text = str(text).casefold()
    return re.sub(r"\s+", " ", text).strip()

results = []

for _, row in coding.iterrows():
    doc_id = str(row["doc_id"])
    excerpt = str(row["excerpt"])

    text_path = texts_dir / f"{doc_id}.txt"

    if not text_path.exists():
        results.append({
            "doc_id": doc_id,
            "section_reference": row["section_reference"],
            "initial_code": row["initial_code"],
            "excerpt_found": False,
            "audit_status": "SOURCE FILE MISSING",
        })
        continue

    source_text = text_path.read_text(
        encoding="utf-8"
    )

    source_normalised = normalise(source_text)
    excerpt_normalised = normalise(excerpt)

    found = excerpt_normalised in source_normalised

    results.append({
        "doc_id": doc_id,
        "section_reference": row["section_reference"],
        "initial_code": row["initial_code"],
        "excerpt_found": found,
        "audit_status": (
            "PASS"
            if found
            else "REVIEW MANUALLY"
        ),
    })

audit = pd.DataFrame(results)

output_path = project_dir / "coding_audit.csv"

audit.to_csv(
    output_path,
    index=False,
    encoding="utf-8-sig"
)

print("Total coding records:", len(audit))
print("\nAudit status:")
print(audit["audit_status"].value_counts())

print("\nRecords requiring review:")
print(
    audit.loc[
        audit["audit_status"] != "PASS",
        [
            "doc_id",
            "section_reference",
            "initial_code",
            "audit_status",
        ],
    ].to_string(index=False)
)

print("\nSaved audit results to:")
print(output_path)
