# Debugging Log — DC11 Text Analysis Pilot

**Project:** DC11 Text Analysis Pilot
**Research focus:** Response diversity, ecosystem resilience and biodiversity policy
**Last updated:** 21 October 2026

This log documents data-quality issues, analytical debugging, methodological decisions and lessons learned during the development of a Python-based text analysis workflow.

---

## Case 1: Textual Inaccuracies During Abstract Extraction

**Category:** Data quality and source verification
**Status:** Partially addressed; source verification remains necessary

### Problem

Initial text validation revealed malformed text, including:

- `ofbiodiversity`
- `responses toenvironmental`
- `insurancehypothesis`
- `ecosys-tem`

The SCI01 text also differed in wording from an earlier version of the abstract.

### Diagnosis

Copying text from formatted documents can introduce missing spaces, line-break hyphenation or unintended changes. Text may also be incomplete or inconsistent with the published source.

### Solution

Revised the abstract text in separate TXT files and used Python to inspect the file contents, character counts and opening passages.

The validation script, `validate_texts.py`, checks whether text files exist, whether metadata is missing, whether document IDs are duplicated, and whether the text files contain readable content.

### Remaining limitation

Successful file reading does not prove that every word matches the publisher's version. Both abstracts still require verification against their authoritative sources before the results can be treated as final research evidence.

### Lesson Learned

Structural validity and textual accuracy are different. A dataset can be technically readable while still containing inaccurate source material.

### Research implication

Textual errors can affect tokenisation, keyword counts and comparisons between documents. Source verification is therefore part of research quality control, not merely a formatting task.

---

## Case 2: Substring Matching Inflated Keyword Counts

**Category:** Text matching and measurement accuracy
**Status:** Corrected; verification required

### Problem

SCI01 initially returned a count of 2 for the monitoring group, although the abstract appeared to contain only one occurrence of `monitoring`.

### Diagnosis

The keyword group included both `monitoring` and `monitor`. The original code used Python's string-counting method:

`cleaned_text.count(term)`

This method counts matching character sequences, including a shorter term contained within a longer word. Consequently, one occurrence of `monitoring` could be counted twice.

### Solution

Replaced ordinary substring counting with regular-expression matching using word boundaries and escaped search terms:

`re.findall(rf"\b{re.escape(term)}\b", cleaned_text)`

This approach distinguishes complete-word matches from matching character sequences inside longer words.

### Verification

Re-ran `analyse_texts.py` and inspected the keyword-group counts for both scientific abstracts.

The expected SCI01 monitoring-group count is 1 if the text contains one standalone occurrence of `monitoring` and no standalone occurrence of `monitor`.

### Lesson Learned

Code that runs successfully can still produce misleading measurements. Matching rules must correspond to the intended definition of a keyword.

### Research implication

Inaccurate keyword counts can distort comparisons between documents. Explicit matching rules make the analysis more transparent and reproducible.

---

## Case 3: Long Abstracts Were Difficult to Manage in CSV

**Category:** Data organisation and file formats
**Status:** Improved

### Problem

Long scientific abstracts were initially stored directly inside CSV records. Replacing text was cumbersome, and commas, quotation marks and other punctuation made the file difficult to edit safely.

### Diagnosis

CSV is suitable for structured metadata but is inconvenient for repeatedly editing long passages of natural language.

### Solution

Separated the metadata and text content into different files:

- `corpus_inventory.csv`: document metadata, publication details and source information.
- `corpus_texts.csv`: document IDs, text types and file paths.
- `texts/SCI01.txt`: the first scientific abstract.
- `texts/SCI02.txt`: the second scientific abstract.

Python now reads the text paths recorded in the CSV file.

### Lesson Learned

File formats should be chosen according to their purpose. Structured metadata belongs in tables, while long original texts can be stored separately as plain-text files.

### Research implication

Separating metadata from source text improves maintainability and makes it easier to trace each analytical result back to its original document.

---

## Case 4: Raw Keyword Counts Do Not Directly Measure Research Importance

**Category:** Research methodology and interpretation
**Status:** Ongoing methodological consideration

### Problem

SCI02 contains more occurrences of `response diversity` than SCI01. However, this does not automatically mean that response diversity is more important in SCI02.

### Diagnosis

Raw counts can be influenced by:

- Different document lengths.
- Differences in author writing styles.
- Different research objectives.
- The choice of keywords and synonyms.
- Whether a term is used to support, question or criticise a claim.

### Planned improvement

After verifying the corpus and adding the policy texts:

1. Calculate keyword frequencies relative to document length where appropriate.
2. Compare patterns across scientific and policy texts.
3. Inspect sentences containing important terms before interpreting the results.
4. Document the keyword definitions and matching rules used in the analysis.

### Lesson Learned

Keyword frequency describes patterns in language, not the full meaning of a text. Quantitative results must be interpreted in their textual and research context.

### Research implication

A defensible text analysis requires more than counting words. It requires explicit measurement rules, appropriate comparisons and careful interpretation of the evidence.

---

## Overall Reflection

This project has required me to address practical challenges in text extraction, data organisation, keyword matching and analytical interpretation.

The work has reinforced four principles:

1. **Data quality:** readable data are not necessarily accurate data.
2. **Reproducibility:** source texts, metadata and analysis rules should remain traceable.
3. **Measurement validity:** the method used to count a concept must reflect what the analysis intends to measure.
4. **Critical interpretation:** quantitative patterns can identify relationships worth investigating, but they do not independently establish meaning or causation.

Future debugging cases will follow the same structure:

- Problem
- Diagnosis
- Solution
- Verification
- Lesson learned
- Research implication


## Case 5: Inconsistent Keyword Definitions Across Scripts

**Category:** Analytical consistency and reproducibility
**Status:** Resolved

### Problem

The analysis script and context-inspection script returned different counts for some terms, including stability.

### Diagnosis

The analysis script counted predefined phrases, such as "ecosystem stability" and "ecological stability". The context-inspection script originally searched for the broader term "stability".

### Solution

Separated the analysis into two categories:
- Core keyword groups, using the same predefined terms as the main analysis.
- Exploratory terms, used to identify additional relevant language in policy texts.

Updated the context-inspection script to apply consistent whole-word matching and whitespace normalisation.

### Verification

Re-ran the script. The core counts matched the main analysis:
- SCI01 stability: 1
- SCI02 stability: 2
- POL01 monitoring group: 2

The script generated 48 context records.

### Lesson Learned

Different counting rules can produce different results without either script necessarily failing. Reproducible analysis requires explicit definitions and consistent matching rules.

### Research implication

Core keyword counts support systematic comparison, while exploratory terms help identify concepts that may be relevant even when the predefined vocabulary does not capture them.
