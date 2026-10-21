
from pathlib import Path
import pandas as pd

# Locate the project folder
PROJECT_DIR = Path(__file__).resolve().parent

# Load the text inventory
inventory_path = PROJECT_DIR / "corpus_texts.csv"
df = pd.read_csv(inventory_path)

print("Corpus inventory shape:", df.shape)
print("\nColumn names:")
print(df.columns.tolist())

# Check missing metadata
print("\nMissing values:")
print(df.isna().sum())

# Check duplicate document IDs
print("\nDuplicate document IDs:")
print(df[df["doc_id"].duplicated(keep=False)])

# Read and validate each text file
print("\nText file validation:")

for _, row in df.iterrows():
    text_path = PROJECT_DIR / row["text_path"]

    print(f"\nDocument ID: {row['doc_id']}")
    print(f"Text path: {row['text_path']}")

    if not text_path.exists():
        print("ERROR: Text file not found.")
        continue

    text = text_path.read_text(encoding="utf-8")

    print("Characters:", len(text))
    print("Characters excluding outer whitespace:", len(text.strip()))
    print("Text is empty:", not bool(text.strip()))
    print("First 100 characters:", repr(text[:100]))

print("\nValidation complete.")
