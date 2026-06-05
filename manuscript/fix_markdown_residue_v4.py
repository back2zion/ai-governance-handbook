import os
import re

def fix_content(content):
    # 1. Bold: **text** -> \textbf{text}
    # This regex is more robust for multi-word and spaced bolding.
    # It excludes cases that are clearly part of code (like **kwargs or arithmetic **)
    # We look for ** followed by non-space, then anything until non-space followed by **.
    content = re.sub(r'\*\*\s*([^* \n][^*]*?[^* \n])\s*\*\*', r'\\textbf{\1}', content)
    content = re.sub(r'\*\*\s*([^* \n]+)\s*\*\*', r'\\textbf{\1}', content)
    
    # 2. Section Headers: 
    # Match lines starting with #, ##, ### (ignoring indentation)
    # We intentionally include headers inside what looks like python strings but are actually part of the text.
    content = re.sub(r'(?m)^\s*###\s+(.*)$', r'\\subsubsection*{\1}', content)
    content = re.sub(r'(?m)^\s*##\s+(.*)$', r'\\subsection*{\1}', content)
    # Be more aggressive with #, but keep common python/config comments.
    content = re.sub(r'(?m)^\s*#\s+(?!(?:Requirement|Base|Define|Train|Fit|Or|Predict|Example|inference|Scope|Status|Major|1|2|3|4|5|6|7|8|pip|python|import|from))([^\n]+)$', r'\\section*{\1}', content)

    # 3. Table fragments (not in environment)
    # Lines like "| Item | Value |"
    content = re.sub(r'(?m)^\s*\|.*\|.*\|.*$', '', content)
    # Strip alone markers like "|---|---|---|"
    content = re.sub(r'(?m)^\s*\|[-:\|]+\|\s*$', '', content)

    return content

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Process everything except legitimate lstlisting environments.
    # If the user has pseudo-code that isn't in a block, we fix it.
    pattern = r'(\\begin\{lstlisting\}.*?\\end\{lstlisting\})'
    parts = re.split(pattern, content, flags=re.DOTALL)
    
    new_parts = []
    for part in parts:
        if part.startswith('\\begin{lstlisting}'):
            # Even inside lstlisting, some things might be unintended MD.
            # But let's stay safe and NOT touch lstlisting for now.
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
    chapters_dir = os.path.join(base_dir, "chapters")
    
    for filename in os.listdir(chapters_dir):
        if filename.endswith(".tex"):
            process_file(os.path.join(chapters_dir, filename))
    
    process_file(os.path.join(base_dir, "main.tex"))
