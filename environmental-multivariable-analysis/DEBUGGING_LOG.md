# Debugging Log

This log records practical issues encountered during the multivariable
environmental analysis project.

---

## Case 1: Column-name mismatch caused a KeyError

### Problem
The script raised:

`KeyError: 'site_id'`

### What I expected
The dataset should sort successfully by a site-related column.

### What went wrong
The code referred to a column named `site_id`, but the actual CSV column was
named `site`.

### Diagnosis
The pandas error indicated that the requested column label did not exist.
Checking the dataset columns showed:

- `site`
- `elevation_m`
- `temperature_c`
- `precipitation_mm`
- `ndvi`

### Fix
Used the correct column name and also corrected the analysis goal by sorting
by `ndvi` rather than by site identifier.

### Verification
The sorting operation ran successfully.

### Lesson
`KeyError` in pandas often indicates a mismatch between the code and the
dataset schema. Column names should be checked before analysis.

---

## Case 2: Ellipsis appeared instead of residual values

### Problem
The residual column contained `Ellipsis` instead of numerical residuals.

### What I expected
The column should contain:

`observed NDVI - predicted NDVI`

### What went wrong
The placeholder `...` had been left literally in the code:

`comparison["residual"] = ...`

In Python, `...` is a real `Ellipsis` object.

### Diagnosis
The output showed `Ellipsis` in every row rather than numbers.

### Fix
Replaced the placeholder with the actual calculation:

`comparison["residual"] = comparison["ndvi"] - comparison["predicted_ndvi"]`

### Verification
The residual column returned numerical values such as:

- `-0.030817`
- `-0.037380`
- `-0.047302`
- `-0.057224`

### Lesson
Placeholders in example code must be replaced before execution. Python treats
`...` as an executable object rather than as an informal note.