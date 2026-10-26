from pathlib import Path

import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    ConfusionMatrixDisplay,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


# ============================================================
# 1. Paths
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parent

DATA_DIR = (
    PROJECT_DIR
    / "data"
    / "fsdd"
    / "recordings"
)

RESULTS_DIR = PROJECT_DIR / "results"
RESULTS_DIR.mkdir(exist_ok=True)


# ============================================================
# 2. Parse metadata from filename
# Example: 7_jackson_32.wav
# ============================================================

def parse_filename(path):
    parts = path.stem.split("_")

    digit = int(parts[0])
    speaker = parts[1]
    recording_index = int(parts[2])

    return digit, speaker, recording_index


# ============================================================
# 3. Extract acoustic features
# ============================================================

def extract_features(path):
    audio, sample_rate = librosa.load(
        path,
        sr=None,
        mono=True,
    )

    # 13 MFCC coefficients across time
    mfcc = librosa.feature.mfcc(
        y=audio,
        sr=sample_rate,
        n_mfcc=13,
    )

    # Convert a variable-length recording into
    # a fixed-length feature vector.
    mfcc_mean = mfcc.mean(axis=1)
    mfcc_std = mfcc.std(axis=1)

    duration = len(audio) / sample_rate

    rms_energy = librosa.feature.rms(
        y=audio
    ).mean()

    features = {}

    for i, value in enumerate(
        mfcc_mean,
        start=1,
    ):
        features[f"mfcc_mean_{i}"] = value

    for i, value in enumerate(
        mfcc_std,
        start=1,
    ):
        features[f"mfcc_std_{i}"] = value

    features["duration"] = duration
    features["rms_energy"] = rms_energy

    return features


# ============================================================
# 4. Build dataset
# ============================================================

def build_dataset():
    wav_files = sorted(
        DATA_DIR.glob("*.wav")
    )

    if not wav_files:
        raise FileNotFoundError(
            f"No WAV files found in {DATA_DIR}"
        )

    print(
        f"Found {len(wav_files)} WAV files."
    )

    rows = []

    for i, path in enumerate(
        wav_files,
        start=1,
    ):
        digit, speaker, recording_index = (
            parse_filename(path)
        )

        features = extract_features(path)

        row = {
            "file": path.name,
            "path": str(path),
            "digit": digit,
            "speaker": speaker,
            "recording_index": recording_index,
        }

        row.update(features)

        rows.append(row)

        if i % 500 == 0:
            print(
                f"Processed {i} / "
                f"{len(wav_files)} files"
            )

    df = pd.DataFrame(rows)

    output_path = (
        RESULTS_DIR
        / "acoustic_features.csv"
    )

    df.to_csv(
        output_path,
        index=False,
    )

    print(
        "\nFeature dataset saved to:"
    )
    print(output_path)

    return df


# ============================================================
# 5. Plot one example waveform
# ============================================================

def save_example_waveform(df):
    path = Path(df.iloc[0]["path"])

    audio, sample_rate = librosa.load(
        path,
        sr=None,
    )

    time = (
        np.arange(len(audio))
        / sample_rate
    )

    plt.figure(figsize=(9, 4))

    plt.plot(
        time,
        audio,
    )

    plt.xlabel("Time (seconds)")
    plt.ylabel("Amplitude")

    plt.title(
        f"Waveform: {path.name}"
    )

    plt.tight_layout()

    output = (
        RESULTS_DIR
        / "waveform_example.png"
    )

    plt.savefig(
        output,
        dpi=150,
    )

    plt.close()


# ============================================================
# 6. Plot spectrogram
# ============================================================

def save_example_spectrogram(df):
    path = Path(df.iloc[0]["path"])

    audio, sample_rate = librosa.load(
        path,
        sr=None,
    )

    stft = librosa.stft(audio)

    db = librosa.amplitude_to_db(
        np.abs(stft),
        ref=np.max,
    )

    plt.figure(figsize=(9, 4))

    librosa.display.specshow(
        db,
        sr=sample_rate,
        x_axis="time",
        y_axis="hz",
    )

    plt.xlabel("Time")
    plt.ylabel("Frequency (Hz)")

    plt.title(
        f"Spectrogram: {path.name}"
    )

    plt.tight_layout()

    output = (
        RESULTS_DIR
        / "spectrogram_example.png"
    )

    plt.savefig(
        output,
        dpi=150,
    )

    plt.close()


# ============================================================
# 7. Define feature groups
# ============================================================

def get_feature_columns(df):
    mfcc_features = [
        col
        for col in df.columns
        if col.startswith("mfcc_")
    ]

    enriched_features = (
        mfcc_features
        + [
            "duration",
            "rms_energy",
        ]
    )

    return (
        mfcc_features,
        enriched_features,
    )


# ============================================================
# 8. Build classifier
# ============================================================

def make_model():
    return Pipeline(
        [
            (
                "scaler",
                StandardScaler(),
            ),
            (
                "classifier",
                LogisticRegression(
                    max_iter=3000,
                    random_state=42,
                ),
            ),
        ]
    )


# ============================================================
# 9. Evaluate one experiment
# ============================================================

