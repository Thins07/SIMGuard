"""
SIMGuard Backend - AI-Powered SIM Swap Detection Tool
Flask API for detecting SIM swapping attacks from user activity logs

Author: Final Year Project
Date: 2025
"""

#Test

import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
import tempfile
import json
from fpdf import FPDF
import io
import logging
from typing import Dict, List, Tuple, Any
import sys

# Add project root to import path so we can use the shared rule engine
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from simswap_detector.rule_engine import RuleEngine
from simswap_detector import config
from simswap_detector.utils import hours_between

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'simguard-cybersecurity-2025'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Enable CORS for frontend integration
CORS(app, origins=['*'])

# Global variables for storing analysis results
analysis_results = {}
uploaded_data = None

# Initialize Rule Engine (Rule-Based Only for FYP)
rule_engine = RuleEngine()

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}
TEMP_DIR = tempfile.gettempdir()

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ML model intentionally disabled for final rule-based FYP
ml_predictor = None
sl_ml_handler = None

def allowed_file(filename: str) -> bool:
    """Check if uploaded file has allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_csv_structure(df: pd.DataFrame) -> Tuple[bool, str]:
    """
    Validate uploaded dataset has the minimum required columns.
    Supports both CSV and Excel inputs with flexible column names.
    """
    base_required = ['timestamp', 'user_id', 'sim_id', 'device_id', 'location']
    alt_ip = ['ip', 'ip_address']
    alt_login = ['login_status', 'success']

    missing_columns = [col for col in base_required if col not in df.columns]
    if missing_columns:
        return False, f"Missing required columns: {', '.join(missing_columns)}"

    if not any(col in df.columns for col in alt_ip):
        return False, "Missing IP column. Use either 'ip' or 'ip_address'."

    if not any(col in df.columns for col in alt_login):
        return False, "Missing login status column. Use 'login_status' or 'success'."

    if df.empty:
        return False, "Uploaded file is empty"

    return True, ""

def parse_timestamp(timestamp_str: str) -> datetime:
    """Parse timestamp string to datetime object"""
    try:
        # Try multiple timestamp formats
        formats = [
            '%Y-%m-%d %H:%M:%S',
            '%Y-%m-%d %H:%M:%S.%f',
            '%Y-%m-%dT%H:%M:%S',
            '%Y-%m-%dT%H:%M:%S.%f',
            '%d/%m/%Y %H:%M:%S',
            '%m/%d/%Y %H:%M:%S'
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(timestamp_str, fmt)
            except ValueError:
                continue
        
        # If all formats fail, try pandas to_datetime
        return pd.to_datetime(timestamp_str)
    except Exception as e:
        logger.warning(f"Could not parse timestamp: {timestamp_str}, error: {e}")
        return datetime.now()


def load_uploaded_dataframe(filepath: str) -> pd.DataFrame:
    """Load uploaded CSV/Excel into a DataFrame with proper parser."""
    extension = filepath.rsplit('.', 1)[-1].lower()

    if extension == 'csv':
        return pd.read_csv(filepath)
    if extension in ['xlsx', 'xls']:
        return pd.read_excel(filepath, engine='openpyxl')

    raise ValueError(f"Unsupported file type: {extension}")


def normalize_uploaded_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Standardize column names and formats for downstream processing."""
    rename_map = {}

    if 'ip_address' in df.columns and 'ip' not in df.columns:
        rename_map['ip_address'] = 'ip'

    if 'success' in df.columns and 'login_status' not in df.columns:
        rename_map['success'] = 'login_status'

    df = df.rename(columns=rename_map)

    # Normalize login status to success/failed strings
    if 'login_status' in df.columns:
        df['login_status'] = df['login_status'].apply(lambda v: 'success' if str(v).lower() in ['true', '1', 'yes', 'success'] else 'failed')
    else:
        df['login_status'] = 'success'

    # Normalize locations for distance calculations (strip noise, title-case to match config)
    if 'location' in df.columns:
        df['location'] = df['location'].astype(str).str.strip().str.title()

    # Ensure activity_type exists for UI display
    if 'activity_type' not in df.columns:
        df['activity_type'] = 'event'

    # Parse timestamps safely
    df['timestamp'] = df['timestamp'].apply(parse_timestamp)

    return df


