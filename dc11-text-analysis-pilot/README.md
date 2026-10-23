
# DC11 Text Analysis Pilot

## 1. Project Overview

This pilot explores how response diversity is conceptualised and measured in ecological research, and how these concepts relate to ecological monitoring requirements in biodiversity policy.

The project combines exploratory text analysis in Python with manual qualitative coding to examine potential connections and differences between scientific and policy texts.

## 2. Research Questions

1. How is response diversity conceptualised and measured in the selected scientific abstracts?
2. What methodological challenges are identified in empirical research on response diversity?
3. How do the ecological monitoring requirements in the selected policy provision relate to the concepts discussed in the scientific abstracts?

These questions are exploratory and may be refined as the analysis develops.

## 3. Corpus

The initial corpus contains three text units:

- **SCI01:** A scientific abstract presenting a methodological framework for measuring response diversity using environment-dependent functional responses.
- **SCI02:** A scientific abstract discussing empirical research on response diversity and methodological challenges.
- **POL01:** A policy provision specifying ten ecological monitoring requirements, labelled (a)–(j).

The corpus is deliberately small. The analysis focuses on the collected text units rather than claiming to represent the entire scientific literature or the full policy document.

## 4. Data and Methods

### Corpus preparation

The texts were stored as individual text files and accompanied by metadata. Python and pandas were used to inspect document identifiers, missing values, text lengths and file paths.

### Exploratory keyword analysis

Python was used to count predefined keywords and phrases, compare their frequencies per 100 words, and extract surrounding text for contextual inspection.

Keyword groups included response diversity, resilience, stability, environmental change, biodiversity and monitoring.

### Qualitative coding

Manual qualitative coding was used to identify relevant passages, assign initial codes and group related codes into provisional broader themes.

The coding records include excerpts, code labels, broader themes, relationships to the research questions and interpretation notes.

### Cross-text comparison

Keyword results and qualitative coding were compared to examine differences between scientific discussions of response diversity and policy requirements for ecological monitoring.

Keyword counts were treated as exploratory indicators rather than direct measures of conceptual importance.

### Semantic similarity experiment

As a final exploratory step, I used a pretrained sentence-embedding model to compare a scientific definition of response diversity with the ten policy monitoring clauses.

The analysis ranked policy clauses by cosine similarity to the scientific definition. Clause 1(g), concerning pollinator abundance and diversity, received the highest similarity score. Manual interpretation showed, however, that species diversity is not equivalent to response diversity because the clause does not measure variation in species' responses to environmental change.

This experiment illustrates the complementary roles of AI-assisted retrieval and human interpretation: semantic similarity can identify potentially relevant passages, but it cannot establish conceptual equivalence.

## 5. Preliminary Findings

In the collected text units:

- The phrase "response diversity" occurred seven times in SCI01 and eleven times in SCI02.
- Normalised frequencies were approximately 3.04 and 4.42 occurrences per 100 words, respectively.
- POL01 contains requirements concerning habitat condition, biodiversity indicators, species populations and pollinator abundance and diversity.

- The selected policy provision does not explicitly use the phrase "response diversity".

These observations suggest differences in terminology and emphasis between the selected scientific and policy texts. They do not establish whether the policy incorporates the underlying concept through other indicators or provisions.

## 6. Methodological Limitations

The pilot has several limitations:

- The corpus contains only two scientific abstracts and one policy provision.
- Keyword analysis may miss relevant concepts expressed using different terminology.
- Qualitative coding involves researcher judgement and may require revision.
- The relationship between biodiversity indicators and response diversity requires further evidence.
- The current analysis cannot establish causal influence between scientific research and policy development.

The findings should therefore be interpreted as preliminary.

## 7. Project Structure

- `corpus_inventory.csv`: Metadata and selection rationale for the collected texts.
- `texts/`: Individual text files.
- `validate_texts.py`: Checks text files and corpus metadata.
- `analyse_texts.py`: Performs exploratory keyword analysis.
- `inspect_contexts.py`: Extracts keyword contexts for inspection.
- `qualitative_coding.csv`: Records manual coding decisions and interpretation notes.
- `compare_methods.py`: Summarises keyword and qualitative coding results.
- `keyword_counts.csv`: Structured keyword counts and normalised frequencies.
- `keyword_contexts.csv`: Extracted keyword contexts.
- `keyword_comparison_matrix.csv`: Normalised keyword comparison matrix.
- `method_comparison_summary.csv`: Combined summary of keyword and qualitative coding results.

## 8. Next Steps

1. Audit the qualitative coding against the original text.
2. Review whether initial codes and broader themes are consistently defined.
3. Compare keyword patterns with contextual interpretations.
4. Document debugging decisions and methodological changes.
5. Refine the research questions and assess whether additional texts are needed.

## 9. Reproducibility

The project uses Python and pandas for data handling and analysis. Scripts, structured outputs and coding records support transparent inspection of the analytical workflow.

All interpretations should remain traceable to the collected text and should distinguish textual evidence from researcher inference.
## Source Texts and Reuse

This project includes selected text from two open-access scientific articles and one provision of EU legislation for non-commercial research and educational purposes.

- **SCI01:** Ross, S. R. P.-J., Petchey, O. L., Sasaki, T., & Armitage, D. W. (2023). *How to measure response diversity*. Methods in Ecology and Evolution, 14, 1150–1167. https://doi.org/10.1111/2041-210X.14087
- **SCI02:** Ross, S. R. P.-J., & Sasaki, T. (2024). *Limited theoretical and empirical evidence that response diversity determines the resilience of ecosystems to environmental change*. Ecological Research, 39(2), 115–130. https://doi.org/10.1111/1440-1703.12434
- **POL01:** European Parliament and Council of the European Union. (2024). *Regulation (EU) 2024/1991 on nature restoration*, Article 20(1)(a)–(j). https://eur-lex.europa.eu/eli/reg/2024/1991/oj/eng

The two scientific articles are published under Creative Commons Attribution-NonCommercial licences, as indicated by their publishers. Their reuse must comply with the applicable licence terms, including attribution and non-commercial use.

EU-owned content on EUR-Lex is generally reusable under the European Commission's CC BY 4.0 reuse policy unless otherwise indicated. The official source should be acknowledged, and any modifications should be identified.

The source texts remain subject to their respective reuse conditions. These conditions are separate from any licence that may apply to original code or other materials in this repository.