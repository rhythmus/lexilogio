import csv
import shutil
import re
from pathlib import Path

def load_abbreviations(concordance_path: Path):
    """
    Loads a mapping of {el_singular: el_abbr} from the concordance file.
    Only includes entries where el_abbr is populated.
    """
    abbr_map = {}
    with open(concordance_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        try:
            header = next(reader)
            # Find indices for relevant columns
            # Header line: ... el_singular el_plural el_abbr
            # Let's dynamically find them to be safe, or assume standard layout
            
            # Based on previous view:
            # col -3: el_singular
            # col -1: el_abbr
            
            # Let's find index by name if possible, or fall back to negative indexing if headers vary
            try:
                sing_idx = header.index("el_singular")
                abbr_idx = header.index("el_abbr")
            except ValueError:
                # Fallback based on visual inspection of file
                sing_idx = -3
                abbr_idx = -1
                
        except StopIteration:
            return {}
            
        for row in reader:
            if len(row) < 3: continue
            
            try:
                singular = row[sing_idx].strip()
                abbr = row[abbr_idx].strip()
                
                if singular and abbr:
                    abbr_map[singular] = abbr
            except IndexError:
                continue
                
    return abbr_map

def standardize_pos_columns(target_file: Path, abbr_map: dict):
    print(f"Standardizing POS in {target_file.name}...")
    temp_path = target_file.with_suffix('.tmp')
    
    # Sort keys by length descending to prevent partial replacements of longer terms
    sorted_keys = sorted(abbr_map.keys(), key=len, reverse=True)
    
    # Compile regex patterns for efficiency and robustness
    # We use \b for word boundaries. 
    # Note: Greek characters are alphanumeric so \b should work, but for safety with punctuation
    # we can use lookarounds or just rely on re.sub with whole words.
    # Actually, simpler loop with compiled regexes:
    patterns = []
    for key in sorted_keys:
        # Escape key (e.g. contains parenthesis? unlikely for singulars but safe)
        pattern = re.compile(r'\b' + re.escape(key) + r'\b')
        patterns.append((pattern, abbr_map[key]))
    
    count = 0
    
    with open(target_file, 'r', encoding='utf-8') as f_in, \
         open(temp_path, 'w', encoding='utf-8', newline='') as f_out:
        
        reader = csv.reader(f_in, delimiter='\t')
        writer = csv.writer(f_out, delimiter='\t')
        
        try:
            header = next(reader)
        except StopIteration:
            return

        writer.writerow(header)
        
        try:
            pos_idx = header.index("τύπος λέξης")
        except ValueError:
            # Fallback to older name if needed, or just fail
            try:
                 pos_idx = header.index("μέρος του λόγου (part of speech)")
            except ValueError:
                 print(f"Error: Could not find 'τύπος λέξης' or 'μέρος του λόγου (part of speech)' column in {header}")
                 return

        for row in reader:
            if len(row) <= pos_idx:
                writer.writerow(row)
                continue
            
            original_pos_str = row[pos_idx]
            new_pos_str = original_pos_str
            
            # Apply all replacements sequentially
            for pattern, replacement in patterns:
                new_pos_str = pattern.sub(replacement, new_pos_str)
            
            # Special cleanup: ensure "κ.ό.," doesn't become "κ.ό." losing comma if regex ate it?
            # \b matches position, so comma remains.
            
            if new_pos_str != original_pos_str:
                row[pos_idx] = new_pos_str
                count += 1
            
            writer.writerow(row)
            
    shutil.move(str(temp_path), str(target_file))
    print(f"Updated {count} rows with standardized abbreviations.")
    
if __name__ == "__main__":
    base_dir = Path("/Users/woutersoudan/Grieks@CLT")
    concordance_file = base_dir / "PoS-concordance.tsv"
    target_file = base_dir / "CEFR__CLARINEL_KELLY_word-list_Greek.tsv"
    
    mapping = load_abbreviations(concordance_file)
    print(f"Loaded {len(mapping)} abbreviations from concordance.")
    
    standardize_pos_columns(target_file, mapping)
