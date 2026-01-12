"""
Rule Engine for SIM Swap Detection
Implements all detection rules and risk scoring

MVP: Rule-Based Detection Only (No ML)

FUTURE WORK - Machine Learning Integration Points:
==================================================

1. FEATURE ENGINEERING (Add after line 150):
   - Extract additional features from user behavior
   - Create time-series features
   - Generate interaction features between rules
   - Normalize features for ML models

2. ML MODEL TRAINING (Add new class):
   - Train XGBoost/Random Forest classifier
   - Use rule outputs as features
   - Train on labeled SIM swap dataset
   - Implement cross-validation
   - Save trained model

3. HYBRID APPROACH (Modify evaluate_user method):
   - Combine rule-based scores with ML predictions
   - Use rules for explainability
   - Use ML for improved accuracy
   - Weighted ensemble of both approaches

4. MODEL EVALUATION (Add new methods):
   - Calculate precision, recall, F1-score
   - ROC-AUC analysis
   - Confusion matrix
   - Feature importance analysis

5. ONLINE LEARNING (Future enhancement):
   - Update model with new labeled data
   - Adaptive thresholds based on feedback
   - Continuous model improvement
"""

from typing import Dict, List, Tuple
from datetime import datetime
import config
from utils import calculate_distance, hours_between, percentage_change


