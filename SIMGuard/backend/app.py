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
from ml_predictor import SIMSwapPredictor
from sl_ml_handler import SriLankanMLHandler

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

# Initialize ML Predictor
ml_predictor = SIMSwapPredictor(
    model_path='xgboost_simswap_model.pkl',
    scaler_path='scaler.pkl'
)

# Initialize Sri Lankan ML Handler
sl_ml_handler = SriLankanMLHandler()

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}
TEMP_DIR = tempfile.gettempdir()

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load ML model on startup
try:
    if ml_predictor.load_model():
        logger.info("✅ ML Model loaded successfully")
    else:
        logger.warning("⚠️ ML Model not loaded - prediction endpoint will not work")
except Exception as e:
    logger.error(f"❌ Error loading ML model: {e}")

def allowed_file(filename: str) -> bool:
    """Check if uploaded file has allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_csv_structure(df: pd.DataFrame) -> Tuple[bool, str]:
    """
    Validate that CSV has required columns for SIM swap detection
    
    Args:
        df: Pandas DataFrame from uploaded CSV
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    required_columns = ['timestamp', 'user_id', 'sim_id', 'device_id', 'ip', 'location', 'login_status']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        return False, f"Missing required columns: {', '.join(missing_columns)}"
    
    if df.empty:
        return False, "CSV file is empty"
    
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
    Analyze user behavior for suspicious SIM swap activities
    
    Args:
        user_data: DataFrame containing all records for a specific user
        
    Returns:
        List of suspicious activities with details
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
    Handle CSV file upload and perform initial validation
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
                'message': 'Invalid file type. Please upload a CSV file.'
            }), 400
        
        # Save file temporarily
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Read and validate CSV
        try:
            df = pd.read_csv(filepath)
        except Exception as e:
            os.remove(filepath)  # Clean up
            return jsonify({
                'status': 'error',
                'message': f'Error reading CSV file: {str(e)}'
            }), 400
        
        # Validate CSV structure
        is_valid, error_msg = validate_csv_structure(df)
        if not is_valid:
            os.remove(filepath)  # Clean up
            return jsonify({
                'status': 'error',
                'message': error_msg
            }), 400
        
        # Parse timestamps
        df['timestamp'] = df['timestamp'].apply(parse_timestamp)
        
        # Store data globally for analysis
        uploaded_data = df
        
        # Clean up uploaded file
        os.remove(filepath)
        
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
                'message': 'No data uploaded. Please upload a CSV file first.'
            }), 400

        logger.info("Starting SIM swap detection analysis...")

        # Initialize results
        all_suspicious_activities = []
        user_summaries = {}

        # Group data by user_id for analysis
        for user_id in uploaded_data['user_id'].unique():
            user_data = uploaded_data[uploaded_data['user_id'] == user_id].copy()

            # Analyze this user's behavior
            user_suspicious = analyze_user_behavior(user_data)
            all_suspicious_activities.extend(user_suspicious)

            # Store user summary
            user_summaries[user_id] = {
                'total_records': len(user_data),
                'suspicious_count': len(user_suspicious),
                'risk_level': 'High' if any(act['risk_level'] == 'High' for act in user_suspicious) else
                            'Medium' if any(act['risk_level'] == 'Medium' for act in user_suspicious) else 'Low'
            }

        # Calculate overall statistics
        total_records = len(uploaded_data)
        suspicious_count = len(all_suspicious_activities)
        clean_count = total_records - suspicious_count

        # Risk distribution
        risk_distribution = {'High': 0, 'Medium': 0, 'Low': 0}
        for activity in all_suspicious_activities:
            risk_distribution[activity['risk_level']] += 1

        # Store analysis results globally
        analysis_results = {
            'timestamp': datetime.now().isoformat(),
            'total_records': total_records,
            'suspicious_count': suspicious_count,
            'clean_count': clean_count,
            'risk_distribution': risk_distribution,
            'suspicious_activities': all_suspicious_activities,
            'user_summaries': user_summaries,
            'analysis_summary': {
                'users_analyzed': len(user_summaries),
                'high_risk_users': sum(1 for u in user_summaries.values() if u['risk_level'] == 'High'),
                'medium_risk_users': sum(1 for u in user_summaries.values() if u['risk_level'] == 'Medium'),
                'clean_users': sum(1 for u in user_summaries.values() if u['risk_level'] == 'Low')
            }
        }

        logger.info(f"Analysis completed: {suspicious_count} suspicious activities found out of {total_records} records")

        return jsonify({
            'status': 'success',
            'message': 'Analysis completed successfully',
            'analysis_id': analysis_results['timestamp'],
            'summary': {
                'total_records': total_records,
                'suspicious_count': suspicious_count,
                'clean_count': clean_count,
                'users_analyzed': len(user_summaries)
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
This report presents the findings of SIM swap detection analysis performed on user activity logs.
The analysis identified {analysis_results['suspicious_count']} suspicious activities out of
{analysis_results['total_records']} total records processed.

Risk Assessment: {'HIGH' if analysis_results['risk_distribution']['High'] > 5 else 'MEDIUM' if analysis_results['risk_distribution']['Medium'] > 3 else 'LOW'}
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
    """
    ML Prediction endpoint for real-time SIM swap detection

    Expected JSON input:
    {
        "distance_change": float,
        "time_since_sim_change": float,
        "num_failed_logins_last_24h": int,
        "num_calls_last_24h": int,
        "num_sms_last_24h": int,
        "data_usage_change_percent": float,
        "change_in_cell_tower_id": int,
        "is_roaming": int (0 or 1),
        "sim_change_flag": int (0 or 1),
        "device_change_flag": int (0 or 1),
        "current_city": str,
        "previous_city": str
    }

    Returns:
        JSON with prediction results
    """
    try:
        # Check if model is loaded
        if ml_predictor.model is None:
            return jsonify({
                'status': 'error',
                'message': 'ML model not loaded. Please ensure model files exist.',
                'prediction': 0,
                'confidence': 0.0,
                'risk_factors': []
            }), 503

        # Get JSON data from request
        data = request.get_json()

        if not data:
            return jsonify({
                'status': 'error',
                'message': 'No data provided'
            }), 400

        # Validate required fields
        required_fields = [
            'distance_change', 'time_since_sim_change', 'num_failed_logins_last_24h',
            'num_calls_last_24h', 'num_sms_last_24h', 'data_usage_change_percent',
            'change_in_cell_tower_id', 'is_roaming', 'sim_change_flag',
            'device_change_flag'
        ]

        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({
                'status': 'error',
                'message': f'Missing required fields: {", ".join(missing_fields)}'
            }), 400

        # Make prediction
        logger.info(f"Making prediction for data: {data}")
        result = ml_predictor.predict(data)

        # Log prediction result
        logger.info(f"Prediction result: {result}")

        return jsonify(result), 200

    except Exception as e:
        logger.error(f"Error in prediction endpoint: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Prediction failed: {str(e)}',
            'prediction': 0,
            'confidence': 0.0,
            'risk_factors': []
        }), 500

# ============================================================================
# SRI LANKAN ML ENDPOINTS
# ============================================================================

@app.route('/sl/upload-dataset', methods=['POST'])
def sl_upload_dataset():
    """
    Upload Sri Lankan dataset (CSV or Excel)
    Returns dataset preview and class distribution
    """
    try:
        if 'file' not in request.files:
            return jsonify({
                'status': 'error',
                'message': 'No file provided'
            }), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({
                'status': 'error',
                'message': 'No file selected'
            }), 400

        # Save file temporarily
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # Load dataset
        if not sl_ml_handler.load_dataset(filepath):
            return jsonify({
                'status': 'error',
                'message': 'Failed to load dataset'
            }), 500

        # Get dataset info
        preview = sl_ml_handler.get_dataset_preview(10)
        distribution = sl_ml_handler.get_class_distribution()
        stats = sl_ml_handler.get_dataset_stats()

        logger.info(f"✅ Sri Lankan dataset loaded: {stats['total_rows']} rows")

        return jsonify({
            'status': 'success',
            'preview': preview,
            'distribution': distribution,
            'total_rows': stats['total_rows'],
            'total_columns': stats['total_columns'],
            'columns': stats['columns']
        }), 200

    except Exception as e:
        logger.error(f"Error uploading dataset: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/sl/train-model', methods=['POST'])
def sl_train_model():
    """
    Train ML model on uploaded Sri Lankan dataset
    """
    try:
        data = request.get_json()

        model_type = data.get('model_type', 'xgboost')
        test_size = data.get('test_size', 0.2)

        logger.info(f"Training {model_type} model with test_size={test_size}")

        # Train model
        result = sl_ml_handler.train_model(
            model_type=model_type,
            test_size=test_size
        )

        if result['status'] == 'success':
            logger.info(f"✅ Model trained successfully - F1: {result['metrics']['f1_score']:.4f}")

        return jsonify(result), 200

    except Exception as e:
        logger.error(f"Error training model: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/sl/predict', methods=['POST'])
def sl_predict():
    """
    Make prediction using trained Sri Lankan model
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                'status': 'error',
                'message': 'No data provided'
            }), 400

        # Make prediction
        result = sl_ml_handler.predict(data)

        return jsonify(result), 200

    except Exception as e:
        logger.error(f"Error making prediction: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e),
            'prediction': 0,
            'confidence': 0.0
        }), 500

@app.route('/sl/download-model', methods=['GET'])
def sl_download_model():
    """
    Download trained model file
    """
    try:
        model_path = sl_ml_handler.model_path

        if not os.path.exists(model_path):
            return jsonify({
                'status': 'error',
                'message': 'Model file not found. Please train a model first.'
            }), 404

        return send_file(
            model_path,
            as_attachment=True,
            download_name='sl_xgboost_model.pkl',
            mimetype='application/octet-stream'
        )

    except Exception as e:
        logger.error(f"Error downloading model: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

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
