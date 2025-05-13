import sys
import re

def greek_to_dutch_phonetic(text):
    # Mapping for single Greek letters
    mapping = {
        'α': 'a', 'β': 'v', 'γ': 'g', 'δ': 'd', 'ε': 'e', 'ζ': 'z', 'η': 'i',
        'θ': 'th', 'ι': 'i', 'κ': 'k', 'λ': 'l', 'μ': 'm', 'ν': 'n', 'ξ': 'ks',
        'ο': 'o', 'π': 'p', 'ρ': 'r', 'σ': 's', 'ς': 's', 'τ': 't', 'υ': 'i',
        'φ': 'f', 'χ': 'ch', 'ψ': 'ps', 'ω': 'o',
        'Α': 'A', 'Β': 'V', 'Γ': 'G', 'Δ': 'D', 'Ε': 'E', 'Ζ': 'Z', 'Η': 'I',
        'Θ': 'Th', 'Ι': 'I', 'Κ': 'K', 'Λ': 'L', 'Μ': 'M', 'Ν': 'N', 'Ξ': 'Ks',
        'Ο': 'O', 'Π': 'P', 'Ρ': 'R', 'Σ': 'S', 'Τ': 'T', 'Υ': 'I',
        'Φ': 'F', 'Χ': 'Ch', 'Ψ': 'Ps', 'Ω': 'O',
    }
    # Diphthongs and special cases (order matters)
    specials = [
        (r'αι', 'è'), (r'Αι', 'È'),
        (r'ει', 'i'), (r'Ει', 'I'),
        (r'οι', 'i'), (r'Οι', 'I'),
        (r'υι', 'i'), (r'Υι', 'I'),
        (r'ου', 'oe'), (r'Ου', 'Oe'),
        (r'ευ([θκξπστφχψ])', r'ef\1'), (r'ευ', 'ev'),
        (r'αυ([θκξπστφχψ])', r'af\1'), (r'αυ', 'av'),
        (r'ηυ([θκξπστφχψ])', r'if\1'), (r'ηυ', 'iv'),
        (r'γγ', 'ng'), (r'γκ', 'gk'), (r'Γκ', 'Gk'),
        (r'ντ', 'nd'), (r'Ντ', 'Nd'),
        (r'μπ', 'mb'), (r'Μπ', 'Mb'),
        (r'τσ', 'ts'), (r'Τσ', 'Ts'),
        (r'τζ', 'dz'), (r'Τζ', 'Dz'),
    ]
    # Handle specials first
    for pat, repl in specials:
        text = re.sub(pat, repl, text)
    # Handle gamma before front vowels (γι, γε, γη, γυ, γι, γει, γοι, γυι)
    text = re.sub(r'γ([εηιυαιειοιυι])', r'j\1', text)
    text = re.sub(r'Γ([εηιυαιειοιυι])', r'J\1', text)
    # Now map single letters
    result = ''
    for c in text:
        result += mapping.get(c, c)
    return result

def main():
    if len(sys.argv) > 1:
        greek = ' '.join(sys.argv[1:])
    else:
        greek = input('Geef Griekse tekst: ')
    print('/' + greek_to_dutch_phonetic(greek) + '/')

if __name__ == '__main__':
    main() 