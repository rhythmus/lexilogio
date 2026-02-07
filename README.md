# Lexilogio Data Repository

This repository contains the structured data powering the [Lexilogio vocabulary training webapp](https://ellinika.wso.art). It acts as the backend content source, separating logical curriculum data from the application code.

## 📂 Project Structure

- **Vocabulary Lists:**
  - `2024-2025-1B.csv`: Year 1 (1B) course vocabulary.
  - `2025-2026-2A.csv`: Year 2 (2A) course vocabulary.
  
- **Supplementary Data:**
  - `Constantinides-proverbs.tsv`: Collection of Greek proverbs with translations.
  - `subtitles-top-5000.tsv`: Frequency list of common Greek words.
  - `CEFR__CLARINEL_KELLY_word-list_Greek.tsv`: CEFR-aligned word list.

- **Configuration:**
  - `dataset.manifest.json`: Registry of datasets, defining schemas, subsets (semesters/lessons), and metadata.
  - `themes.yaml`: Hierarchical category definitions (Conversation, Culture, Nature, etc.) used for tagging vocabulary.
  - `rules.md`: **Strict style guide** and rules for data entry (capitalization, PoS tags, etc.).

## 📏 Data Standards

Data quality is maintained through strict adherence to `rules.md`. Key standards include:
- **Dutch/Greek Alignment:** Consistent capitalization and punctuation for sentences/expressions.
- **Part of Speech (PoS):** Standardized Dutch abbreviations (`bnw.`, `ww.`, `znw.`, etc.).
- **Articles:** Explicit inclusion of definite articles for Greek nouns (e.g., `(ο)`, `(η)`, `(το)`).

## 🛠 Usage


## 🏷️ Unified PoS Taxonomy & Concordance (`PoS-concordance.tsv`)

We have established a rigorous **Part-of-Speech (PoS) Concordance** to serve as the "Rosetta Stone" for grammatical tagging in our ecosystem. This master file maps our custom vocabulary data to major international linguistic standards, ensuring interoperability between our educational application and academic NLP resources.

### 🎯 Purpose & Application
The concordance (`PoS-concordance.tsv`) acts as a central lookup table that:
1.  **Normalizes** our custom, pedagogical tags (e.g., `znw.`, `ww.`) into a structured hierarchy (`n` -> `noun`).
2.  **Aligns** Greek morphology with international standards (INTERA, UD, PTB).
3.  **Enables Backward Compatibility**: A dedicated `legacy` column maps historical ad-hoc tags from `2024-2025-1B.csv` and `2025-2026-2A.csv` to the new canonical keys.

### 🏗 Architecture & Design
The taxonomy is designed around a **Hierarchical Key System** (column `Lexilogio tag`) which serves as the stable identifier for application logic. This key is grounded in **Wikidata QIDs** to ensure semantic precision (e.g., distinguishing *Proper Noun* `Q147276` from *Common Noun* `Q147276`).

#### Supported Tagsets
We implicitly support and map to the following authoritative standards:

1.  **Universal Dependencies (UD)**
    *   *Standard*: [Universal Dependencies](https://en.wikipedia.org/wiki/Universal_Dependencies)
    *   *Usage*: Provides broad, cross-linguistic categories (`NOUN`, `VERB`, `ADJ`) facilitating comparison with other languages.

2.  **INTERA (Greek)**
    *   *Standard*: [Greek INTERA Tagset](https://nlp.ilsp.gr/setn-2020/3411408.3411430.pdf) | [Sketch Engine Tagset](https://www.sketchengine.eu/greek-intera-part-of-speech-tagset/) | [Wiki](https://en.wikipedia.org/wiki/Part-of-speech_tagging)
    *   *Usage*: Specialized for Greek morphology, covering specific features like Case (`ptoseis`), Gender (`genos`), and inflectional types.

3.  **Penn Treebank (PTB)**
    *   *Standards*: [Brill Tagger](https://en.wikipedia.org/wiki/Brill_tagger), [Stanford CoreNLP](https://stanfordnlp.github.io/CoreNLP/tools_pos_tagger.html), [Kaggle Dataset](https://www.kaggle.com/datasets/aliakay8/penn-treebank-dataset)
    *   *Usage*: The de-facto standard for English NLP. We map our tags to PTB codes (`NN`, `VB`, `JJ`) to allow integration with tools like the Brill Tagger and Stanford CoreNLP.

### 📚 Authorities & Sources
Our taxonomy validation relies on:
-   **Stanford CoreNLP**: [POS Tagger](https://stanfordnlp.github.io/CoreNLP/pos.html)
-   **Universal Dependencies**: [Feature List](https://en.wikipedia.org/wiki/Universal_Dependencies)
-   **ILSP**: [Greek NLP Resources](https://nlp.ilsp.gr/setn-2020/3411408.3411430.pdf)

## 📊 Frequency Data Normalization

In February 2026, we consolidated our approach to handling frequency data from multiple heterogeneous corpora. This ensures that data from different sources (e.g., educational word lists vs. subtitle analysis) is mathematically commensurable within the client application.

### 1. Methodology & Design Choices
We store **Raw Frequency Counts** only. We explicitly avoid storing derived or pre-normalized values (like percents or permilles) in the source files. This prevents redundancy and loss of precision.

Instead, we store the **Total Corpus Size** for each dataset in the `dataset.manifest.json`. This "magic number" allows the client to dynamically calculate normalized frequencies (such as *Frequency Per Million*) or apply transformations (such as *log10 normalization*) on the fly.

### 2. Available Datasets & Constants

#### A. **CEFR (CLARIN-EL/Kelly)**
*   **File**: `CEFR__CLARINEL_KELLY_word-list_Greek.tsv`
*   **Nature**: A balanced, educational corpus containing both lemmas and expressions.
*   **Corpus Size**: `57,446,651` (Reverse-engineered from original permille data).
*   **Structure**: PARENT LEMMA, Lemma, CEF Level, **Raw Frequency**, PoS.

#### B. **OpenSubtitles (Top 5000)**
*   **File**: `subtitles-top-5000.tsv`
*   **Nature**: A spoken/colloquial corpus containing specific inflected word forms.
*   **Corpus Size**: `111,940,212` (Note: This is the sum of frequencies of the top 5,000 items only, serving as the normalization baseline for this specific subset).
*   **Structure**: Legomenon, **Raw Frequency**.

### 3. Client Implementation Specs

The client application **MUST** consume the `corpus_size` property from the manifest to compute compatible values.

#### Normalization Formula (Per Million)
To compare word A (from CEFR) with word B (from Subtitles):
$$ \text{Frequency}_{pm} = \left( \frac{\text{Raw Count}}{\text{Corpus Size}} \right) \times 1,000,000 $$

#### Weighted Scoring Formula
When merging data for a single word appearing in multiple lists, the application should apply a weighted average based on the preferred bias (e.g., favoring colloquial usage):

$$ \text{Score}_{final} = (w_{sub} \times \text{Freq}_{sub\_pm}) + (w_{cefr} \times \text{Freq}_{cefr\_pm}) $$

*Recommended Weights*: $w_{sub} = 0.6$ (favoring spoken subtitles), $w_{cefr} = 0.4$.

#### Logarithmic Scaling (Zipf's Law)
For UI visualization (e.g., progress bars or heatmaps), use Log10 to handle the power-law distribution of natural language:
$$ \text{Value}_{ui} = \log_{10}(1 + \text{Raw Count}) $$
*Note: Always normalize to a common corpus baseline before applying log if comparing absolute "popularity".*

### 4. Instructions for New Datasets
When adding a new frequency list:
1.  **Store Raw Data**: Do not normalize the counts in the TSV/CSV file.
2.  **Calculate Corpus Size**:
    *   If the source provides the total token count, use it.
    *   If not, sum the frequencies of all items in the list to establish a "Sample Total" baseline.
3.  **Update Manifest**: Add a `"corpus_size": [INTEGER]` field to the dataset's entry in `dataset.manifest.json`.

## 🛡️ Lexical Verification & Auditing

As of February 2026, we have introduced automated auditing pipelines to validatethe integrity of our manually curated word lists against external authorities (Wiktionary).

### The Audit Script (`wiktionary_audit.py`)
This Python script serves as a verification layer for the Part-of-Speech (PoS) tags in `CEFR__CLARINEL_KELLY_word-list_Greek.tsv`.

#### Key Design Choices & Rationale
1.  **Rate-Limited Scraping**:
    *   *Mechanism*: Implements a strictly enforced 0.5-second delay between requests.
    *   *Rationale*: To respect Wiktionary's API usage policies and avoid 403 Forbidden errors/IP bans.
2.  **Robust HTML Parsing**:
    *   *Challenge*: Wiktionary's DOM structure varies (older `<h2>` vs newer `<div class="mw-heading">`).
    *   *Solution*: The script uses a traversal logic that identifies headers regardless of their wrapper, ensuring consistent extraction of "Noun", "Verb", etc. sections.
3.  **Mapping Strategy**:
    *   *Source*: Uses `PoS-concordance.tsv` to map English Wiktionary headers (e.g., "Participle") to our specific Greek abbreviations (e.g., "μτχ.").
    *   *Fallback*: Defaults to `Lexilogio tag` if a specific abbreviation is missing.

#### Usage
```bash
python3 wiktionary_audit.py
```
This generates `CEFR__CLARINEL_KELLY_word-list_Greek_audited.tsv`, adding a `Wiktionary` column for side-by-side comparison of manual vs. external tags.

## 📱 Application Engineering

Beyond data curation, recent engineering efforts have focused on the stability and UX of the consumer application (`rhythmus/lexilogio`).

### UI/UX Refinements
*   **Global Scrollbar Resolution**: Fixed vertical scrolling issues in "Settings" and "Progress" views, ensuring scrollbars respect the AppHeader layout and do not overlay content.
*   **Exercise Composer**: Resolved table overflow issues, ensuring the vocabulary selection table consumes available vertical space without cropping.

### Robustness & Debugging
*   **React Hydration**: Diagnosed and fixed invalid HTML nesting (specifically `<div>` nested within `<p>` tags) in the `FlashcardView` and `FormattedText` components, resolving critical runtime warnings.
*   **Codebase Audits**: Conducted structural audits to identify refactoring opportunities, focusing on component modularity and standardizing hook usage.
