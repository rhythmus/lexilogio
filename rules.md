Here are the rules for each column 

---

### 1. **volgnummer**
- The original line number or unique identifier from the source file.
- Always 4 digits, padded with leading zeros (e.g., 0101).

### 2. **date**
- Usually left empty unless a specific date is present in the source or required for context.
- If a date is present in the source, it is copied here.

### 3. **Dutch**
- The main Dutch entry, cleaned and standardized:
  - **Capitalization:**  
    - Sentences, questions, expressions: Capitalized and proper sentence punctuation (. ! ? … )
    - Proper nouns/place names: Capitalized
    - All other entries: lowercase
  - **Deduplication/Simplification:**  
    - Remove unnecessary articles and plurals unless contextually required.
    - Only the core translation is kept; extra info is moved to the comment column.
  - **Expressions:**  
    - Dutch expressions are matched in style and punctuation to the Greek.

### 4. **Greek**
- The main Greek entry, cleaned and standardized:
  - **Capitalization:**  
    - Sentences, questions, expressions: Capitalized and proper sentence punctuation (. ! ; … )
    - Proper nouns/place names: Capitalized
    - All other entries: lowercase
  - **Articles:**  
    - proper names, abstract nouns and philosophical concepts that in Greek always require the definite article must be prepended with "ο ", "η ", "το ", "οι ", "τα ", etc.
    - all other nouns must also be prepended with the article, but in-between parentheses, e.g. "(ο) "
    - nouns that can be both masculine and feminine must have "(ο/η) " or "ο/η "
    - after the singular main entry, the plural, if applicable, must be given, e.g. "(η) διακοπή, (οι) διακοπές"
  - **Adjectives:**  
    - are given in nominative masculine singular, but with grammatical endings added as needed, e.g. "βρώμικος -η -ο", "χοντρός -ή -ό"
  - **Prepositions:**  
    - Case requirements are specified if relevant, e.g. "από + acc."
  - **Synonyms:**
    - synonyms are listed alphabetically, and separated with a comma, e.g. "άσπρος -η -ο, λευκός -ή -ό"

### 5. **PoS** (Part of Speech)
- Standardized using Dutch abbreviations:
  - bijw. = bijwoord (adverb)
  - bnw. = bijvoeglijk naamwoord (adjective)
  - eigennaam
  - groep = group (for grouped words/phrases)
  - tsw. = tussenwerpsel
  - tw. = telwoord (numeral)
  - uitdr. = uitdrukking (expression)
  - vnw. = voornaamwoord (pronoun)
  - vraagzin = question
  - vw. = voegwoord (conjunction)
  - vz. = voorzetsel (preposition)
  - ww. = werkwoord (verb)
  - zin = sentence
  - znw. = zelfstandig naamwoord (noun)
  - Other combinations as needed (e.g., ww. groep, znw. groep, etc.)
- If the source has a more complex or non-standard PoS, it is mapped to the closest Dutch abbreviation.

### 6. **comment**
- Any extra information, clarifications, or context from the source that does not belong in the main translation.
- Examples: usage notes, diminutive, plural, formality, etc.
- If not needed, this column is left empty.

### 7. **theme**
- Based on its meaning or context, each entry is assigned at least 1 to up to 3 standardized semantical theme category from the following, hierarchical list:
  
  - converseren
    - relaties
    - uitdrukkingen
  - dingen
    - kleuren & vormen
    - voedsel
    - gebouwen
  - meten
    - hoeveelheden
    - kalender
    - tijd
  - cultuur
    - filosofie
    - geografie
    - namen
    - muziek 
  - grammatica
  - maatschappij
    - beroepen
    - school
    - sport
  - behoeftes
    - emoties
    - kleding
    - lichaam
    - routines
    - wonen
    - winkelen
    - reizen
  - natuur
    - dieren
    - planten
    - weer & klimaat


---

**General Rules Applied Across All Columns:**
- **Capitalization and punctuation** are only synchronized for sentences, questions, expressions, and proper nouns/place names.
- **Deduplication and simplification** are applied to Dutch entries.
- **Extra info** is moved to the comment column.
- **PoS and theme** are standardized and mapped consistently.


(ο)
(η)
(το)
(ο/η)
(οι)
(τα)

ος -η -ο;bnw.;;;;;
ός -ή -ό;bnw.;;;;;
ος -α -ο;bnw.;;;;;
ός -ά -ό;bnw.;;;;;
υς -εια -υ;bnw.;;;;;
ύς -εία -ύ;bnw.;;;;;

(π.χ.)
etc. κ.λπ.

*αλλά*:
;
…ω - …ς, …ει, …με, …τε, …νε;ww.;herhaling;
→← 
♀

`， ` (U+FF0C, FULLWIDTH COMMA followed by space) : separator in-between synonymous meanings
¹²³⁴⁵⁶⁷⁸⁹ preceeded by space: separator in-between alternative meanings


Finally I want basic Markdown parsing, such that text in-between `*` and `*` is rendered as <strong> (bold text) and text in-between `_` and `_` is rendered as <em> (italic text). (Obviously in these cases the markup symbols `*` and `_` should be omitted in the rendered result.) For example (and be cautious, because this example also involves the article parsing): "(*η*) οδός" should be rendered with the article `η` as dimmed-out text (because it is an article in-between parentheses, and thus optional), but also using a boldface because it is in-between `*` asterisks.