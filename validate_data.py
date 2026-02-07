import json
import csv
import os
import re
import sys

# Configuration
MANIFEST_PATH = 'dataset.manifest.json'
THEMES_PATH = 'themes.yaml'
POS_PATH = 'PoS.tsv'
CEFR_PATH = 'CEFR__CLARINEL_KELLY_word-list_Greek.tsv'

# Common Greek articles to check for nouns
ARTICLES = [
    "ο ", "η ", "το ", "οι ", "τα ", 
    "(ο) ", "(η) ", "(το) ", "(οι) ", "(τα) ", "(ο/η) ", "ο/η "
]

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_pos_data_from_tsv(path):
    """
    Parses PoS.tsv.
    Returns:
    1. A set of valid Dutch PoS tags (nl + nl_abbr).
    2. A mapping from Dutch PoS (nl_abbr) to Greek PoS (el) for CEFR checking.
    """
    pos_tags = set()
    nl_to_el_map = {}
    
    if not os.path.exists(path):
        print(f"⚠️  Warning: {path} not found. Using empty PoS list.")
        return pos_tags, nl_to_el_map

    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
             # Load all valid Dutch forms
             nl_forms = [
                 row.get('nl_abbr'),
                 row.get('nl_singular'),
                 row.get('nl_plural')
             ]
             
             # Greek target for CEFR is usually full name (el_singular)
             el_target = (row.get('el_singular') or '').strip()
             
             for val in nl_forms:
                 if val:
                     val = val.strip()
                     if val:
                         pos_tags.add(val)
                         if el_target:
                             nl_to_el_map[val] = el_target
                 
    return pos_tags, nl_to_el_map

def load_cefr_data(path):
    """
    Loads the CEFR word list.
    Returns a dictionary: { "lemma": set(["pos1", "pos2"]) }
    """
    cefr_dict = {}
    if not os.path.exists(path):
        print(f"⚠️  Warning: {path} not found. Skipping CEFR checks.")
        return cefr_dict

    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        # Headers: PARENT LEMMA, Λήμμα (Lemma), ..., μέρος του λόγου (part of speech)
        
        for row in reader:
            lemma = row.get('Λήμμα (Lemma)', '').strip()
            # Alternately check 'PARENT LEMMA' if lemma is empty? 
            # Based on file view, column 2 is Lemma.
            
            pos_el = (row.get('μέρος του λόγου (part of speech)') or '').strip().lower()
            
            if lemma:
                if lemma not in cefr_dict:
                    cefr_dict[lemma] = set()
                # Split multiple pos? Sometimes "επίθετο, έκφραση"
                parts = [p.strip() for p in pos_el.split(',')]
                cefr_dict[lemma].update(parts)
                
    return cefr_dict

def normalize_greek_word(text):
    """
    Attempts to extract the core word/lemma from a vocabulary entry 
    for lookup in CEFR list.
    Removes articles, punctuation, footnotes.
    """
    # 1. Remove footnotes
    text = re.sub(r'[¹²³⁴⁵⁶⁷⁸⁹]', '', text)
    
    # 2. Iterate common articles to strip them
    # Simple heuristic: split by space, take last word? 
    # No, adjectives might be 'όμορφος -η -ο'. Nouns '(η) αγάπη'.
    
    # Clean up parentheses
    text = text.replace('(', '').replace(')', '')
    
    parts = text.split()
    # If multiple words, it's hard. CEFR is lemma based.
    # Try the last word if it looks like a noun phrase? "η αγάπη" -> "αγάπη"
    # But "κάνω λάθος" -> "λάθος" or "κάνω"? CEFR has "κάνω" and "λάθος" separately.
    
    # Strategy: Try to find ANY word from the phrase in the CEFR list?
    # Or just clean start?
    
    # Just try strict: if 1 or 2 words, try combinations.
    # For now, just return cleaned text to try basic exact match or substring match.
    return text.strip()

def get_valid_themes_from_yaml(path):
    """
    Parses themes.yaml using regex to avoid external dependencies like PyYAML.
    Extracts values from lines starting with '- nl:' or '  - nl:'.
    """
    themes = set()
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            # Match "nl: value" with optional leading hyphens/spaces
            match = re.search(r'^\s*-?\s*nl:\s*(.+)$', line)
            if match:
                theme_name = match.group(1).strip()
                themes.add(theme_name)
    return themes

def validate_parentheses(text):
    """Check if parentheses are balanced."""
    stack = []
    for char in text:
        if char == '(':
            stack.append(char)
        elif char == ')':
            if not stack:
                return False
            stack.pop()
    return len(stack) == 0

