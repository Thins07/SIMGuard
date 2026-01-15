"""
Configuration file for SIM Swap Detection System
Contains all rule thresholds and risk scoring parameters
"""

# ============================================================================
# RULE THRESHOLDS
# ============================================================================

# SIM Change Detection
SIM_CHANGE_HOURS_THRESHOLD = 72  # Flag if SIM changed within last 72 hours

# Device Change Detection
DEVICE_CHANGE_AFTER_SIM_HOURS = 48  # Flag if device changed within 48h of SIM change

# Location Change Detection
LOCATION_DISTANCE_KM_THRESHOLD = 100  # Flag if location changed >100km
LOCATION_TIME_HOURS_THRESHOLD = 2    # Within 2 hours

# Cell Tower Change Detection
CELL_TOWER_CHANGE_COUNT_THRESHOLD = 5  # Flag if >5 tower changes in short time

# Data Usage Detection
DATA_USAGE_INCREASE_PERCENT = 200  # Flag if data usage increased >200%
DATA_USAGE_DECREASE_PERCENT = 80   # Flag if data usage decreased >80%

# Call/SMS Pattern Detection
CALL_INCREASE_PERCENT = 300        # Flag if calls increased >300%
SMS_INCREASE_PERCENT = 300         # Flag if SMS increased >300%
CALL_DECREASE_PERCENT = 90         # Flag if calls decreased >90%
SMS_DECREASE_PERCENT = 90          # Flag if SMS decreased >90%

# Failed Login Detection
FAILED_LOGIN_COUNT_THRESHOLD = 3   # Flag if >3 failed logins in 24h

# Roaming Detection
ROAMING_AFTER_SIM_HOURS = 24       # Flag if roaming started within 24h of SIM change

# ============================================================================
# RISK SCORING WEIGHTS
# ============================================================================

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

# ============================================================================
# ALERT LEVEL THRESHOLDS
# ============================================================================

ALERT_THRESHOLDS = {
    'LOW': (0, 30),      # Risk score 0-30
    'MEDIUM': (31, 60),  # Risk score 31-60
    'HIGH': (61, 100)    # Risk score 61-100
}

# ============================================================================
# SRI LANKAN TELECOM DATA
# ============================================================================

SRI_LANKAN_CITIES = [
    'Colombo', 'Gampaha', 'Kalutara', 'Kandy', 'Matale', 'Nuwara Eliya',
    'Galle', 'Matara', 'Hambantota', 'Jaffna', 'Kilinochchi', 'Mannar',
    'Vavuniya', 'Mullaitivu', 'Batticaloa', 'Ampara', 'Trincomalee',
    'Kurunegala', 'Puttalam', 'Anuradhapura', 'Polonnaruwa', 'Badulla',
    'Monaragala', 'Ratnapura', 'Kegalle'
]

SRI_LANKAN_OPERATORS = ['Dialog', 'Mobitel', 'Hutch', 'Airtel']

# Approximate coordinates for major cities (for distance calculation)
CITY_COORDINATES = {
    'Colombo': (6.9271, 79.8612),
    'Gampaha': (7.0873, 79.9945),
    'Kalutara': (6.5854, 79.9607),
    'Kandy': (7.2906, 80.6337),
    'Matale': (7.4675, 80.6234),
    'Nuwara Eliya': (6.9497, 80.7891),
    'Galle': (6.0535, 80.2210),
    'Matara': (5.9549, 80.5550),
    'Hambantota': (6.1429, 81.1212),
    'Jaffna': (9.6615, 80.0255),
    'Batticaloa': (7.7310, 81.6747),
    'Trincomalee': (8.5874, 81.2152),
    'Kurunegala': (7.4818, 80.3609),
    'Anuradhapura': (8.3114, 80.4037),
    'Polonnaruwa': (7.9403, 81.0188),
    'Badulla': (6.9934, 81.0550),
    'Ratnapura': (6.7056, 80.3847),

    # Additional global cities used in sample datasets and tests
    'New York': (40.7128, -74.0060),
    'Los Angeles': (34.0522, -118.2437),
    'Chicago': (41.8781, -87.6298),
    'Miami': (25.7617, -80.1918),
    'Seattle': (47.6062, -122.3321),
    'Boston': (42.3601, -71.0589),
    'Dallas': (32.7767, -96.7970),
    'Phoenix': (33.4484, -112.0740),
    'Denver': (39.7392, -104.9903),
    'Atlanta': (33.7490, -84.3880),
    'Portland': (45.5152, -122.6784),
    'London': (51.5074, -0.1278)
}

# ============================================================================
# DATA FILE PATHS
# ============================================================================

DATA_FOLDER = 'data'
OUTPUT_FOLDER = 'output'

