# 📂 Project Organization Guide

## ✅ Successfully Reorganized on January 12, 2026

Your SIMGuard project has been reorganized into a clean, professional structure. Here's what changed and where everything is now located.

## 📊 Before & After Comparison

### Before (30+ files in root):
```
SIMGuard/
├── index.html, ml-dashboard.html, sl-ml-dashboard.html
├── styles.css, ml-dashboard.css, sl-ml-dashboard.css
├── script.js, ml-dashboard.js, sl-ml-dashboard.js
├── 20+ markdown documentation files
├── sample_logs.csv, sample_sl_dataset.csv
├── TEST_FILE_UPLOAD.html
└── backend/, docs/, simswap_detector/
```

### After (Clean & Organized):
```
SIMGuard/
├── frontend/          # All web dashboards
├── backend/           # Flask API
├── docs/              # All documentation
├── data/              # Sample datasets
├── scripts/           # Utility scripts
├── simswap_detector/  # Detection module
└── 4 essential files (README, LICENSE, setup.py, .gitignore)
```

## 🗂️ New Directory Structure

### 1. **frontend/** - All Frontend Assets
```
frontend/
├── dashboards/
│   ├── csv-upload/              # Main CSV Dashboard
│   │   ├── index.html
│   │   ├── styles.css
│   │   └── script.js
│   ├── ml-dashboard/            # ML Prediction Dashboard
│   │   ├── ml-dashboard.html
│   │   ├── ml-dashboard.css
│   │   └── ml-dashboard.js
│   └── sl-ml-dashboard/         # Sri Lankan Dashboard
│       ├── sl-ml-dashboard.html
│       ├── sl-ml-dashboard.css
│       └── sl-ml-dashboard.js
└── testing/
    └── TEST_FILE_UPLOAD.html
```

**Access dashboards:**
- CSV Dashboard: `frontend/dashboards/csv-upload/index.html`
- ML Dashboard: `frontend/dashboards/ml-dashboard/ml-dashboard.html`
- SL Dashboard: `frontend/dashboards/sl-ml-dashboard/sl-ml-dashboard.html`

### 2. **backend/** - Flask API Backend
```
backend/
├── app.py                    # Main Flask application
├── ml_predictor.py           # ML model wrapper
├── sl_ml_handler.py          # Sri Lankan ML handler
├── run.py                    # Server runner
├── requirements.txt          # Dependencies
├── README.md                 # Backend documentation
├── tests/                    # All test scripts
│   ├── test_api.py
│   ├── test_ml_endpoint.py
│   ├── test_sl_endpoints.py
│   └── test_upload.py
└── uploads/                  # File upload directory
```

### 3. **docs/** - All Documentation
```
docs/
├── guides/                      # User Guides
│   ├── START_HERE.md           # ⭐ Start here!
│   ├── QUICK_START_GUIDE.md
│   ├── QUICK_START_ML.md
│   ├── QUICK_START_SL.md
│   ├── MVP_SETUP_GUIDE.md
│   ├── BACKEND_START_GUIDE.md
│   ├── EXCEL_DASHBOARD_GUIDE.md
│   └── TROUBLESHOOTING_GUIDE.md
│
├── development/                 # Development Docs
│   ├── SYSTEM_ARCHITECTURE.md
│   ├── PROJECT_STRUCTURE.md
│   ├── DEPLOYMENT.md
│   ├── DEPLOYMENT_COMPLETE.md
│   └── CONTRIBUTING.md
│
├── readme/                      # Component READMEs
│   ├── ML_DASHBOARD_README.md
│   ├── SL_DASHBOARD_README.md
│   └── README_SIMSWAP_DETECTOR.md
│
├── changelogs/                  # Version History
│   ├── CHANGELOG.md
│   ├── CHANGES_SUMMARY.md
│   ├── MVP_COMPLETE.md
│   ├── FINAL_HANDOVER.md
│   ├── FIXES_AND_FEATURES.md
│   └── FILE_UPLOAD_FIX_SUMMARY.md
│
├── checklists/                  # Project Management
│   ├── GITHUB_UPLOAD_CHECKLIST.md
│   ├── FILE_UPLOAD_FIX.md
│   └── QUICK_TEST.md
│
└── PROJECT_SUMMARY.md           # Complete project summary
```

