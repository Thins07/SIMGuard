from typing import Dict, Tuple, List
from .config import (
    SIM_CHANGE_HOURS_THRESHOLD, 
    DEVICE_CHANGE_AFTER_SIM_HOURS,
    FAILED_LOGIN_COUNT_THRESHOLD, 
    ROAMING_AFTER_SIM_HOURS,
    LOCATION_DISTANCE_KM_THRESHOLD,
    RISK_WEIGHTS
)
from .utils import calculate_distance, format_alert_level, format_alert_emoji

class RuleEngine:
    """
    Core Logic for SIM Swap Detection.
    Calculates a cumulative Risk Score based on weighted rules.
    """
    def __init__(self):
        # Register all rules defined in the thesis requirements
        self.rules = {
            'recent_sim_change': self.check_recent_sim_change,
            'device_change_after_sim': self.check_device_change_after_sim,
            'failed_login_attempts': self.check_failed_login_attempts,
            'sudden_location_change': self.check_sudden_location_change,
            'roaming_after_sim_change': self.check_roaming_after_sim_change
        }

    def check_recent_sim_change(self, user_data: Dict) -> Tuple[bool, str]:
        """Rule: SIM Card Identity (IMSI/ICCID) changed recently"""
        hours = user_data.get('hours_since_sim_change', 999)
        if hours <= SIM_CHANGE_HOURS_THRESHOLD:
            return True, f"SIM changed {hours:.1f} hours ago (Threshold: {SIM_CHANGE_HOURS_THRESHOLD}h)"
        return False, ""
    
    def check_device_change_after_sim(self, user_data: Dict) -> Tuple[bool, str]:
        """Rule: Device (IMEI) changed shortly after SIM change"""
        if user_data.get('device_changed_after_sim', False):
            hours = user_data.get('hours_between_sim_device_change', 0)
            return True, f"Device changed {hours:.1f}h after SIM change"
        return False, ""
    
    def check_failed_login_attempts(self, user_data: Dict) -> Tuple[bool, str]:
        """Rule: Multiple failed login attempts detected"""
        count = user_data.get('failed_logins_24h', 0)
        if count >= FAILED_LOGIN_COUNT_THRESHOLD:
            return True, f"High failed logins: {count} in 24h"
        return False, ""

    def check_sudden_location_change(self, user_data: Dict) -> Tuple[bool, str]:
        """Rule: Impossible travel or sudden location shift"""
        prev = user_data.get('previous_city', '')
        curr = user_data.get('current_city', '')
        
        # Only check if both exist and are different
        if prev and curr and prev != curr:
            dist = calculate_distance(prev, curr)
            if dist > LOCATION_DISTANCE_KM_THRESHOLD:
                return True, f"Sudden location jump: {prev} to {curr} ({dist}km)"
        return False, ""

    def check_roaming_after_sim_change(self, user_data: Dict) -> Tuple[bool, str]:
        """Rule: International roaming activated immediately after SIM change"""
        is_roaming = user_data.get('is_roaming', False)
        hours = user_data.get('hours_since_sim_change', 999)
        
        if is_roaming and hours <= ROAMING_AFTER_SIM_HOURS:
            return True, "Roaming active shortly after SIM change"
        return False, ""

    def evaluate_user(self, user_data: Dict) -> Dict:
        """
        Run all rules against user data.
        Returns accumulated Risk Score and Alert Level.
        """
        triggered_rules = []
        risk_score = 0
        
        for rule_name, rule_func in self.rules.items():
            triggered, reason = rule_func(user_data)
            if triggered:
                weight = RISK_WEIGHTS.get(rule_name, 0)
                risk_score += weight
                triggered_rules.append({
                    'rule': rule_name, 
                    'reason': reason, 
                    'weight': weight
                })
        
        # Determine High/Medium/Low based on accumulated score
        alert_level = format_alert_level(risk_score)
        alert_emoji = format_alert_emoji(alert_level)
        
        return {
            'user_id': user_data.get('user_id', 'UNKNOWN'),
            'risk_score': risk_score,
            'alert_level': alert_level,
            'alert_emoji': alert_emoji,
            'triggered_rules': triggered_rules,
            'total_rules_triggered': len(triggered_rules)
        }
