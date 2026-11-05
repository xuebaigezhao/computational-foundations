# Policy vs Environmental Science: A Toy Text Classification Study

A **learning project** demonstrating a reproducible NLP classification workflow using Python, TF-IDF, and logistic regression. The task is to distinguish policy/governance-oriented sentences from environmental-science-oriented sentences.

> **Scope:** All 24 sentences are synthetic examples written for learning. This is **not** a research-grade dataset, a validated literature-screening model, or evidence of real-world classification performance.

## Research-style question

Can a basic supervised text classifier distinguish policy/governance language from environmental-science language, and what do its errors reveal about the limitations of small training corpora?

## Workflow

1. **Data and labels:** 12 invented Policy sentences and 12 invented Science sentences.
2. **Split:** stratified 75% training / 25% held-out testing (`random_state=42`): 18 training sentences, six test sentences (three per class).
3. **Text features:** `TfidfVectorizer` converts text into a document-term feature matrix. It is fitted **only on training data** via a scikit-learn pipeline.
4. **Classifier:** `LogisticRegression(max_iter=1000)` learns weights for the two classes.
5. **Evaluation:** held-out accuracy, precision, recall, F1, and a confusion matrix.
6. **Diagnostics:** inspect learned TF-IDF coefficients, which tokens are known versus unseen, and how individual token contributions affect misclassifications.
7. **Threshold experiment:** compare the effect of different Policy probability thresholds. This is a teaching demonstration, **not** valid test-set-based threshold optimization.

## Files

| File | Purpose |
| --- | --- |
| `policy_classifier.py` | Train/test classification and predictions on two new example sentences |
| `policy_classifier_analysis.py` | Confusion matrix, feature coefficients, and error analysis |
| `policy_classifier_thresholds.py` | Illustrative Policy precision/recall trade-off at different probability thresholds |
| `requirements.txt` | Minimal Python dependency |

## Run locally

Use Python 3.9+ with a virtual environment. In a terminal opened in this folder:

```bash
python -m pip install -r requirements.txt
python policy_classifier.py
python policy_classifier_analysis.py
python policy_classifier_thresholds.py
```

The analysis script imports the example texts from `policy_classifier.py`, so keep the three `.py` files together.

## Held-out test results

| Metric | Result |
| --- | ---: |
| Training samples | 18 |
| Test samples | 6 |
| Accuracy | 0.667 (4/6 correct) |
| Policy precision / recall / F1 | 0.667 / 0.667 / 0.667 |
| Science precision / recall / F1 | 0.667 / 0.667 / 0.667 |
| Macro F1 | 0.667 |

Confusion matrix (rows = actual, columns = predicted; class order = Policy, Science):

| Actual \\ Predicted | Policy | Science |
| --- | ---: | ---: |
| Policy | 2 | 1 |
| Science | 1 | 2 |

These metrics have **very high sampling uncertainty** because there are only three test samples per class.

## Error analysis

### False positive: Science classified as Policy

> A statistical model estimated drought impacts on plant growth.

- Prediction: Policy; `P(Policy) ≈ 0.508`.
- The training TF-IDF vocabulary recognized only `model` and `on`.
- Key science-related terms (`drought`, `plant`, `growth`) were absent from the learned vocabulary.
- In this model, `on` pushed the decision toward Policy and `model` toward Science; their contributions were small, and the probability was near the 0.5 decision threshold.

### False negative: Policy classified as Science

> Regulatory enforcement determines compliance with emission standards.

- Prediction: Science; `P(Policy) ≈ 0.461`.
- The learned vocabulary recognized only `with`.
- Key governance terminology (`regulatory`, `enforcement`, `compliance`, `standards`) was missing.
- Consequently, the decision was made using almost no relevant lexical evidence. The word `with` had a small contribution toward Science.

## Interpreting coefficients

`LogisticRegression.classes_` returns `['Policy', 'Science']` in this example. Accordingly, **negative** coefficients point toward Policy and **positive** coefficients point toward Science. Always check the class order rather than assuming positive weights mean Policy.

Examples of observed associations:

| Toward Policy (negative) | Toward Science (positive) |
| --- | --- |
| `emissions` | `temperature` |
| `carbon` | `vegetation` |
| `energy` | `habitats` |
| `for` | `and` |

The appearance of common function words such as `for` and `and` among influential features illustrates how tiny synthetic datasets can yield unstable, non-substantive associations. Coefficients describe **this fitted model**, not causal effects, universal topic indicators, or policy importance.

## Probability threshold experiment

The illustrative thresholds were applied to the **same six held-out test items**, without retraining:

| Policy threshold | Precision | Recall | F1 |
| ---: | ---: | ---: | ---: |
| 0.50 | 0.667 | 0.667 | 0.667 |
| 0.45 | 0.600 | 1.000 | 0.750 |
| 0.40 | 0.500 | 1.000 | 0.667 |
| 0.30 | 0.500 | 1.000 | 0.667 |

Lowering the threshold increased recall in this toy example but also admitted more false positives. **Do not** select a threshold by optimizing on a final test set; use a separate validation set or cross-validation, then reserve an independent test set for final reporting.

## Limitations

- **Synthetic and extremely small corpus:** the examples are neither representative nor independently annotated.
- **Poor vocabulary coverage:** important terms in test documents may be unseen and ignored by TF-IDF.
- **Lexical rather than semantic representation:** TF-IDF does not inherently connect related word forms or paraphrases.
- **Unstable estimated performance:** six test examples cannot support reliable generalization claims.
- **Limited external validity:** results should not be used to screen or exclude real research publications.
- **Feature interpretation caveat:** word-level coefficient directions do not alone explain every prediction; the intercept, TF-IDF normalization and combined feature contributions also matter.

## Reasonable next steps for a genuine research application

1. Define operational labeling criteria and assemble a sufficiently large set of **real** abstracts or policy texts with provenance and permitted usage.
2. Label texts consistently, check inter-annotator agreement where possible, and handle ambiguity/multilabel documents explicitly.
3. Prevent leakage using appropriate document/group/time-aware splits, and fit every preprocessing step only on training folds.
4. Compare a dummy baseline, TF-IDF + logistic regression, and (if justified) embedding-based approaches with validation/cross-validation.
5. Report per-class precision, recall, F1, uncertainty, error patterns and vocabulary coverage. Select thresholds on validation data, not the final test set.

## Learning outcomes

This exercise demonstrates familiarity with constructing a reproducible scikit-learn pipeline, supervised text classification, train/test separation, per-class evaluation metrics, decision-threshold trade-offs, feature-weight inspection and qualitative error analysis. It should be described as a **learning exercise** until extended and validated with real data.
