#!/usr/bin/env python3
"""Fix citations in section headings by wrapping them with \\texorpdfstring."""
import re, os, glob

def fix_section_cites(text):
    """Find section/subsection/subsubsection commands with \\cite in them,
    and wrap the \\cite with \\texorpdfstring."""

    def replace_cite_in_heading(match):
        full = match.group(0)
        # Only process if there's a \cite inside
        if r'\cite{' not in full:
            return full
        # Replace \cite{...} with \texorpdfstring{\cite{...}}{}
        result = re.sub(
            r'\\cite\{([^}]+)\}',
            r'\\texorpdfstring{\\cite{\1}}{}',
            full
        )
        return result

    # Match \section{...}, \subsection{...}, \subsubsection{...}
    # Need to handle nested braces carefully
    pattern = r'\\(?:sub)*section\{[^}]*\\cite\{[^}]+\}[^}]*\}'
    text = re.sub(pattern, replace_cite_in_heading, text)
    return text

changed = 0
for filepath in sorted(glob.glob("chapters/*.tex")):
    with open(filepath, 'r', encoding='utf-8') as f:
        original = f.read()
    modified = fix_section_cites(original)
    if modified != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(modified)
        # Count changes
        n = modified.count(r'\texorpdfstring{\cite') - original.count(r'\texorpdfstring{\cite')
        print(f"{os.path.basename(filepath)}: {n} citations wrapped")
        changed += 1

print(f"\nDone: {changed} files modified")
