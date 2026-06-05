import os
import re

def translate_remaining(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    trans_map = {
        '각 뉴런의 범위': 'range of each neuron',
        '각 뉴런의 Scope': 'scope of each neuron',
        '패턴 및 구조 분석 기반 인젝션': 'injection based on pattern and structure analysis',
        '가중 평균 기반 로컬 모델 집계': 'weighted average based local model aggregation',
        '가중 평균 기반 로컬 Model 집계': 'weighted average based local model aggregation',
        '사용자 속성, 자산 민감도, 환경 맥락을 결합한 접근 제어': 'access control combining user attributes, asset sensitivity, and context',
        '사용자 Attribute, 자산 민감도, 환경 맥락을 결합한 접근 Control': 'access control combining user attributes, asset sensitivity, and context',
        '범위': 'range',
        '기반': 'based on',
        '탐지': 'Detection',
        '분석': 'analysis',
        '패턴': 'Pattern',
        '구축': 'Implementation',
        '속성': 'Attribute',
        '민감도': 'Sensitivity',
        '맥락': 'Context',
        '결합': 'combin',
        '접근': 'Access',
        '제어': 'Control',
        '가중': 'Weight',
        '평균': 'Average',
        '집계': 'Aggregation',
        '로컬': 'Local',
        '사용자': 'User',
        '인젝션': 'Injection',
        '보안': 'Security',
        '정책': 'Policy',
        '위반': 'Violation',
        '필터링': 'Filtering',
        '통합': 'Integrated',
        '파이프라인': 'Pipeline',
        '전처리': 'Preprocessing',
        '후처리': 'Post-processing'
    }

    def translate_match(match):
        listing_content = match.group(0)
        # Sort keys by length descending to replace longest phrases first
        for kor in sorted(trans_map.keys(), key=len, reverse=True):
            listing_content = listing_content.replace(kor, trans_map[kor])
        
        # Final safety: strip any remaining Korean char from code block
        listing_content = re.sub(r'[가-힣]', '', listing_content)
        return listing_content

    content = re.sub(r'\\begin\{lstlisting\}.*?\\end\{lstlisting\}', translate_match, content, flags=re.DOTALL)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    chapters_dir = 'chapters'
    for filename in os.listdir(chapters_dir):
        if filename.endswith('.tex'):
            translate_remaining(os.path.join(chapters_dir, filename))
    print("Final code block translation completed.")

if __name__ == '__main__':
    main()
