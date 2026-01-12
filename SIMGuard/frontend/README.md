# Frontend Dashboards

This directory contains all the frontend web dashboards for SIMGuard.

## 📂 Structure

```
frontend/
├── dashboards/
│   ├── csv-upload/              # Main CSV Upload Dashboard
│   │   ├── index.html           # Entry point for CSV analysis
│   │   ├── styles.css           # CSV dashboard styles
│   │   └── script.js            # CSV dashboard logic
│   │
│   ├── ml-dashboard/            # Machine Learning Dashboard
│   │   ├── ml-dashboard.html    # ML prediction interface
│   │   ├── ml-dashboard.css     # ML dashboard styles
│   │   └── ml-dashboard.js      # ML prediction logic
│   │
│   └── sl-ml-dashboard/         # Sri Lankan ML Dashboard
│       ├── sl-ml-dashboard.html # SL-specific ML interface
│       ├── sl-ml-dashboard.css  # SL dashboard styles
│       └── sl-ml-dashboard.js   # SL prediction logic
│
└── testing/
    └── TEST_FILE_UPLOAD.html    # Test file for upload functionality
```

## 🚀 Getting Started

### CSV Upload Dashboard
Access at: `frontend/dashboards/csv-upload/index.html`
- Upload CSV files with user activity logs
- Batch analysis and detection
- PDF report generation

### ML Dashboard
Access at: `frontend/dashboards/ml-dashboard/ml-dashboard.html`
- Real-time individual predictions
- Manual input form
- Prediction history

### Sri Lankan ML Dashboard
Access at: `frontend/dashboards/sl-ml-dashboard/sl-ml-dashboard.html`
- CSV/Excel file support
- Model training interface
- Sri Lankan telecom data analysis

## 🔗 Navigation

All dashboards are interconnected with navigation links. You can switch between them using the navigation menu at the top of each page.

## ⚙️ Backend Requirement

All dashboards require the Flask backend API to be running:
```bash
cd backend
python run.py
```

The API runs on `http://localhost:5000` by default.

## 📝 Notes

- All dashboards use relative paths for navigation
- CSS and JS files are co-located with their HTML files
- External dependencies (Chart.js, Font Awesome, etc.) are loaded via CDN
