# SIMGuard - AI-Powered SIM Swap Detection Tool

A comprehensive cybersecurity tool that detects SIM swapping attacks using AI and user behavior analytics. This project includes both a modern web frontend and a robust Flask backend API.

![SIMGuard Logo](https://img.shields.io/badge/SIMGuard-Cybersecurity-blue?style=for-the-badge&logo=shield)

## 🛡️ Project Overview

SIMGuard is a final year cybersecurity project that analyzes user activity logs to identify suspicious SIM swapping attempts. The tool combines behavioral analytics, geolocation analysis, and device fingerprinting to detect potential security threats.

### Key Features

- **🤖 ML-Powered Detection**: XGBoost machine learning model for real-time predictions
- **🇱🇰 Sri Lankan Dataset Support**: Specialized dashboard for Sri Lankan telecom data
- **🔍 Behavioral Analytics**: Advanced algorithms to identify SIM swap patterns
- **📊 Real-time Analysis**: Process and analyze user activity logs instantly
- **📈 Interactive Dashboards**:
  - CSV Upload Dashboard for batch analysis
  - ML Dashboard for real-time individual predictions
  - **NEW!** Sri Lankan ML Dashboard with CSV/Excel support
- **📄 PDF Reports**: Comprehensive investigation reports for digital forensics
- **🌐 RESTful API**: Clean backend API with ML prediction endpoint
- **📱 Responsive Design**: Works on desktop, tablet, and mobile devices
- **💾 LocalStorage**: Automatic prediction history saving
- **📊 Excel Support**: Upload and analyze `.xlsx` files directly

## 🏗️ Architecture

```
SIMGuard/
├── frontend/                       # All frontend dashboards
│   ├── dashboards/
│   │   ├── csv-upload/            # CSV Upload Dashboard
│   │   │   ├── index.html
│   │   │   ├── styles.css
│   │   │   └── script.js
│   │   ├── ml-dashboard/          # ML Prediction Dashboard
│   │   │   ├── ml-dashboard.html
│   │   │   ├── ml-dashboard.css
│   │   │   └── ml-dashboard.js
│   │   └── sl-ml-dashboard/       # 🇱🇰 Sri Lankan ML Dashboard
│   │       ├── sl-ml-dashboard.html
│   │       ├── sl-ml-dashboard.css
│   │       └── sl-ml-dashboard.js
│   └── testing/
│       └── TEST_FILE_UPLOAD.html
│
├── backend/                       # Flask API backend
│   ├── app.py                    # Main Flask application
│   ├── ml_predictor.py           # ML model wrapper
│   ├── sl_ml_handler.py          # Sri Lankan ML handler
│   ├── requirements.txt          # Python dependencies
│   ├── tests/                    # All test scripts
│   │   ├── test_api.py
│   │   ├── test_ml_endpoint.py
│   │   ├── test_sl_endpoints.py
│   │   └── test_upload.py
│   └── uploads/                  # Uploaded files directory
│
├── simswap_detector/             # Detection engine module
│   ├── config.py
│   ├── dashboard.py
│   ├── rule_engine.py
│   └── ...
│
├── data/                         # Sample datasets
│   ├── samples/
│   │   ├── sample_logs.csv
│   │   ├── sample_sl_dataset.csv
│   │   └── sample_sl_dataset.xlsx
│   └── DOWNLOADABLE_SAMPLE_DATASETS.md
│
├── docs/                         # 📚 All documentation
│   ├── guides/                   # User guides
│   ├── development/              # Development docs
│   ├── readme/                   # Component READMEs
│   ├── changelogs/               # Version history
│   └── checklists/               # Project checklists
│
├── scripts/                      # Utility scripts
│   └── convert_csv_to_excel.py
│
├── README.md                     # Main documentation
├── LICENSE                       # MIT License
└── setup.py                      # Package setup
```

### Frontend
- **Technology**: Vanilla HTML5, CSS3, JavaScript (ES6+)
- **Styling**: Custom CSS with dark cybersecurity theme
- **Charts**: Chart.js for data visualization
- **Icons**: Font Awesome
- **Fonts**: Google Fonts (Inter)
- **Two Dashboards**:
  - **CSV Upload Dashboard**: Batch analysis of log files
  - **ML Dashboard**: Real-time individual predictions with XGBoost

### Backend
- **Framework**: Flask (Python)
- **Machine Learning**: XGBoost 2.0.3, scikit-learn 1.3.2
- **Data Processing**: Pandas, NumPy
- **Report Generation**: FPDF
- **API**: RESTful endpoints with CORS support
- **File Handling**: Secure file upload and validation
- **ML Endpoint**: `/predict` for real-time predictions

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Modern web browser
- Git (for cloning)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/SIMGuard.git
cd SIMGuard
```

2. **Set up the backend**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Place ML model files (for ML Dashboard)**
```bash
# Place these files in the backend/ directory:
# - xgboost_simswap_model.pkl
# - scaler.pkl
# See ML_DASHBOARD_README.md for details

# Check if models are ready:
python check_models.py
```

4. **Start the backend server**
```bash
python app.py
# or
python run.py
```

5. **Open the frontend**
```bash
# Open any dashboard in your browser:
# CSV Upload Dashboard:
frontend/dashboards/csv-upload/index.html

# ML Dashboard:
frontend/dashboards/ml-dashboard/ml-dashboard.html

# Sri Lankan ML Dashboard:
frontend/dashboards/sl-ml-dashboard/sl-ml-dashboard.html
```
cd ..
# Open either dashboard in your browser:
open index.html         # CSV Upload Dashboard
open ml-dashboard.html  # ML Prediction Dashboard
```

6. **Access the application**
- **CSV Dashboard**: `index.html` - Batch analysis of log files
- **ML Dashboard**: `ml-dashboard.html` - Real-time predictions
- **Backend API**: http://localhost:5000
- **API Documentation**: http://localhost:5000/

## 📖 Usage Guide

### Option 1: CSV Upload Dashboard (Batch Analysis)

1. **Upload Data**
   - Navigate to the Upload section
   - Drag and drop or select a CSV file with user activity logs
   - Supported format: CSV with required columns (see documentation)

2. **Analyze Data**
   - Click "Analyze File" after uploading
   - The system will process the data and identify suspicious activities
   - View real-time progress and statistics

3. **Review Results**
   - Examine the detection summary with statistics
   - View suspicious activities in the table
   - Download PDF investigation report

### Option 2: ML Dashboard (Real-Time Predictions)

1. **Fill in User Data**
   - Enter behavioral metrics (distance, time, logins, etc.)
   - Toggle status flags (roaming, SIM change, device change)
   - Enter location information

2. **Analyze Risk**
   - Click "Analyze Risk" button
   - ML model processes data with feature engineering
   - View instant prediction results

3. **Review Results**
   - See risk status (SAFE ✅ or SUSPICIOUS 🚨)
   - Check confidence score percentage
   - Review identified risk factors
   - View prediction history table
   - Download detailed text report

**See `ML_DASHBOARD_README.md` for detailed ML Dashboard documentation.**

### 3. Review Results (CSV Dashboard)
- Examine the detection summary with statistics
- Review the suspicious activities table
- Analyze risk levels and flag reasons

### 4. Generate Reports
- Download comprehensive PDF investigation reports
- Reports include technical metadata for digital forensics
- Suitable for security teams and legal proceedings

## 🔧 API Documentation

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check and API info |
| POST | `/upload` | Upload CSV file for analysis |
| POST | `/analyze` | Perform SIM swap detection |
| GET | `/results` | Get analysis results |
| GET | `/report` | Download PDF report |
| GET | `/status` | System status |
| POST | `/clear` | Clear data |

### Sample API Usage

```bash
# Upload file
curl -X POST -F "file=@sample_logs.csv" http://localhost:5000/upload

# Analyze data
curl -X POST http://localhost:5000/analyze

# Get results
curl -X GET http://localhost:5000/results

# Download report
curl -X GET http://localhost:5000/report -o report.pdf
```

## 📊 Detection Algorithms

SIMGuard uses multiple detection algorithms:

### 1. SIM ID Change Detection
- **Risk Level**: High
- **Criteria**: Different SIM ID for same user
- **Use Case**: Direct SIM swap detection

### 2. Impossible Travel Detection
- **Risk Level**: High
- **Criteria**: >500km distance in <2 hours
- **Use Case**: Geolocation-based fraud detection

### 3. Device Fingerprint Analysis
- **Risk Level**: Medium
- **Criteria**: Unexpected device changes
- **Use Case**: Device-based anomaly detection

### 4. IP Address Analysis
- **Risk Level**: Medium
- **Criteria**: Suspicious network changes
- **Use Case**: Network-based threat detection

### 5. Behavioral Pattern Analysis
- **Risk Level**: Variable
- **Criteria**: Rapid successive changes
- **Use Case**: Behavioral anomaly detection

## 📁 File Format

### Required CSV Columns

| Column | Description | Example |
|--------|-------------|---------|
| `timestamp` | Activity timestamp | `2025-01-10 14:30:15` |
| `user_id` | Unique user identifier | `USR0001` |
| `sim_id` | SIM card identifier | `SIM12345` |
| `device_id` | Device identifier | `DEV001` |
| `ip` | IP address | `192.168.1.100` |
| `location` | User location | `New York` |
| `login_status` | Login result | `success`/`failed` |

### Sample Data
```csv
timestamp,user_id,sim_id,device_id,ip,location,login_status
2025-01-10 14:30:15,USR0001,SIM12345,DEV001,192.168.1.100,New York,success
2025-01-10 14:35:12,USR0001,SIM54321,DEV003,203.0.113.45,Miami,success
```

## 🧪 Testing

### Backend Testing
```bash
cd backend
python test_api.py                    # Run full test suite
python test_api.py --interactive      # Interactive testing mode
```

### Frontend Testing
1. Open `index.html` in browser
2. Upload `sample_logs.csv`
3. Run analysis and verify results
4. Download and verify PDF report

## 🔒 Security Features

- **File Validation**: Strict CSV format validation
- **Size Limits**: 16MB maximum file size
- **Input Sanitization**: Secure filename handling
- **CORS Protection**: Configured for specific origins
- **Error Handling**: Comprehensive error management
- **Data Cleanup**: Automatic temporary file removal

## 📈 Performance

- **Concurrent Processing**: Multi-threaded Flask server
- **Memory Efficient**: Pandas-based data processing
- **Scalable**: Designed for large datasets
- **Fast Analysis**: Optimized detection algorithms

## 🎨 UI/UX Features

- **Modern Design**: Cybersecurity-inspired theme
- **Responsive Layout**: Mobile-friendly interface
- **Interactive Charts**: Real-time data visualization
- **Progress Indicators**: User feedback during processing
- **Error Handling**: User-friendly error messages
- **Accessibility**: WCAG-compliant design

## 📚 Documentation

- [Backend API Documentation](backend/README.md)
- [Frontend Documentation](docs/frontend.md)
- [Detection Algorithms](docs/algorithms.md)
- [Deployment Guide](docs/deployment.md)

## 🤝 Contributing

This is a final year project, but contributions and suggestions are welcome:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is created for educational purposes as part of a final year cybersecurity project.

## 👨‍💻 Author

**[Your Name]** - Final Year Cybersecurity Student
- Email: [your.email@university.edu]
- LinkedIn: [Your LinkedIn Profile]
- University: [Your University Name]

## 🙏 Acknowledgments

- Cybersecurity research community
- Flask and Python communities
- Chart.js for visualization
- Font Awesome for icons
- Academic supervisors and peers

## 📞 Support

For questions, issues, or academic inquiries:
- Create an issue in this repository
- Contact the author via email
- Refer to the documentation

---

**SIMGuard** - Protecting against SIM swapping attacks through intelligent detection and analysis.

![Made with Python](https://img.shields.io/badge/Made%20with-Python-blue?style=flat&logo=python)
![Flask](https://img.shields.io/badge/Flask-API-green?style=flat&logo=flask)
![JavaScript](https://img.shields.io/badge/Frontend-JavaScript-yellow?style=flat&logo=javascript)
![Cybersecurity](https://img.shields.io/badge/Domain-Cybersecurity-red?style=flat&logo=security)
