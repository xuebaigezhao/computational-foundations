
from pathlib import Path
import pandas as pd
import re

PROJECT_DIR = Path(__file__).resolve().parent

inventory = pd.read_csv(PROJECT_DIR / "corpus_texts.csv")

# Core keyword groups: use the same definitions
# as analyse_texts.py.
keyword_groups = {
    "response diversity": [
        "response diversity"
    ],
    "resilience": [
        "ecosystem resilience",
        "ecological resilience"
    ],
    "stability": [
        "ecosystem stability",
        "ecological stability"
    ],
    "environmental change": [
        "environmental change"
    ],
    "biodiversity": [
        "biodiversity"
    ],
    "monitoring": [
        "monitoring",
        "monitor"
    ]
}

# Additional terms for exploratory reading.
exploratory_terms = [
    "habitat",
    "condition",
    "quality",
    "indicator",
    "pollinator",
    "restoration"
]

results = []

for _, row in inventory.iterrows():
    text_path = PROJECT_DIR / row["text_path"]
    text = text_path.read_text(encoding="utf-8")

    # Normalise whitespace so line breaks do not
    # interfere with phrase matching.
    text = re.sub(r"\s+", " ", text)

    # 1. Search predefined keyword groups.
    for group, terms in keyword_groups.items():
        for term in terms:
            pattern = re.compile(
                rf"\b{re.escape(term)}\b",
                flags=re.IGNORECASE
            )

            for match in pattern.finditer(text):
                start = max(0, match.start() - 70)
                end = min(len(text), match.end() + 70)

                results.append({
                    "doc_id": row["doc_id"],
                    "match_type": "core_keyword",
                    "concept": group,
                    "matched_term": term,
                    "context": text[start:end]
                })

    # 2. Search additional exploratory terms.
    for term in exploratory_terms:
        pattern = re.compile(
            rf"\b{re.escape(term)}\b",
            flags=re.IGNORECASE
        )

        for match in pattern.finditer(text):
            start = max(0, match.start() - 70)
            end = min(len(text), match.end() + 70)

            results.append({
                "doc_id": row["doc_id"],
                "match_type": "exploratory",
                "concept": term,
                "matched_term": term,
                "context": text[start:end]
            })

contexts_df = pd.DataFrame(
    results,
    columns=[
        "doc_id",
        "match_type",
        "concept",
        "matched_term",
        "context"
    ]
)

output_path = PROJECT_DIR / "keyword_contexts.csv"
contexts_df.to_csv(output_path, index=False)

print("Context records:", len(contexts_df))

print("\nCore keyword matches:")
core = contexts_df[
    contexts_df["match_type"] == "core_keyword"
]

if not core.empty:
    print(
        core.groupby(["doc_id", "concept"])
        .size()
        .to_string()
    )

print("\nExploratory term matches:")
exploratory = contexts_df[
    contexts_df["match_type"] == "exploratory"
]

if not exploratory.empty:
    print(
        exploratory.groupby(["doc_id", "concept"])
        .size()
        .to_string()
    )

print("\nSaved contexts to:", output_path)
