"""
Utility functions for distance calculation and formatting
"""
from datetime import datetime

def calculate_distance(city1, city2):
    # Mock distance calculation for demo purposes
    # In a real app, this would use Geopy or similar
    if not city1 or not city2: return 0
    if city1.lower() == city2.lower(): return 0
    return 150 # Mock distance for different cities

def hours_between(dt1, dt2):
    if not dt1 or not dt2: return 0
    return abs((dt1 - dt2).total_seconds()) / 3600.0

def percentage_change(old, new):
    if old == 0: return 0
    return ((new - old) / old) * 100

def format_alert_level(score):
    if score >= 60: return 'HIGH'
    if score >= 30: return 'MEDIUM'
    return 'LOW'

def format_alert_emoji(level):
    if level == 'HIGH': return '🚨'
    if level == 'MEDIUM': return '⚠️'
    return '✅'
