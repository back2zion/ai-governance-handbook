"""
공정성 진단 엔진 (Fairness Auditor)

AI 기본법 §8 (차별 금지), EU AI Act Art. 10 (데이터 품질),
NIST AI RMF MAP 5.1 (공정성 측정) 구현.

4/5 Rule (0.8 기준): Demographic Parity Ratio < 0.8 → 차별 위험
Equal Opportunity Difference > 0.1 → 기회 불평등
"""
from __future__ import annotations
import numpy as np
import pandas as pd
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


@dataclass
class FairnessReport:
    """공정성 진단 결과 보고서."""
    model_name: str
    sensitive_attr: str
    demographic_parity_ratio: float      # 1.0 = 완전 공정, < 0.8 = 위험
    equal_opportunity_diff: float        # 0.0 = 완전 공정, > 0.1 = 위험
    disparate_impact: float
    group_metrics: Dict[str, Dict]
    risk_level: str = ""
    recommendations: List[str] = field(default_factory=list)

    def __post_init__(self):
        self.risk_level = self._assess_risk()
        self.recommendations = self._generate_recommendations()

    def _assess_risk(self) -> str:
        if self.demographic_parity_ratio < 0.5 or self.equal_opportunity_diff > 0.2:
            return "HIGH"  # AI 기본법: 즉시 운영 중단 검토
        if self.demographic_parity_ratio < 0.8 or self.equal_opportunity_diff > 0.1:
            return "MEDIUM"  # 완화 조치 필요
        return "LOW"

    def _generate_recommendations(self) -> List[str]:
        recs = []
        if self.demographic_parity_ratio < 0.8:
            recs.append("학습 데이터 리샘플링 또는 재가중치 적용 권장 (Fairlearn Reductions 참조)")
        if self.equal_opportunity_diff > 0.1:
            recs.append("후처리 임계값 조정(Equalized Odds Post-processing) 검토")
        if self.disparate_impact < 0.8:
            recs.append("AI 기본법 §8 위반 위험: 법무팀 검토 및 CAIO 보고 필요")
        return recs if recs else ["현재 공정성 기준 충족 — 분기별 재평가 권장"]

    def summary(self) -> str:
        lines = [
            f"=== 공정성 진단 보고서: {self.model_name} ===",
            f"민감 속성: {self.sensitive_attr}",
            f"Demographic Parity Ratio : {self.demographic_parity_ratio:.3f} (기준: ≥0.8)",
            f"Equal Opportunity Diff   : {self.equal_opportunity_diff:.3f} (기준: ≤0.1)",
            f"Disparate Impact         : {self.disparate_impact:.3f} (4/5 Rule: ≥0.8)",
            f"위험 등급                : {self.risk_level}",
            "",
            "권고 사항:",
        ]
        for rec in self.recommendations:
            lines.append(f"  • {rec}")
        return "\n".join(lines)


class FairnessAuditor:
    """
    AI 공정성 자동 진단 엔진.

    AI 기본법 §8(차별 금지), EU AI Act Art.10, NIST AI RMF MAP 5.1 준수.

    Example:
        auditor = FairnessAuditor(model, "gender")
        report = auditor.audit(X_test, y_test, y_pred)
        print(report.summary())
    """

    def __init__(self, model=None, sensitive_attribute: str = "gender",
                 model_name: str = "Unknown Model"):
        self.model = model
        self.sensitive_attribute = sensitive_attribute
        self.model_name = model_name

    def audit(self, X: pd.DataFrame, y_true: np.ndarray,
              y_pred: np.ndarray) -> FairnessReport:
        """전체 공정성 진단 수행."""
        if self.sensitive_attribute not in X.columns:
            raise ValueError(f"'{self.sensitive_attribute}' 컬럼이 데이터에 없습니다.")

        groups = X[self.sensitive_attribute].unique()
        group_metrics = {}

        for g in groups:
            mask = X[self.sensitive_attribute] == g
            n = mask.sum()
            if n == 0:
                continue
            pos_rate = y_pred[mask].mean()          # 양성 예측률
            tpr = self._true_positive_rate(y_true[mask], y_pred[mask])
            acc = (y_pred[mask] == y_true[mask]).mean()
            group_metrics[str(g)] = {
                "n": int(n),
                "positive_rate": float(pos_rate),
                "true_positive_rate": float(tpr),
                "accuracy": float(acc),
            }

        dpr, eod, di = self._compute_metrics(group_metrics)

        return FairnessReport(
            model_name=self.model_name,
            sensitive_attr=self.sensitive_attribute,
            demographic_parity_ratio=dpr,
            equal_opportunity_diff=eod,
            disparate_impact=di,
            group_metrics=group_metrics,
        )

    def _true_positive_rate(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """True Positive Rate (재현율) 계산."""
        pos_mask = y_true == 1
        if pos_mask.sum() == 0:
            return 0.0
        return float(y_pred[pos_mask].mean())

    def _compute_metrics(self, group_metrics: Dict) -> Tuple[float, float, float]:
        """DPR, EOD, Disparate Impact 계산."""
        if len(group_metrics) < 2:
            return 1.0, 0.0, 1.0

        pos_rates = [m["positive_rate"] for m in group_metrics.values()]
        tprs = [m["true_positive_rate"] for m in group_metrics.values()]

        max_pr, min_pr = max(pos_rates), min(pos_rates)
        dpr = min_pr / max_pr if max_pr > 0 else 1.0
        eod = float(max(tprs) - min(tprs))
        di = min_pr / max_pr if max_pr > 0 else 1.0  # Disparate Impact = 4/5 Rule

        return round(dpr, 4), round(eod, 4), round(di, 4)

    def quick_check(self, X: pd.DataFrame, y_true: np.ndarray,
                    y_pred: np.ndarray) -> bool:
        """빠른 합격/불합격 판정. True = 기준 충족."""
        report = self.audit(X, y_true, y_pred)
        return report.risk_level == "LOW"
