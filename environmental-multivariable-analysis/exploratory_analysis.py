import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm

from statsmodels.stats.outliers_influence import variance_inflation_factor


# ============================================================
# Helper functions
# ============================================================

def calculate_rmse(residuals):
    squared_errors = residuals ** 2
    mse = squared_errors.mean()
    rmse = mse ** 0.5
    return rmse


def fit_and_evaluate(train_df, test_df, predictors):

    X_train = train_df[predictors]
    X_train = sm.add_constant(
        X_train,
        has_constant="add"
    )

    y_train = train_df["ndvi"]

    model = sm.OLS(y_train, X_train).fit()

    X_test = test_df[predictors]
    X_test = sm.add_constant(
        X_test,
        has_constant="add"
    )

    y_test = test_df["ndvi"]

    predictions = model.predict(X_test)

    residuals = y_test - predictions

    rmse = calculate_rmse(residuals)

    return model, predictions, rmse


def loocv_rmse(data, predictors):

    predictions = []
    observations = []

    for i in range(len(data)):

        test = data.iloc[[i]]
        train = data.drop(data.index[i])

        X_train = train[predictors]
        X_train = sm.add_constant(
            X_train,
            has_constant="add"
        )

        y_train = train["ndvi"]

        X_test = test[predictors]
        X_test = sm.add_constant(
            X_test,
            has_constant="add"
        )

        model = sm.OLS(y_train, X_train).fit()

        prediction = model.predict(X_test).iloc[0]

        predictions.append(prediction)
        observations.append(test["ndvi"].iloc[0])

    residuals = [
        obs - pred
        for obs, pred in zip(observations, predictions)
    ]

    squared_errors = [
        residual ** 2
        for residual in residuals
    ]

    rmse = (
        sum(squared_errors) / len(squared_errors)
    ) ** 0.5

    return rmse


# ============================================================
# 1. Load data
# ============================================================

df = pd.read_csv(
    "environmental-multivariable-analysis/environmental_sites.csv"
)

pd.set_option("display.max_columns", None)


# ============================================================
# 2. Initial data inspection
# ============================================================

print("\nFirst five rows:")
print(df.head())

print("\nDataset shape:")
print(df.shape)

print("\nColumns:")
print(df.columns)

print("\nData types:")
print(df.dtypes)

print("\nMissing values:")
print(df.isna().sum())

print("\nSummary statistics:")
print(df.describe().T)


# ============================================================
# 3. Sorting and filtering
# ============================================================

sorted_df = df.sort_values(
    by="ndvi",
    ascending=False
)

print("\nSites sorted by NDVI:")
print(sorted_df)

high_elevation = df[
    df["elevation_m"] > 1000
]

print("\nSites above 1000 m:")
print(high_elevation)


# ============================================================
# 4. Correlation analysis
# ============================================================

numerical_df = df[
    [
        "elevation_m",
        "temperature_c",
        "precipitation_mm",
        "ndvi"
    ]
]

print("\nCorrelation matrix:")
print(numerical_df.corr())


# ============================================================
# 5. Prepare complete cases for modelling
# ============================================================

model_df = df.dropna(
    subset=[
        "temperature_c",
        "elevation_m",
        "precipitation_mm",
        "ndvi"
    ]
).copy()

model_df = model_df.sort_values(
    "elevation_m"
).copy()

x = model_df[
    [
        "temperature_c",
        "elevation_m",
        "precipitation_mm"
    ]
]

y = model_df["ndvi"]

print("\nPredictor matrix shape:")
print(x.shape)

print("\nOutcome shape:")
print(y.shape)

print("\nPredictors:")
print(x.head())

print("\nOutcome:")
print(y.head())


# ============================================================
# 6. Full multiple regression
# ============================================================

X = sm.add_constant(x)

model = sm.OLS(
    y,
    X
).fit()

print("\nFull multiple regression:")
print(model.summary())


# ============================================================
# 7. Multicollinearity: VIF
# ============================================================

vif_X = sm.add_constant(x)

vif_data = pd.DataFrame()

vif_data["variable"] = vif_X.columns

vif_data["VIF"] = [
    variance_inflation_factor(
        vif_X.values,
        i
    )
    for i in range(vif_X.shape[1])
]

print("\nVIF:")
print(vif_data)


# ============================================================
# 8. Coefficient instability
# ============================================================

# Temperature-only model

X_temp = model_df[
    ["temperature_c"]
]

X_temp = sm.add_constant(X_temp)

model_temp = sm.OLS(
    y,
    X_temp
).fit()

print("\nTemperature-only model:")
print(model_temp.summary())


# Temperature + elevation model

X_temp_elev = model_df[
    [
        "temperature_c",
        "elevation_m"
    ]
]

X_temp_elev = sm.add_constant(
    X_temp_elev
)

model_temp_elev = sm.OLS(
    y,
    X_temp_elev
).fit()

