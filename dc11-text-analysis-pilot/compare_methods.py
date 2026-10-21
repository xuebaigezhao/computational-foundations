
from pathlib import Path
import pandas as pd

# Locate files relative to this script.
project_dir = Path(__file__).resolve().parent

keyword_path = project_dir / "keyword_counts.csv"
coding_path = project_dir / "qualitative_coding.csv"

# Load the two datasets.
keywords = pd.read_csv(keyword_path)
coding = pd.read_csv(coding_path)

print("Keyword data columns:")
print(keywords.columns.tolist())

print("\nQualitative coding columns:")
print(coding.columns.tolist())

# Check that the expected columns exist.
required_keyword_columns = {
    "doc_id", "keyword_group", "count"
}

required_coding_columns = {
    "doc_id", "initial_code", "broader_theme"
}

if not required_keyword_columns.issubset(keywords.columns):
    raise ValueError(
        "keyword_counts.csv is missing expected columns."
    )

if not required_coding_columns.issubset(coding.columns):
    raise ValueError(
        "qualitative_coding.csv is missing expected columns."
    )

# Summarise raw keyword counts.
keyword_counts = keywords.pivot_table(
    index="doc_id",
    columns="keyword_group",
    values="count",
    aggfunc="sum",
    fill_value=0
)

keyword_counts.columns = [
    f"keyword_count__{col}"
    for col in keyword_counts.columns
]

keyword_counts = keyword_counts.reset_index()

# Summarise normalised keyword frequencies, if available.
if "count_per_100_words" in keywords.columns:
    keyword_rates = keywords.pivot_table(
        index="doc_id",
        columns="keyword_group",
        values="count_per_100_words",
        aggfunc="sum",
        fill_value=0
    )

    keyword_rates.columns = [
        f"keyword_rate_per_100_words__{col}"
        for col in keyword_rates.columns
    ]

    keyword_rates = keyword_rates.reset_index()

    keyword_counts = keyword_counts.merge(
        keyword_rates,
        on="doc_id",
        how="outer"
    )

# Summarise manual qualitative coding.
qualitative_summary = (
    coding.groupby("doc_id")
    .agg(
        coded_passages=("initial_code", "size"),
        initial_codes=(
            "initial_code",
            lambda s: " | ".join(s.dropna().astype(str))
        ),
        broader_themes=(
            "broader_theme",
            lambda s: " | ".join(
                pd.unique(s.dropna().astype(str))
            )
        )
    )
    .reset_index()
)

# Combine the summaries without treating them as equivalent measures.
comparison = keyword_counts.merge(
    qualitative_summary,
    on="doc_id",
    how="outer"
)

output_path = project_dir / "method_comparison_summary.csv"

comparison.to_csv(
    output_path,
    index=False,
    encoding="utf-8-sig"
)

print("\nMethod comparison summary:")
print(comparison.to_string(index=False))

print("\nSaved to:")
print(output_path)
