# AI Governance Handbook

**The executable standard for AI Governance.**

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/back2zion/ai-governance-handbook/blob/main/notebooks/ch10.ipynb)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

> *"거버넌스가 없는 AI는 브레이크 없는 자동차다. 이 저장소는 그 브레이크의 설계도다."*

---

## The Problem We Solve

- **규제 준수 지옥**: AI 기본법(한국), EU AI Act, NIST AI RMF — 중첩되는 규제들을 어떻게 동시에 만족시키는가? 이 저장소는 각 규제 조항을 실행 가능한 코드로 직접 매핑합니다.
- **모델 신뢰성 붕괴**: 프로덕션 AI 시스템의 80% 이상이 드리프트, 편향, 환각 문제를 사후에야 발견합니다. 우리는 사전 탐지 파이프라인을 코드로 제공합니다.
- **AI 공급망 보안 공백**: 오픈소스 모델, 서드파티 API, 데이터 파이프라인의 보안 취약점은 단일 조직이 감당할 수 없습니다. 이 저장소는 공급망 전반의 거버넌스 컴포넌트를 제공합니다.

---

## What This Is

단순한 예제 코드가 아닙니다. 이 저장소는:

- **즉시 프로덕션에 적용 가능한 AI 거버넌스 컴포넌트** — 복사-붙여넣기가 아닌 `pip install`로 시작하는 실무 라이브러리
- **AI 기본법(한국), EU AI Act, NIST AI RMF를 실코드로 구현한 유일한 오픈소스** — 법령 조항과 코드 모듈의 1:1 매핑
- **22개 챕터, 129개 실행 가능 코드블록, `core/` 재사용 라이브러리** — 처음부터 끝까지 일관된 거버넌스 아키텍처

---

## Quick Start

### Option 1: Google Colab (클릭 한 번)

아래 챕터 테이블에서 원하는 주제의 Colab 배지를 클릭하면 즉시 실행됩니다. 별도 설치 불필요.

### Option 2: DevContainer (완전 통제 환경)

```bash
# VS Code에서
git clone https://github.com/back2zion/ai-governance-handbook
code ai-governance-handbook
# "Reopen in Container" 클릭
```

DevContainer는 Python 3.10, 모든 의존성, Jupyter 서버를 자동으로 구성합니다.

### Option 3: 로컬 설치

```bash
git clone https://github.com/back2zion/ai-governance-handbook
cd ai-governance-handbook
pip install -e .
python -m aigov --help
```

---

## Core Framework

거버넌스 로직은 `core/` 라이브러리로 추출되어 있어 노트북 밖에서도 재사용할 수 있습니다.

```
core/
├── fairness.py    # 공정성 진단 엔진 (Demographic Parity, Equal Opportunity)
├── drift.py       # 드리프트 감지 (데이터 드리프트, 개념 드리프트)
├── audit.py       # 알고리즘 감사 (SHAP 기반 설명 가능성, 감사 리포트)
└── cli.py         # CLI 도구 (check / audit / drift 서브커맨드)
```

## CLI

```bash
# 모델 공정성 및 편향 점검
python -m aigov check --model model.pkl --data data.csv

# 알고리즘 감사 리포트 생성
python -m aigov audit --report output.json

# 프로덕션 드리프트 탐지
python -m aigov drift --baseline train.csv --current prod.csv
```

---

## "거버넌스 없이는 이렇게 됩니다" — 반면교사 데이터셋

`data/` 폴더에는 의도적으로 편향·드리프트가 주입된 데이터셋이 포함되어 있습니다.

| 데이터셋 | 주입된 문제 | 탐지 챕터 |
|---------|-----------|---------|
| `data/biased_hiring.csv` | 성별 편향 (Demographic Parity 위반) | ch03, ch11 |
| `data/drifted_credit.csv` | 분포 드리프트 (12개월 누적) | ch12, ch14 |
| `data/poisoned_supply.csv` | 데이터 공급망 오염 | ch15 |

각 노트북에서 거버넌스 도구가 이 문제들을 어떻게 자동 탐지하는지 직접 확인하세요.

---

## 규제 매핑

| 코드 모듈 | AI 기본법(한국) | EU AI Act | NIST AI RMF |
|---------|--------------|----------|------------|
| `core/fairness.py` | 제22조 (차별 금지) | Art. 10 (데이터 거버넌스) | GOVERN 1.2 |
| `core/audit.py` | 제28조 (알고리즘 투명성) | Art. 13 (투명성 의무) | MAP 3.5 |
| `core/drift.py` | 제30조 (모니터링 의무) | Art. 9 (위험 관리 시스템) | MEASURE 2.5 |
| `ch15` (보안) | 제35조 (보안 요건) | Art. 15 (견고성 및 보안) | MANAGE 2.2 |
| `ch09` (데이터) | 제18조 (데이터 품질) | Art. 10 (훈련 데이터) | MAP 1.6 |