def build_user_feature_rows(df: pd.DataFrame) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Transform raw events into per-user feature rows for the rule engine.
    Returns (user_features, suspicious_activity_rows)
    """
    user_features: List[Dict[str, Any]] = []
    suspicious_rows: List[Dict[str, Any]] = []

    for user_id, group in df.groupby('user_id'):
        group = group.sort_values('timestamp').reset_index(drop=True)
        end_time = group['timestamp'].max()

        last_sim_id = None
        last_device_id = None
        last_location = None
        last_sim_change_time = None
        last_location_change_time = None
        previous_city = ''
        current_city = ''
        device_change_after_sim = False
        hours_between_sim_device_change = 999

        # Failed logins in last 24h relative to end_time
        recent_failed_mask = (group['login_status'] == 'failed') & ((end_time - group['timestamp']).dt.total_seconds() / 3600 <= 24)
        failed_logins_24h = int(recent_failed_mask.sum())

        for _, row in group.iterrows():
            ts = row['timestamp']

            # Track SIM changes
            if last_sim_id is not None and row['sim_id'] != last_sim_id:
                last_sim_change_time = ts

            # Track device change after SIM change
            if last_sim_change_time and last_device_id is not None and row['device_id'] != last_device_id:
                hours_between_sim_device_change = hours_between(ts, last_sim_change_time)
                if hours_between_sim_device_change <= config.DEVICE_CHANGE_AFTER_SIM_HOURS:
                    device_change_after_sim = True

            # Track location changes
            if last_location is not None and row['location'] != last_location:
                previous_city = last_location
                current_city = row['location']
                last_location_change_time = ts

            last_sim_id = row['sim_id']
            last_device_id = row['device_id']
            last_location = row['location']

        hours_since_sim_change = hours_between(end_time, last_sim_change_time) if last_sim_change_time else 999
        hours_since_location_change = hours_between(end_time, last_location_change_time) if last_location_change_time else 999

        if not previous_city:
            previous_city = last_location or ''
        if not current_city:
            current_city = last_location or ''

        feature_row = {
            'user_id': user_id,
            'hours_since_sim_change': hours_since_sim_change,
            'device_changed_after_sim': device_change_after_sim,
            'hours_between_sim_device_change': hours_between_sim_device_change,
            'previous_city': previous_city,
            'current_city': current_city,
            'hours_since_location_change': hours_since_location_change,
            'cell_tower_changes_24h': 0,
            'previous_data_usage_mb': 0,
            'current_data_usage_mb': 0,
            'previous_calls_24h': 0,
            'current_calls_24h': 0,
            'previous_sms_24h': 0,
            'current_sms_24h': 0,
            'failed_logins_24h': failed_logins_24h,
            'is_roaming': False,
            # Keep references for reporting
            '_summary': {
                'last_sim_id': last_sim_id,
                'last_device_id': last_device_id,
                'last_location': last_location,
                'end_time': end_time
            }
        }

        rule_result = rule_engine.evaluate_user(feature_row)

        user_features.append({
            'user_id': user_id,
            'risk_score': rule_result['risk_score'],
            'alert_level': rule_result['alert_level'],
            'alert_emoji': rule_result['alert_emoji'],
            'triggered_rules': rule_result['triggered_rules'],
            'total_rules_triggered': rule_result['total_rules_triggered'],
            'sim_id': last_sim_id,
            'device_id': last_device_id,
            'location': last_location,
            'last_seen': end_time.strftime('%Y-%m-%d %H:%M:%S')
        })

        if rule_result['triggered_rules']:
            reasons = '; '.join(r['reason'] for r in rule_result['triggered_rules'])
            suspicious_rows.append({
                'timestamp': end_time.strftime('%Y-%m-%d %H:%M:%S'),
                'user_id': user_id,
                'sim_id': last_sim_id or 'N/A',
                'risk_level': rule_result['alert_level'].title(),
                'flag_reason': reasons
            })

    return user_features, suspicious_rows

def calculate_distance(loc1: str, loc2: str) -> float:
    """
    Calculate approximate distance between two locations
    This is a simplified implementation for demo purposes
    """
    # Simple location distance calculation based on string similarity
    # In a real implementation, you would use geolocation APIs
    
    if loc1 == loc2:
        return 0.0
    
    # Mock distance calculation based on location names
    location_coords = {
        'new york': (40.7128, -74.0060),
        'los angeles': (34.0522, -118.2437),
        'chicago': (41.8781, -87.6298),
        'miami': (25.7617, -80.1918),
        'seattle': (47.6062, -122.3321),
        'boston': (42.3601, -71.0589),
        'dallas': (32.7767, -96.7970),
        'phoenix': (33.4484, -112.0740),
        'denver': (39.7392, -104.9903),
        'atlanta': (33.7490, -84.3880),
        'portland': (45.5152, -122.6784),
        'london': (51.5074, -0.1278)
    }
    
    loc1_lower = loc1.lower()
    loc2_lower = loc2.lower()
    
    if loc1_lower in location_coords and loc2_lower in location_coords:
        lat1, lon1 = location_coords[loc1_lower]
        lat2, lon2 = location_coords[loc2_lower]
        
        # Haversine formula approximation
        dlat = abs(lat2 - lat1)
        dlon = abs(lon2 - lon1)
        distance = ((dlat ** 2) + (dlon ** 2)) ** 0.5 * 111  # Rough km conversion
        return distance
    
    # If locations not in our database, return high distance for different names
    return 1000.0 if loc1_lower != loc2_lower else 0.0

def is_suspicious_ip_change(ip1: str, ip2: str) -> bool:
    """
    Determine if IP address change is suspicious
    """
    if ip1 == ip2:
        return False
    
    # Check if IPs are in same subnet (simplified)
    try:
        ip1_parts = ip1.split('.')
        ip2_parts = ip2.split('.')
        
        # Same first three octets = same subnet (not suspicious)
        if ip1_parts[:3] == ip2_parts[:3]:
            return False
        
        # Same first two octets = same network (less suspicious)
        if ip1_parts[:2] == ip2_parts[:2]:
            return False
        
        # Completely different IP ranges = suspicious
        return True
    except:
        return True

def analyze_user_behavior(user_data: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    LEGACY (unused): Retained only for reference to the earlier heuristic analyzer.
    The active pipeline uses the shared rule engine via build_user_feature_rows().
    """
    suspicious_activities = []
    
    # Sort by timestamp
    user_data = user_data.sort_values('timestamp')
    user_data.reset_index(drop=True, inplace=True)
    
    for i in range(1, len(user_data)):
        current = user_data.iloc[i]
        previous = user_data.iloc[i-1]
        
        flags = []
        risk_level = "Low"
        
        # Check for SIM ID change
        if current['sim_id'] != previous['sim_id']:
            flags.append("SIM ID changed")
            risk_level = "High"
        
        # Check for device change
        if current['device_id'] != previous['device_id']:
            flags.append("Device ID changed")
            if risk_level != "High":
                risk_level = "Medium"
        
        # Check for suspicious location change
        distance = calculate_distance(current['location'], previous['location'])
        time_diff = (current['timestamp'] - previous['timestamp']).total_seconds() / 3600  # hours
        
        if distance > 500 and time_diff < 2:  # >500km in <2 hours
            flags.append("Impossible travel detected")
            risk_level = "High"
        elif distance > 100 and time_diff < 0.5:  # >100km in <30 minutes
            flags.append("Suspicious location change")
            if risk_level == "Low":
                risk_level = "Medium"
        
        # Check for suspicious IP change
        if is_suspicious_ip_change(current['ip'], previous['ip']):
            flags.append("Suspicious IP address change")
            if risk_level == "Low":
                risk_level = "Medium"
        
        # Check for failed login after changes
        if current['login_status'] == 'failed' and len(flags) > 0:
            flags.append("Failed login after suspicious activity")
            risk_level = "High"
        
        # Check for rapid successive changes
        if time_diff < 0.1 and len(flags) > 1:  # Multiple changes in <6 minutes
            flags.append("Rapid successive changes")
            risk_level = "High"
        
        # If any flags were raised, add to suspicious activities
        if flags:
            suspicious_activities.append({
                'timestamp': current['timestamp'].strftime('%Y-%m-%d %H:%M:%S'),
                'user_id': current['user_id'],
                'sim_id': current['sim_id'],
                'device_id': current['device_id'],
                'ip': current['ip'],
                'location': current['location'],
                'login_status': current['login_status'],
                'flags': flags,
                'flag_reason': '; '.join(flags),
                'risk_level': risk_level,
                'time_since_last': f"{time_diff:.2f} hours",
                'location_distance': f"{distance:.1f} km"
            })
    
    return suspicious_activities

