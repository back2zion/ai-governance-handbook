# Contributing to AI Governance Handbook

이 저장소는 전 세계 AI 거버넌스 실무자들이 함께 만드는 생동하는 표준입니다.
코드 한 줄, 번역 한 문장, 버그 리포트 하나가 모두 실무 현장의 AI를 더 안전하게 만듭니다.

---

## 기여 유형

1. **버그 수정**: 실행 오류, import 오류, 노트북 셀 로직 오류
2. **새 거버넌스 지표**: `core/fairness.py`, `core/drift.py`, `core/audit.py`에 메트릭 추가
3. **규제 업데이트**: 새 법령/가이드라인(AI 기본법 시행령, EU AI Act 위임 규정 등) 반영
4. **번역**: 한국어↔영어 노트북 주석 및 문서 개선
5. **사례 연구**: 실제 산업 적용 사례 및 데이터셋 기여

---

## 개발 환경 설정

### Option A: DevContainer (권장)

VS Code와 Docker가 설치된 환경에서:

```bash
git clone https://github.com/back2zion/ai-governance-handbook
code ai-governance-handbook
# VS Code 좌하단 "Reopen in Container" 클릭
```

DevContainer가 Python 3.10, 모든 의존성, Jupyter 서버를 자동으로 구성합니다.

### Option B: 로컬 설치

```bash
git clone https://github.com/back2zion/ai-governance-handbook
cd ai-governance-handbook

# 개발 의존성 포함 설치
pip install -e ".[dev]"

# 테스트 실행
python -m pytest tests/
```

개발 의존성(`[dev]`)에는 pytest, nbval(노트북 테스트), black, ruff가 포함됩니다.

---

## PR 가이드

### 브랜치 명명 규칙

| 유형 | 형식 | 예시 |
|------|------|------|
| 새 기능/지표 | `feat/기능명` | `feat/equalized-odds-metric` |
| 버그 수정 | `fix/오류명` | `fix/ch03-import-error` |
| 문서 개선 | `docs/문서명` | `docs/ch10-korean-comments` |
| 규제 업데이트 | `reg/법령명` | `reg/eu-ai-act-article15` |

### 체크리스트

**노트북 추가/수정 시:**
- [ ] 노트북 JSON 유효성 확인: `python -m pytest tests/` 또는 `jupyter nbconvert --to script notebooks/chXX.ipynb`
- [ ] 첫 번째 셀에 `pip install` 명령어로 의존성 명시
- [ ] 한국어 주석 포함 (영어 병기 권장)
- [ ] Google Colab에서 처음부터 끝까지 실행 확인 (Runtime > Run all)

**새 거버넌스 지표 추가 시:**
- [ ] `core/` 모듈에 함수/클래스 추가
- [ ] 해당 챕터 노트북에 사용 예시 반영
- [ ] 관련 규제 조항 docstring에 명시 (예: `# AI 기본법 제22조, EU AI Act Art.10`)
- [ ] `python -m aigov check` CLI와 연동 여부 확인

**규제 업데이트 시:**
- [ ] 법령 원문 링크 또는 출처 명시
- [ ] 변경된 조항 번호와 내용 요약을 PR 본문에 포함
- [ ] 영향 받는 챕터/모듈 목록 제시

---

## 코드 스타일

- Python: [Black](https://black.readthedocs.io/) 포맷터 사용 (`black core/`)
- 린터: [Ruff](https://docs.astral.sh/ruff/) (`ruff check core/`)
- 노트북 주석: 한국어 우선, 기술 용어는 영어 병기

```python
# 공정성 지표 계산 — Demographic Parity Difference
# AI 기본법 제22조(차별 금지), EU AI Act Art. 10
def demographic_parity_difference(y_true, y_pred, sensitive_feature):
    ...
```

---

## 이슈 및 토론

- 버그: [Issue 템플릿](https://github.com/back2zion/ai-governance-handbook/issues/new?template=bug_report.md) 사용
- 새 기능 제안: [Feature Request 템플릿](https://github.com/back2zion/ai-governance-handbook/issues/new?template=feature_request.md) 사용
- 규제 해석 질문: GitHub Discussions 활용

---

## 행동 강령

이 프로젝트는 포용적이고 전문적인 커뮤니티를 지향합니다.

- 기여자의 경력, 국적, 언어에 관계없이 동등하게 존중합니다.
- 기술적 의견 불일치는 코드와 근거로 해결합니다.
- AI 거버넌스라는 공공선(公共善)을 위한 협업임을 항상 기억합니다.

기여해주셔서 감사합니다.
