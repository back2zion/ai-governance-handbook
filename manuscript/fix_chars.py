import os
import re

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Global character replacements for symbols that confuse pdflatex/listings
    replacements = {
        '→': '->',
        '≥': '>=',
        '≤': '<=',
        '×': 'x',
        '÷': '/',
        '…': '...',
        '·': '.',
        '『': '"',
        '』': '"',
        '「': "'",
        '」': "'",
        '’': "'",
        '‘': "'",
        '”': '"',
        '“': '"',
        '✅': '[OK]',
        '⚠': '[WARN]',
        '❌': '[FAIL]',
        'ℹ': '[INFO]',
        '📍': '[LOC]',
        '🔍': '[SEARCH]',
        '🛡': '[PROTECT]',
        '🚀': '[LAUNCH]',
        '📊': '[CHART]',
        '📋': '[CLI]',
        '✅': '[PASS]',
        '❌': '[FAIL]'
    }
    
    for old, new in replacements.items():
        content = content.replace(old, new)
    
    # Final cleanup of common small words or patterns if any
    content = re.sub(r'(\[Translated\]\s*){2,}', '[Translated] ', content)

    # Broad approach: strip everything that is NOT ASCII and NOT Korean
    # Korean range: [\uAC00-\uD7AF\u1100-\u11FF\u3130-\u318F]
    # ASCII range: [\x00-\x7f]
    # We remove everything else.
    content = re.sub(r'[^\x00-\x7f\uAC00-\uD7AF\u1100-\u11FF\u3130-\u318F]', '', content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    chapters_dir = 'chapters'
    for filename in os.listdir(chapters_dir):
        if filename.endswith('.tex'):
            fix_file(os.path.join(chapters_dir, filename))
    print("Fixed non-ASCII and non-Korean characters in all chapters.")

if __name__ == '__main__':
    main()
