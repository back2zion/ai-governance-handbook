import os
import re

def fix_content(content):
    # 1. Bold: **text** -> \textbf{text}
    # More aggressive bold matching (handles spaces, multiple words)
    content = re.sub(r'\*\*\s*(.+?)\s*\*\*', r'\\textbf{\1}', content)
    
    # 2. Section Headers: 
    # ### -> \subsubsection*
    # ## -> \subsection*
    # # -> \section*
    # Removing headers even if they are inside string literals if they look like MD artifacts
    content = re.sub(r'(?m)^###\s+(.*)$', r'\\subsubsection*{\1}', content)
    content = re.sub(r'(?m)^##\s+(.*)$', r'\\subsection*{\1}', content)
    # Target headers like "# AI Governance Audit Plan" even if they are in a python-like report block
    content = re.sub(r'(?m)^#\s+(?!(?:Requirement|Base|Define|Train|Fit|Or|Predict|Example|inference|Scope|Status|Major|1|2|3|4|5|6|7|8))([^\n]+)$', r'\\section*{\1}', content)

    return content

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # For these problematic files, we will be more selective about what we skip.
    # We will ONLY skip actual lstlisting environments, not general python-like code fragments
    pattern = r'(\\begin\{lstlisting\}.*?\\end\{lstlisting\})'
    parts = re.split(pattern, content, flags=re.DOTALL)
    
    new_parts = []
    for part in parts:
        if part.startswith('\\begin{lstlisting}'):
            new_parts.append(part)
        else:
            new_parts.append(fix_content(part))
    
    new_content = "".join(new_parts)
    
    if content != new_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Fixed residue in: {file_path}")
    else:
        print(f"No residue found in: {file_path}")

if __name__ == "__main__":
    base_dir = "/home/babelai/personal-dev/latex-book"
    # Target only problematic files
    targets = [
        "chapters/05_industry_applications.tex",
        "chapters/11_audit_certification.tex",
        "chapters/06_governance_tools.tex",
        "chapters/07_case_studies.tex",
        "chapters/04_organization.tex"
    ]
    
    for rel_path in targets:
        process_file(os.path.join(base_dir, rel_path))
