"""SLP mini-project: Policy vs Environmental Science text classification.

Learning-only synthetic examples, not a real research dataset.
Run: python policy_classifier.py
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline


# 1 means nothing special here: we use clear string labels.
# These examples are invented solely for learning the workflow.
POLICY_TEXTS = [
    "Government regulations require industries to reduce carbon emissions.",
    "Climate legislation establishes binding targets for national emissions.",
    "Public agencies coordinate policies for a fair energy transition.",
    "Carbon pricing creates incentives for companies to cut pollution.",
    "Environmental governance depends on transparent public institutions.",
    "Policymakers evaluate subsidies for renewable electricity investment.",
    "International agreements define national climate commitments.",
    "Regulatory enforcement determines compliance with emission standards.",
    "Public consultation shapes urban climate adaptation policies.",
    "The ministry introduced incentives for low carbon manufacturing.",
    "Municipal authorities adopted rules on building energy efficiency.",
    "Institutional coordination improves implementation of conservation laws.",
]

SCIENCE_TEXTS = [
    "Satellite imagery reveals seasonal changes in forest vegetation.",
    "Researchers measured soil moisture across mountain ecosystems.",
    "Field observations indicate declining glacier mass in summer.",
    "A climate model simulates temperature and precipitation anomalies.",
    "Ecologists monitored biodiversity in fragmented habitats.",
    "Remote sensing data track land cover and vegetation productivity.",
    "Ocean sensors recorded changing water temperature and salinity.",
    "The experiment measured carbon uptake in wetland plants.",
    "Scientists analyzed river discharge during extreme rainfall.",
    "Species abundance varies with elevation and habitat conditions.",
    "Atmospheric measurements show shifts in methane concentrations.",
    "A statistical model estimated drought impacts on plant growth.",
]


def main():
    texts = POLICY_TEXTS + SCIENCE_TEXTS
    labels = (["Policy"] * len(POLICY_TEXTS)
              + ["Science"] * len(SCIENCE_TEXTS))

    # Split BEFORE fitting TF-IDF: the test data must stay unseen.
    train_texts, test_texts, train_labels, test_labels = train_test_split(
        texts,
        labels,
        test_size=0.25,
        random_state=42,
        stratify=labels,
    )

    # The pipeline fits TF-IDF only on training data and then trains
    # logistic regression; it applies the same vocabulary at test time.
    model = make_pipeline(
        TfidfVectorizer(),
        LogisticRegression(max_iter=1000),
    )
    model.fit(train_texts, train_labels)

    print(f"Training texts: {len(train_texts)}")
    print(f"Test texts:     {len(test_texts)}")

    predicted = model.predict(test_texts)
    print("\n=== Results on held-out test texts ===")
    print(classification_report(test_labels, predicted, zero_division=0))

    print("=== Individual test predictions ===")
    for text, actual, guess in zip(test_texts, test_labels, predicted):
        print(f"Actual: {actual:7} | Predicted: {guess:7} | {text}")

    new_texts = [
        "The government introduced new regulations for carbon markets.",
        "Satellite measurements reveal changes in alpine vegetation.",
    ]
    print("\n=== Predictions for new text ===")
    for text, guess in zip(new_texts, model.predict(new_texts)):
        print(f"Predicted: {guess:7} | {text}")

    print("\nDone. (This toy dataset is too small for reliable performance claims.)")


if __name__ == "__main__":
    main()
