import re

file_path = "/home/babelai/personal-dev/latex-book/chapters/00_book_plan.tex"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Fix spacing between sections (Parts) - Adding \vspace{0.5cm} or similar
# We look for \end{itemize} followed by \subsection*
content = re.sub(r'(\\end\{itemize\})\s*(\\subsection\*\{제\d부:)', r'\1\n\n\\vspace{0.5cm}\n\2', content)

# 2. Fix spacing between Chapters
# We look for \end{itemize} followed by \textbf{제N장.
content = re.sub(r'(\\end\{itemize\})\s*(\\textbf\{제\d+장\.)', r'\1\n\n\\medskip\n\2', content)

# 3. Completely replace the appendix section to ensure accuracy
new_appendix_section = r"""\section*{4. 부록 구성}

\begin{itemize}
 \item \textbf{부록 A.} 용어 사전 (국문-영문 대조)
 \item \textbf{부록 B.} 참조 법규 및 표준 목록 (국내외)
 \item \textbf{부록 C.} 실무 도구 모음 (전자 파일 다운로드 안내)
 \item \textbf{부록 D.} AI 거버넌스 성숙도 평가 도구 상세 버전
 \item \textbf{부록 E.} 추천 학습 자료 및 커뮤니티
\end{itemize}"""

# Find the appendix section and replace it
# It starts with \section*{4. 부록 구성} and goes to the end of the itemize block
pattern = r'\\section\*\{4\. 부록 구성\}.*?\\end\{itemize\}'
content = re.sub(pattern, new_appendix_section, content, flags=re.DOTALL)

# Cleanup double spacing that might have been created
content = content.replace('\\item\n\n\\item', '\\item')
content = content.replace('\\medskip\n\n\\medskip', '\\medskip')
content = content.replace('\\vspace{0.5cm}\n\n\\vspace{0.5cm}', '\\vspace{0.5cm}')

# One more thing: the user said the spacing is not right in the "strategy/design" part too.
# Let's ensure there are spaces around major headings.
content = content.replace('\\section*', '\n\\section*')
content = content.replace('\\subsection*', '\n\\subsection*')
content = content.replace('\\textbf{제', '\n\\textbf{제')

# Remove triple newlines
content = re.sub(r'\n{3,}', '\n\n', content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully updated 00_book_plan.tex with better spacing and appendix list.")