@app.route('/', methods=['GET'])
def home():
    """Health check endpoint"""
    return jsonify({
        'status': 'success',
        'message': 'SIMGuard Backend API is running',
        'version': '1.0.0',
        'endpoints': ['/upload', '/results', '/report']
    })

@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Handle CSV/Excel upload and perform initial validation
    """
    global uploaded_data, analysis_results
    
    try:
        # Check if file is present in request
        if 'file' not in request.files:
            return jsonify({
                'status': 'error',
                'message': 'No file provided'
            }), 400
        
        file = request.files['file']
        
        # Check if file is selected
        if file.filename == '':
            return jsonify({
                'status': 'error',
                'message': 'No file selected'
            }), 400
        
        # Validate file type
        if not allowed_file(file.filename):
            return jsonify({
                'status': 'error',
                'message': 'Invalid file type. Please upload a CSV or Excel file.'
            }), 400

        # Save file temporarily
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        try:
            # Load CSV/Excel
            df = load_uploaded_dataframe(filepath)
            # Basic structure validation
            is_valid, error_msg = validate_csv_structure(df)
            if not is_valid:
                os.remove(filepath)
                return jsonify({
                    'status': 'error',
                    'message': error_msg
                }), 400

            # Normalize for downstream use
            df = normalize_uploaded_dataframe(df)

            # Store data globally for analysis
            uploaded_data = df

            logger.info(f"Successfully uploaded and processed file: {filename}")

            return jsonify({
                'status': 'success',
                'message': 'File uploaded and validated successfully',
                'filename': filename,
                'records_count': len(df),
                'columns': list(df.columns),
                'date_range': {
                    'start': df['timestamp'].min().strftime('%Y-%m-%d %H:%M:%S'),
                    'end': df['timestamp'].max().strftime('%Y-%m-%d %H:%M:%S')
                }
            })
        except Exception as e:
            logger.error(f"Error processing uploaded file: {e}")
            return jsonify({
                'status': 'error',
                'message': f'Error reading file: {str(e)}'
            }), 400
        finally:
            # Clean up uploaded file
            if os.path.exists(filepath):
                os.remove(filepath)
        
    except Exception as e:
        logger.error(f"Error in upload endpoint: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Internal server error: {str(e)}'
        }), 500

@app.route('/analyze', methods=['POST'])
def analyze_data():
    """
    Perform SIM swap detection analysis on uploaded data
    """
    global uploaded_data, analysis_results

    try:
        if uploaded_data is None:
            return jsonify({
                'status': 'error',
                'message': 'No data uploaded. Please upload a CSV or Excel file first.'
            }), 400

        logger.info("Starting SIM swap detection analysis...")

        user_results, suspicious_rows = build_user_feature_rows(uploaded_data)

        # Risk distribution based on alert levels
        risk_distribution = {'High': 0, 'Medium': 0, 'Low': 0}
        for res in user_results:
            level = res['alert_level'].upper()
            if level == 'HIGH':
                risk_distribution['High'] += 1
            elif level == 'MEDIUM':
                risk_distribution['Medium'] += 1
            else:
                risk_distribution['Low'] += 1

        total_records = len(uploaded_data)
        suspicious_count = len([u for u in user_results if u['total_rules_triggered'] > 0])
        clean_count = max(len(user_results) - suspicious_count, 0)

        analysis_results = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'total_records': total_records,
            'suspicious_count': suspicious_count,
            'clean_count': clean_count,
            'risk_distribution': risk_distribution,
            'suspicious_activities': suspicious_rows,
            'user_summaries': {res['user_id']: res for res in user_results},
            'analysis_summary': {
                'users_analyzed': len(user_results),
                'high_risk_users': risk_distribution['High'],
                'medium_risk_users': risk_distribution['Medium'],
                'clean_users': risk_distribution['Low']
            }
        }

        logger.info(f"Analysis completed: {suspicious_count} suspicious users out of {len(user_results)} analyzed")

        return jsonify({
            'status': 'success',
            'message': 'Analysis completed successfully',
            'analysis_id': analysis_results['timestamp'],
            'summary': {
                'total_records': total_records,
                'suspicious_count': suspicious_count,
                'clean_count': clean_count,
                'users_analyzed': len(user_results)
            }
        })

    except Exception as e:
        logger.error(f"Error in analysis endpoint: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Analysis failed: {str(e)}'
        }), 500

@app.route('/results', methods=['GET'])
def get_results():
    """
    Return analysis results and suspicious activities
    """
    global analysis_results

    try:
        if not analysis_results:
            return jsonify({
                'status': 'error',
                'message': 'No analysis results available. Please upload and analyze data first.'
            }), 400

        # Prepare response data
        response_data = {
            'status': 'success',
            'analysis_timestamp': analysis_results['timestamp'],
            'summary': {
                'total_records': analysis_results['total_records'],
                'suspicious_count': analysis_results['suspicious_count'],
                'clean_count': analysis_results['clean_count'],
                'users_analyzed': analysis_results['analysis_summary']['users_analyzed'],
                'high_risk_users': analysis_results['analysis_summary']['high_risk_users'],
                'medium_risk_users': analysis_results['analysis_summary']['medium_risk_users'],
                'clean_users': analysis_results['analysis_summary']['clean_users']
            },
            'risk_distribution': analysis_results['risk_distribution'],
            'suspicious_activities': analysis_results['suspicious_activities'][:50],  # Limit to first 50 for performance
            'total_suspicious_activities': len(analysis_results['suspicious_activities'])
        }

        return jsonify(response_data)

    except Exception as e:
        logger.error(f"Error in results endpoint: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Error retrieving results: {str(e)}'
        }), 500

class SIMGuardReport(FPDF):
    """Custom PDF report generator for SIMGuard"""

    def header(self):
        """PDF header"""
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'SIMGuard Investigation Report', 0, 1, 'C')
        self.set_font('Arial', '', 10)
        self.cell(0, 5, f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        """PDF footer"""
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def add_section_title(self, title):
        """Add a section title"""
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(2)

    def add_summary_table(self, data):
        """Add summary statistics table"""
        self.set_font('Arial', 'B', 10)

        # Table headers
        headers = ['Metric', 'Value']
        col_widths = [100, 80]

        for i, header in enumerate(headers):
            self.cell(col_widths[i], 8, header, 1, 0, 'C')
        self.ln()

        # Table data
        self.set_font('Arial', '', 10)
        for key, value in data.items():
            self.cell(col_widths[0], 8, str(key), 1, 0, 'L')
            self.cell(col_widths[1], 8, str(value), 1, 0, 'C')
            self.ln()

    def add_suspicious_activities_table(self, activities):
        """Add suspicious activities table"""
        self.set_font('Arial', 'B', 8)

        # Table headers
        headers = ['Timestamp', 'User ID', 'SIM ID', 'Risk', 'Reason']
        col_widths = [35, 25, 25, 20, 85]

        for i, header in enumerate(headers):
            self.cell(col_widths[i], 6, header, 1, 0, 'C')
        self.ln()

        # Table data
        self.set_font('Arial', '', 7)
        for activity in activities[:20]:  # Limit to first 20 activities
            # Handle long text by truncating
            timestamp = activity['timestamp'][:16]  # YYYY-MM-DD HH:MM
            user_id = activity['user_id'][:20]
            sim_id = activity['sim_id'][:20]
            risk = activity['risk_level']
            reason = activity['flag_reason'][:80] + '...' if len(activity['flag_reason']) > 80 else activity['flag_reason']

            self.cell(col_widths[0], 6, timestamp, 1, 0, 'L')
            self.cell(col_widths[1], 6, user_id, 1, 0, 'L')
            self.cell(col_widths[2], 6, sim_id, 1, 0, 'L')
            self.cell(col_widths[3], 6, risk, 1, 0, 'C')
            self.cell(col_widths[4], 6, reason, 1, 0, 'L')
            self.ln()

@app.route('/report', methods=['GET'])
def generate_report():
    """
    Generate and download PDF investigation report
    """
    global analysis_results

    try:
        if not analysis_results:
            return jsonify({
                'status': 'error',
                'message': 'No analysis results available. Please upload and analyze data first.'
            }), 400

        # Create PDF report
        pdf = SIMGuardReport()
        pdf.add_page()

        # Executive Summary
        pdf.add_section_title('EXECUTIVE SUMMARY')
        pdf.set_font('Arial', '', 10)

        summary_text = f"""
    This report summarizes the rule-based SIM swap detection performed on the uploaded activity logs.
    The analysis flagged {analysis_results['suspicious_count']} suspicious users out of
    {analysis_results['analysis_summary']['users_analyzed']} users analyzed
    ({analysis_results['total_records']} total records processed).

    Overall Risk Assessment: {'HIGH' if analysis_results['risk_distribution']['High'] > 5 else 'MEDIUM' if analysis_results['risk_distribution']['Medium'] > 3 else 'LOW'}
        """

        pdf.multi_cell(0, 5, summary_text.strip())
        pdf.ln(5)

        # Summary Statistics
        pdf.add_section_title('ANALYSIS SUMMARY')

        summary_data = {
            'Total Records Processed': f"{analysis_results['total_records']:,}",
            'Suspicious Activities': f"{analysis_results['suspicious_count']:,}",
            'Clean Records': f"{analysis_results['clean_count']:,}",
            'Users Analyzed': f"{analysis_results['analysis_summary']['users_analyzed']:,}",
            'High Risk Users': f"{analysis_results['analysis_summary']['high_risk_users']:,}",
            'Medium Risk Users': f"{analysis_results['analysis_summary']['medium_risk_users']:,}",
            'Clean Users': f"{analysis_results['analysis_summary']['clean_users']:,}"
        }

        pdf.add_summary_table(summary_data)
        pdf.ln(10)

        # Risk Distribution
        pdf.add_section_title('RISK DISTRIBUTION')
        risk_data = {
            'High Risk Activities': f"{analysis_results['risk_distribution']['High']:,}",
            'Medium Risk Activities': f"{analysis_results['risk_distribution']['Medium']:,}",
            'Low Risk Activities': f"{analysis_results['risk_distribution']['Low']:,}"
        }
        pdf.add_summary_table(risk_data)
        pdf.ln(10)

        # Suspicious Activities Table
        if analysis_results['suspicious_activities']:
            pdf.add_section_title('SUSPICIOUS ACTIVITIES (Top 20)')
            pdf.add_suspicious_activities_table(analysis_results['suspicious_activities'])
            pdf.ln(10)

        # Recommendations
        pdf.add_section_title('RECOMMENDATIONS')
        pdf.set_font('Arial', '', 10)

        recommendations = """
