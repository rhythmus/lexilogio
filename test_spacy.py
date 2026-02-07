import spacy

# Load the large Greek model
nlp = spacy.load("el_core_news_lg")

# Test words: 
# 1. ψηφίο (digit) - should be NOUN
# 2. ένα (one) - cardinal numeral
# 3. πρώτος (first) - ordinal numeral
# 4. πέντε (five) - cardinal numeral
# 5. τρέχω (I run) - Verb
# 6. εγώ (I) - Personal Pronoun
# 7. ποιος (who) - Interrogative Pronoun (or similar)
# 8. δικός (own/mine) - Possessive

words = [
    "ψηφίο", 
    "ένα", 
    "πρώτος", 
    "πέντε", 
    "τρέχω", 
    "εγώ", 
    "ποιος", 
    "δικός",
    "εκατό"
]

print(f"{'Word':<10} | {'UPOS':<6} | {'Morphological Features'}")
print("-" * 60)

for word in words:
    doc = nlp(word)
    token = doc[0]
    print(f"{token.text:<10} | {token.pos_:<6} | {token.morph}")
