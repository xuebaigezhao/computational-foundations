import numpy as np

temperatures_list = [4.2, 4.5, 4.9, 5.0, 5.4, 5.2]

temperatures_array = np.array(temperatures_list)

print("Python list:")
print(temperatures_list * 2)

print("\nNumPy array:")
print(temperatures_array * 2)
years = np.array([2018, 2019, 2021, 2022, 2024, 2025])
temperatures = np.array([4.2, 4.5, 4.9, 5.0, 5.4, 5.2])

mean_year = years.mean()
mean_temperature = temperatures.mean()

print("Mean year:", mean_year)
print("Mean temperature:", mean_temperature)

product = (years - mean_year) * (temperatures - mean_temperature)
numerator = product.sum()
denominator = (years - mean_year)**2
slope = numerator / denominator.sum()
print("Slope:", slope)

import pandas as pd

observations = [
    {"year": 2018, "temperature": 4.2},
    {"year": 2019, "temperature": 4.5},
    {"year": 2020, "temperature": None},
    {"year": 2021, "temperature": 4.9},
    {"year": 2022, "temperature": 5.0},
    {"year": 2023, "temperature": None},
    {"year": 2024, "temperature": 5.4},
    {"year": 2025, "temperature": 5.2},
]

df = pd.DataFrame(observations)

print(df)

print("Total rows:", len(df))
print("Missing temperatures:", df["temperature"].isna().sum())

clean_df = df.dropna(subset=["temperature"]).copy()

print(clean_df)

years = clean_df["year"]
temperatures = clean_df["temperature"]
mean_year = years.mean()
mean_temperature = temperatures.mean()

year_deviation = years - mean_year
temperature_deviation = temperatures - mean_temperature

numerator = (year_deviation * temperature_deviation).sum()
denominator = (year_deviation**2).sum()
slope = numerator / denominator
print("Pandas Slope:", slope)

incept = mean_temperature - slope * mean_year
clean_df["predicted_temperature"] = slope * clean_df["year"] + incept
clean_df["residual"] = clean_df["temperature"] - clean_df["predicted_temperature"]
clean_df["year"]
clean_df["temperature"]
print(clean_df)
clean_df["squared_error"] = clean_df["residual"] ** 2
mse = clean_df["squared_error"].mean()
rmse = np.sqrt(mse)

print("Mean Squared Error (MSE):", mse)
print("Root Mean Squared Error (RMSE):", rmse)