### 4. **data/** - Sample Datasets
```
data/
├── samples/
│   ├── sample_logs.csv          # CSV sample data
│   ├── sample_sl_dataset.csv    # Sri Lankan CSV data
│   └── sample_sl_dataset.xlsx   # Sri Lankan Excel data
└── DOWNLOADABLE_SAMPLE_DATASETS.md
```

### 5. **scripts/** - Utility Scripts
```
scripts/
└── convert_csv_to_excel.py      # CSV to Excel converter
```

### 6. **simswap_detector/** - Detection Module
```
simswap_detector/
├── __init__.py
├── config.py
├── dashboard.py
├── data_generator.py
├── data_ingestion.py
├── rule_engine.py
├── test_system.py
└── utils.py
```

## 🚀 Quick Start Commands

### Start the Backend:
```bash
cd backend
python run.py
```

### Open Dashboards:
Open these files in your browser:
- `frontend/dashboards/csv-upload/index.html`
- `frontend/dashboards/ml-dashboard/ml-dashboard.html`
- `frontend/dashboards/sl-ml-dashboard/sl-ml-dashboard.html`

### Run Tests:
```bash
cd backend/tests
python test_api.py
python test_ml_endpoint.py
python test_sl_endpoints.py
```

## 📝 What Changed?

### ✅ Updated Files:
1. **HTML Navigation Links** - All dashboards now use relative paths
   - `index.html` → `../csv-upload/index.html`
   - `ml-dashboard.html` → `../ml-dashboard/ml-dashboard.html`
   
2. **README.md** - Updated architecture section with new structure

3. **Created New Files**:
   - `.gitignore` - Git ignore rules
   - `frontend/README.md` - Frontend documentation
   - `backend/uploads/.gitkeep` - Preserve uploads directory

### ⚠️ Important Notes:

1. **All dashboards work with navigation** - You can switch between them using the nav menu
2. **Backend paths unchanged** - API endpoints remain the same
3. **CSS/JS files stay with HTML** - No path updates needed for stylesheets
4. **Test files organized** - All in `backend/tests/`
5. **Documentation accessible** - Everything in `docs/` with logical subfolders

## 🎯 Benefits of New Structure

✅ **Professional GitHub Appearance** - Clean root directory
✅ **Easy Navigation** - Find files by purpose, not type
✅ **Scalable** - Easy to add new dashboards or docs
✅ **Team-Friendly** - Clear where to add files
✅ **Deployment Ready** - Standard project structure
✅ **Better Documentation** - Organized by category

## 📚 Recommended Reading Order

1. **docs/guides/START_HERE.md** - Project overview
2. **README.md** (root) - Main documentation
3. **docs/PROJECT_SUMMARY.md** - Complete project details
4. **docs/guides/QUICK_START_GUIDE.md** - Get started quickly
5. **frontend/README.md** - Frontend details
6. **backend/README.md** - Backend API details

## 🔄 Git Status

After this reorganization, you should commit these changes:

```bash
git add .
git commit -m "Reorganize project structure for better organization

- Move frontend assets to frontend/dashboards/
- Organize all documentation in docs/ subdirectories
- Move sample data to data/samples/
- Organize test files in backend/tests/
- Move utility scripts to scripts/
- Update navigation links in HTML files
- Add .gitignore and frontend README
- Update main README with new structure"
```

---

**Questions?** Check [docs/guides/TROUBLESHOOTING_GUIDE.md](docs/guides/TROUBLESHOOTING_GUIDE.md)
