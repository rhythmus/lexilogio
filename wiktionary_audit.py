import csv
import logging
import time
import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Set, Optional

# --- Configuration ---
SOURCE_FILE = 'CEFR__CLARINEL_KELLY_word-list_Greek.tsv'
MAPPING_FILE = 'PoS-concordance.tsv'
OUTPUT_FILE = 'CEFR__CLARINEL_KELLY_word-list_Greek_audited.tsv'
WIKTIONARY_BASE_URL = 'https://en.wiktionary.org/wiki/'
DELAY_BETWEEN_REQUESTS = 0.5  # Seconds

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("wiktionary_audit.log"),
        logging.StreamHandler()
    ]
)

def load_pos_mapping(mapping_file: str) -> Dict[str, str]:
    """
    Loads the PoS mapping from the concordance file.
    Returns a dictionary mapping English PoS (e.g., 'noun') to Greek Abbreviation (e.g., 'ουσ.').
    """
    mapping = {}
    try:
        with open(mapping_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter='\t')
            for row in reader:
                # Primary key: English singular name (lowercase)
                # Alternatives: English abbr, Lexilogio tag?
                # The user wants "en_singular" -> "el_abbr" 
                # (column names need to be verified from file header)
                
                # Based on file inspection:
                # 'en_singular' -> 'el_abbr'
                # Also need to handle cases where Wiktionary gives "Proper noun" -> "proper noun"
                
                en_name = row.get('en_singular', '').strip().lower()
                el_abbr = row.get('el_abbr', '').strip()
                lexilogio = row.get('Lexilogio tag', '').strip()
                
                target_val = el_abbr if el_abbr else lexilogio
                
                if en_name and target_val:
                    mapping[en_name] = target_val
                    
                # Also map synonyms if present? Wiktionary headers are usually standard.
                # "Noun", "Verb", "Adjective" etc.
    except Exception as e:
        logging.error(f"Error loading mapping file: {e}")
        return {}

    # Hardcoded/fallback mappings common in Wiktionary
    # Wiktionary headers are capitalized, we'll lower() them for lookup
    mapping['noun'] = mapping.get('noun', 'ουσ.')
    mapping['verb'] = mapping.get('verb', 'ρ.')
    mapping['adjective'] = mapping.get('adjective', 'επίθ.')
    mapping['adverb'] = mapping.get('adverb', 'επίρρ.')
    mapping['pronoun'] = mapping.get('pronoun', 'αντων.')
    mapping['particle'] = mapping.get('particle', 'μόρ.')
    mapping['preposition'] = mapping.get('preposition', 'πρόθ.')
    mapping['conjunction'] = mapping.get('conjunction', 'σύνδ.')
    mapping['interjection'] = mapping.get('interjection', 'επιφ.')
    mapping['proper noun'] = mapping.get('proper noun', 'κ.ό.')
    mapping['article'] = mapping.get('article', 'άρθρ.')
    mapping['participle'] = mapping.get('participle', 'μτχ.') # Explicitly requested
    mapping['numeral'] = mapping.get('numeral', 'αριθ.')
    
    return mapping

