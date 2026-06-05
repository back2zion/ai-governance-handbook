import os
import re

def clean_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Identify and mask lstlisting blocks
    placeholders = []
    def mask_listings(match):
        placeholder = f"__LSTLISTING_PLACEHOLDER_{len(placeholders)}__"
        placeholders.append(match.group(0))
        return placeholder

    # Mask \begin{lstlisting} ... \end{lstlisting}
    # Use re.DOTALL and non-greedy match
    content = re.sub(r'\\begin\{lstlisting\}.*?\\end\{lstlisting\}', mask_listings, content, flags=re.DOTALL)

    # 2. Identify and mask texttt and other inline code commands (optional but safer)
    # content = re.sub(r'\\texttt\{.*?\}', mask_listings, content)

    # 3. Perform replacements on the non-code text
    
    # Remove remaining [Translated] markers
    content = content.replace('[Translated]', '')

    mapping = {
        'Performance': '성능',
        'Definition': '정의',
        'Management': '관리',
        'Assessment': '평가',
        'Institution': '기관',
        'System': '시스템',
        'Alignment': '정렬',
        'Federated': '연합',
        'Validation': '검증',
        'Target': '대상',
        'Priority': '우선순위',
        'Attribute': '속성',
        'Decision': '결정',
        'Integrated': '통합',
        'Compliance': '준수',
        'Reference': '참조',
        'Principle': '원칙',
        'Framework': '프레임워크',
        'Archiv': '아카이브',
        'Project': '프로젝트',
        'Process': '프로세스',
        'Model': '모델',
        'Data': '데이터',
        'Public': '공공',
        'Governance': '거버넌스',
        'Learning': '학습',
        'Audit': '감사',
        'Approval': '승인',
        'Comparison': '비교',
        'Scope': '범위',
        'Case': '사례',
        'Control': '제어',
        'Architecture': '아키텍처',
        'Operational': '운영',
        'Detection': '탐지',
        'Ethics': '윤리',
        'Optimization': '최적화',
        'Design': '설계',
        'Defense': '방어',
        'Classification': '분류',
        'Security': '보안',
        'Level': '수준',
        'Tracking': '추적',
        'Metric': '지표'
    }

    for eng, kor in mapping.items():
        # Pattern 1: KoreanChar + EnglishWord
        content = re.sub(fr'([가-힣]){eng}', fr'\1{kor}', content)
        # Pattern 2: EnglishWord + KoreanChar
        content = re.sub(fr'{eng}([가-힣])', fr'{kor}\1', content)
        # Pattern 3: Standalone in KR context
        content = re.sub(fr'(?<=[가-힣]\s){eng}(?=\s|[\.\,\?\!\:\;\)])', kor, content)
        content = re.sub(fr'(?<=\s){eng}(?=\s[가-힣])', kor, content)
        # Manual replacements for joins without spaces
        content = re.sub(fr'\b{eng}\b(?=[\.\,\?\!\:\;\)])', kor, content)

    # 4. Restore masked blocks
    for i, original in enumerate(placeholders):
        placeholder = f"__LSTLISTING_PLACEHOLDER_{i}__"
        content = content.replace(placeholder, original)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    chapters_dir = 'chapters'
    for filename in os.listdir(chapters_dir):
        if filename.endswith('.tex'):
            clean_file(os.path.join(chapters_dir, filename))
    print("Smarter terminology cleanup completed.")

if __name__ == '__main__':
    main()
