"""
SIMGuard Backend - AI-Powered SIM Swap Detection Tool
Flask API for detecting SIM swapping attacks from user activity logs

Author: Final Year Project
Date: 2025
"""

import os
import sys

# CRITICAL: Explicitly add the backend directory to sys.path to ensure module resolution works
# regardless of how the script is executed (direct python call, via run.py, etc.)
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

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

# Import custom modules
# We wrap these in try-except blocks to give better error messages if imports fail
try:
    from ml_core import ThinkerModel
    from simswap_detector.rule_engine import RuleEngine
    from simswap_detector import config
    from simswap_detector.utils import hours_between
except ImportError as e:
    print(f"❌ Import Error in app.py: {e}")
    print(f"   sys.path is: {sys.path}")
    raise e

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'simguard-cybersecurity-2025'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Enable CORS for frontend integration
CORS(app, origins=['*'])

# Global variables
analysis_results = {}
uploaded_data = None
ml_engine = ThinkerModel() # Initialize the Thinker ML Engine
rule_engine = RuleEngine() # Initialize Rule Engine

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def parse_timestamp(timestamp_str: str) -> datetime:
    try:
        formats = ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M:%S.%f', '%Y-%m-%dT%H:%M:%S', '%d/%m/%Y %H:%M:%S']
        for fmt in formats:
            try:
                return datetime.strptime(str(timestamp_str), fmt)
            except ValueError:
                continue
        return pd.to_datetime(timestamp_str)
    except Exception as e:
        return datetime.now()

def load_uploaded_dataframe(filepath: str) -> pd.DataFrame:
    extension = filepath.rsplit('.', 1)[-1].lower()
    if extension == 'csv': return pd.read_csv(filepath)
    if extension in ['xlsx', 'xls']: return pd.read_excel(filepath, engine='openpyxl')
    raise ValueError(f"Unsupported file type: {extension}")

def normalize_uploaded_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    rename_map = {}
    if 'ip_address' in df.columns and 'ip' not in df.columns: rename_map['ip_address'] = 'ip'
    if 'success' in df.columns and 'login_status' not in df.columns: rename_map['success'] = 'login_status'
    df = df.rename(columns=rename_map)
    
    # Normalize Login Status
    if 'login_status' in df.columns:
        df['login_status'] = df['login_status'].apply(lambda v: 'success' if str(v).lower() in ['true', '1', 'yes', 'success'] else 'failed')
    else: df['login_status'] = 'success'
    
    # Normalize Location
    if 'location' in df.columns: df['location'] = df['location'].astype(str).str.strip().str.title()
    
    # Normalize Roaming (if present)
    if 'is_roaming' not in df.columns and 'roaming' in df.columns:
        df['is_roaming'] = df['roaming']
    
    if 'activity_type' not in df.columns: df['activity_type'] = 'event'
    df['timestamp'] = df['timestamp'].apply(parse_timestamp)
    return df

