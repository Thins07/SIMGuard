"""
Utility functions for SIM Swap Detection System
"""

import math
from datetime import datetime, timedelta
from typing import Tuple
from .config import CITY_COORDINATES


def calculate_distance(city1: str, city2: str) -> float:
    """
    Calculate distance between two cities using Haversine formula
    
    Args:
        city1: First city name
        city2: Second city name
        
    Returns:
        Distance in kilometers
    """
    if city1 not in CITY_COORDINATES or city2 not in CITY_COORDINATES:
        return 0.0
    
    lat1, lon1 = CITY_COORDINATES[city1]
    lat2, lon2 = CITY_COORDINATES[city2]
    
    # Haversine formula
    R = 6371  # Earth's radius in kilometers
    
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)
    
    a = math.sin(delta_lat / 2) ** 2 + \
        math.cos(lat1_rad) * math.cos(lat2_rad) * \
        math.sin(delta_lon / 2) ** 2
    
    c = 2 * math.asin(math.sqrt(a))
    
    distance = R * c
    return round(distance, 2)


def parse_datetime(dt_str: str) -> datetime:
    """
    Parse datetime string to datetime object
    
    Args:
        dt_str: Datetime string in various formats
        
    Returns:
        datetime object
    """
    formats = [
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%d %H:%M:%S.%f',
        '%Y-%m-%dT%H:%M:%S',
        '%Y/%m/%d %H:%M:%S',
        '%d-%m-%Y %H:%M:%S'
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(str(dt_str), fmt)
        except ValueError:
            continue
    
    # If all formats fail, try pandas
    try:
        import pandas as pd
        return pd.to_datetime(dt_str)
    except:
        raise ValueError(f"Unable to parse datetime: {dt_str}")


def hours_between(dt1: datetime, dt2: datetime) -> float:
    """
    Calculate hours between two datetime objects
    
    Args:
        dt1: First datetime
        dt2: Second datetime
        
    Returns:
        Hours between the two datetimes (absolute value)
    """
    delta = abs(dt2 - dt1)
    return delta.total_seconds() / 3600


def format_alert_level(risk_score: int) -> str:
    """
    Determine alert level based on risk score
    
    Args:
        risk_score: Risk score (0-100)
        
    Returns:
        Alert level: 'LOW', 'MEDIUM', or 'HIGH'
    """
    from config import ALERT_THRESHOLDS
    
    for level, (min_score, max_score) in ALERT_THRESHOLDS.items():
        if min_score <= risk_score <= max_score:
            return level
    
    return 'HIGH' if risk_score > 60 else 'LOW'


def format_alert_emoji(alert_level: str) -> str:
    """
    Get emoji for alert level
    
    Args:
        alert_level: 'LOW', 'MEDIUM', or 'HIGH'
        
    Returns:
        Emoji string
    """
    emojis = {
        'LOW': '✅',
        'MEDIUM': '⚠️',
        'HIGH': '🚨'
    }
    return emojis.get(alert_level, '❓')


def percentage_change(old_value: float, new_value: float) -> float:
    """
    Calculate percentage change between two values
    
    Args:
        old_value: Original value
        new_value: New value
        
    Returns:
        Percentage change
    """
    if old_value == 0:
        return 0.0 if new_value == 0 else 100.0
    
    change = ((new_value - old_value) / old_value) * 100
    return round(change, 2)