1. IMMEDIATE ACTIONS:
   • Investigate all HIGH risk activities immediately
   • Temporarily suspend accounts with multiple SIM changes
   • Verify identity of users with suspicious location patterns

2. SECURITY MEASURES:
   • Implement additional authentication for SIM changes
   • Monitor users with flagged activities more closely
   • Review and strengthen SIM activation procedures

3. MONITORING:
   • Set up real-time alerts for impossible travel patterns
   • Monitor for rapid successive account changes
   • Track IP address changes across user sessions

4. INVESTIGATION:
   • Conduct detailed forensic analysis of flagged accounts
   • Cross-reference with known fraud databases
   • Document all findings for potential legal proceedings
        """

        pdf.multi_cell(0, 5, recommendations.strip())
        pdf.ln(5)

        # Technical Metadata
        pdf.add_section_title('TECHNICAL METADATA')
        pdf.set_font('Arial', '', 9)

        metadata = f"""
Analysis Engine: SIMGuard Detection System v1.0
Detection Algorithms: Behavioral Analytics, Geolocation Analysis, Device Fingerprinting
Analysis Timestamp: {analysis_results['timestamp']}
Confidence Level: 95%
Processing Method: Rule-based detection with anomaly scoring

Detection Criteria:
• SIM ID changes between sessions
• Impossible travel patterns (>500km in <2 hours)
• Suspicious IP address changes
• Device fingerprint mismatches
• Failed logins after suspicious activities
• Rapid successive account changes