def build_user_feature_rows(df: pd.DataFrame) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """Transform raw events into per-user feature rows for the rule engine."""
    user_features = []
    suspicious_rows = []

    for user_id, group in df.groupby('user_id'):
        group = group.sort_values('timestamp').reset_index(drop=True)
        end_time = group['timestamp'].max()
        
        # Calculate heuristics
        last_sim_id = None
        last_device_id = None
        last_location = None
        last_sim_change_time = None
        
        previous_city = ''
        current_city = ''
        device_change_after_sim = False
        hours_between_sim_device_change = 999
        is_roaming = False
        
        # Count failed logins in last 24h
        recent_failed = group[(group['login_status'] == 'failed') & 
                             (group['timestamp'] >= end_time - timedelta(hours=24))]
        failed_logins_24h = len(recent_failed)

        for _, row in group.iterrows():
            ts = row['timestamp']
            
            # SIM Change
            if last_sim_id is not None and row['sim_id'] != last_sim_id:
                last_sim_change_time = ts
            
            # Device Change post SIM
            if last_sim_change_time and last_device_id is not None and row['device_id'] != last_device_id:
                diff = hours_between(ts, last_sim_change_time)
                if diff <= config.DEVICE_CHANGE_AFTER_SIM_HOURS:
                    device_change_after_sim = True
                    hours_between_sim_device_change = diff
            
            # Location
            if last_location is not None and row['location'] != last_location:
                previous_city = last_location
                current_city = row['location']
            
            # Roaming Check
            if 'is_roaming' in row:
                val = str(row['is_roaming']).lower()
                if val in ['true', '1', 'yes']:
                    is_roaming = True

            last_sim_id = row['sim_id']
            last_device_id = row['device_id']
            last_location = row['location']

        hours_since_sim_change = hours_between(end_time, last_sim_change_time) if last_sim_change_time else 999
        
        feature_row = {
            'user_id': user_id,
            'hours_since_sim_change': hours_since_sim_change,
            'device_changed_after_sim': device_change_after_sim,
            'hours_between_sim_device_change': hours_between_sim_device_change,
            'previous_city': previous_city or last_location or '',
            'current_city': current_city or last_location or '',
            'failed_logins_24h': failed_logins_24h,
            'is_roaming': is_roaming
        }
        
        # Run Rule Engine
        rule_result = rule_engine.evaluate_user(feature_row)
        
        user_features.append({
            'user_id': user_id,
            'risk_score': rule_result['risk_score'],
            'alert_level': rule_result['alert_level'],
            'alert_emoji': rule_result['alert_emoji'],
            'triggered_rules': rule_result['triggered_rules'],
            'total_rules_triggered': rule_result['total_rules_triggered']
        })
        
        if rule_result['triggered_rules']:
             reasons = '; '.join(r['reason'] for r in rule_result['triggered_rules'])
             suspicious_rows.append({
                 'timestamp': end_time.strftime('%Y-%m-%d %H:%M:%S'),
                 'user_id': user_id,
                 'sim_id': last_sim_id,
                 'risk_level': rule_result['alert_level'],
                 'flag_reason': reasons
             })
             
    return user_features, suspicious_rows

@app.route('/', methods=['GET'])
def home():
    return jsonify({'status': 'success', 'message': 'SIMGuard Backend API is running'})

@app.route('/upload', methods=['POST'])
def upload_file():
    global uploaded_data
    try:
        if 'file' not in request.files: return jsonify({'status': 'error', 'message': 'No file'}), 400
        file = request.files['file']
        if file.filename == '': return jsonify({'status': 'error', 'message': 'No selected file'}), 400
        
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        try:
            df = load_uploaded_dataframe(filepath)
            df = normalize_uploaded_dataframe(df)
            uploaded_data = df
            
            return jsonify({
                'status': 'success', 
                'filename': filename,
                'records_count': len(df),
                'columns': list(df.columns),
                'date_range': {
                    'start': df['timestamp'].min().strftime('%Y-%m-%d %H:%M:%S'),
                    'end': df['timestamp'].max().strftime('%Y-%m-%d %H:%M:%S')
                }
            })
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 400
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/analyze', methods=['POST'])
def analyze_data():
    global uploaded_data, analysis_results
    if uploaded_data is None: return jsonify({'status': 'error', 'message': 'No data uploaded'}), 400
    
    try:
        user_results, suspicious_rows = build_user_feature_rows(uploaded_data)
        
        high = len([u for u in user_results if u['alert_level'] == 'HIGH'])
        medium = len([u for u in user_results if u['alert_level'] == 'MEDIUM'])
        low = len(user_results) - high - medium
        
        analysis_results = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'summary': {
                'total_records': len(uploaded_data),
                'suspicious_count': high + medium,
                'clean_count': low,
                'users_analyzed': len(user_results),
                'high_risk_users': high,
                'medium_risk_users': medium,
                'clean_users': low
            },
            'risk_distribution': {'High': high, 'Medium': medium, 'Low': low},
            'suspicious_activities': suspicious_rows,
            'total_suspicious_activities': len(suspicious_rows)
        }
        return jsonify({'status': 'success', 'summary': analysis_results['summary']})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/results', methods=['GET'])
