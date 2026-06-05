import os
import re

terms_mapping = {
    r'Demographic Parity': '인구통계학적 공정성(DP)',
    r'Equalized Odds': '균등 기회(Equalized Odds)',
    r'Fairness': '공정성',
    r'Risk': '리스크',
    r'Performance': '성능',
    r'Management': '관리',
    r'Lifecycle': '생명주기',
    r'Framework': '프레임워크',
    r'Governance': '거버넌스',
    r'Algorithm': '알고리즘',
    r'Implementation': '구현',
    r'Assessment': '평가',
    r'Drift': '드리프트',
    r'Lineage': '계보',
    r'Requirement': '요구사항',
    r'Validation': '검증',
    r'Evaluation': '평가',
    r'Case Study': '사례 연구',
    r'Operation': '운영',
    r'Lifecycle': '생명주기',
    r'Role': '역할',
    r'Responsibility': '책임',
    r'Policy': '정책',
    r'Standard': '표준',
    r'Procedure': '절차',
    r'Incident': '인시던트',
    r'Monitoring': '모니터링',
    r'Audit': '감사',
    r'Compliance': '컴플라이언스',
    r'Transparency': '투명성',
    r'Accountability': '책임성',
    r'Safety': '안전성',
    r'Reliability': '신뢰성',
    r'Robustness': '강건성',
    r'Explainability': '설명가능성',
    r'XAI': '설명가능한 AI(XAI)',
    r'Integrated': '통합된',
    r'Automation': '자동화',
    r'Architecture': '아키텍처',
    r'Platform': '플랫폼',
    r'Environment': '환경',
    r'Infrastructure': '인프라',
    r'Deployment': '배포',
    r'Release': '릴리스',
    r'Pipeline': '파이프라인',
    r'Registry': '레지스트리',
    r'Catalog': '카탈로그',
    r'Version': '버전',
    r'Metric': '지표',
    r'Dashboard': '대시보드',
    r'Reporting': '보고',
    r'Approval': '승인',
    r'Classification': '분류',
    r'Inventory': '인벤토리',
    r'Maturity': '성숙도',
    r'Roadmap': '로드맵',
    r'Portfolio': '포트폴리오',
    r'Proposal': '제안',
    r'Evaluation': '평가',
    r'Execution': '실행',
    r'Optimization': '최적화',
    r'Strategy': '전략',
    r'Design': '설계',
    r'Tool': '도구',
    r'Checklist': '체크리스트',
    r'Template': '템플릿',
    r'Guide': '가이드',
}

# Fix for checkboxes in tables
# Searching for patterns like \square Y \square N or \square Yes \square No
checkbox_mapping = {
    r'\\square Y \\square N': r'\\checkmark / \\times',
    r'\\square Yes \\square No': r'\\checkmark / \\times',
    r'\\square 정의됨 \\square 미정': r'\\checkmark / \\times',
    r'\\square 운영 중 \\square 미운영': r'\\checkmark / \\times',
    r'\\square 수행 \\square 미수행': r'\\checkmark / \\times',
    r'\\square 수립됨 \\square 미수립': r'\\checkmark / \\times',
    r'\$\\square\$ Y \$\\square\$ N': r'\\checkmark / \\times',
    r'\$\\square\$ Yes \$\\square\$ No': r'\\checkmark / \\times',
    r'Y / N': r'\\checkmark / \\times',
}

def clean_tex_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Mask lstlisting blocks to avoid breaking code
    blocks = []
    def mask(match):
        blocks.append(match.group(0))
        return f"__LSTBLOCK_{len(blocks)-1}__"
    
    content = re.sub(r'\\begin\{lstlisting\}.*?\\end\{lstlisting\}', mask, content, flags=re.DOTALL)

    # Apply term mapping
    for eng, kor in terms_mapping.items():
        # Match standalone English words or English words followed by Korean particles
        pattern = r'\b' + eng + r'\b'
        content = re.sub(pattern, kor, content)

    # Apply checkbox mapping
    for eng, kor in checkbox_mapping.items():
        content = re.sub(eng, kor, content)

    # Unmask lstlisting blocks
    for i, block in enumerate(blocks):
        content = content.replace(f"__LSTBLOCK_{i}__", block)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    chapters_dir = '/home/babelai/personal-dev/latex-book/chapters'
    for filename in os.listdir(chapters_dir):
        if filename.endswith('.tex'):
            print(f"Cleaning {filename}...")
            clean_tex_file(os.path.join(chapters_dir, filename))

if __name__ == "__main__":
    main()
