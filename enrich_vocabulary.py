import spacy
import csv
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import shutil

class PoSHierarchy:
    def __init__(self, tsv_path: Path):
        self.tsv_path = tsv_path
        self.ud_to_lexilogio: Dict[str, str] = {}
        self.tag_details: Dict[str, Dict[str, str]] = {}
        self._load_hierarchy()

    def _load_hierarchy(self):
        """
        Parses the PoS-concordance.tsv file to map UD tags to Lexilogio tags
        and store detailed Greek labels.
        """
        if not self.tsv_path.exists():
            raise FileNotFoundError(f"PoS concordance file not found at: {self.tsv_path}")

        with open(self.tsv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter='\t')
            for row in reader:
                ud_tag = row.get('UD', '').strip()
                lexilogio_tag = row.get('Lexilogio tag', '').strip()
                el_singular = row.get('el_singular', '').strip()
                el_abbr = row.get('el_abbr', '').strip()
                
                if lexilogio_tag:
                    self.tag_details[lexilogio_tag] = {
                        'el_singular': el_singular,
                        'el_abbr': el_abbr
                    }
                
                # Only store if both exist. 
                if ud_tag and lexilogio_tag:
                    ud_tag = ud_tag.split(',')[0].strip()
                    if ud_tag not in self.ud_to_lexilogio:
                         self.ud_to_lexilogio[ud_tag] = lexilogio_tag

class SmartTagger:
    def __init__(self, hierarchy: PoSHierarchy):
        self.hierarchy = hierarchy
        print("Loading spaCy model 'el_core_news_lg'...")
        try:
            self.nlp = spacy.load("el_core_news_lg")
        except OSError:
            raise OSError("Could not load 'el_core_news_lg'. Please ensure it is installed.")

    def get_detailed_pos(self, text: str) -> Dict[str, str]:
        """
        Analyzes the text and returns a dictionary with analysis results:
        """
        doc = self.nlp(text)
        if not doc:
            return {"text": text, "ud_pos": "", "morph": "", "lexilogio_pos": ""}
            
        # Find the root token for better phrase handling, or fallback to first token
        root_tokens = [t for t in doc if t.dep_ == "ROOT"]
        token = root_tokens[0] if root_tokens else doc[0]
        
        ud_pos = token.pos_
        morph_dict = token.morph.to_dict()
        morph_str = str(token.morph)
        
        # --- SMART MAPPING LOGIC ---
        lexilogio_pos = self._apply_smart_rules(ud_pos, morph_dict)
        
        return {
            "text": token.text,
            "ud_pos": ud_pos,
            "morph": morph_str,
            "lexilogio_pos": lexilogio_pos
        }

    def _apply_smart_rules(self, ud_pos: str, morph: Dict[str, str]) -> str:
        """
        Applies specific rules to refine the coarse UD tag into a detailed Lexilogio tag.
        """
        
        # 1. NUMERALS
        if ud_pos == "NUM":
            num_type = morph.get("NumType")
            if num_type == "Ord":
                return "num.ord"  # Ordinal
            elif num_type == "Card":
                return "num.card" # Cardinal
            return "num"

        # 2. DETERMINERS
        if ud_pos == "DET":
            pron_type = morph.get("PronType")
            definite = morph.get("Definite")
            if pron_type == "Art":
                if definite == "Def":
                    return "art.def"
                elif definite == "Ind":
                    return "art.ind"
                return "art"
            return "det"

        # 3. PRONOUNS
        if ud_pos == "PRON":
            pron_type = morph.get("PronType")
            if pron_type == "Prs":
                if morph.get("Poss") == "Yes":
                    return "pron.poss"
                return "pron.pers"
            elif pron_type == "Int":
                return "pron.int"
            elif pron_type == "Rel":
                return "pron.rel"
            elif pron_type == "Dem":
                return "pron.dem"
            elif pron_type == "Ind":
                return "pron.ind"
            return "pron"

        # 4. VERBS
        if ud_pos == "VERB":
            return "v"
            
        if ud_pos == "AUX":
            return "v.aux"

        # 5. ADJECTIVES
        if ud_pos == "ADJ":
            degree = morph.get("Degree")
            if degree == "Cmp":
                return "adj.comp"
            elif degree == "Sup":
                return "adj.sup"
            return "adj"

        # 6. ADVERBS
        if ud_pos == "ADV":
             return "adv"

        # 7. NOUNS
        if ud_pos == "NOUN":
            return "n"
            
        if ud_pos == "PROPN":
            return "prop.n"

        # Fallback to hierarchy lookup
        if ud_pos in self.hierarchy.ud_to_lexilogio:
            return self.hierarchy.ud_to_lexilogio[ud_pos]

        return ud_pos.lower() 

