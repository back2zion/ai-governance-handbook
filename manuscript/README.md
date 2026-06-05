# AI Governance Practical Guide (AI 거버넌스 실무 지침서)

이 저장소는 **"AI 거버넌스 실무 지침서: 이론과 실무의 가교"** 도서의 소스 코드와 실무 도구들을 포함하고 있습니다.

## 프로젝트 구조

- `chapters/`: 도서의 각 장별 LaTeX 소스 파일
- `src/`: 도서에 소개된 AI 거버넌스 실무용 파이썬 클래스 및 도구
- `figures/`: 도서에 포함된 이미지 및 다이어그램
- `main.tex`: 전체 도서 컴파일을 위한 메인 LaTeX 파일

## 주요 실무 도구 (src/)

본 저장소의 `src/` 폴더에는 다음과 같은 핵심 도구들이 포함되어 있습니다:

1. **Future Governance Tools (`future_governance_tools.py`)**: 
   - `AGIGovernanceReadinessEvaluator`: AGI 정렬 및 감독 준비도 평가
   - `NeuroSymbolicGovernanceManager`: 신경망 판단에 논리 규칙(법령 등) 강제 적용
   - `AIESGGovernance`: AI의 환경/사회적 영향도 리포팅

## 설치 및 사용법

파이썬 실무 도구를 실행하려면 Python 3.8+ 환경이 필요합니다.

```bash
# 의존성 설치 (필요시)
pip install -r requirements.txt
```

## 도서 컴파일 방법

LaTeX 환경(TeXLive 등)에서 `main.tex`를 컴파일하십시오.

```bash
pdflatex main.tex
biber main
pdflatex main.tex
```

## 저자 및 라이선스

- **Copyright**: 2026 DataStreams & Author
- **License**: MIT License (for source code)
