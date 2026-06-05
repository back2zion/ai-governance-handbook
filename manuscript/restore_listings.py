import os
import re

def restore_listings(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    mapping_rev = {
        '모델': 'Model',
        '데이터': 'Data',
        '학습': 'Learning',
        '시스템': 'System',
        '거버넌스': 'Governance',
        '프레임워크': 'Framework',
        '관리': 'Management',
        '평가': 'Assessment',
        '검증': 'Validation',
        '원칙': 'Principle',
        '성능': 'Performance',
        '탐지': 'Detection',
        '설계': 'Design',
        '방어': 'Defense',
        '분류': 'Classification',
        '보안': 'Security',
        '결정': 'Decision',
        '속성': 'Attribute',
        '정의': 'Definition',
        '기관': 'Institution',
        '정렬': 'Alignment',
        '연합': 'Federated',
        '대상': 'Target',
        '우선순위': 'Priority',
        '통합': 'Integrated',
        '준수': 'Compliance',
        '참조': 'Reference',
        '아카이브': 'Archiv',
        '프로젝트': 'Project',
        '프로세스': 'Process',
        '공공': 'Public',
        '감사': 'Audit',
        '승인': 'Approval',
        '비교': 'Comparison',
        '범위': 'Scope',
        '사례': 'Case',
        '제어': 'Control',
        '아키텍처': 'Architecture',
        '운영': 'Operational',
        '윤리': 'Ethics',
        '최적화': 'Optimization',
        '수준': 'Level',
        '추적': 'Tracking',
        '지표': 'Metric'
    }

    def fix_match(match):
        listing_content = match.group(0)
        for kor, eng in mapping_rev.items():
            # Be careful not to replace legitimate Korean in comments if they exist
            # but currently we expect pure English in code blocks (except strings we translated)
            # Actually, the user wants English in code blocks.
            listing_content = listing_content.replace(kor, eng)
        return listing_content

    # Target only lstlisting blocks
    content = re.sub(r'\\begin\{lstlisting\}.*?\\end\{lstlisting\}', fix_match, content, flags=re.DOTALL)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    chapters_dir = 'chapters'
    for filename in os.listdir(chapters_dir):
        if filename.endswith('.tex'):
            restore_listings(os.path.join(chapters_dir, filename))
    print("Restored technical terms in lstlisting blocks.")

if __name__ == '__main__':
    main()
