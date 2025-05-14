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
    - Sentences, questions, expressions, and proper nouns/place names: Capitalized.
    - All other entries: Lowercase.
  - **Punctuation:**  
    - Synchronized with the Greek column (question mark, exclamation mark, period, etc.).
  - **Deduplication/Simplification:**  
    - Remove unnecessary articles and plurals unless contextually required.
    - Only the core translation is kept; extra info is moved to the comment column.
  - **Expressions:**  
    - Dutch expressions are matched in style and punctuation to the Greek.

### 4. **Greek**
- The main Greek entry, cleaned and standardized:
  - **Capitalization:**  
    - Sentences, questions, expressions, and proper nouns/place names: Capitalized.
    - All other entries: Lowercase.
  - **Punctuation:**  
    - Synchronized with the Dutch column.
  - **Articles:**  
    - Proper articles are ensured for proper names and abstract nouns.
  - **Adjectives:**  
    - Grammatical endings are added as needed.
  - **Prepositions:**  
    - Case requirements are specified if relevant.
  - **Expressions:**  
    - Greek expressions are matched in style and punctuation to the Dutch.

### 5. **PoS** (Part of Speech)
- Standardized using Dutch abbreviations:
  - znw. = zelfstandig naamwoord (noun)
  - bnw. = bijvoeglijk naamwoord (adjective)
  - ww. = werkwoord (verb)
  - vnw. = voornaamwoord (pronoun)
  - tw. = telwoord (numeral)
  - bw. = bijwoord (adverb)
  - vz. = voorzetsel (preposition)
  - vw. = voegwoord (conjunction)
  - uitdr. = uitdrukking (expression)
  - vraagzin = question
  - zin = sentence
  - groep = group (for grouped words/phrases)
  - Other combinations as needed (e.g., ww. groep, znw. groep, etc.)
- If the source has a more complex or non-standard PoS, it is mapped to the closest Dutch abbreviation.

### 6. **comment**
- Any extra information, clarifications, or context from the source that does not belong in the main translation.
- Examples: usage notes, diminutive, plural, formality, etc.
- If not needed, this column is left empty.

### 7. **theme**
- Each entry is assigned to a standardized theme based on its meaning or context.
- Examples:  
  - persoonlijk & familie
  - namen noemen
  - wensen
  - kennismaken
  - school & werk  
  - communicatie  
  - emoties  
  - kalender
  - geografie  
  - muziek  
  - voedsel  
  - kleding  
  - vervoer  
  - natuur  
  - hoeveelheden
  - taalkunde
  - sport
  - varia
- The theme is inferred from the word’s meaning and context, matching the list you provided or established in previous batches.

---

**General Rules Applied Across All Columns:**
- **Capitalization and punctuation** are only synchronized for sentences, questions, expressions, and proper nouns/place names.
- **Deduplication and simplification** are applied to Dutch entries.
- **Extra info** is moved to the comment column.
- **PoS and theme** are standardized and mapped consistently.

If you need a more detailed breakdown for a specific column or want to see examples, let me know!
