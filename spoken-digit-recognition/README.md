# Spoken Digit Recognition

## Project Overview

This project explores speaker-independent spoken-digit recognition using acoustic features extracted from the Free Spoken Digit Dataset (FSDD).

A simple logistic-regression classifier is used as a baseline to compare conventional random train-test evaluation with a more demanding speaker-independent setting.

## Research Question

How well can a simple MFCC-based classifier recognise spoken English digits from a completely unseen speaker, compared with a conventional random train-test split, and do additional acoustic features such as duration and RMS energy improve speaker-independent generalisation?


## Dataset

This project uses the Free Spoken Digit Dataset (FSDD), containing 3,000 English spoken-digit recordings from six speakers.

Dataset:
https://github.com/Jakobovski/free-spoken-digit-dataset

FSDD is distributed under the Creative Commons Attribution-ShareAlike 4.0 International licence.

The raw dataset is not included in this repository. The `data/` directory is excluded from version control.

## Key Results

Three classification experiments were conducted using multinomial logistic regression.

| Experiment | Accuracy |
| --- | ---: |
| Random 80/20 split using MFCC features | 92.0% |
| Held-out speaker using MFCC features | 82.2% |
| Held-out speaker using MFCC + duration + RMS energy | 76.4% |

The approximately 9.8 percentage-point reduction between the random split and the held-out-speaker evaluation indicates a substantial speaker-generalisation gap in this experiment.

Adding duration and RMS energy did not improve speaker-independent performance. Instead, accuracy decreased from 82.2% to 76.4%, illustrating that adding acoustic features does not necessarily improve generalisation.

Error analysis showed that misclassifications were concentrated in several digit pairs. In particular, 27 of the 50 recordings of digit 9 were incorrectly classified as digit 1. Digit 1 achieved 100% recall but only 58.1% precision because the classifier frequently predicted other digits as 1.

These findings are specific to the selected held-out speaker and model configuration and should not be interpreted as general properties of spoken-digit recognition.

## Limitations

- Only one speaker was used as the held-out test speaker.
- MFCC statistics collapse temporal information into means and standard deviations.
- Logistic regression provides a simple baseline rather than a modern speech-recognition architecture.
- The acoustic causes of individual confusion pairs were not established through detailed phonetic analysis.
- Performance on this small spoken-digit dataset cannot be generalised to continuous automatic speech recognition.
