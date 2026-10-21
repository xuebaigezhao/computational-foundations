
import pandas as pd

# 1. Load the corpus inventory
df = pd.read_csv("dc11-text-analysis-pilot/corpus_inventory.csv")

# 2. Inspect the dataset
print("First five rows:")
print(df.head())

print("\nShape:")
print(df.shape)

print("\nColumn names:")
print(df.columns.tolist())

print("\nData types:")
print(df.dtypes)

# 3. Check missing values
print("\nMissing values:")
print(df.isna().sum())

# 4. Check duplicate document IDs
print("\nDuplicate document IDs:")
print(df[df["doc_id"].duplicated(keep=False)])

# 5. Check document categories
print("\nCorpus type counts:")
print(df["corpus_type"].value_counts())

# 6. Check publication years
print("\nYear range:")
print(df["year"].min(), "to", df["year"].max())

# 7. Check empty titles and source URLs
print("\nEmpty titles:", df["title"].isna().sum())
print("Empty source URLs:", df["source_url"].isna().sum())

# 8. Check whether the inventory has the expected number of records
print("\nNumber of documents:", len(df))
print("Expected number of documents: 5")
