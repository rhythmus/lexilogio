import csv
import shutil
from pathlib import Path

def load_pos_mapping(concordance_path: Path):
    mapping = {}
    with open(concordance_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        # Skip header
        try:
            next(reader)
        except StopIteration:
            pass
            
        for row in reader:
            if len(row) < 16:
                continue
            
            # Columns based on 0-index from analysis
            # el_singular = 13
            # el_plural = 14
            # el_abbr = 15
            
            el_sing = row[13].strip()
            el_plur = row[14].strip()
            el_abbr = row[15].strip()
            
            if not el_abbr:
                continue
                
            # Map valid Greek descriptions to the abbreviation
            if el_sing:
                mapping[el_sing] = el_abbr
                mapping[el_sing.lower()] = el_abbr
            if el_plur:
                mapping[el_plur] = el_abbr
                mapping[el_plur.lower()] = el_abbr
            
            # Map the abbreviation to itself
            mapping[el_abbr] = el_abbr
            
            # Map clean versions
            if el_abbr.endswith('.'):
                mapping[el_abbr[:-1]] = el_abbr
                
    # Manual overrides for robustness or common variations
    # 'v' -> 'ρ.' (In case English slipped in? Actually usually 'ρήμα' is present)
    mapping['ρήμα'] = 'ρ.'
    mapping['επιφώνημα'] = 'επιφ.'
    mapping['ουσιαστικό'] = 'ουσ.'
    mapping['επίθετο'] = 'επίθ.'
    mapping['επίρρημα'] = 'επίρρ.'
    mapping['σύνδεσμος'] = 'σύνδ.'
    mapping['αντωνυμία'] = 'αντων.' # or 'αντων.' matches user?
    # Concordance might have diff abbrs, check later to be sure. 
    # But usually reading the file is safer.
    
    return mapping

def finalize_file(file_path: Path, mapping: dict):
    print(f"Finalizing {file_path.name}...")
    temp_path = file_path.with_suffix('.tmp')
    
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
            lex_idx = header.index("Lexilogio")
            el_sing_idx = header.index("el_singular")
            el_abbr_idx = header.index("el_abbr")
        except ValueError as e:
            print(f"Error: Missing columns in header. {e}")
            return

        cnt = 0
        skipped_first = False
        start_processing = False
        
        for i, row in enumerate(reader):
            # Logic: If row has non-empty Lexilogio (and hasn't been cleared), 
            # it indicates the start of the unedited region.
            # User edits have cleared Lexilogio (mostly).
            # Simplified rows (by previous script) also cleared Lexilogio.
            # Conflicting rows (NOT validly simplified) kept Lexilogio.
            
            # So, if Lexilogio is present, we process.
            # If Lexilogio is empty, we generally skip (assume User or Script handled it).
            # EXCEPT: If we are scanning past the "Start Point", we might want to check?
            # But "Lexilogio empty" implies "Done".
            
            lex_val = row[lex_idx].strip() if len(row) > lex_idx else ""
            
            # Identify if we're in the "unedited" region
            # We treat any row with populated Lexilogio as "Need to finalize".
            
            if not lex_val:
                # Already finalized (by user or previous run)
                writer.writerow(row)
                continue
            
            # Process row
            current_pos = row[pos_idx].strip() if len(row) > pos_idx else ""
            
            # If POS is empty, use el_abbr from Lexilogio-derived columns
            if not current_pos:
                smart_abbr = row[el_abbr_idx].strip() if len(row) > el_abbr_idx else ""
                if smart_abbr:
                    current_pos = smart_abbr
            
            # Abbreviate current_pos
            parts = [p.strip() for p in current_pos.split(',') if p.strip()]
            new_parts = []
            
            for p in parts:
                low_p = p.lower()
                if p in mapping:
                    new_parts.append(mapping[p])
                elif low_p in mapping:
                    new_parts.append(mapping[low_p])
                else:
                    # Keep as is, maybe log warning?
                    new_parts.append(p)
            
            new_pos_str = ", ".join(new_parts)
            
            # Update row
            row[pos_idx] = new_pos_str
            
            # Clear auxiliary columns
            if len(row) > lex_idx: row[lex_idx] = ""
            if len(row) > el_sing_idx: row[el_sing_idx] = ""
            if len(row) > el_abbr_idx: row[el_abbr_idx] = ""
            
            writer.writerow(row)
            cnt += 1
            
    shutil.move(str(temp_path), str(file_path))
    print(f"Processed and finalized {cnt} rows.")

if __name__ == "__main__":
    concordance = Path("/Users/woutersoudan/Grieks@CLT/PoS-concordance.tsv")
    target_file = Path("/Users/woutersoudan/Grieks@CLT/CEFR__CLARINEL_KELLY_word-list_Greek.tsv")
    
    mapping = load_pos_mapping(concordance)
    print(f"Loaded {len(mapping)} mappings.")
    finalize_file(target_file, mapping)
