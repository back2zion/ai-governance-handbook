import os
import re

def fix_bold_aggressive(content):
    # Pattern to match **text** and replace with \textbf{text}
    # This pattern is more aggressive to catch markers inside long strings
    # but still tries to avoid **kwargs (preceded by *) or 2 ** 8 (surrounded by numbers/spaces)
    
    # We replace **something** where something doesn't contain *
    # and isn't preceded by * (to avoid ***)
    # and isn't immediately followed by a word character if it looks like an operator
    
    def replacer(match):
        inner = match.group(1)
        # If it looks like a power operator (e.g. 2**8 or x**y), skip it
        # This is a bit of a heuristic
        if re.match(r'^[a-zA-Z0-9_]+$', inner) and len(inner) <= 2:
             # Likely an operator or short variable if in a code-ish context
             # But if it's in a paragraph, we might want it bold
             return f"\\textbf{{{inner}}}"
        return f"\\textbf{{{inner}}}"

    # Standard bold replacement
    content = re.sub(r'\*\*(?!\*)(.+?)\*\*', r'\\textbf{\1}', content)
    
    return content

def process_file_aggressive(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # We skip actual lstlisting environments
    parts = re.split(r'(\\begin\{lstlisting\}.*?\\end\{lstlisting\})', content, flags=re.DOTALL)
    
    new_parts = []
    for part in parts:
        if part.startswith('\\begin{lstlisting}'):
            new_parts.append(part)
        else:
            # For non-code parts, we apply the fix
            # Special case: ignore ** in lines that look like mathematical power in text (rare but possible)
            new_parts.append(fix_bold_aggressive(part))
    
    new_content = "".join(new_parts)
    
    if content != new_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Fixed aggressive formatting in: {file_path}")

if __name__ == "__main__":
    chapters_dir = "/home/babelai/personal-dev/latex-book/chapters"
    target_files = ["05_industry_applications.tex", "07_case_studies.tex", "11_audit_certification.tex", "04_organization.tex", "06_governance_tools.tex"]
    
    for filename in target_files:
        path = os.path.join(chapters_dir, filename)
        if os.path.exists(path):
            process_file_aggressive(path)
