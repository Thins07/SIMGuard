
"""
Configuration constants for SIM Swap Detection Rules.

There are two usage patterns:
1. Legacy log-based rules (hours since SIM change, roaming after SIM, etc.)
2. New per-user telco features used in the batch CSV format:
   user_id, phone_number, sim_swap_request_count_30d, days_since_last_sim_swap,
   device_change_flag, location_change_flag, failed_otp_attempts_24h,
   account_age_days, avg_monthly_call_duration, avg_monthly_data_usage_gb,
   num_unique_contacts_30d, recent_password_change_flag, fraud_report_flag.
"""

# --- Legacy thresholds (kept for backwards compatibility) ---
SIM_CHANGE_HOURS_THRESHOLD = 72
DEVICE_CHANGE_AFTER_SIM_HOURS = 48
LOCATION_DISTANCE_KM_THRESHOLD = 100
LOCATION_TIME_HOURS_THRESHOLD = 2
CELL_TOWER_CHANGE_COUNT_THRESHOLD = 5
FAILED_LOGIN_COUNT_THRESHOLD = 3
ROAMING_AFTER_SIM_HOURS = 24

# --- New per-user feature thresholds (batch CSV) ---

# How many SIM swap requests in the last 30 days is considered suspicious
SIM_SWAP_REQUEST_HIGH_30D = 2

# How many days since last SIM swap is considered "recent"
DAYS_SINCE_LAST_SIM_RECENT = 7

# Failed OTP attempts in last 24h considered abnormal
FAILED_OTP_HIGH_24H = 3

# Young account threshold (in days)
ACCOUNT_AGE_NEW_DAYS = 180

# Usage pattern thresholds
AVG_CALL_DURATION_LOW_MIN = 30          # minutes per month
AVG_DATA_USAGE_HIGH_GB = 10.0          # GB per month

# Contacts diversity thresholds
UNIQUE_CONTACTS_LOW_30D = 5

RISK_WEIGHTS = {
    # Legacy rule names (kept so older datasets still work)
    'recent_sim_change': 20,
    'device_change_after_sim': 25,
    'sudden_location_change': 15,
    'abnormal_cell_tower_change': 10,
    'abnormal_data_usage': 10,
    'abnormal_call_pattern': 8,
    'abnormal_sms_pattern': 7,
    'failed_login_attempts': 20,
    'roaming_after_sim_change': 15,

    # New per-user batch rules
    'high_sim_swap_activity': 30,
    'recent_sim_swap': 25,
    'device_or_location_change': 20,
    'failed_otp_anomaly': 20,
    'account_age_risk': 10,
    'usage_pattern_anomaly': 10,
    'contact_anomaly': 5,
    'security_events': 15,
    'fraud_reported': 40,
}

