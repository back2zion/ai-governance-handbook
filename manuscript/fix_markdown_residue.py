import os
import re

def fix_content(content):
    # 1. Bold: **text** -> \textbf{text}
    content = re.sub(r'\*\*((?:[^*]|\*[^*])*?)\*\*', r'\\textbf{\1}', content)
    
    # 2. Section Headers: 
    # ### -> \subsubsection*
    # ## -> \subsection*
    # # -> \section* (Only if it starts at the beginning of a line)
    content = re.sub(r'(?m)^###\s+(.*)$', r'\\subsubsection*{\1}', content)
    content = re.sub(r'(?m)^##\s+(.*)$', r'\\subsection*{\1}', content)
    # We use a negative lookahead to avoid matching # in LaTeX comments or labels
    content = re.sub(r'(?m)^#\s+(?!(?:Requirement|Base|Define|Train|Fit|Or|Predict|Example|inference|Scope|Status|Major|1|2|3|4|5|6|7|8))([^\n]+)$', r'\\section*{\1}', content)

    # 3. Table/List artifacts like "| | |" or "1. ", "- "
    # Often these appear in blocks. Let's handle some common ones.
    # Replace "| Item | Status |" (simple markdown table row) if not in tabular
    # This is tricky, so we only do very obvious ones or just flag them.
    # For now, let's just clean obvious markdown-style list markers if they are at the start of lines
    # and not already in a LaTeX environment. (Wait, let's be careful with lists).
    
    return content

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by environments to avoid corrupting code or tables that are ALREADY LaTeX
    # We ignore lstlisting, tabular, tcolorbox, practicaltool
    pattern = r'(\\begin\{(?:lstlisting|tabular|tabularx|tcolorbox|practicaltool)\}.*?\\end\{(?:lstlisting|tabular|tabularx|tcolorbox|practicaltool)\})'
    parts = re.split(pattern, content, flags=re.DOTALL)
    
    new_parts = []
    for part in parts:
        if part.startswith('\\begin{'):
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
    
    # Process all .tex in chapters/
    for filename in os.listdir(chapters_dir):
        if filename.endswith(".tex"):
            process_file(os.path.join(chapters_dir, filename))
    
    # Process main.tex
    process_file(os.path.join(base_dir, "main.tex"))
