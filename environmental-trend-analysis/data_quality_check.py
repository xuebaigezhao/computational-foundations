import pandas as pd

df = pd.read_csv(
    "environmental-trend-analysis/temperature_observations_dirty.csv"
)

print(df)

print(df.duplicated())
count_duplicates = df.duplicated().sum()
print("Number of duplicate rows:", count_duplicates)
duplicate_years = df.duplicated(subset=["year"])
print("Duplicate years:")
print(df[duplicate_years])

invalid_temperature = (df["temperature"] > 60) | (df["temperature"] < -50)
print("Invalid temperature values:")
print(df[invalid_temperature])
print(
    "Years monotonically increasing:",
    df["year"].is_monotonic_increasing
)

year_difference = df["year"].diff()

print(year_difference)
invalid_year_order = year_difference <= 0
print("Invalid chronological records:")
print(df[invalid_year_order])

print("\nChronological check:")
print(df["year"].is_monotonic_increasing)

year_difference = df["year"].diff()

invalid_year_order = year_difference <= 0

print("Invalid chronological records:")
print(df[invalid_year_order])