def fetch_wiktionary_pos(lemma: str) -> List[str]:
    """
    Fetches the Wiktionary page for the lemma and extracts PoS headers from the Greek section.
    """
    url = f"{WIKTIONARY_BASE_URL}{lemma}"
    headers = {
        'User-Agent': 'WiktionaryAuditScript/1.0 (mailto:woutersoudan@example.com) based on asking for educational purposes'
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 404:
            logging.warning(f"Page not found for: {lemma}")
            return []
        if response.status_code != 200:
            logging.error(f"Failed to fetch {lemma}: Status {response.status_code}")
            return []
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Methodology:
        # 1. Find the "Greek" h2 header.
        # 2. Iterate siblings until the next h2.
        # 3. Look for h3 or h4 headers that match known PoS types.
        
        greek_header = soup.find('span', {'id': 'Greek'})
        if not greek_header:
             # Try fallback for "Ancient Greek" vs "Greek" if needed, but user specified "Greek"
             # Sometimes the id is different or extracted differently.
             # The id is usually inside the h2.
             for h2 in soup.find_all('h2'):
                 if 'Greek' in h2.get_text():
                     greek_header = h2
                     break
        
        if not greek_header:
            logging.warning(f"No Greek section found for: {lemma}. Available h2s: {[h.get_text() for h in soup.find_all('h2')]}")
            return []
            
        # If greek_header is inside a div.mw-heading, we want to iterate from that div
        if greek_header.parent and 'mw-heading' in greek_header.parent.get('class', []):
            current_element = greek_header.parent.next_sibling
        else:
            current_element = greek_header.next_sibling
            
        found_pos = set()
        
        while current_element:
            # Handle headers wrapped in div.mw-heading
            header_node = None
            if current_element.name == 'div' and 'mw-heading' in current_element.get('class', []):
                header_node = current_element.find(['h2', 'h3', 'h4', 'h5'])
            elif current_element.name in ['h2', 'h3', 'h4', 'h5']:
                header_node = current_element
            
            if header_node:
                if header_node.name == 'h2':
                    break # Reached next language section
                
                header_text = header_node.get_text().strip()
                header_text = header_text.replace('[edit]', '').strip()
                
                # logging.info(f"Found header in Greek section: {header_text}")

                # Check if this header corresponds to a PoS
                lower_text = header_text.lower()
                
                known_pos_types = [
                    'noun', 'verb', 'adjective', 'adverb', 'pronoun', 
                    'preposition', 'conjunction', 'interjection', 
                    'proper noun', 'article', 'participle', 'numeral', 'particle'
                ]
                
                for pos_type in known_pos_types:
                    if pos_type == lower_text or pos_type in lower_text.split(): # rough match
                         # Precise match is better, but heeaders can be "Adjective 1" etc.
                         if lower_text.startswith(pos_type):
                             found_pos.add(pos_type)
            
            current_element = current_element.next_sibling
            
        return sorted(list(found_pos))

    except Exception as e:
        logging.error(f"Exception fetching {lemma}: {e}")
        return []

def normalize_el_pos(pos_str: str) -> Set[str]:
    """
    Splits the existing PoS string (e.g. "ουσ., ρ.") into a set of normalized tags.
    """
    if not pos_str:
        return set()
    # Split by comma or semicolon
    parts = pos_str.replace(';', ',').split(',')
    return {p.strip() for p in parts if p.strip()}

def audit_word_list():
    """
    Main function to process the word list.
    """
    logging.info("Starting audit...")
    pos_mapping = load_pos_mapping(MAPPING_FILE)
    logging.info(f"Loaded {len(pos_mapping)} PoS mappings.")
    
    # Check specific test case first?
    # No, we will run the script, but maybe just for the requested one if we want to confirm?
    # The user asked for a script to "go over all the rows".
    # I will add a command line arg to limit rows for testing.
    
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--limit', type=int, help='Limit number of rows to process')
    parser.add_argument('--target', type=str, help='Process only a specific lemma')
    args = parser.parse_args()

    processed_count = 0
    updated_count = 0
    
    try:
        with open(SOURCE_FILE, 'r', encoding='utf-8') as fin, \
             open(OUTPUT_FILE, 'w', encoding='utf-8', newline='') as fout:
            
            reader = csv.DictReader(fin, delimiter='\t')
            fieldnames = reader.fieldnames
            if 'Wiktionary' not in fieldnames:
                fieldnames.append('Wiktionary')
            
            writer = csv.DictWriter(fout, fieldnames=fieldnames, delimiter='\t')
            writer.writeheader()
            
            for row in reader:
                lemma = row.get('λήμμα', '').strip()
                if not lemma:
                    writer.writerow(row)
                    continue

                # Filter logic
                if args.target and lemma != args.target:
                    writer.writerow(row)
                    continue
                
                if args.limit and processed_count >= args.limit:
                    if not args.target: # If target is set, keep searching
                         writer.writerow(row)
                         continue

                # Process this row
                logging.info(f"Checking: {lemma}")
                current_pos_raw = row.get('τύπος λέξης', '')
                current_pos_set = normalize_el_pos(current_pos_raw)
                
                wiktionary_pos_english = fetch_wiktionary_pos(lemma)
                wiktionary_pos_greek_set = set()
                
                for en_pos in wiktionary_pos_english:
                    if en_pos in pos_mapping:
                        wiktionary_pos_greek_set.add(pos_mapping[en_pos])
                    else:
                        logging.warning(f"Unmapped Wiktionary PoS '{en_pos}' for lemma '{lemma}'")
                
                # Compare sets
                # We need to see if they "match".
                # The user said: "If they are at odds, then the Wiktionary value(s) should be appended..."
                # "At odds" usually means not equal.
                # However, our current tags might be subsets or just different abbreviations.
                # The user wants "converted (if possible) into the 'el_abbr' value... with 'Lexilogio tag' as fallback."
                
                # Logic: If sets are not identical, update.
                if current_pos_set != wiktionary_pos_greek_set and wiktionary_pos_greek_set:
                    # Construct the new string
                    # sort for consistency
                    new_val_str = ", ".join(sorted(list(wiktionary_pos_greek_set)))
                    row['Wiktionary'] = new_val_str
                    updated_count += 1
                    logging.info(f"Mismatch for {lemma}. Current: {current_pos_raw} -> Wiktionary: {new_val_str}")
                else:
                    if not wiktionary_pos_greek_set:
                         logging.info(f"No Wiktionary data found matching our mapping for {lemma}")
                    else:
                         logging.info(f"Match for {lemma}")

                writer.writerow(row)
                processed_count += 1
                time.sleep(DELAY_BETWEEN_REQUESTS)
                
                if args.limit and processed_count >= args.limit and not args.target:
                    break

    except Exception as e:
        logging.critical(f"Fatal error: {e}")

    logging.info(f"Audit complete. processed {processed_count} rows, updated {updated_count} rows.")

if __name__ == "__main__":
    audit_word_list()
