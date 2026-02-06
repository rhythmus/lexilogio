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
