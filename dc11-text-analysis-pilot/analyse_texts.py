
from pathlib import Path
from collections import Counter
import re
import pandas as pd

# 1. Locate the project directory
PROJECT_DIR = Path(__file__).resolve().parent

# 2. Load the text inventory
df = pd.read_csv(PROJECT_DIR / "corpus_texts.csv")

# 3. Define a simple text-cleaning function
def clean_text(text):
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# 4. Define the terms we want to investigate
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
        "ecological stability",
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

# Common words that are usually less informative
stopwords = {
    "the", "a", "an", "and", "or", "of", "to", "in",
    "is", "are", "was", "were", "for", "with", "by",
    "from", "on", "as", "it", "this", "that", "these",
    "those", "be", "been", "being", "we", "they", "their",
    "has", "have", "had", "can", "may", "should", "will"
}

# 5. Read and analyse each text
results = []
for _, row in df.iterrows():
    text_path = PROJECT_DIR / row["text_path"]
    raw_text = text_path.read_text(encoding="utf-8")

    cleaned_text = clean_text(raw_text)

    # Extract individual words
    tokens = re.findall(
        r"[a-z]+(?:[-'][a-z]+)*",
        cleaned_text
    )

    # Remove common words for a more informative frequency list
    content_words = [
        word for word in tokens
        if word not in stopwords
    ]

    word_counts = Counter(content_words)

    print("\n" + "=" * 50)
    print("Document:", row["doc_id"])
    print("=" * 50)

    print("Total word tokens:", len(tokens))
    print("Unique word tokens:", len(set(tokens)))

    print("\nTop 10 content words:")
    for word, count in word_counts.most_common(10):
        print(f"{word}: {count}")


    print("\nKeyword group counts:")

    for group, terms in keyword_groups.items():
        count = sum(
            len(
                re.findall(
                    rf"\b{re.escape(term)}\b",
                    cleaned_text
    )
)
            for term in terms
        )
        print(f"{group}: {count}")

        results.append({
            "doc_id": row["doc_id"],
            "keyword_group": group,
            "count": count,
            "total_word_tokens": len(tokens),
            "count_per_100_words": round(
                count / len(tokens) * 100, 3
            )
        })

# 6. Save keyword counts to CSV
results_df = pd.DataFrame(results)

output_path = PROJECT_DIR / "keyword_counts.csv"
results_df.to_csv(output_path, index=False)

print("\nSaved keyword counts to:", output_path)
print("\nStructured results:")
print(results_df)


# 7. Create a comparison matrix
comparison_matrix = results_df.pivot(
    index="doc_id",
    columns="keyword_group",
    values="count_per_100_words"
)

print("\nNormalized keyword comparison matrix:")
print(comparison_matrix.round(3))

# 8. Save the comparison matrix
matrix_path = PROJECT_DIR / "keyword_comparison_matrix.csv"
comparison_matrix.to_csv(matrix_path)

print("\nSaved comparison matrix to:", matrix_path)
