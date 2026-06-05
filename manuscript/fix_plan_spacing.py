import re

file_path = "/home/babelai/personal-dev/latex-book/chapters/00_book_plan.tex"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Fix spacing between subsections (Parts)
content = re.sub(r'(\\begin\{itemize\}.*?\\end\{itemize\})\s*(\\subsection\*\{제\d부:)', r'\1\n\n\\vspace{0.5cm}\n\2', content, flags=re.DOTALL)

# 2. Fix spacing between Chapters
content = re.sub(r'(\\begin\{itemize\}.*?\\end\{itemize\})\s*(\\textbf\{제\d+장\.)', r'\1\n\n\\medskip\n\2', content, flags=re.DOTALL)

# 3. Fix the specific cluster in Section 3 (Appendices)
# The user mentioned "안내 부록 D" or similar. Let's find the appendix list.
appendix_section = r'\\section\*\{4\. 부록 구성\}.*?\\end\{itemize\}'
new_appendix_list = r"""\section*{4. 부록 구성}

\begin{itemize}
 \item \textbf{부록 A.} 용어 사전 (국문-영문 대조)
 \item \textbf{부록 B.} 참조 법규 및 표준 목록 (국내외)
 \item \textbf{부록 C.} 실무 도구 모음 (전자 파일 다운로드 안내)
 \item \textbf{부록 D.} AI 거버넌스 성숙도 평가 도구 상세 버전
 \item \textbf{부록 E.} 추천 학습 자료 및 커뮤니티
\end{itemize}"""

content = re.sub(appendix_section, new_appendix_list, content, flags=re.DOTALL)

# 4. Clean up any double vspaces or medskips
content = content.replace('\\medskip\n\n\\medskip', '\\medskip')
content = content.replace('\\vspace{0.5cm}\n\n\\vspace{0.5cm}', '\\vspace{0.5cm}')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully updated 00_book_plan.tex")