def validate_dataset(name, config, valid_themes, valid_pos, nl_to_el_map, cefr_dict):
    path = config.get('path')
    if not path:
        print(f"⚠️  Skipping {name}: No path defined.")
        return 0, 0
    
    if not os.path.exists(path):
        print(f"❌ Error: File {path} not found for dataset {name}")
        return 1, 0

    schema = config.get('schema', [])
    
    print(f"🔍 Validating {name} ({path})...")
    
    errors = 0
    cefr_warnings = 0
    row_count = 0
    
    # Detect delimiter based on extension or content?
    delimiter = '\t' if path.endswith('.tsv') else ';'
    
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        
        for i, row in enumerate(reader, start=2): # Start at 2 for line number (1 is header)
            row_count += 1
            
            # 1. PoS Validation
            pos = row.get('woordsoort', '').strip()
            # Allow lenient matching for trailing dots
            is_valid_pos = (
                pos in valid_pos or 
                pos.rstrip('.') in valid_pos or 
                f"{pos}." in valid_pos
            )
            
            if pos and not is_valid_pos:
                print(f"  [Line {i}] Invalid PoS: '{pos}'")
                errors += 1
            
            # 2. Theme Validation
            theme_field = row.get('thema', '')
            if theme_field:
                # Split by comma and strip
                themes = [t.strip() for t in theme_field.split(',') if t.strip()]
                for t in themes:
                    if t not in valid_themes:
                        print(f"  [Line {i}] Invalid Theme: '{t}'")
                        errors += 1

            # 3. Greek Article Check for Nouns
            greek = row.get('Grieks', '').strip()
            
            # CEFR Cross-Check
            cleaned_greek = normalize_greek_word(greek)
            
            if cleaned_greek in cefr_dict and pos:
                 # Get expected Greek PoS from our Dutch tag
                 # Handle dot leniently for mapping lookup
                 lookup_pos = pos
                 if lookup_pos not in nl_to_el_map:
                     lookup_pos = pos.rstrip('.')
                
                 expected_el_pos = nl_to_el_map.get(lookup_pos)
                 
                 if expected_el_pos:
                     allowed_cefr_tags = cefr_dict[cleaned_greek]
                     # Check if our mapped tag is in the allowed CEFR tags
                     
                     match_found = False
                     if expected_el_pos in allowed_cefr_tags:
                         match_found = True
                     # Flexible matching: 'znw' (noun) matches if 'ουσιαστικό' is one of the tags
                     elif 'έκφραση' in allowed_cefr_tags and ('groep' in pos or 'uitdr' in pos):
                         match_found = True
                     
                     if not match_found:
                         # Warning only
                         print(f"  [Line {i}] ⚠️  CEFR PoS Mismatch: '{greek}' is {pos} ({expected_el_pos}), CEFR says {allowed_cefr_tags}")
                         cefr_warnings += 1

            
            VALID_STARTERS = [
                # Definite Nominative
                "ο ", "η ", "το ", "οι ", "τα ", 
                "(ο) ", "(η) ", "(το) ", "(οι) ", "(τα) ",
                "(ο/η) ", "ο/η ",
                # Indefinite
                "ένας ", "ένα ", "μία ", "μια ", "έναν ",
                # Inflected 
                "τον ", "την ", "των ", "τους ", "τις ",
                # Special cases 
                "¹", "²"
            ]

            if 'znw' in pos:
                check_val = greek.lower()
                has_valid_start = False
                for starter in VALID_STARTERS:
                    if check_val.startswith(starter):
                        has_valid_start = True
                        break
                
                if not has_valid_start:
                    is_sentence = any(greek.endswith(p) for p in ['.', '!', ';', '?'])
                    has_internal_article = False
                    for starter in VALID_STARTERS:
                        if starter in check_val:
                            has_internal_article = True
                            break
                            
                    if is_sentence:
                         print(f"  [Line {i}] Suspected PoS Mismatch (Sentence marked as Noun): '{greek}'")
                         errors += 1
                    elif has_internal_article:
                         print(f"  [Line {i}] Suspected PoS Mismatch (Phrase/MWE marked as Noun): '{greek}'")
                         errors += 1
                    elif len(check_val.split()) > 1:
                         # User requested heuristic: >1 word likely means Phraseme/MWE if not a sentence
                         print(f"  [Line {i}] Suspected PoS Mismatch (Multi-word phrase marked as Noun): '{greek}'")
                         errors += 1
                    elif "=" in greek or "<" in greek:
                        pass 
                    elif "(" in greek and not greek.startswith("("):
                         pass
                    else:
                        print(f"  [Line {i}] Noun missing article (or non-standard start): '{greek}'")
                        errors += 1
            
            # 4. Parentheses Check
            if not validate_parentheses(greek):
                 print(f"  [Line {i}] Unbalanced parentheses in Greek: '{greek}'")
                 errors += 1
    
    if errors == 0:
        print(f"✅ {name}: OK ({row_count} rows)")
    else:
        print(f"❌ {name}: {errors} errors found")
    
    if cefr_warnings > 0:
        print(f"   (⚠️  {cefr_warnings} CEFR PoS mismatches found)")
    
    return errors, row_count

def main():
    print("🚀 Starting Data Validation...")
    
    # Load resources
    try:
        manifest = load_json(MANIFEST_PATH)
        valid_themes = get_valid_themes_from_yaml(THEMES_PATH)
        valid_pos, nl_to_el_map = get_pos_data_from_tsv(POS_PATH)
        cefr_dict = load_cefr_data(CEFR_PATH)
        print(f"DEBUG: Loaded CEFR dict with {len(cefr_dict)} lemmas.")
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"🔥 Critical Error loading config: {e}")
        sys.exit(1)
        
    datasets = manifest.get('datasets', {})
    total_errors = 0
    total_rows = 0
    
    for name, config in datasets.items():
        # Only validate vocabulary types for now
        if config.get('type') == 'vocabulary':
            errs, rows = validate_dataset(name, config, valid_themes, valid_pos, nl_to_el_map, cefr_dict)
            total_errors += errs
            total_rows += rows
            
    print("-" * 40)
    print(f"DONE. Processed {total_rows} rows.")
    if total_errors > 0:
        print(f"Found {total_errors} total errors.")
        sys.exit(1)
    else:
        print("All checks passed! 🎉")
        sys.exit(0)

if __name__ == "__main__":
    main()
