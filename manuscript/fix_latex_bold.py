import os
import re

def fix_bold(content):
    # Regex to find **text** and replace with \textbf{text}
    # We use a non-greedy match [^*]+ and ensure it's balanced
    # We also attempt to ignore common false positives like **kwargs or 2 ** 8
    
    # Pattern 1: **text** (Standard Markdown bold)
    content = re.sub(r'\*\*([^* \n][^*]*?[^* \n])\*\*', r'\\textbf{\1}', content)
    
    # Pattern 2: ** text ** (Slightly loose Markdown bold)
    content = re.sub(r'\*\*\s+([^* \n][^*]*?[^* \n])\s+\*\*', r'\\textbf{\1}', content)

    # Note: This might still catch 2 ** 8 if not careful, but usually math is in $...$
    # and code is in \begin{lstlisting}
    return content

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by code blocks to avoid corruption
    # This is a bit naive but works for simple cases
    parts = re.split(r'(\\begin\{lstlisting\}.*?\\end\{lstlisting\})', content, flags=re.DOTALL)
    
    new_parts = []
    for part in parts:
        if part.startswith('\\begin{lstlisting}'):
            new_parts.append(part)
        else:
            new_parts.append(fix_bold(part))
    
    new_content = "".join(new_parts)
    
    if content != new_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Fixed formatting in: {file_path}")

if __name__ == "__main__":
    chapters_dir = "/home/babelai/personal-dev/latex-book/chapters"
    for filename in os.listdir(chapters_dir):
        if filename.endswith(".tex"):
            process_file(os.path.join(chapters_dir, filename))
    
    # Also process main.tex
    process_file("/home/babelai/personal-dev/latex-book/main.tex")
