from pathlib import Path
import pandas as pd
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

# --------------------------------------------------
# 1. Locate project files
# --------------------------------------------------

project_dir = Path(__file__).resolve().parent
coding_path = project_dir / "qualitative_coding.csv"

coding = pd.read_csv(coding_path)

# --------------------------------------------------
# 2. Define the scientific concept
# --------------------------------------------------

query = (
    "Response diversity describes the variation in species' "
    "ecological responses to environmental change."
)

# --------------------------------------------------
# 3. Select the ten POL01 clauses
# --------------------------------------------------

policy = coding[coding["doc_id"] == "POL01"].copy()

policy = policy[
    ["section_reference", "excerpt", "initial_code", "broader_theme"]
].reset_index(drop=True)

print("Policy clauses loaded:", len(policy))

# --------------------------------------------------
# 4. Load a pretrained sentence-embedding model
# --------------------------------------------------

model_name = "sentence-transformers/all-MiniLM-L6-v2"

print("\nLoading model:")
print(model_name)

model = SentenceTransformer(model_name)

# --------------------------------------------------
# 5. Convert query and policy clauses into embeddings
# --------------------------------------------------

query_embedding = model.encode(
    query,
    convert_to_tensor=True
)

policy_embeddings = model.encode(
    policy["excerpt"].tolist(),
    convert_to_tensor=True
)

# --------------------------------------------------
# 6. Calculate cosine similarity
# --------------------------------------------------

similarities = cos_sim(
    query_embedding,
    policy_embeddings
)[0]

policy["semantic_similarity"] = (
    similarities.cpu().numpy()
)

# --------------------------------------------------
# 7. Rank the policy clauses
# --------------------------------------------------

ranked = policy.sort_values(
    "semantic_similarity",
    ascending=False
).reset_index(drop=True)

ranked.insert(
    0,
    "rank",
    range(1, len(ranked) + 1)
)

# --------------------------------------------------
# 8. Save and display results
# --------------------------------------------------

output_path = (
    project_dir /
    "semantic_similarity_results.csv"
)

ranked.to_csv(
    output_path,
    index=False,
    encoding="utf-8-sig"
)

print("\nQuery:")
print(query)

print("\nSemantic similarity ranking:\n")

print(
    ranked[
        [
            "rank",
            "section_reference",
            "semantic_similarity",
            "initial_code",
        ]
    ].to_string(index=False)
)

print("\nTop 3 clauses for manual interpretation:\n")

for _, row in ranked.head(3).iterrows():
    print("=" * 70)
    print("Rank:", row["rank"])
    print("Clause:", row["section_reference"])
    print(
        "Similarity:",
        round(row["semantic_similarity"], 3)
    )
    print("Excerpt:")
    print(row["excerpt"])
    print()

print("Saved results to:")
print(output_path)