# Environmental Trend Analysis

## Purpose

This mini-analysis is a computational foundations exercise designed to practise a complete environmental data analysis workflow in Python.

The dataset is illustrative rather than an empirical climate dataset. The purpose is to understand the logic behind data cleaning, linear regression, residual diagnostics, model evaluation, and reproducible research practices.

## Research Question

Given a short series of annual summer temperature observations with missing values, is there evidence of an increasing linear trend over time?

## Data

The illustrative dataset covers 2018–2025.

- Total years: 8
- Valid observations: 6
- Missing years: 2020 and 2023

Missing observations are removed while preserving the year-temperature pairing for all valid records.

## Workflow

The analysis was implemented from basic Python operations rather than using statistical or machine-learning libraries for the regression itself.

The workflow includes:

1. Inspecting missing observations
2. Removing incomplete records
3. Extracting year and temperature variables
4. Comparing endpoint change
5. Calculating the linear regression slope manually
6. Generating fitted values
7. Calculating residuals
8. Calculating MSE and RMSE
9. Plotting observations and the fitted trend
10. Inspecting residuals over time

## Results

For the six valid observations:

- Endpoint temperature change: approximately +1.0 °C
- Fitted linear slope: approximately +0.155 °C/year
- In-sample RMSE: approximately 0.127 °C

The fitted model suggests an upward linear tendency within this illustrative dataset.

## Interpretation

The regression slope summarizes the overall relationship between year and temperature across all valid observations rather than relying only on the first and last observations.

Residuals are calculated as:

`actual - predicted`

Positive residuals indicate that the model underestimated the observation, while negative residuals indicate that the model overestimated it.

## Limitations

This exercise does not provide evidence of real-world climate change.

Important limitations include:

- the dataset is illustrative
- only six valid observations are available
- the time span is very short
- RMSE is calculated on the same observations used to fit the model
- no uncertainty estimates or confidence intervals are calculated
- temporal autocorrelation is not assessed
- measurement consistency and other environmental drivers are not considered

Therefore, the fitted slope should be interpreted only as a demonstration of linear trend estimation.

## Challenges and Lessons

### Preserving record structure

When removing missing temperatures, the entire observation record was retained rather than extracting temperatures alone. This preserves the relationship between year and temperature.

### Execution order and hidden state

An early version calculated the regression intercept before recalculating the slope. In an interactive notebook, an older slope value could remain in memory and allow apparently valid results.

This demonstrated why analysis code should follow explicit dependency order and be reproducible from a fresh environment.

### Software dependencies

The analysis initially failed on the local machine because `matplotlib` was not installed.

A project-specific Python virtual environment was created to isolate dependencies.

### Version control

Git was used to track changes, inspect modifications with `git diff`, restore an earlier working version, and synchronize the project with GitHub.


## Reproducibility

This analysis was developed in Python using a project-specific virtual environment.

To reproduce the analysis:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r environmental-trend-analysis/requirements.txt
python3 environmental-trend-analysis/analysis.py

## Next Steps

Future exercises will extend this workflow using:

- NumPy
- pandas
- statistical model libraries
- uncertainty estimation
- validation on unseen observations
- larger environmental datasets
## Data

The datasets in this exercise are illustrative and were created for
computational training rather than climate inference.

Variables:

- `year`: observation year
- `temperature`: illustrative summer mean air temperature in degrees Celsius (°C)

`temperature_observations_dirty.csv` intentionally contains missing values,
a duplicate year, and an implausible temperature value for data-quality
checking practice.