def evaluate_experiment(
    name,
    train_df,
    test_df,
    feature_columns,
):
    X_train = train_df[
        feature_columns
    ]

    y_train = train_df["digit"]

    X_test = test_df[
        feature_columns
    ]

    y_test = test_df["digit"]

    model = make_model()

    model.fit(
        X_train,
        y_train,
    )

    predictions = model.predict(
        X_test
    )

    accuracy = accuracy_score(
        y_test,
        predictions,
    )

    print(
        "\n"
        + "=" * 70
    )

    print(
        f"Experiment: {name}"
    )

    print(
        f"Accuracy: {accuracy:.4f}"
    )

    print(
        "\nClassification report:"
    )

    print(
        classification_report(
            y_test,
            predictions,
            digits=3,
        )
    )

    # Save confusion matrix
    plt.figure(figsize=(7, 7))

    ConfusionMatrixDisplay.from_predictions(
        y_test,
        predictions,
        labels=list(range(10)),
    )

    plt.title(
        f"Confusion Matrix: {name}"
    )

    plt.tight_layout()

    output = (
        RESULTS_DIR
        / f"confusion_matrix_{name}.png"
    )

    plt.savefig(
        output,
        dpi=150,
    )

    plt.close()

    return (
        model,
        predictions,
        accuracy,
    )


# ============================================================
# 10. Main experiments
# ============================================================

def main():

    # ------------------------------------------
    # Feature extraction
    # ------------------------------------------

    df = build_dataset()

    print("\nDataset shape:")
    print(df.shape)

    print("\nSpeakers:")
    print(
        sorted(
            df["speaker"].unique()
        )
    )

    print("\nDigit counts:")
    print(
        df["digit"]
        .value_counts()
        .sort_index()
    )

    save_example_waveform(df)
    save_example_spectrogram(df)

    (
        mfcc_features,
        enriched_features,
    ) = get_feature_columns(df)

    # ========================================================
    # Experiment A:
    # Random train/test split
    # ========================================================

    random_train, random_test = (
        train_test_split(
            df,
            test_size=0.20,
            random_state=42,
            stratify=df["digit"],
        )
    )

    _, _, random_accuracy = (
        evaluate_experiment(
            name="random_split_mfcc",
            train_df=random_train,
            test_df=random_test,
            feature_columns=mfcc_features,
        )
    )

    # ========================================================
    # Experiment B:
    # Completely unseen speaker
    # ========================================================

    speakers = sorted(
        df["speaker"].unique()
    )

    test_speaker = speakers[-1]

    speaker_train = df[
        df["speaker"]
        != test_speaker
    ].copy()

    speaker_test = df[
        df["speaker"]
        == test_speaker
    ].copy()

    print(
        "\nHeld-out speaker:"
    )
    print(test_speaker)

    (
        speaker_model,
        speaker_predictions,
        speaker_accuracy,
    ) = evaluate_experiment(
        name="unseen_speaker_mfcc",
        train_df=speaker_train,
        test_df=speaker_test,
        feature_columns=mfcc_features,
    )

    # ========================================================
    # Experiment C:
    # MFCC + duration + energy
    # ========================================================

    (
        enriched_model,
        enriched_predictions,
        enriched_accuracy,
    ) = evaluate_experiment(
        name="unseen_speaker_mfcc_duration_energy",
        train_df=speaker_train,
        test_df=speaker_test,
        feature_columns=enriched_features,
    )

    # ========================================================
    # Save experiment comparison
    # ========================================================

    results = pd.DataFrame(
        [
            {
                "experiment":
                    "random_split_mfcc",
                "accuracy":
                    random_accuracy,
                "test_condition":
                    "Random 20% split",
                "feature_set":
                    "MFCC mean + std",
            },
            {
                "experiment":
                    "unseen_speaker_mfcc",
                "accuracy":
                    speaker_accuracy,
                "test_condition":
                    f"Held-out speaker: "
                    f"{test_speaker}",
                "feature_set":
                    "MFCC mean + std",
            },
            {
                "experiment":
                    "unseen_speaker_mfcc_duration_energy",
                "accuracy":
                    enriched_accuracy,
                "test_condition":
                    f"Held-out speaker: "
                    f"{test_speaker}",
                "feature_set":
                    (
                        "MFCC mean + std "
                        "+ duration + RMS energy"
                    ),
            },
        ]
    )

    results_path = (
        RESULTS_DIR
        / "experiment_results.csv"
    )

    results.to_csv(
        results_path,
        index=False,
    )

    print(
        "\n"
        + "=" * 70
    )

    print(
        "Experiment comparison:"
    )

    print(
        results.to_string(
            index=False
        )
    )

    # ========================================================
    # Save misclassified examples
    # ========================================================

    errors = speaker_test[
        [
            "file",
            "speaker",
            "digit",
            "path",
        ]
    ].copy()

    errors["prediction"] = (
        speaker_predictions
    )

    errors = errors[
        errors["digit"]
        != errors["prediction"]
    ]

    errors_path = (
        RESULTS_DIR
        / "unseen_speaker_errors.csv"
    )

    errors.to_csv(
        errors_path,
        index=False,
    )

    print(
        "\nMisclassified unseen-speaker "
        f"examples: {len(errors)}"
    )

    print(
        "Saved to:"
    )

    print(errors_path)


if __name__ == "__main__":
    main()