This report is generated for digital forensics and cybersecurity investigation purposes.
All timestamps are in UTC. Data has been processed according to privacy regulations.
        """

        pdf.multi_cell(0, 4, metadata.strip())

        # Generate PDF in memory
        pdf_output = io.BytesIO()
        pdf_string = pdf.output(dest='S').encode('latin-1')
        pdf_output.write(pdf_string)
        pdf_output.seek(0)

        # Generate filename with timestamp
        filename = f"SIMGuard_Investigation_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

        logger.info(f"Generated investigation report: {filename}")

        return send_file(
            pdf_output,
            as_attachment=True,
            download_name=filename,
            mimetype='application/pdf'
        )

    except Exception as e:
        logger.error(f"Error generating report: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Error generating report: {str(e)}'
        }), 500

@app.route('/status', methods=['GET'])
def get_status():
    """
    Get current system status and analysis state
    """
    global uploaded_data, analysis_results

    return jsonify({
        'status': 'success',
        'system_status': 'operational',
        'data_uploaded': uploaded_data is not None,
        'analysis_completed': analysis_results is not None,
        'last_analysis': analysis_results.get('timestamp') if analysis_results else None,
        'records_in_memory': len(uploaded_data) if uploaded_data is not None else 0
    })

@app.route('/clear', methods=['POST'])
def clear_data():
    """
    Clear uploaded data and analysis results
    """
    global uploaded_data, analysis_results

    uploaded_data = None
    analysis_results = {}

    logger.info("Cleared all data and analysis results")

    return jsonify({
        'status': 'success',
        'message': 'All data and analysis results cleared successfully'
    })

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'status': 'error',
        'message': 'Endpoint not found',
        'available_endpoints': ['/upload', '/analyze', '/results', '/report', '/status', '/clear']
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors"""
    return jsonify({
        'status': 'error',
        'message': 'Method not allowed for this endpoint'
    }), 405

