"""
드리프트 감지 엔진 (Drift Detector)

AI 기본법 §7 (모델 성능 유지 의무), EU AI Act Art. 9 (위험 관리 시스템),
NIST AI RMF MEASURE 2.5 (모니터링) 구현.

PSI (Population Stability Index):
  < 0.1  : 안정  (No significant change)
  0.1~0.25: 경고  (Moderate change — 재검토 권장)
  > 0.25  : 드리프트 (Major change — 재학습 필요)
"""
from __future__ import annotations
import numpy as np
import pandas as pd
from dataclasses import dataclass, field
from typing import Dict, List, Optional
import warnings


@dataclass
class DriftReport:
    """드리프트 진단 결과."""
    feature: str
    psi: float
    status: str           # "stable" | "warning" | "drift"
    baseline_dist: Dict
    current_dist: Dict
    action_required: bool = False
    recommendation: str = ""

    def __post_init__(self):
        self.action_required = self.psi > 0.1
        self.recommendation = self._recommend()

    def _recommend(self) -> str:
        if self.psi > 0.25:
            return (f"'{self.feature}' 심각한 드리프트 (PSI={self.psi:.3f}). "
                    "즉시 재학습 또는 모델 교체 검토. AI 기본법: CAIO 보고 필요.")
        if self.psi > 0.1:
            return (f"'{self.feature}' 경고 수준 드리프트 (PSI={self.psi:.3f}). "
                    "2주 내 원인 분석 및 재학습 일정 수립 권장.")
        return f"'{self.feature}' 안정 (PSI={self.psi:.3f}). 다음 정기 점검까지 모니터링 유지."


class DriftDetector:
    """
    데이터 드리프트 자동 감지 엔진.

    PSI(Population Stability Index) 기반으로 피처별 분포 변화를 감지합니다.
    AI 기본법 §7: 고영향 AI는 월 1회 이상 드리프트 점검 권장.

    Example:
        detector = DriftDetector(baseline_df)
        reports = detector.detect(current_df)
        detector.print_summary(reports)
    """

    def __init__(self, baseline: pd.DataFrame, n_bins: int = 10,
                 psi_warning: float = 0.1, psi_critical: float = 0.25):
        self.baseline = baseline
        self.n_bins = n_bins
        self.psi_warning = psi_warning
        self.psi_critical = psi_critical

    def detect(self, current: pd.DataFrame,
               features: Optional[List[str]] = None) -> List[DriftReport]:
        """모든 수치형 피처에 대해 드리프트 감지."""
        if features is None:
            features = [c for c in self.baseline.columns
                        if pd.api.types.is_numeric_dtype(self.baseline[c])]

        reports = []
        for feat in features:
            if feat not in current.columns:
                warnings.warn(f"'{feat}' 컬럼이 현재 데이터에 없습니다.")
                continue
            report = self._check_feature(feat, self.baseline[feat], current[feat])
            reports.append(report)

        return sorted(reports, key=lambda r: r.psi, reverse=True)

    def _check_feature(self, feature: str,
                       baseline_series: pd.Series,
                       current_series: pd.Series) -> DriftReport:
        """단일 피처 PSI 계산."""
        # 공통 bin 경계값 설정 (baseline 기준)
        bins = np.histogram_bin_edges(
            baseline_series.dropna(), bins=self.n_bins
        )
        bins[0] = -np.inf
        bins[-1] = np.inf

        base_counts, _ = np.histogram(baseline_series.dropna(), bins=bins)
        curr_counts, _ = np.histogram(current_series.dropna(), bins=bins)

        # 비율 계산 (0 나누기 방지)
        base_pct = (base_counts + 1e-6) / len(baseline_series)
        curr_pct = (curr_counts + 1e-6) / len(current_series)

        psi = float(np.sum((curr_pct - base_pct) * np.log(curr_pct / base_pct)))

        if psi > self.psi_critical:
            status = "drift"
        elif psi > self.psi_warning:
            status = "warning"
        else:
            status = "stable"

        return DriftReport(
            feature=feature,
            psi=round(psi, 4),
            status=status,
            baseline_dist={"mean": float(baseline_series.mean()),
                           "std": float(baseline_series.std())},
            current_dist={"mean": float(current_series.mean()),
                          "std": float(current_series.std())},
        )

    def print_summary(self, reports: List[DriftReport]) -> None:
        """드리프트 요약 출력."""
        drifted = [r for r in reports if r.status == "drift"]
        warned = [r for r in reports if r.status == "warning"]
        stable = [r for r in reports if r.status == "stable"]

        print(f"\n{'='*55}")
        print(f"  드리프트 감지 결과 ({len(reports)}개 피처)")
        print(f"{'='*55}")
        print(f"  🔴 드리프트(PSI>0.25): {len(drifted)}개")
        print(f"  🟡 경고(PSI 0.1~0.25): {len(warned)}개")
        print(f"  🟢 안정(PSI<0.1)     : {len(stable)}개")
        print(f"{'='*55}")

        for r in reports:
            icon = {"drift": "🔴", "warning": "🟡", "stable": "🟢"}[r.status]
            print(f"  {icon} {r.feature:<25} PSI={r.psi:.4f}")
            if r.action_required:
                print(f"     → {r.recommendation}")
        print()
