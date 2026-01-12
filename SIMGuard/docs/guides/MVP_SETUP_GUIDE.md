# 🚀 MVP Setup Guide - SIM Swap Detection System

## ✅ Complete Rule-Based MVP (No Machine Learning)

This guide provides step-by-step instructions to run the complete MVP system.

---

## 📋 Table of Contents

1. [System Requirements](#system-requirements)
2. [Installation](#installation)
3. [Built-in Datasets](#built-in-datasets)
4. [Running the Dashboard](#running-the-dashboard)
5. [Using the System](#using-the-system)
6. [Report Generation](#report-generation)
7. [Demo Walkthrough](#demo-walkthrough)
8. [Troubleshooting](#troubleshooting)

---

## 🖥️ System Requirements

- **Python**: 3.8 or higher
- **IDE**: VS Code (recommended)
- **OS**: Windows, macOS, or Linux
- **RAM**: 4GB minimum
- **Disk Space**: 500MB

---

## 📦 Installation

### Step 1: Open Terminal in VS Code

1. Open VS Code
2. Open the project folder: `SIMGuard`
3. Open terminal: `Terminal` → `New Terminal`

### Step 2: Install Dependencies

```bash
cd simswap_detector
pip install -r requirements.txt
```

**Expected output**:
```
Successfully installed streamlit-1.29.0 pandas-2.1.3 numpy-1.24.3 openpyxl-3.1.2
```

### Step 3: Verify Installation

```bash
python -c "import streamlit; import pandas; import openpyxl; print('✅ All dependencies installed')"
```

---

## 📊 Built-in Datasets

The system includes **4 built-in Excel datasets** stored in `simswap_detector/datasets/`:

| Dataset | Users | Legitimate | Suspicious | Use Case |
|---------|-------|------------|------------|----------|
| **dataset_demo_20users.xlsx** | 20 | 15 | 5 | Quick demo (recommended) |
| **dataset_standard_100users.xlsx** | 100 | 80 | 20 | Standard testing |
| **dataset_large_500users.xlsx** | 500 | 400 | 100 | Performance testing |
| **dataset_highrisk_50users.xlsx** | 50 | 25 | 25 | High-risk scenario |

### Regenerate Datasets (Optional)

If datasets are missing:

```bash
cd simswap_detector
python data_generator.py
```

**Output**:
```
============================================================
Generating Built-in Excel Test Datasets
============================================================

📊 Dataset 1: Standard Test Dataset (100 users)
   ✅ Saved: dataset_standard_100users.xlsx

📊 Dataset 2: Small Demo Dataset (20 users)
   ✅ Saved: dataset_demo_20users.xlsx

📊 Dataset 3: Large Test Dataset (500 users)
   ✅ Saved: dataset_large_500users.xlsx

📊 Dataset 4: High Risk Scenario (50 users, 50% suspicious)
   ✅ Saved: dataset_highrisk_50users.xlsx

✅ All built-in datasets generated successfully!
```

---

## 🎯 Running the Dashboard

### Start the Dashboard

```bash
cd simswap_detector
streamlit run dashboard.py
```

**Expected output**:
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

**Browser opens automatically** at `http://localhost:8501`

### Stop the Dashboard

Press `Ctrl + C` in the terminal

---

## 🔍 Using the System

### Option 1: Use Built-in Datasets (Recommended)

1. **Select Data Source**: Choose "Built-in Datasets" (default)
2. **Select Dataset**: Choose "Demo 20Users" from dropdown
3. **View Summary**: See dataset info in sidebar
4. **Run Detection**: Click "Run Detection" button
5. **View Results**: See detection results and metrics

### Option 2: Upload Excel File

1. **Select Data Source**: Choose "Upload Excel File"
2. **Upload File**: Click "Browse files" and select `.xlsx` file
3. **Run Detection**: Click "Run Detection" button
4. **View Results**: See detection results and metrics

---

## 📄 Report Generation

### Generate Forensic Report

1. **Run Detection**: Complete detection first
2. **Choose Format**: Select "Excel (.xlsx)" or "CSV (.csv)"
3. **Generate Report**: Click "📥 Generate & Download Report"
4. **Download**: Click download button to save report

### Report Contents

Each report includes:

- **Detection_Timestamp**: When detection was performed
- **User_ID**: Unique user identifier
- **Risk_Score**: Calculated risk score (0-100)
- **Alert_Level**: LOW / MEDIUM / HIGH
- **Alert_Severity**: Emoji + level
- **Total_Rules_Triggered**: Number of rules triggered
- **Triggered_Rules_Details**: Detailed reasons for each rule
- **Dataset_Source**: Source dataset name
- **Detection_Method**: "Rule-Based (No ML)"
- **Requires_Investigation**: YES / REVIEW / NO

---

## 🎬 Demo Walkthrough (5 Minutes)

### Minute 1: Start System

```bash
cd simswap_detector
streamlit run dashboard.py
```

Browser opens automatically.

### Minute 2: Select Dataset

1. Data Source: "Built-in Datasets" (already selected)
2. Select: "Demo 20Users"
3. See: "✅ Loaded 20 records"

### Minute 3: Run Detection

1. Click: "Run Detection" button
2. Wait: 2-3 seconds
3. See: "✅ Detection complete!"

### Minute 4: View Results

**Summary Metrics**:
- Total Users: 20
- 🚨 High Risk: ~5 users
- ⚠️ Medium Risk: ~0 users
- ✅ Low Risk: ~15 users

**Detailed Analysis**:
1. Scroll down to "Detailed User Analysis"
2. Select a HIGH risk user (e.g., USER_0018)
3. View triggered rules and reasons

### Minute 5: Generate Report

1. Scroll to "Forensic Report Generation"
2. Format: "Excel (.xlsx)"
3. Click: "📥 Generate & Download Report"
4. Download: Excel report with all details

---

## 🎓 Academic Demo Script

### Introduction (1 minute)

"This is a rule-based SIM swap detection system developed for my final year project. It uses 9 behavioral rules to detect SIM swap attacks without machine learning."

### System Overview (1 minute)

"The system includes:
- 4 built-in Excel test datasets
- Interactive web dashboard
- 9 detection rules
- Forensic report generation"

### Live Demonstration (3 minutes)

1. **Show Dashboard**: "Here's the web interface"
2. **Select Dataset**: "I'll use the demo dataset with 20 users"
3. **Run Detection**: "Click Run Detection"
4. **Show Results**: "5 high-risk users detected"
5. **Explain Detection**: "Let's look at USER_0018..."
   - "SIM changed 18 hours ago"
   - "Device changed 3 hours after SIM"
   - "Location jumped 250km in 1 hour"
   - "8 failed login attempts"
   - "Risk score: 88 - HIGH risk"

### Report Generation (1 minute)

"The system generates forensic reports in Excel or CSV format with all detection details for investigation."

[Generate and download report]

### Conclusion (30 seconds)

"The system successfully detects SIM swap attacks using explainable rule-based logic, ready for real-world deployment."

**Total Time**: ~6-7 minutes

---

## 🐛 Troubleshooting

### Issue 1: "No module named 'streamlit'"

**Solution**:
```bash
cd simswap_detector
pip install -r requirements.txt
```

### Issue 2: "No built-in datasets found"

**Solution**:
```bash
cd simswap_detector
python data_generator.py
```

### Issue 3: Dashboard won't start

**Solution**:
```bash
# Check Python version
python --version  # Should be 3.8+

# Reinstall streamlit
pip install streamlit==1.29.0

# Try again
streamlit run dashboard.py
```

### Issue 4: Port 8501 already in use

**Solution**:
```bash
# Use different port
streamlit run dashboard.py --server.port 8502
```

### Issue 5: Excel file won't upload

**Solution**:
- Ensure file is `.xlsx` format (not `.xls` or `.csv`)
- Check file size (should be < 200MB)
- Verify file has required columns (see README)

---

## ✅ Pre-Demo Checklist

Before demonstration:

- [ ] Python 3.8+ installed
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Built-in datasets generated (`python data_generator.py`)
- [ ] Dashboard starts successfully (`streamlit run dashboard.py`)
- [ ] Can select built-in dataset
- [ ] Detection runs without errors
- [ ] Results display correctly
- [ ] Report generation works
- [ ] Practiced demo script

---

## 📁 Project Structure

```
SIMGuard/
├── simswap_detector/
│   ├── datasets/                    # Built-in Excel datasets
│   │   ├── dataset_demo_20users.xlsx
│   │   ├── dataset_standard_100users.xlsx
│   │   ├── dataset_large_500users.xlsx
│   │   └── dataset_highrisk_50users.xlsx
│   ├── config.py                    # Configuration
│   ├── utils.py                     # Utilities
│   ├── data_ingestion.py            # Data loading
│   ├── rule_engine.py               # Detection rules (NO ML)
│   ├── dashboard.py                 # Streamlit dashboard
│   ├── data_generator.py            # Dataset generator
│   ├── test_system.py               # Automated tests
│   └── requirements.txt             # Dependencies
└── Documentation/
    ├── MVP_SETUP_GUIDE.md           # This file
    ├── README_SIMSWAP_DETECTOR.md   # Full documentation
    └── QUICK_START_GUIDE.md         # Quick reference
```

---

## 🎉 You're Ready!

Your MVP system is now:
- ✅ Fully installed
- ✅ Built-in datasets ready
- ✅ Dashboard functional
- ✅ Report generation working
- ✅ Ready for demonstration

**Next Step**: Run `streamlit run dashboard.py` and start exploring!

---

**Last Updated**: December 21, 2024  
**Version**: MVP 1.0.0 (Rule-Based Only, No ML)

