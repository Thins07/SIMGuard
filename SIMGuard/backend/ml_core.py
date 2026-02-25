
#!/usr/bin/env python3
"""
SIMGuard ML Core - The "Thinker" Model
Implements the specific XGBoost architecture for behavioral analysis.
Features: 5 Core Telemetry Points
Logic: Noise Injection, Heavy Regularization to prevent overfitting
"""

import pandas as pd
import numpy as np
import joblib
import os
import logging
from typing import Dict, Any, Tuple

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from xgboost import XGBClassifier
    from sklearn.preprocessing import StandardScaler
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
except ImportError:
    logger.warning("ML libraries not found. Core ML features will run in mock mode.")

class ThinkerModel:
    """
    The 'Thinker' Model Logic.
    Focuses on behavioral patterns rather than memorizing IDs/Locations.
    """

    def __init__(self):
        # Use absolute paths to ensure Flask finds the files regardless of where it's launched
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.model_path = os.path.join(base_dir, 'sim_swap_model.pkl')
        self.scaler_path = os.path.join(base_dir, 'preprocessor.pkl')
        
        self.model = None
        self.scaler = None
        
        # The 5 Core Behavioral Features (MUST match training data exactly)
        self.features = [
            'time_since_last_sim_change',
            'num_calls_last_24h',
            'data_usage_last_24h',
            'change_in_data_usage',
            'distance_change_km'
        ]
        
        self.load_model()

    def load_model(self) -> bool:
        """Load trained model and scaler from disk"""
        try:
            if os.path.exists(self.model_path) and os.path.exists(self.scaler_path):
                self.model = joblib.load(self.model_path)
                self.scaler = joblib.load(self.scaler_path)
                logger.info(f"✅ Thinker Model loaded from {self.model_path}")
                return True
            else:
                logger.warning(f"⚠️ Model files not found at {self.model_path}")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
        return False

    def clean_and_prepare(self, df: pd.DataFrame, is_training: bool = False) -> pd.DataFrame:
        """
        Preprocesses data:
        1. Selects only the 5 core features.
        2. Handles missing values.
        """
        # Ensure all columns exist, fill with 0 if missing
        for col in self.features:
            if col not in df.columns:
                df[col] = 0.0
        
        # Select only the core features (Feature Stripping)
        X = df[self.features].copy()
        
        # Handle non-numeric junk
        X = X.apply(pd.to_numeric, errors='coerce').fillna(0)
        
        return X

    def run_diagnostics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Run the loaded model on a validation dataset.
        Returns prediction stats and metrics (if labels exist).
        """
        try:
            if self.model is None:
                if not self.load_model():
                     return {'status': 'error', 'message': 'No model loaded. Place .pkl files in backend folder.'}

            X = self.clean_and_prepare(df)
            
            # Use the loaded scaler
            X_scaled = self.scaler.transform(X)
            y_pred = self.model.predict(X_scaled)
            
            results = {
                'total_samples': len(df),
                'fraud_detected': int(sum(y_pred)),
                'clean_detected': int(len(df) - sum(y_pred))
            }

            # If labels exist, calculate performance metrics
            if 'label' in df.columns:
                y_true = df['label'].astype(int)
                results['accuracy'] = float(accuracy_score(y_true, y_pred))
                results['precision'] = float(precision_score(y_true, y_pred, zero_division=0))
                results['recall'] = float(recall_score(y_true, y_pred, zero_division=0))
                results['f1_score'] = float(f1_score(y_true, y_pred, zero_division=0))
                results['confusion_matrix'] = confusion_matrix(y_true, y_pred).tolist()

            return {
                'status': 'success',
                'model_info': {'type': 'XGBoost (Thinker)', 'status': 'Active'},
                'results': results
            }

        except Exception as e:
            logger.error(f"Diagnostics failed: {e}")
            return {'status': 'error', 'message': str(e)}

    def _rule_based_risk_probability(self, data: Dict[str, Any]) -> float:
        """
        Compute a 0-1 risk probability from manual-check inputs so that:
        - HIGH risk (e.g. 2h SIM, 500km, 300% data, 5 failed logins, sim_change_flag) -> > 0.8
        - MEDIUM risk (e.g. 24h, 50km, 150%, 1 failed login) -> 0.5 to 0.8
        - LOW risk (e.g. 500h, 5km, 10%, 0 failed logins) -> < 0.5
        Uses continuous scoring so risk levels are clearly differentiated.
        """
        hours = float(data.get('time_since_sim_change', data.get('time_since_last_sim_change', 999)))
        distance_km = float(data.get('distance_change', data.get('distance_change_km', 0)))
        data_pct = float(data.get('data_usage_change_percent', data.get('change_in_data_usage', 0)))
        failed_logins = int(data.get('num_failed_logins_last_24h', 0))
        sim_flag = bool(data.get('sim_change_flag', False))
        device_flag = bool(data.get('device_change_flag', False))
        is_roaming = bool(data.get('is_roaming', False))

        # Time since SIM change: very recent = high risk (2h->0.95, 24h->0.6, 500h->0.05)
        if hours >= 168:
            time_score = 0.05
        elif hours >= 72:
            time_score = 0.20
        elif hours >= 24:
            time_score = 0.60
        elif hours >= 6:
            time_score = 0.75
        else:
            time_score = 0.95

        # Distance (km): large jump = high risk (500->0.9, 50->0.4, 5->0.05)
        if distance_km >= 400:
            dist_score = 0.90
        elif distance_km >= 200:
            dist_score = 0.70
        elif distance_km >= 100:
            dist_score = 0.50
        elif distance_km >= 50:
            dist_score = 0.40
        elif distance_km >= 20:
            dist_score = 0.15
        else:
            dist_score = 0.05

        # Data usage change %: big spike = high risk (300->0.9, 150->0.65, 10->0)
        if data_pct >= 250:
            data_score = 0.90
        elif data_pct >= 150:
            data_score = 0.65
        elif data_pct >= 80:
            data_score = 0.35
        elif data_pct >= 30:
            data_score = 0.10
        else:
            data_score = 0.0

        # Failed logins: cap contribution so 5+ -> strong signal
        fail_score = min(1.0, failed_logins / 4.0) * 0.30

        # Status flags (additive)
        flag_bonus = 0.0
        if sim_flag:
            flag_bonus += 0.15
        if device_flag:
            flag_bonus += 0.08
        if is_roaming:
            flag_bonus += 0.07

        # Weighted combination (weights tuned to match HIGH/MEDIUM/LOW examples)
        rule_prob = (
            time_score * 0.35 +
            dist_score * 0.25 +
            data_score * 0.20 +
            fail_score +
            flag_bonus
        )
        return min(1.0, max(0.0, rule_prob))

    def predict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make a prediction for a single user event.
        Uses rule-based risk probability (from all form inputs) and blends with
        ML model when available so HIGH/MEDIUM/LOW are clearly differentiated.
        """
        try:
            # Map frontend keys (left) to model features (right)
            mapped_data = {
                'time_since_last_sim_change': float(data.get('time_since_sim_change', 0)),
                'num_calls_last_24h': float(data.get('num_calls_last_24h', 0)),
                'data_usage_last_24h': float(data.get('data_usage_last_24h', 0)),
                'change_in_data_usage': float(data.get('data_usage_change_percent', 0)),
                'distance_change_km': float(data.get('distance_change', 0))
            }

            rule_prob = self._rule_based_risk_probability(data)

            if self.model is None or self.scaler is None:
                if not self.load_model():
                    return self._fallback_predict(data, rule_prob)

            # Convert to DF
            df_input = pd.DataFrame([mapped_data])
            X = df_input[self.features]

            # Scale and get ML probability
            X_scaled = self.scaler.transform(X)
            ml_prob = float(self.model.predict_proba(X_scaled)[0][1])

            # Blend rule-based and ML: 60% rule / 40% ML so manual inputs (incl. flags, failed logins) matter
            final_prob = 0.6 * rule_prob + 0.4 * ml_prob
            pred = int(final_prob > 0.5)

            return {
                'status': 'success',
                'prediction': pred,
                'confidence': float(final_prob)
            }

        except Exception as e:
            logger.error(f"Prediction error: {e}")
            return {'status': 'error', 'message': str(e)}

    def _fallback_predict(self, data: Dict[str, Any], rule_prob: float) -> Dict[str, Any]:
        """Use rule-based risk probability when ML model is missing."""
        logger.warning("Using rule-based risk (model not found)")
        pred = 1 if rule_prob > 0.5 else 0
        return {
            'status': 'success',
            'prediction': pred,
            'confidence': float(rule_prob),
            'message': 'Model files missing - using rule-based risk score'
        }
