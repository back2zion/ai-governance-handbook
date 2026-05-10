"""
알고리즘 감사 엔진 (Governance Auditor)

AI 기본법 §7 (알고리즘 투명성), EU AI Act Art. 13 (투명성 의무),
NIST AI RMF MAP 3.5 (AI 영향 평가) 구현.
"""
from __future__ import annotations
import json
import hashlib
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class AuditRecord:
    """단일 감사 기록."""
    audit_id: str
    model_name: str
    auditor: str
    timestamp: str
    checks: Dict[str, bool]
    score: float           # 0.0 ~ 1.0
    risk_level: str
    findings: List[str]
    recommendations: List[str]

    def to_json(self) -> str:
        return json.dumps(self.__dict__, ensure_ascii=False, indent=2)

    def passed(self) -> bool:
        return self.score >= 0.8 and self.risk_level != "HIGH"


class GovernanceAuditor:
    """
    AI 거버넌스 종합 감사 엔진.

    AI 기본법 §7(알고리즘 투명성), EU AI Act Art.13,
    NIST AI RMF MAP 3.5를 체크리스트로 구현합니다.

    Example:
        auditor = GovernanceAuditor("대출심사AI", "김감사")
        record = auditor.audit(model_card, fairness_report, drift_reports)
        print(record.to_json())
    """

    CHECKLIST = {
        # 데이터 거버넌스
        "data_lineage_documented": "데이터 계보(출처→가공→학습) 문서화",
        "data_bias_tested": "학습 데이터 편향 사전 검증",
        "pii_anonymized": "개인정보 가명화 처리 확인",
        # 모델 투명성
        "model_card_exists": "모델 카드(Model Card) 최신 상태",
        "xai_applied": "설명 가능성(XAI) 기법 적용",
        "performance_benchmarked": "성능 기준값 및 임계치 정의",
        # 공정성
        "fairness_tested": "보호 집단별 공정성 검증 수행",
        "demographic_parity_ok": "Demographic Parity Ratio ≥ 0.8",
        # 운영
        "human_oversight_active": "고영향 AI: 인간 최종 결정 절차 존재",
        "drift_monitoring_active": "드리프트 모니터링 운영 중",
        "incident_response_ready": "인시던트 대응 플레이북 보유",
        # 규제
        "ai_act_compliant": "AI 기본법/EU AI Act 해당 조항 준수 확인",
        "user_notified": "이용자에게 AI 판단임을 고지",
    }

    def __init__(self, model_name: str, auditor_name: str):
        self.model_name = model_name
        self.auditor_name = auditor_name

    def audit(self,
              model_card: Optional[Dict] = None,
              fairness_report=None,
              drift_reports: Optional[List] = None,
              manual_checks: Optional[Dict[str, bool]] = None) -> AuditRecord:
        """종합 감사 수행."""
        checks: Dict[str, bool] = {}

        # 모델 카드 기반 자동 체크
        if model_card:
            checks["model_card_exists"] = True
            checks["xai_applied"] = bool(model_card.get("xai_method"))
            checks["data_lineage_documented"] = bool(model_card.get("data_source"))
            checks["user_notified"] = bool(model_card.get("disclosure_ui"))

        # 공정성 결과 기반 자동 체크
        if fairness_report:
            checks["fairness_tested"] = True
            checks["demographic_parity_ok"] = (
                fairness_report.demographic_parity_ratio >= 0.8
            )

        # 드리프트 결과 기반 자동 체크
        if drift_reports is not None:
            checks["drift_monitoring_active"] = True
            drifted = [r for r in drift_reports if r.status == "drift"]
            if drifted:
                checks["drift_monitoring_active"] = False  # 드리프트 미해결

        # 수동 체크 항목 병합
        if manual_checks:
            checks.update(manual_checks)

        # 미체크 항목은 False 처리
        for key in self.CHECKLIST:
            if key not in checks:
                checks[key] = False

        # 점수 계산
        score = round(sum(checks.values()) / len(checks), 3)
        passed_count = sum(checks.values())
        risk_level = "LOW" if score >= 0.85 else ("MEDIUM" if score >= 0.6 else "HIGH")

        findings = [
            f"미충족: {self.CHECKLIST[k]}"
            for k, v in checks.items() if not v
        ]
        recommendations = self._generate_recommendations(checks)

        audit_id = hashlib.sha256(
            f"{self.model_name}{datetime.now().isoformat()}".encode()
        ).hexdigest()[:12].upper()

        return AuditRecord(
            audit_id=f"AUD-{audit_id}",
            model_name=self.model_name,
            auditor=self.auditor_name,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            checks=checks,
            score=score,
            risk_level=risk_level,
            findings=findings,
            recommendations=recommendations,
        )

    def _generate_recommendations(self, checks: Dict[str, bool]) -> List[str]:
        recs = []
        if not checks.get("fairness_tested"):
            recs.append("FairnessAuditor.audit() 실행 후 결과를 감사 기록에 포함하십시오.")
        if not checks.get("model_card_exists"):
            recs.append("부록 C.3 모델 카드 양식을 작성하고 거버넌스 시스템에 등록하십시오.")
        if not checks.get("human_oversight_active"):
            recs.append("AI 기본법 §6: 고영향 AI 결정에 인간 검토 절차를 즉시 도입하십시오.")
        if not checks.get("drift_monitoring_active"):
            recs.append("DriftDetector를 CI/CD 파이프라인에 연동하여 자동 감지 체계를 구축하십시오.")
        return recs
