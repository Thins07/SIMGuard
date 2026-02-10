
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

    def predict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make a prediction for a single user event.
        Maps frontend keys to the 5 core features required by the model.
        """
        try:
            # Map frontend keys (left) to model features (right)
            mapped_data = {
                'time_since_last_sim_change': float(data.get('time_since_sim_change', 0)),
                'num_calls_last_24h': float(data.get('num_calls_last_24h', 0)),
                'data_usage_last_24h': float(data.get('data_usage_last_24h', 0)), 
                'change_in_data_usage': float(data.get('data_usage_change_percent', 0)), # Maps 'percent' to 'change'
                'distance_change_km': float(data.get('distance_change', 0))
            }

            if self.model is None or self.scaler is None:
                # If model isn't loaded, try loading it now
                if not self.load_model():
                    return self._fallback_predict(mapped_data)

            # Convert to DF
            df_input = pd.DataFrame([mapped_data])
            X = df_input[self.features] # Ensure specific column order
            
            # Scale
            X_scaled = self.scaler.transform(X)
            
            # Predict
            # Returns [Prob_Legit, Prob_Fraud]
            prob = self.model.predict_proba(X_scaled)[0][1] 
            pred = int(prob > 0.5)

            return {
                'status': 'success',
                'prediction': pred,
                'confidence': float(prob)
            }

        except Exception as e:
            logger.error(f"Prediction error: {e}")
            return {'status': 'error', 'message': str(e)}

    def _fallback_predict(self, data: Dict[str, float]) -> Dict[str, Any]:
        """Simple rule-based fallback if ML model is missing"""
        logger.warning("Using Fallback Heuristics (Model not found)")
        score = 0
        if data['time_since_last_sim_change'] < 48: score += 0.4
        if data['distance_change_km'] > 100: score += 0.3
        if data['change_in_data_usage'] > 200: score += 0.2
        
        is_fraud = score > 0.5
        return {
            'status': 'success',
            'prediction': 1 if is_fraud else 0,
            'confidence': min(0.99, score + 0.1) if is_fraud else 0.1,
            'message': 'Model files missing - using heuristic fallback'
        }
