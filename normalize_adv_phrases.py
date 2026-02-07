import csv
import shutil
from pathlib import Path

def normalize_adverbial_phrases(file_path: Path):
    print(f"Normalizing Adverbial Phrases in {file_path.name}...")
    temp_path = file_path.with_suffix('.tmp')
    
    replacements = {
        "έκφρ., επίρρ.": "επιρρηματική φράση",
        "έκφρ., επίρρημα": "επιρρηματική φράση", # Cover variations
        "έκφραση, επίρρημα": "επιρρηματική φράση",
        "έκφραση, επίρρ.": "επιρρηματική φράση"
    }

    count = 0
    with open(file_path, 'r', encoding='utf-8') as f_in, \
         open(temp_path, 'w', encoding='utf-8', newline='') as f_out:
        
        reader = csv.reader(f_in, delimiter='\t')
        writer = csv.writer(f_out, delimiter='\t')
        
        try:
            header = next(reader)
        except StopIteration:
            return
            
        writer.writerow(header)
        
        try:
            pos_idx = header.index("μέρος του λόγου (part of speech)")
        except ValueError:
            print("Error: Could not find 'μέρος του λόγου (part of speech)' column.")
            return

        for row in reader:
            if len(row) <= pos_idx:
                writer.writerow(row)
                continue
                
            original_pos = row[pos_idx].strip()
            
            # Direct replacement for exact matches
            if original_pos in replacements:
                row[pos_idx] = replacements[original_pos]
                count += 1
            else:
                # Check for "starts with" or "contains" careful logic
                # User pattern: "έκφρ., επίρρ., κ.ό." -> "επιρρηματική φράση, κ.ό."
                # We can do a string replace of the KEY part.
                
                # Normalize spaces for check
                norm_pos = original_pos.replace(", ", ",")
                
                replaced = False
                for key, val in replacements.items():
                    # Simple string replace for the phrase "έκφρ., επίρρ."
                    if key in original_pos:
                        row[pos_idx] = original_pos.replace(key, val)
                        replaced = True
                        break # Only one replacement type per cell usually
                
                if replaced:
                    count += 1
            
            writer.writerow(row)
            
    shutil.move(str(temp_path), str(file_path))
    print(f"Updated {count} rows with Adverbial Phrase normalization.")

if __name__ == "__main__":
    target_file = Path("/Users/woutersoudan/Grieks@CLT/CEFR__CLARINEL_KELLY_word-list_Greek.tsv")
    normalize_adverbial_phrases(target_file)
