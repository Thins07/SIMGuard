"""
SIMGuard ML Predictor Module
Handles model loading, feature engineering, and predictions
"""

import os
import pickle
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Any

class SIMSwapPredictor:
    """ML Model predictor for SIM swap detection"""
    
    def __init__(self, model_path: str = 'xgboost_simswap_model.pkl', 
                 scaler_path: str = 'scaler.pkl'):
        """
        Initialize predictor with model and scaler paths
        
        Args:
            model_path: Path to the trained XGBoost model
            scaler_path: Path to the fitted scaler
        """
        self.model_path = model_path
        self.scaler_path = scaler_path
        self.model = None
        self.scaler = None
        self.feature_names = None
        
    def load_model(self) -> bool:
        """
        Load the trained model and scaler
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Load XGBoost model
            if os.path.exists(self.model_path):
                with open(self.model_path, 'rb') as f:
                    self.model = pickle.load(f)
                print(f"✅ Model loaded from {self.model_path}")
            else:
                print(f"❌ Model file not found: {self.model_path}")
                return False
            
            # Load scaler
            if os.path.exists(self.scaler_path):
                with open(self.scaler_path, 'rb') as f:
                    self.scaler = pickle.load(f)
                print(f"✅ Scaler loaded from {self.scaler_path}")
            else:
                print(f"❌ Scaler file not found: {self.scaler_path}")
                return False
            
            return True
            
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            return False
    
    def engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Apply feature engineering to input data
        
        Args:
            df: Input DataFrame with raw features
            
        Returns:
            DataFrame with engineered features
        """
        df_engineered = df.copy()
        
        # 1. Location Velocity (km/hour)
        # Avoid division by zero
        time_hours = df_engineered['time_since_sim_change'].replace(0, 0.001)
        df_engineered['loc_velocity'] = df_engineered['distance_change'] / time_hours
        
        # 2. Tower Change Frequency (binary flag)
        df_engineered['tower_change_freq'] = (
            df_engineered['change_in_cell_tower_id'] > 0
        ).astype(int)
        
        # 3. High Risk Behavior (composite flag)
        df_engineered['high_risk_behavior'] = (
            (df_engineered['num_failed_logins_last_24h'] > 3) |
            (df_engineered['is_roaming'] == 1) |
            (df_engineered['sim_change_flag'] == 1)
        ).astype(int)
        
        return df_engineered
    
    def prepare_features(self, data: Dict[str, Any]) -> pd.DataFrame:
        """
        Prepare features from input dictionary
        
        Args:
            data: Dictionary containing input features
            
        Returns:
            DataFrame ready for prediction
        """
        # Create DataFrame from input
        df = pd.DataFrame([data])
        
        # Apply feature engineering
        df = self.engineer_features(df)
        
        # Define expected feature order (adjust based on your training)
        expected_features = [
            'distance_change',
            'time_since_sim_change',
            'num_failed_logins_last_24h',
            'num_calls_last_24h',
            'num_sms_last_24h',
            'data_usage_change_percent',
            'change_in_cell_tower_id',
            'is_roaming',
            'sim_change_flag',
            'device_change_flag',
            'loc_velocity',
            'tower_change_freq',
            'high_risk_behavior'
        ]
        
        # Select and order features
        df_features = df[expected_features]
        
        return df_features
    
    def predict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make prediction on input data
        
        Args:
            data: Dictionary containing input features
            
        Returns:
            Dictionary with prediction results
        """
        try:
            # Prepare features
            df_features = self.prepare_features(data)
            
            # Scale features
            if self.scaler:
                features_scaled = self.scaler.transform(df_features)
            else:
                features_scaled = df_features.values
            
            # Make prediction
            prediction = self.model.predict(features_scaled)[0]
            
            # Get prediction probability
            prediction_proba = self.model.predict_proba(features_scaled)[0]
            confidence = float(prediction_proba[int(prediction)] * 100)
            
            # Get feature importances for risk factors
            risk_factors = self.get_risk_factors(df_features, prediction)
            
            return {
                'prediction': int(prediction),
                'confidence': round(confidence, 2),
                'risk_factors': risk_factors,
                'status': 'success'
            }
            
        except Exception as e:
            print(f"❌ Prediction error: {e}")
            return {
                'prediction': 0,
                'confidence': 0.0,
                'risk_factors': [],
                'status': 'error',
                'error': str(e)
            }
    
    def get_risk_factors(self, df_features: pd.DataFrame, prediction: int) -> List[str]:
        """
        Identify key risk factors based on feature values
        
        Args:
            df_features: DataFrame with feature values
            prediction: Model prediction (0 or 1)
            
        Returns:
            List of risk factor descriptions
        """
        risk_factors = []
        
        # Extract feature values
        features = df_features.iloc[0]
        
        # Only show risk factors if prediction is suspicious
        if prediction == 1:
            if features['num_failed_logins_last_24h'] > 3:
                risk_factors.append(
                    f"High number of failed logins: {int(features['num_failed_logins_last_24h'])}"
                )
            
            if features['loc_velocity'] > 500:
                risk_factors.append(
                    f"Impossible travel detected: {features['loc_velocity']:.1f} km/h"
                )
            
            if features['sim_change_flag'] == 1:
                risk_factors.append("Recent SIM card change detected")
            
            if features['device_change_flag'] == 1:
                risk_factors.append("Device change detected")
            
            if features['is_roaming'] == 1:
                risk_factors.append("User is currently roaming")
            
            if features['tower_change_freq'] == 1:
                risk_factors.append(
                    f"Multiple cell tower changes: {int(features['change_in_cell_tower_id'])}"
                )
            
            if features['data_usage_change_percent'] > 100:
                risk_factors.append(
                    f"Unusual data usage spike: +{features['data_usage_change_percent']:.1f}%"
                )
            elif features['data_usage_change_percent'] < -50:
                risk_factors.append(
                    f"Unusual data usage drop: {features['data_usage_change_percent']:.1f}%"
                )
        
        return risk_factors[:5]  # Return top 5 risk factors
