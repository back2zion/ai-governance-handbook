import os
import re

def fix_content(content):
    # 1. Bold: **text** -> \textbf{text}
    # Handling cases like **text** or ** text ** or **text **
    content = re.sub(r'\*\*\s*([^* \n][^*]*?[^* \n])\s*\*\*', r'\\textbf{\1}', content)
    # Single word bold: **word**
    content = re.sub(r'\*\*\s*([^* \n]+)\s*\*\*', r'\\textbf{\1}', content)
    
    # 2. Section Headers: 
    # ### -> \subsubsection*
    # ## -> \subsection*
    # # -> \section*
    content = re.sub(r'(?m)^###\s+(.*)$', r'\\subsubsection*{\1}', content)
    content = re.sub(r'(?m)^##\s+(.*)$', r'\\subsection*{\1}', content)
    # Special handle for # headers that are not code or comments
    # If a line starts with '#' followed by space, and it's not a common python comment header
    content = re.sub(r'(?m)^#\s+(?!(?:Requirement|Base|Define|Train|Fit|Or|Predict|Example|inference|Scope|Status|Major|1|2|3|4|5|6|7|8))([^\n]+)$', r'\\section*{\1}', content)

    # 3. Table artifacts: | | |
    # If a line contains | | | and is not in a tabular environment
    content = re.sub(r'(?m)^.*\|.*\|.*\|.*$', lambda m: m.group(0) if '\\begin{tabular}' in content else '', content)
    # Actually, a safer way for tables is to replace individual "|" with space or just remove them if they look like MD artifacts
    
    return content

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by environments to avoid corrupting code or tables that are ALREADY LaTeX
    pattern = r'(\\begin\{(?:lstlisting|tabular|tabularx|tcolorbox|practicaltool|enumerate|itemize)\}.*?\\end\{(?:lstlisting|tabular|tabularx|tcolorbox|practicaltool|enumerate|itemize)\})'
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
    
    for filename in os.listdir(chapters_dir):
        if filename.endswith(".tex"):
            process_file(os.path.join(chapters_dir, filename))
    
    process_file(os.path.join(base_dir, "main.tex"))
