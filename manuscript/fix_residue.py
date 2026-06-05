import os
import re

def fix_latex_residue(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # We want to catch **Text** and replace with Text or \textbf{Text}
    # Since these are inside strings, usually plain text is safer to avoid LaTeX command interpretation
    # inside a string which might be rendered literally in lstlisting
    
    # Pattern: ** something ** or **something**
    # We use a lazy match to avoid matching across lines
    new_content = re.sub(r'\*\*\s*([^*]+?)\s*\*\*', r'\1', content)
    
    if content != new_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Fixed residue in: {file_path}")

if __name__ == "__main__":
    chapters_dir = "/home/babelai/personal-dev/latex-book/chapters"
    for filename in os.listdir(chapters_dir):
        if filename.endswith(".tex"):
            fix_latex_residue(os.path.join(chapters_dir, filename))
