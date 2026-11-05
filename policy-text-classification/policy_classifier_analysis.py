"""Inspect a toy TF-IDF + Logistic Regression text classifier.

Put this file beside policy_classifier.py and run:
    python policy_classifier_analysis.py

Training examples are synthetic and too small for research-grade conclusions.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline

from policy_classifier import POLICY_TEXTS, SCIENCE_TEXTS


def show_feature_contributions(text, vectorizer, classifier, limit=5):
    """Show which observed tokens push a prediction toward each class.

    For binary sklearn LogisticRegression, positive logit contributions point
    toward classes_[1], and negative contributions toward classes_[0].
    """
    row = vectorizer.transform([text])
    feature_names = vectorizer.get_feature_names_out()
    coefficients = classifier.coef_[0]
    contributions = [
        (feature_names[j], row[0, j] * coefficients[j])
        for j in row.indices
    ]
    toward_first = sorted(
        (entry for entry in contributions if entry[1] < 0),
        key=lambda entry: entry[1],
    )[:limit]
    toward_second = sorted(
        (entry for entry in contributions if entry[1] > 0),
        key=lambda entry: entry[1], reverse=True,
    )[:limit]

    def fmt(items):
        return ", ".join(f"{word} ({value:+.3f})" for word, value in items) or "none"

    print(f"    Toward {classifier.classes_[0]}: {fmt(toward_first)}")
    print(f"    Toward {classifier.classes_[1]}: {fmt(toward_second)}")
    print("    (Contributions = TF-IDF value × coefficient; intercept not shown.)")


def main():
    texts = POLICY_TEXTS + SCIENCE_TEXTS
    labels = ["Policy"] * len(POLICY_TEXTS) + ["Science"] * len(SCIENCE_TEXTS)

    train_texts, test_texts, train_labels, test_labels = train_test_split(
        texts, labels, test_size=0.25, random_state=42, stratify=labels
    )
    model = make_pipeline(
        TfidfVectorizer(),
        LogisticRegression(max_iter=1000),
    )
    model.fit(train_texts, train_labels)

    vectorizer = model.named_steps["tfidfvectorizer"]
    classifier = model.named_steps["logisticregression"]
    words = vectorizer.get_feature_names_out()
    coefficients = classifier.coef_[0]
    ranked = sorted(zip(words, coefficients), key=lambda item: item[1])

    print("=== Data and evaluation ===")
    print(f"Training texts: {len(train_texts)} | Test texts: {len(test_texts)}")
    print("Class order:", list(classifier.classes_))
    predictions = model.predict(test_texts)
    print("Confusion matrix (rows=actual, columns=predicted):")
    print(confusion_matrix(test_labels, predictions, labels=classifier.classes_))
    print(classification_report(test_labels, predictions, zero_division=0))

    print("=== Strongest learned word weights ===")
    print(f"Toward {classifier.classes_[0]} (negative weights):")
    for word, weight in ranked[:8]:
        print(f"  {word:<18} {weight:+.4f}")
    print(f"Toward {classifier.classes_[1]} (positive weights):")
    for word, weight in reversed(ranked[-8:]):
        print(f"  {word:<18} {weight:+.4f}")

    print("\n=== Misclassified test texts ===")
    policy_column = list(classifier.classes_).index("Policy")
    policy_probs = model.predict_proba(test_texts)[:, policy_column]
    error_count = 0
    for text, actual, predicted, prob in zip(
        test_texts, test_labels, predictions, policy_probs
    ):
        if actual != predicted:
            error_count += 1
            print(f"\nError {error_count}: actual={actual}, predicted={predicted}, P(Policy)={prob:.3f}")
            print("  Text:", text)
            analyzable = vectorizer.build_analyzer()(text)
            recognized = [token for token in analyzable if token in vectorizer.vocabulary_]
            unseen = [token for token in analyzable if token not in vectorizer.vocabulary_]
            print("  Recognized training-vocabulary tokens:", recognized)
            print("  Unseen tokens (ignored by TF-IDF):", unseen)
            show_feature_contributions(text, vectorizer, classifier)
    if error_count == 0:
        print("No errors in this small test set.")

    assert len(train_texts) == 18 and len(test_texts) == 6
    assert len(classifier.classes_) == 2
    print("\nAnalysis complete. Interpret cautiously: synthetic data, only six test texts.")


if __name__ == "__main__":
    main()
