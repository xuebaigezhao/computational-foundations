import matplotlib.pyplot as plt


# -----------------------------
# 1. Raw environmental data
# -----------------------------

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


# -----------------------------
# 2. Inspect missing data
# -----------------------------

def inspect_observations(observations):
    total_years = len(observations)
    valid_data = 0
    missing_years = []

    for observation in observations:
        if observation["temperature"] is not None:
            valid_data = valid_data + 1
        else:
            missing_years.append(observation["year"])

    return total_years, valid_data, missing_years


total_years, valid_data, missing_years = inspect_observations(observations)

print("Total years:", total_years)
print("Valid observations:", valid_data)
print("Missing years:", missing_years)


# -----------------------------
# 3. Remove missing observations
# -----------------------------

def remove_missing_observations(observations):
    cleaned = []

    for observation in observations:
        if observation["temperature"] is not None:
            cleaned.append(observation)

    return cleaned


cleaned_observations = remove_missing_observations(observations)


# -----------------------------
# 4. Extract year and temperature
# -----------------------------

def extract_variables(cleaned_observations):
    years = []
    temperatures = []

    for observation in cleaned_observations:
        years.append(observation["year"])
        temperatures.append(observation["temperature"])

    return years, temperatures


years, temperatures = extract_variables(cleaned_observations)

print("Years:", years)
print("Temperatures:", temperatures)


# -----------------------------
# 5. Endpoint comparison
# -----------------------------

def endpoint_change(cleaned_observations):
    first_temperature = cleaned_observations[0]["temperature"]
    last_temperature = cleaned_observations[-1]["temperature"]

    return last_temperature - first_temperature


change = endpoint_change(cleaned_observations)

print("Endpoint change:", change, "°C")


# -----------------------------
# 6. Calculate linear regression slope
# -----------------------------

mean_year = sum(years) / len(years)
mean_temperature = sum(temperatures) / len(temperatures)

numerator = 0
denominator = 0

for year, temperature in zip(years, temperatures):
    year_deviation = year - mean_year
    temperature_deviation = temperature - mean_temperature

    product = year_deviation * temperature_deviation

    numerator = numerator + product
    denominator = denominator + year_deviation ** 2

slope = numerator / denominator

print("Mean year:", mean_year)
print("Mean temperature:", mean_temperature)
print("Slope:", slope, "°C/year")


# -----------------------------
# 7. Calculate intercept
# -----------------------------

intercept = mean_temperature - slope * mean_year

print("Intercept:", intercept)


# -----------------------------
# 8. Generate model predictions
# -----------------------------

predicted_temperatures = []

for year in years:
    predicted = intercept + slope * year
    predicted_temperatures.append(predicted)


print("\nActual vs predicted:")

for year, actual, predicted in zip(
    years,
    temperatures,
    predicted_temperatures
):
    print(year, actual, predicted)


# -----------------------------
# 9. Calculate residuals
# -----------------------------

residuals = []

for actual, predicted in zip(
    temperatures,
    predicted_temperatures
):
    residual = actual - predicted
    residuals.append(residual)

print("\nResiduals:", residuals)


# -----------------------------
# 10. Calculate MSE and RMSE
# -----------------------------

squared_errors = []

for residual in residuals:
    squared_error = residual ** 2
    squared_errors.append(squared_error)

mse = sum(squared_errors) / len(squared_errors)
rmse = mse ** 0.5

print("MSE:", mse)
print("RMSE:", rmse, "°C")


# -----------------------------
# 11. Plot observations and fitted trend
# -----------------------------

plt.scatter(years, temperatures)
plt.plot(years, predicted_temperatures)

plt.xlabel("Year")
plt.ylabel("Temperature (°C)")
plt.title("Observed Summer Temperature and Linear Trend")

plt.show()


# -----------------------------
# 12. Plot residuals over time
# -----------------------------

plt.scatter(years, residuals)
plt.axhline(0)

plt.xlabel("Year")
plt.ylabel("Residual (°C)")
plt.title("Residuals over Time")

plt.show()