class RuleEngine:
    """
    Rule-based SIM swap detection engine

    MVP: Uses only rule-based logic for detection
    Future: Can be extended with ML models (see comments above)
    """

    def __init__(self):
        """
        Initialize rule engine with all detection rules

        FUTURE ML INTEGRATION:
        - Add ml_model parameter to load trained model
        - Add feature_scaler for ML preprocessing
        - Add hybrid_mode flag to enable ML+Rules
        """
        self.rules = {
            'recent_sim_change': self.check_recent_sim_change,
            'device_change_after_sim': self.check_device_change_after_sim,
            'sudden_location_change': self.check_sudden_location_change,
            'abnormal_cell_tower_change': self.check_abnormal_cell_tower_change,
            'abnormal_data_usage': self.check_abnormal_data_usage,
            'abnormal_call_pattern': self.check_abnormal_call_pattern,
            'abnormal_sms_pattern': self.check_abnormal_sms_pattern,
            'failed_login_attempts': self.check_failed_login_attempts,
            'roaming_after_sim_change': self.check_roaming_after_sim_change
        }

        # FUTURE ML INTEGRATION: Uncomment when ML is ready
        # self.ml_model = None  # Load trained model here
        # self.feature_scaler = None  # Load feature scaler here
        # self.use_ml = False  # Enable ML predictions
    
    def check_recent_sim_change(self, user_data: Dict) -> Tuple[bool, str]:
        """Rule 1: Check if SIM was recently changed"""
        hours_since_sim_change = user_data.get('hours_since_sim_change', 999)
        
        if hours_since_sim_change <= config.SIM_CHANGE_HOURS_THRESHOLD:
            return True, f"SIM changed {hours_since_sim_change:.1f} hours ago (threshold: {config.SIM_CHANGE_HOURS_THRESHOLD}h)"
        return False, ""
    
    def check_device_change_after_sim(self, user_data: Dict) -> Tuple[bool, str]:
        """Rule 2: Check if device changed shortly after SIM change"""
        device_changed = user_data.get('device_changed_after_sim', False)
        hours_between_changes = user_data.get('hours_between_sim_device_change', 999)
        
        if device_changed and hours_between_changes <= config.DEVICE_CHANGE_AFTER_SIM_HOURS:
            return True, f"Device changed {hours_between_changes:.1f}h after SIM change (threshold: {config.DEVICE_CHANGE_AFTER_SIM_HOURS}h)"
        return False, ""
    
    def check_sudden_location_change(self, user_data: Dict) -> Tuple[bool, str]:
        """Rule 3: Check for sudden location change"""
        prev_city = user_data.get('previous_city', '')
        curr_city = user_data.get('current_city', '')
        hours_since_change = user_data.get('hours_since_location_change', 999)
        
        if prev_city and curr_city and prev_city != curr_city:
            distance = calculate_distance(prev_city, curr_city)
            
            if distance >= config.LOCATION_DISTANCE_KM_THRESHOLD and \
               hours_since_change <= config.LOCATION_TIME_HOURS_THRESHOLD:
                return True, f"Location changed {distance}km ({prev_city}→{curr_city}) in {hours_since_change:.1f}h"
        return False, ""
    
    def check_abnormal_cell_tower_change(self, user_data: Dict) -> Tuple[bool, str]:
        """Rule 4: Check for abnormal cell tower changes"""
        tower_changes = user_data.get('cell_tower_changes_24h', 0)
        
        if tower_changes >= config.CELL_TOWER_CHANGE_COUNT_THRESHOLD:
            return True, f"{tower_changes} cell tower changes in 24h (threshold: {config.CELL_TOWER_CHANGE_COUNT_THRESHOLD})"
        return False, ""
    
    def check_abnormal_data_usage(self, user_data: Dict) -> Tuple[bool, str]:
        """Rule 5: Check for abnormal data usage patterns"""
        prev_data = user_data.get('previous_data_usage_mb', 0)
        curr_data = user_data.get('current_data_usage_mb', 0)
        
        if prev_data > 0:
            change_pct = percentage_change(prev_data, curr_data)
            
            if change_pct >= config.DATA_USAGE_INCREASE_PERCENT:
                return True, f"Data usage increased {change_pct:.1f}% ({prev_data}MB→{curr_data}MB)"
            elif change_pct <= -config.DATA_USAGE_DECREASE_PERCENT:
                return True, f"Data usage decreased {abs(change_pct):.1f}% ({prev_data}MB→{curr_data}MB)"
        return False, ""
    
    def check_abnormal_call_pattern(self, user_data: Dict) -> Tuple[bool, str]:
        """Rule 6: Check for abnormal call patterns"""
        prev_calls = user_data.get('previous_calls_24h', 0)
        curr_calls = user_data.get('current_calls_24h', 0)
        
        if prev_calls > 0:
            change_pct = percentage_change(prev_calls, curr_calls)
            
            if change_pct >= config.CALL_INCREASE_PERCENT:
                return True, f"Calls increased {change_pct:.1f}% ({prev_calls}→{curr_calls} calls)"
            elif change_pct <= -config.CALL_DECREASE_PERCENT:
                return True, f"Calls decreased {abs(change_pct):.1f}% ({prev_calls}→{curr_calls} calls)"
        return False, ""
    
    def check_abnormal_sms_pattern(self, user_data: Dict) -> Tuple[bool, str]:
        """Rule 7: Check for abnormal SMS patterns"""
        prev_sms = user_data.get('previous_sms_24h', 0)
        curr_sms = user_data.get('current_sms_24h', 0)
        
        if prev_sms > 0:
            change_pct = percentage_change(prev_sms, curr_sms)
            
            if change_pct >= config.SMS_INCREASE_PERCENT:
                return True, f"SMS increased {change_pct:.1f}% ({prev_sms}→{curr_sms} messages)"
            elif change_pct <= -config.SMS_DECREASE_PERCENT:
                return True, f"SMS decreased {abs(change_pct):.1f}% ({prev_sms}→{curr_sms} messages)"
        return False, ""
    
    def check_failed_login_attempts(self, user_data: Dict) -> Tuple[bool, str]:
        """Rule 8: Check for failed login attempts"""
        failed_logins = user_data.get('failed_logins_24h', 0)
        
        if failed_logins >= config.FAILED_LOGIN_COUNT_THRESHOLD:
            return True, f"{failed_logins} failed login attempts in 24h (threshold: {config.FAILED_LOGIN_COUNT_THRESHOLD})"
        return False, ""
    
    def check_roaming_after_sim_change(self, user_data: Dict) -> Tuple[bool, str]:
        """Rule 9: Check if roaming started after SIM change"""
        is_roaming = user_data.get('is_roaming', False)
        hours_since_sim_change = user_data.get('hours_since_sim_change', 999)
        
        if is_roaming and hours_since_sim_change <= config.ROAMING_AFTER_SIM_HOURS:
            return True, f"Roaming started {hours_since_sim_change:.1f}h after SIM change (threshold: {config.ROAMING_AFTER_SIM_HOURS}h)"
        return False, ""
    
    def evaluate_user(self, user_data: Dict) -> Dict:
        """
        Evaluate all rules for a user and calculate risk score

        MVP: Uses only rule-based scoring

        FUTURE ML INTEGRATION:
        ----------------------
        1. Extract features from user_data
        2. Get ML model prediction probability
        3. Combine rule score with ML score:
           final_score = (rule_score * 0.6) + (ml_score * 0.4)
        4. Use ML confidence for alert level adjustment
        5. Add ML prediction to output for comparison

        Example ML integration code:
        ```python
        if self.use_ml and self.ml_model is not None:
            # Extract features for ML
            features = self._extract_ml_features(user_data)

            # Get ML prediction
            ml_probability = self.ml_model.predict_proba(features)[0][1]
            ml_score = ml_probability * 100

            # Hybrid scoring
            risk_score = (risk_score * 0.6) + (ml_score * 0.4)
        ```

        Args:
            user_data: Dictionary containing user activity data

        Returns:
            Dictionary with risk score, alert level, and triggered rules
        """
        triggered_rules = []
        risk_score = 0

        # STEP 1: Evaluate each rule (Rule-Based Detection)
        for rule_name, rule_func in self.rules.items():
            triggered, reason = rule_func(user_data)

            if triggered:
                weight = config.RISK_WEIGHTS.get(rule_name, 0)
                risk_score += weight
                triggered_rules.append({
                    'rule': rule_name,
                    'reason': reason,
                    'weight': weight
                })

        # STEP 2: FUTURE ML INTEGRATION POINT
        # Uncomment when ML model is ready:
        # if self.use_ml and self.ml_model is not None:
        #     ml_features = self._extract_ml_features(user_data)
        #     ml_prediction = self.ml_model.predict_proba(ml_features)[0][1]
        #     ml_score = ml_prediction * 100
        #     risk_score = (risk_score * 0.6) + (ml_score * 0.4)  # Hybrid approach

        # STEP 3: Determine alert level
        from utils import format_alert_level, format_alert_emoji
        alert_level = format_alert_level(risk_score)
        alert_emoji = format_alert_emoji(alert_level)

        return {
            'user_id': user_data.get('user_id', 'UNKNOWN'),
            'risk_score': risk_score,
            'alert_level': alert_level,
            'alert_emoji': alert_emoji,
            'triggered_rules': triggered_rules,
            'total_rules_triggered': len(triggered_rules)
            # FUTURE: Add 'ml_score' and 'ml_confidence' fields
        }

    # FUTURE ML INTEGRATION: Add these methods when implementing ML
    #
    # def _extract_ml_features(self, user_data: Dict) -> np.ndarray:
    #     """Extract features for ML model"""
    #     features = [
    #         user_data.get('hours_since_sim_change', 0),
    #         1 if user_data.get('device_changed_after_sim', False) else 0,
    #         user_data.get('hours_between_sim_device_change', 0),
    #         user_data.get('cell_tower_changes_24h', 0),
    #         user_data.get('failed_logins_24h', 0),
    #         # Add more features as needed
    #     ]
    #     return np.array(features).reshape(1, -1)
    #
    # def load_ml_model(self, model_path: str):
    #     """Load trained ML model"""
    #     import joblib
    #     self.ml_model = joblib.load(model_path)
    #     self.use_ml = True
    #
    # def train_ml_model(self, training_data: pd.DataFrame):
    #     """Train ML model on labeled data"""
    #     from sklearn.ensemble import RandomForestClassifier
    #     # Implementation here
    #     pass

