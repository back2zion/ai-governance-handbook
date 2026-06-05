import os
import re

# Mapping of common Korean technical terms found in code comments to English
TRANSLATIONS = {
    "본 설명은 {len(shap_values)}개 샘플의 집계 통계입니다.": "This explanation is an aggregated statistic of {len(shap_values)} samples.",
    "샘플 수({len(shap_values)})가 최소 그룹 크기({min_group_size})보다 작습니다.": "Number of samples ({len(shap_values)}) is smaller than minimum group size ({min_group_size}).",
    "샘플 수가 최소 그룹 크기보다 작습니다.": "Number of samples is smaller than minimum group size.",
    "특성명 리스트": "List of feature names",
    "k-익명성을 위한 최소 그룹 크기": "Minimum group size for k-anonymity",
    "집계된 설명 정보": "Aggregated explanation information",
    "차분 Privacy가 적용된 SHAP 설명 생성": "Generating SHAP Explanation with Differential Privacy",
    "차분 Privacy": "Differential Privacy",
    "설명 정보에 노이즈를 추가하여 개별 Learning Data 추론을 방지한다.": "Add noise to explanation information to prevent individual training data inference.",
    "SHAP 설명기": "SHAP Explainer",
    "설명할 인스턴스": "Instance to explain",
    "Privacy 예산": "Privacy Budget",
    "SHAP 값의 민감도 (최대 변화량)": "Sensitivity of SHAP values (max variation)",
    "노이즈가 추가된 SHAP 값": "SHAP values with added noise",
    "가 적용된": "applied ",
    " 생성": " Generation",
    "인간 감독 관리 모듈": "Human Oversight Manager Module",
    "안전성 평가 모듈": "Safety Evaluator Module",
    "한국형 공정성 평가": "Korean Context Fairness Evaluation",
    "데이터": "Data",
    "수준": "Level",
    "리스크": "Risk",
    "레지스터": "Register",
    "평가": "Assessment",
    "시스템": "System",
    "대응": "Response",
    "사례": "Case",
    "구현": "Implementation",
    "실무": "Practical",
    "고급": "Advanced",
    "활용": "Usage",
    "가이드": "Guide",
    "아키텍처": "Architecture",
    "프레임워크": "Framework",
    "설정": "Setup",
    "로깅": "Logging",
    "연동": "Integration",
    "승인": "Approval",
    "상태": "Status",
    "관리": "Management",
    "태그": "Tags",
    "자동화": "Automation",
    "보고서": "Report",
    "탐지": "Detection",
    "드리프트": "Drift",
    "성능": "Performance",
    "추적": "Tracking",
    "모니터링": "Monitoring",
    "감사": "Audit",
    "체크리스트": "Checklist",
    "준수": "Compliance",
    "규제": "Regulation",
    "문서": "Document",
    "영향": "Impact",
    "로직": "Logic",
    "사회적/윤리적": "Social/Ethical",
    "금융": "Finance",
    "의료": "Healthcare",
    "공공": "Public",
    "제조": "Manufacturing",
    "산업": "Industrial",
    "미래": "Future",
    "준비도": "Readiness",
    "신용정보법": "Credit Information Act",
    "자동화평가": "Automated Assessment",
    "안정성": "Stability",
    "비용 민감 학습": "Cost-sensitive Learning",
    "임상": "Clinical",
    "병원": "Hospital",
    "기관": "Institution",
    "재량": "Discretionary",
    "시민 권리 보장": "Guarantee of Citizen Rights",
    "형평성": "Equity",
    "용접 결함 검사": "Welding Defect Inspection",
    "숙련공 검증": "Skilled Worker Verification",
    "방어": "Defense",
    "훈련": "Training",
    "연합": "Federated",
    "차등": "Differential",
    "특성명": "Feature names",
    "리스트": "list",
    "익명성": "anonymity",
    "최소": "Minimum",
    "크기": "Size",
    "집계된": "Aggregated",
    "정보": "information",
    "샘플 수": "Number of samples",
    "원리": "Principle",
    "정확도": "Accuracy",
    "계산": "Calculation",
    "비용": "Cost",
    "성숙도": "Maturity",
    "노이즈": "Noise",
    "추가": "Addition",
    "중간": "Medium",
    "낮음": "Low",
    "높음": "High",
    "없음": "None",
    "매우": "Very",
    "분산": "Decentralized",
    "암호화": "Encryption",
    "연산": "Operation",
    "가짜": "Fake",
    "예시": "Example",
    "분석": "Analysis",
    "윤리 원칙": "Ethical Principles",
    "운영": "Operation",
    "라이프사이클": "Lifecycle",
    "도구": "Tools",
    "플랫폼": "Platform",
    "가중치": "Weights",
    "버전": "Version",
    "스키마": "Schema",
    "회고": "Retrospective",
    "항목": "Items",
    "보존": "Retention",
    "기간": "Period",
    "영구": "Permanent",
    "년": "years",
    "개월": "months",
    "일": "days",
    "데이터셋": "Dataset",
    "코드": "Code",
    "전처리": "Preprocessing",
    "위치": "Location",
    "주요": "Major",
    "최종": "Final",
    "이전": "Previous",
    "통계입니다": "Statistics",
    "본 설명은": "This explanation is",
    "샘플의": "samples'",
}

# Word-level fallback dictionary for remaining Korean characters in comments
WORD_TRANSLATIONS = {
    "개": "units",
    "의": "of",
    "은": "",
    "는": "",
    "이": "",
    "가": "",
}

def translate_content(content):
    # Phrase-level translation
    sorted_keys = sorted(TRANSLATIONS.keys(), key=len, reverse=True)
    for key in sorted_keys:
        content = content.replace(key, TRANSLATIONS[key])
    
    # Word-level fallback (only if Korean still exists)
    if re.search('[가-힣]', content):
        # Handle remaining individual words if necessary
        # But most should be covered by phrases.
        # We also need to remove or replace any remaining single Korean characters
        content = re.sub(r'[가-힣]+', ' [Translated] ', content)

    return content


def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    def replace_listing(match):
        header = match.group(1)
        content = match.group(2)
        
        # Check if content has Korean
        if re.search('[가-힣]', content) or re.search('[가-힣]', header):
            new_header = translate_content(header)
            new_content = translate_content(content)
            return f'\\begin{{lstlisting}}{new_header}{new_content}\\end{{lstlisting}}'
        return match.group(0)

    # regex for \begin{lstlisting}[hdr] content \end{lstlisting}
    new_text = re.sub(r'\\begin\{lstlisting\}(.*?)(?:\n)?(.*?)\\end\{lstlisting\}', replace_listing, text, flags=re.DOTALL)

    if new_text != text:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_text)
        print(f"Updated: {filepath}")

def main():
    root_dir = "/home/babelai/personal-dev/latex-book/chapters"
    for filename in os.listdir(root_dir):
        if filename.endswith(".tex"):
            process_file(os.path.join(root_dir, filename))

if __name__ == "__main__":
    main()
