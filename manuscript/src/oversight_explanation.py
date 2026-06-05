import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier

class OversightManager:
    """Manages human oversight records and detects automation bias."""
    
    def __init__(self, retention_years=5):
        self.retention_years = retention_years
        self.records = []

    def record_decision(self, record_id, ai_rec, human_dec, rationale, reviewer_id):
        record = {
            'id': record_id,
            'timestamp': pd.Timestamp.now(),
            'ai_rec': ai_rec,
            'human_dec': human_dec,
            'rationale': rationale,
            'reviewer_id': reviewer_id,
            'agreed': ai_rec == human_dec
        }
        self.records.append(record)
        return record

    def analyze_automation_bias(self, threshold=0.95):
        if not self.records:
            return 0, "No records"
        agreement_rate = sum(r['agreed'] for r in self.records) / len(self.records)
        status = "SUSPECTED" if agreement_rate > threshold else "NORMAL"
        return agreement_rate, status

def create_surrogate_model(original_model, X, max_depth=5):
    """Creates a transparent surrogate model to explain a black-box model."""
    y_blackbox = original_model.predict(X)
    surrogate = DecisionTreeClassifier(max_depth=max_depth)
    surrogate.fit(X, y_blackbox)
    fidelity = accuracy_score(y_blackbox, surrogate.predict(X))
    return surrogate, fidelity

def apply_differential_privacy_to_shap(shap_values, epsilon=1.0, sensitivity=0.1):
    """Adds Laplace noise to SHAP values for privacy preservation."""
    scale = sensitivity / epsilon
    noise = np.random.laplace(0, scale, shap_values.shape)
    return shap_values + noise