def update_kelly_file(file_path: Path, tagger: SmartTagger, limit: int = None):
    """
    Updates the CEFR__CLARINEL_KELLY_word-list_Greek.tsv file by appending 'Lexilogio', 
    'el_singular', and 'el_abbr' columns.
    """
    print(f"Updating rows of {file_path.name}...")
    
    temp_path = file_path.with_suffix('.tmp')
    
    with open(file_path, 'r', encoding='utf-8') as f_in, \
         open(temp_path, 'w', encoding='utf-8', newline='') as f_out:
        
        reader = csv.reader(f_in, delimiter='\t')
        writer = csv.writer(f_out, delimiter='\t')
        
        header = next(reader)
        
        # Helper to ensure column exists
        def ensure_column(name):
            if name in header:
                return header.index(name)
            else:
                header.append(name)
                return len(header) - 1

        lex_idx = ensure_column("Lexilogio")
        el_sing_idx = ensure_column("el_singular")
        el_abbr_idx = ensure_column("el_abbr")
            
        writer.writerow(header)
        
        try:
            lemma_idx = header.index("Λήμμα (Lemma)")
        except ValueError:
            print("Error: Could not find 'Λήμμα (Lemma)' column.")
            return

        count = 0
        for i, row in enumerate(reader):
            # Ensure row has enough columns for existing data
            if len(row) <= lemma_idx:
                 writer.writerow(row)
                 continue
                 
            # Pad row if strictly needed to match new header length
            while len(row) < len(header):
                row.append("")

            if limit is None or count < limit:
                lemma = row[lemma_idx].strip()
                if lemma:
                    try:
                        # 1. Get Lexilogio Tag
                        if not row[lex_idx]: # If not already populated, run tagger
                            res = tagger.get_detailed_pos(lemma)
                            new_pos = res['lexilogio_pos']
                            row[lex_idx] = new_pos
                        else:
                            new_pos = row[lex_idx]

                        # 2. Look up Greek labels
                        if new_pos and new_pos in tagger.hierarchy.tag_details:
                             details = tagger.hierarchy.tag_details[new_pos]
                             row[el_sing_idx] = details['el_singular']
                             row[el_abbr_idx] = details['el_abbr']

                    except Exception as e:
                        print(f"Error processing row {i+2} ('{lemma}'): {e}")
                count += 1
            writer.writerow(row)
            
    # Replace original file
    shutil.move(str(temp_path), str(file_path))
    print(f"Updated {count} rows.")

# --- Main Execution Block ---
if __name__ == "__main__":
    base_path = Path("/Users/woutersoudan/Grieks@CLT")
    tsv_file = base_path / "PoS-concordance.tsv"
    kelly_file = base_path / "CEFR__CLARINEL_KELLY_word-list_Greek.tsv"
    
    try:
        hierarchy = PoSHierarchy(tsv_file)
        tagger = SmartTagger(hierarchy)
        
        update_kelly_file(kelly_file, tagger)
            
    except Exception as e:
        print(f"Error: {e}")