print("\nTemperature + elevation model:")
print(model_temp_elev.summary())


# ============================================================
# 9. High-elevation extrapolation split
# ============================================================

train_df = model_df.iloc[:-4].copy()
test_df = model_df.iloc[-4:].copy()

print("\nTraining data:")
print(
    train_df[
        ["site", "elevation_m", "temperature_c", "ndvi"]
    ]
)

print("\nExtrapolation test data:")
print(
    test_df[
        ["site", "elevation_m", "temperature_c", "ndvi"]
    ]
)


# ============================================================
# 10. Temperature-only extrapolation
# ============================================================

model_temp_extrap, pred_temp, rmse_temp = fit_and_evaluate(
    train_df,
    test_df,
    ["temperature_c"]
)

comparison = test_df[
    [
        "site",
        "elevation_m",
        "temperature_c",
        "ndvi"
    ]
].copy()

comparison["predicted_ndvi"] = pred_temp

comparison["residual"] = (
    comparison["ndvi"]
    - comparison["predicted_ndvi"]
)

print("\nTemperature-only extrapolation:")
print(comparison)

print(
    "\nTemperature-only extrapolation RMSE:",
    rmse_temp
)


# ============================================================
# 11. Interpolation test
# ============================================================

interp_test = model_df.iloc[
    [2, 5, 8, 11]
].copy()

interp_train = model_df.drop(
    interp_test.index
).copy()

print("\nInterpolation training temperature range:")
print(
    interp_train["temperature_c"].min(),
    interp_train["temperature_c"].max()
)

print("\nInterpolation test data:")
print(
    interp_test[
        [
            "site",
            "elevation_m",
            "temperature_c",
            "ndvi"
        ]
    ]
)

interp_model, interp_predictions, interp_rmse = fit_and_evaluate(
    interp_train,
    interp_test,
    ["temperature_c"]
)

interp_comparison = interp_test[
    [
        "site",
        "elevation_m",
        "temperature_c",
        "ndvi"
    ]
].copy()

interp_comparison["predicted_ndvi"] = (
    interp_predictions
)

interp_comparison["residual"] = (
    interp_comparison["ndvi"]
    - interp_comparison["predicted_ndvi"]
)

print("\nInterpolation predictions:")
print(interp_comparison)

print(
    "\nInterpolation RMSE:",
    interp_rmse
)

print("\nInterpolation vs extrapolation:")
print(
    "Extrapolation RMSE:",
    rmse_temp
)
print(
    "Interpolation RMSE:",
    interp_rmse
)


# ============================================================
# 12. Extrapolation model comparison
# ============================================================

model_elev, pred_elev, rmse_elev = fit_and_evaluate(
    train_df,
    test_df,
    ["elevation_m"]
)

predictors_full = [
    "temperature_c",
    "elevation_m",
    "precipitation_mm"
]

model_full, pred_full, rmse_full = fit_and_evaluate(
    train_df,
    test_df,
    predictors_full
)

print("\nExtrapolation model comparison:")
print(
    "Temperature only:",
    rmse_temp
)
print(
    "Elevation only:",
    rmse_elev
)
print(
    "Full model:",
    rmse_full
)


# ============================================================
# 13. Leave-One-Out Cross-Validation
# ============================================================

rmse_temp_cv = loocv_rmse(
    model_df,
    ["temperature_c"]
)

rmse_elev_cv = loocv_rmse(
    model_df,
    ["elevation_m"]
)

rmse_full_cv = loocv_rmse(
    model_df,
    predictors_full
)

print("\nLOOCV comparison:")
print(
    "Temperature only:",
    rmse_temp_cv
)
print(
    "Elevation only:",
    rmse_elev_cv
)
print(
    "Full model:",
    rmse_full_cv
)


# ============================================================
# 14. Visualise extrapolation
# ============================================================

plt.scatter(
    train_df["temperature_c"],
    train_df["ndvi"],
    label="Training"
)

plt.scatter(
    test_df["temperature_c"],
    test_df["ndvi"],
    label="Extrapolation test"
)

plt.scatter(
    test_df["temperature_c"],
    pred_temp,
    marker="x",
    label="Predicted"
)

plt.xlabel("Temperature (°C)")
plt.ylabel("NDVI")
plt.title(
    "Temperature-only model: extrapolation"
)
plt.legend()
plt.show()


# ============================================================
# 15. Visualise interpolation
# ============================================================

plt.scatter(
    interp_train["temperature_c"],
    interp_train["ndvi"],
    label="Training"
)

plt.scatter(
    interp_test["temperature_c"],
    interp_test["ndvi"],
    label="Interpolation test"
)

plt.scatter(
    interp_test["temperature_c"],
    interp_predictions,
    marker="x",
    label="Predicted"
)

plt.xlabel("Temperature (°C)")
plt.ylabel("NDVI")
plt.title(
    "Temperature-only model: interpolation"
)
plt.legend()
plt.show()