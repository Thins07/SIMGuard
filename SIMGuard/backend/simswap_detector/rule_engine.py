from typing import Dict, Tuple, List
from .config import (
    SIM_CHANGE_HOURS_THRESHOLD,
    DEVICE_CHANGE_AFTER_SIM_HOURS,
    FAILED_LOGIN_COUNT_THRESHOLD,
    ROAMING_AFTER_SIM_HOURS,
    LOCATION_DISTANCE_KM_THRESHOLD,
    SIM_SWAP_REQUEST_HIGH_30D,
    DAYS_SINCE_LAST_SIM_RECENT,
    FAILED_OTP_HIGH_24H,
    ACCOUNT_AGE_NEW_DAYS,
    AVG_CALL_DURATION_LOW_MIN,
    AVG_DATA_USAGE_HIGH_GB,
    UNIQUE_CONTACTS_LOW_30D,
    CELL_TOWER_CHANGE_COUNT_THRESHOLD,
    RISK_WEIGHTS,
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
            # Legacy / generic behavior rules (also re-used for new CSV schema)
            'recent_sim_change': self.check_recent_sim_change,
            'device_change_after_sim': self.check_device_change_after_sim,
            'failed_login_attempts': self.check_failed_login_attempts,
            'sudden_location_change': self.check_sudden_location_change,
            'roaming_after_sim_change': self.check_roaming_after_sim_change,

            # New per-user batch CSV rules (used when the relevant fields exist)
            'high_sim_swap_activity': self.check_high_sim_swap_activity,
            'recent_sim_swap': self.check_recent_sim_swap,
            'device_or_location_change': self.check_device_or_location_change,
            'failed_otp_anomaly': self.check_failed_otp_anomaly,
            'account_age_risk': self.check_account_age_risk,
            'usage_pattern_anomaly': self.check_usage_pattern_anomaly,
            'contact_anomaly': self.check_contact_anomaly,
            'security_events': self.check_security_events,
            'fraud_reported': self.check_fraud_reported,
        }

    def check_recent_sim_change(self, user_data: Dict) -> Tuple[bool, str]:
        """Rule: SIM card changed recently (hours-based)."""
        # Support both legacy 'hours_since_sim_change' and new 'time_since_last_sim_change'
        hours = user_data.get(
            'hours_since_sim_change',
            user_data.get('time_since_last_sim_change', 999),
        )
        if hours <= SIM_CHANGE_HOURS_THRESHOLD:
            return True, f"SIM changed {hours:.1f} hours ago (Threshold: {SIM_CHANGE_HOURS_THRESHOLD}h)"
        return False, ""
    
    def check_device_change_after_sim(self, user_data: Dict) -> Tuple[bool, str]:
        """
        Rule: Device changed shortly after SIM change.

        Legacy datasets use a boolean 'device_changed_after_sim' and
        'hours_between_sim_device_change'.
        The newer Sri Lankan CSV uses simple flags:
        - sim_change_flag
        - device_change_flag
        - time_since_last_sim_change (hours)
        """
        # New schema: explicit flags
        sim_flag = int(user_data.get('sim_change_flag', 0) or 0)
        dev_flag = int(user_data.get('device_change_flag', 0) or 0)
        hours = float(
            user_data.get(
                'hours_between_sim_device_change',
                user_data.get('time_since_last_sim_change', 999),
            )
            or 999
        )

        if (sim_flag and dev_flag and hours <= DEVICE_CHANGE_AFTER_SIM_HOURS) or user_data.get(
            'device_changed_after_sim', False
        ):
            return True, f"Device changed within {hours:.1f}h of SIM change"
        return False, ""
    
    def check_failed_login_attempts(self, user_data: Dict) -> Tuple[bool, str]:
        """Rule: Multiple failed login attempts detected (login-based anomaly)."""
        count = user_data.get(
            'failed_logins_24h',
            user_data.get('num_failed_logins_last_24h', 0),
        )
        if count >= FAILED_LOGIN_COUNT_THRESHOLD:
            return True, f"High failed logins: {count} in 24h"
        return False, ""

    def check_sudden_location_change(self, user_data: Dict) -> Tuple[bool, str]:
        """Rule: Impossible travel or sudden location shift"""
        # New CSV directly provides pre-computed distance change
        dist = user_data.get('distance_change_km')
        if dist is not None:
            try:
                dist_val = float(dist)
            except (TypeError, ValueError):
                dist_val = 0.0
            if dist_val > LOCATION_DISTANCE_KM_THRESHOLD:
                return True, f"Sudden location jump: {dist_val:.1f} km (threshold: {LOCATION_DISTANCE_KM_THRESHOLD} km)"
            return False, ""

        # Legacy behaviour based on city names (fallback)
        prev = user_data.get('previous_city', '')
        curr = user_data.get('current_city', '')
        if prev and curr and prev != curr:
            dist_val = calculate_distance(prev, curr)
            if dist_val > LOCATION_DISTANCE_KM_THRESHOLD:
                return True, f"Sudden location jump: {prev} to {curr} ({dist_val}km)"
        return False, ""

    def check_roaming_after_sim_change(self, user_data: Dict) -> Tuple[bool, str]:
        """Rule: International roaming activated immediately after SIM change"""
        is_roaming = user_data.get('is_roaming', False)
        hours = user_data.get(
            'hours_since_sim_change',
            user_data.get('time_since_last_sim_change', 999),
        )
        
        if is_roaming and hours <= ROAMING_AFTER_SIM_HOURS:
            return True, "Roaming active shortly after SIM change"
        return False, ""

    # --- New per-user CSV rules ---

    def check_high_sim_swap_activity(self, user_data: Dict) -> Tuple[bool, str]:
        """Rule: Many SIM swap requests in last 30 days."""
        count = int(user_data.get('sim_swap_request_count_30d', 0) or 0)
        if count >= SIM_SWAP_REQUEST_HIGH_30D:
            return True, f"High SIM swap activity: {count} requests in 30 days (threshold: {SIM_SWAP_REQUEST_HIGH_30D})"
        return False, ""

    def check_recent_sim_swap(self, user_data: Dict) -> Tuple[bool, str]:
        """Rule: Recent SIM swap (small days_since_last_sim_swap)."""
        days = float(user_data.get('days_since_last_sim_swap', 1e9) or 1e9)
        if days <= DAYS_SINCE_LAST_SIM_RECENT:
            return True, f"Recent SIM swap: {days:.0f} days ago (≤ {DAYS_SINCE_LAST_SIM_RECENT} days)"
        return False, ""

    def check_device_or_location_change(self, user_data: Dict) -> Tuple[bool, str]:
        """Rule: Device or location changed around SIM activity."""
        device_flag = int(user_data.get('device_change_flag', 0) or 0)
        loc_flag = int(user_data.get('location_change_flag', 0) or 0)
        if device_flag or loc_flag:
            reasons: List[str] = []
            if device_flag:
                reasons.append("device change detected")
            if loc_flag:
                reasons.append("location change detected")
            return True, f"{' and '.join(reasons).capitalize()}"
        return False, ""

    def check_failed_otp_anomaly(self, user_data: Dict) -> Tuple[bool, str]:
        """Rule: Abnormally high failed OTP attempts in last 24h."""
        failed_otp = int(user_data.get('failed_otp_attempts_24h', 0) or 0)
        if failed_otp >= FAILED_OTP_HIGH_24H:
            return True, f"High failed OTP attempts: {failed_otp} in 24h (threshold: {FAILED_OTP_HIGH_24H})"
        return False, ""

    def check_account_age_risk(self, user_data: Dict) -> Tuple[bool, str]:
        """Rule: Very new account is more vulnerable."""
        age_days = float(user_data.get('account_age_days', 1e9) or 1e9)
        if age_days <= ACCOUNT_AGE_NEW_DAYS:
            return True, f"New account: {age_days:.0f} days old (≤ {ACCOUNT_AGE_NEW_DAYS} days)"
        return False, ""

    def check_usage_pattern_anomaly(self, user_data: Dict) -> Tuple[bool, str]:
        """
        Rule: Unusual usage pattern.
        Example: very low calls but high data spikes compared to thresholds.
        """
        # Support both monthly aggregates and last-24h behaviour.
        avg_calls = float(
            user_data.get(
                'avg_monthly_call_duration',
                user_data.get('num_calls_last_24h', 0),
            )
            or 0
        )
        avg_data = float(
            user_data.get(
                'avg_monthly_data_usage_gb',
                user_data.get('data_usage_last_24h', 0.0),
            )
            or 0.0
        )

        if avg_calls < AVG_CALL_DURATION_LOW_MIN and avg_data > AVG_DATA_USAGE_HIGH_GB:
            return True, (
                f"Unusual usage pattern: low call duration ({avg_calls:.1f} mins/mo) "
                f"with high data usage ({avg_data:.1f} GB/mo)"
            )
        return False, ""

    def check_contact_anomaly(self, user_data: Dict) -> Tuple[bool, str]:
        """Rule: Very few unique contacts in last 30 days (could be mule / bot)."""
        contacts = int(user_data.get('num_unique_contacts_30d', 0) or 0)
        if contacts <= UNIQUE_CONTACTS_LOW_30D:
            return True, f"Low contact diversity: {contacts} unique contacts in 30 days (≤ {UNIQUE_CONTACTS_LOW_30D})"
        return False, ""

    def check_security_events(self, user_data: Dict) -> Tuple[bool, str]:
        """Rule: Recent security events like password change."""
        pwd_change = int(user_data.get('recent_password_change_flag', 0) or 0)
        if pwd_change:
            return True, "Recent password change event detected"
        return False, ""

    def check_fraud_reported(self, user_data: Dict) -> Tuple[bool, str]:
        """Rule: This SIM/account has an associated fraud report flag."""
        fraud_flag = int(user_data.get('fraud_report_flag', 0) or 0)
        if fraud_flag:
            return True, "Fraud report flag present for this SIM/account"
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
        #you can adjust thresholds as needed
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