---

## 주요 실습 내용

- **공정성 검증**: Fairlearn 기반 Demographic Parity, Equal Opportunity 측정
- **설명가능성(XAI)**: SHAP, LIME을 활용한 모델 해석
- **차등 프라이버시**: diffprivlib로 구현하는 DP 학습
- **드리프트 감지**: evidently, alibi-detect 기반 데이터/개념 드리프트 모니터링
- **MLOps 거버넌스**: MLflow 실험 추적 및 모델 레지스트리
- **보안**: 적대적 공격 탐지, 페더레이션 러닝
- **GenAI 거버넌스**: RAG, 환각 제어, 워터마킹

---

## 22개 챕터 노트북

| 챕터 | 제목 | 코드 수 | Colab 실행 |
|------|------|---------|-----------|
| ch01 | AI 거버넌스 개념과 필요성 | 1 | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/back2zion/ai-governance-handbook/blob/main/notebooks/ch01.ipynb) |
| ch02 | 글로벌 AI 거버넌스 프레임워크 | 2 | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/back2zion/ai-governance-handbook/blob/main/notebooks/ch02.ipynb) |
| ch03 | AI 윤리 실무화 | 12 | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/back2zion/ai-governance-handbook/blob/main/notebooks/ch03.ipynb) |
| ch04 | AI 거버넌스 조직 체계 | 3 | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/back2zion/ai-governance-handbook/blob/main/notebooks/ch04.ipynb) |
| ch05a | AI 정책 설계 | 4 | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/back2zion/ai-governance-handbook/blob/main/notebooks/ch05a.ipynb) |
| ch05b | 산업별 AI 적용 | 5 | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/back2zion/ai-governance-handbook/blob/main/notebooks/ch05b.ipynb) |
| ch06 | 거버넌스 도구와 플랫폼 | 6 | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/back2zion/ai-governance-handbook/blob/main/notebooks/ch06.ipynb) |
| ch07 | 사례 연구 | 4 | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/back2zion/ai-governance-handbook/blob/main/notebooks/ch07.ipynb) |
| ch08 | 유즈케이스 발굴 | 5 | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/back2zion/ai-governance-handbook/blob/main/notebooks/ch08.ipynb) |
| ch09 | 데이터 거버넌스 | 7 | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/back2zion/ai-governance-handbook/blob/main/notebooks/ch09.ipynb) |
| ch10 | 모델 개발 거버넌스 | 6 | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/back2zion/ai-governance-handbook/blob/main/notebooks/ch10.ipynb) |
| ch11 | 알고리즘 감사와 인증 | 3 | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/back2zion/ai-governance-handbook/blob/main/notebooks/ch11.ipynb) |
| ch12 | 운영 및 생명주기 관리 | 6 | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/back2zion/ai-governance-handbook/blob/main/notebooks/ch12.ipynb) |
| ch12b | 생성 AI 거버넌스 | 3 | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/back2zion/ai-governance-handbook/blob/main/notebooks/ch12b.ipynb) |
| ch13 | 거버넌스 아키텍처 | 9 | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/back2zion/ai-governance-handbook/blob/main/notebooks/ch13.ipynb) |
| ch14 | 도구 및 플랫폼 | 9 | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/back2zion/ai-governance-handbook/blob/main/notebooks/ch14.ipynb) |
| ch15 | 보안과 프라이버시 | 13 | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/back2zion/ai-governance-handbook/blob/main/notebooks/ch15.ipynb) |
| ch16 | 의료 AI 거버넌스 | 3 | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/back2zion/ai-governance-handbook/blob/main/notebooks/ch16.ipynb) |
| ch17 | 금융 AI 거버넌스 | 10 | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/back2zion/ai-governance-handbook/blob/main/notebooks/ch17.ipynb) |
| ch18 | 공공 AI 거버넌스 | 6 | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/back2zion/ai-governance-handbook/blob/main/notebooks/ch18.ipynb) |
| ch19 | 산업 AI 거버넌스 | 6 | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/back2zion/ai-governance-handbook/blob/main/notebooks/ch19.ipynb) |
| ch20 | AI 거버넌스의 미래 | 5 | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/back2zion/ai-governance-handbook/blob/main/notebooks/ch20.ipynb) |

---

## Contributing

AI 거버넌스는 혼자 완성할 수 없습니다. 규제 업데이트, 새 지표, 번역, 버그 수정 모두 환영합니다.

[CONTRIBUTING.md](CONTRIBUTING.md)를 참고해 기여를 시작하세요.

---

## License

Apache 2.0 — 상업적 활용을 포함한 자유로운 사용을 허가합니다.

> 본 저장소는 **『AI 거버넌스 실무 지침서』** (곽두일, AI 컨설턴트)의 실습 코드를 기반으로 발전한 오픈소스 프로젝트입니다.