def get_results():
    if not analysis_results: return jsonify({'status': 'error', 'message': 'No analysis'}), 400
    return jsonify({
        'status': 'success', 
        'analysis_timestamp': analysis_results['timestamp'],
        'summary': analysis_results['summary'],
        'risk_distribution': analysis_results['risk_distribution'],
        'suspicious_activities': analysis_results['suspicious_activities'],
        'total_suspicious_activities': analysis_results['total_suspicious_activities']
    })

# --- ML ENDPOINTS (INTEGRATED) ---

@app.route('/predict', methods=['POST'])
def predict():
    """Manual prediction using the new Thinker Model"""
    try:
        data = request.json
        result = ml_engine.predict(data)
        
        # Determine visual risk level
        risk_level = 'LOW'
        if result['prediction'] == 1:
            risk_level = 'HIGH' if result['confidence'] > 0.8 else 'MEDIUM'
            
        return jsonify({
            'status': 'success',
            'prediction': int(result['prediction']),
            'confidence': float(result['confidence']),
            'risk_level': risk_level,
            'message': 'Potential SIM Swap Detected' if result['prediction'] == 1 else 'No Suspicious Activity'
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/upload_train', methods=['POST'])
def upload_train():
    """Upload dataset for ML training/diagnostics"""
    if 'file' not in request.files: return jsonify({'status': 'error'}), 400
    file = request.files['file']
    path = os.path.join(UPLOAD_FOLDER, 'training_data.csv') # Save as generic name
    file.save(path)
    
    # Just verify we can load it
    try:
        if path.endswith('.csv'):
            df = pd.read_csv(path)
        else:
            df = pd.read_excel(path, engine='openpyxl')
        
        stats = {
            'total_rows': len(df),
            'columns': list(df.columns)
        }
        return jsonify({'status': 'success', 'stats': stats})
    except Exception as e:
         return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/diagnostics', methods=['POST'])
def run_diagnostics():
    """Run model evaluation/diagnostics on the uploaded dataset"""
    try:
        csv_path = os.path.join(UPLOAD_FOLDER, 'training_data.csv')
        if os.path.exists(csv_path):
             df = pd.read_csv(csv_path) if csv_path.endswith('.csv') else pd.read_excel(csv_path, engine='openpyxl')
        else:
             return jsonify({'status': 'error', 'message': 'No dataset uploaded'}), 400
        
        res = ml_engine.run_diagnostics(df)
        return jsonify(res)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/train', methods=['POST'])
def train():
    """Train the 'Thinker' ML model"""
    try:
        # Load the uploaded file
        # We check both csv and excel
        csv_path = os.path.join(UPLOAD_FOLDER, 'training_data.csv')
        
        if os.path.exists(csv_path):
             df = pd.read_csv(csv_path) if csv_path.endswith('.csv') else pd.read_excel(csv_path, engine='openpyxl')
        else:
             return jsonify({'status': 'error', 'message': 'No training file uploaded'}), 400
             
        config = request.json
        res = ml_engine.train_model(
            df,
            test_size=config.get('test_size', 20) / 100.0
        )
        return jsonify(res)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

class SIMGuardReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'SIMGuard Investigation Report', 0, 1, 'C')
        self.ln(10)
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

@app.route('/report', methods=['GET'])
def generate_report():
    if not analysis_results: return jsonify({'status': 'error'}), 400
    
    pdf = SIMGuardReport()
    pdf.add_page()
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f"Analysis Time: {analysis_results['timestamp']}", 0, 1)
    pdf.cell(0, 10, f"Suspicious Users: {analysis_results['summary']['suspicious_count']}", 0, 1)
    
    pdf_output = io.BytesIO()
    pdf_string = pdf.output(dest='S').encode('latin-1')
    pdf_output.write(pdf_string)
    pdf_output.seek(0)
    
    return send_file(pdf_output, as_attachment=True, download_name='simguard_report.pdf', mimetype='application/pdf')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True, threaded=True)
