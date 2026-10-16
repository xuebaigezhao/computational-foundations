import pandas as pd

df = pd.read_csv(
    "environmental-trend-analysis/temperature_observations.csv"
)

print(df)

print("\nShape:")
print(df.shape)

print("\nColumn names:")
print(df.columns)

print("\nData types:")
print(df.dtypes)

print("\nMissing values:")
print(df.isna().sum())

print("\nSummary statistics:")
print(df.describe())
clean_df = df.dropna(subset=["temperature"]).copy()
print("\nCleaned data:")
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
intercept = mean_temperature - slope * mean_year
predicted_temperatures = slope * years + intercept
residuals = temperatures - predicted_temperatures
rmse = (residuals**2).mean() ** 0.5
clean_df["predicted_temperature"] = predicted_temperatures
clean_df["residual"] = residuals

print("\nCleaned data with predictions and residuals:")
print(clean_df)
print("\nRMSE:")
print(rmse)
print("\nSlope:", slope)
print("Intercept:", intercept)
print("Mean year:", mean_year)
print("Mean temperature:", mean_temperature)
print(df.dtypes)