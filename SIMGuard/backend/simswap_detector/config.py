
"""
Configuration constants for SIM Swap Detection Rules
"""

SIM_CHANGE_HOURS_THRESHOLD = 72
DEVICE_CHANGE_AFTER_SIM_HOURS = 48
LOCATION_DISTANCE_KM_THRESHOLD = 100
LOCATION_TIME_HOURS_THRESHOLD = 2
CELL_TOWER_CHANGE_COUNT_THRESHOLD = 5
FAILED_LOGIN_COUNT_THRESHOLD = 3
ROAMING_AFTER_SIM_HOURS = 24

RISK_WEIGHTS = {
    'recent_sim_change': 20,
    'device_change_after_sim': 25,
    'sudden_location_change': 15,
    'abnormal_cell_tower_change': 10,
    'abnormal_data_usage': 10,
    'abnormal_call_pattern': 8,
    'abnormal_sms_pattern': 7,
    'failed_login_attempts': 20,
    'roaming_after_sim_change': 15
}
