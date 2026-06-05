import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix

class IndustryAIEvaluator:
    """Validator for Industry-specific AI (Finance, Healthcare)."""
    
    @staticmethod
    def evaluate_financial_fairness(y_pred, sensitive_features, protected_attrs):
        """Calculates Adverse Impact Ratio (4/5 rule)."""
        results = {}
        for attr in protected_attrs:
            groups = sensitive_features[attr].unique()
            rates = {g: y_pred[sensitive_features[attr] == g].mean() for g in groups}
            max_rate = max(rates.values())
            results[attr] = {g: r / max_rate if max_rate > 0 else 1.0 for g, r in rates.items()}
        return results

    @staticmethod
    def evaluate_clinical_performance(y_true, y_prob, threshold=0.5):
        """Evaluates medical diagnostic metrics."""
        y_pred = (y_prob >= threshold).astype(int)
        tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
        sensitivity = tp / (tp + fn) if (tp + fn) > 0 else 0
        specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
        return {
            "sensitivity": sensitivity,
            "specificity": specificity,
            "precision": tp / (tp + fp) if (tp + fp) > 0 else 0
        }

    @staticmethod
    def analyze_clinical_discrepancy(ai_result, physician_result):
        """Safety audit for AI vs Physician disagreements."""
        if ai_result == 1 and physician_result == 0:
            return "OVERDIAGNOSIS_RISK"
        if ai_result == 0 and physician_result == 1:
            return "MISS_RISK_CRITICAL"
        return "AGREEMENT"