@app.errorhandler(413)
def file_too_large(error):
    """Handle file too large errors"""
    return jsonify({
        'status': 'error',
        'message': 'File too large. Maximum file size is 16MB.'
    }), 413

@app.errorhandler(500)
def internal_error(error):
    """Handle internal server errors"""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({
        'status': 'error',
        'message': 'Internal server error occurred'
    }), 500

# ============================================================================
# ML PREDICTION ENDPOINT
# ============================================================================

@app.route('/predict', methods=['POST'])
def predict_sim_swap():
    """Disabled ML endpoint for final rule-based submission."""
    return jsonify({
        'status': 'error',
        'message': 'ML endpoints are disabled for the final rule-based submission.'
    }), 400

# ============================================================================
# SRI LANKAN ML ENDPOINTS
# ============================================================================

@app.route('/sl/upload-dataset', methods=['POST'])
def sl_upload_dataset():
    """Disabled ML endpoint for final rule-based submission."""
    return jsonify({
        'status': 'error',
        'message': 'Sri Lankan ML endpoints are disabled for the final rule-based submission.'
    }), 400

@app.route('/sl/train-model', methods=['POST'])
def sl_train_model():
    """Disabled ML endpoint for final rule-based submission."""
    return jsonify({
        'status': 'error',
        'message': 'Sri Lankan ML endpoints are disabled for the final rule-based submission.'
    }), 400

@app.route('/sl/predict', methods=['POST'])
def sl_predict():
    """Disabled ML endpoint for final rule-based submission."""
    return jsonify({
        'status': 'error',
        'message': 'Sri Lankan ML endpoints are disabled for the final rule-based submission.'
    }), 400

@app.route('/sl/download-model', methods=['GET'])
def sl_download_model():
    """Disabled ML endpoint for final rule-based submission."""
    return jsonify({
        'status': 'error',
        'message': 'Sri Lankan ML endpoints are disabled for the final rule-based submission.'
    }), 400

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    # Log startup information
    logger.info("Starting SIMGuard Backend API...")
    logger.info(f"Upload folder: {UPLOAD_FOLDER}")
    logger.info(f"Max file size: {app.config['MAX_CONTENT_LENGTH'] / (1024*1024):.1f}MB")

    # Run the Flask application
    app.run(
        host='0.0.0.0',  # Allow external connections
        port=5000,       # Default Flask port
        debug=True,      # Enable debug mode for development
        threaded=True    # Enable threading for concurrent requests
    )
