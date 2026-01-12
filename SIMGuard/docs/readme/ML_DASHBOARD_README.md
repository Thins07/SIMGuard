# 🤖 SIMGuard ML Dashboard

## Overview

The ML Dashboard is a professional, production-ready interface for real-time SIM swap attack detection using machine learning. It features a modern dark cybersecurity theme with interactive visualizations and comprehensive reporting.

## 🎯 Features

### Frontend Features
- **2-Column Responsive Layout**: Input form on left, results on right
- **Modern Dark Theme**: Cybersecurity-inspired design with blue/teal accents
- **Interactive UI Components**:
  - Numeric inputs for behavioral metrics
  - Toggle switches for status flags
  - Text inputs for location data
  - Real-time risk indicator with animations
  - Confidence score progress bar
  - Risk factors list with slide-in animations
  - Recent predictions table (last 5 predictions)
- **LocalStorage Integration**: Automatically saves prediction history
- **Export Functionality**: Download detailed text reports
- **Loading States**: Smooth transitions and spinner animations
- **Responsive Design**: Mobile-first approach, works on all devices

### Backend Features
- **XGBoost ML Model Integration**: Production-ready model loading
- **Feature Engineering Pipeline**:
  - Location velocity calculation
  - Tower change frequency detection
  - High-risk behavior composite scoring
- **RESTful API**: `/predict` endpoint for real-time predictions
- **Comprehensive Error Handling**: Graceful degradation
- **Risk Factor Analysis**: Intelligent identification of suspicious patterns

## 📋 Prerequisites

### Required Files
You need to place these files in the `backend/` directory:

1. **`xgboost_simswap_model.pkl`** - Your trained XGBoost model
2. **`scaler.pkl`** - Your fitted StandardScaler/MinMaxScaler

### How to Get These Files

If you trained your model in Google Colab, download them using:

```python
# In your Colab notebook, after training:
import pickle

# Save the model
with open('xgboost_simswap_model.pkl', 'wb') as f:
    pickle.dump(model, f)

# Save the scaler
with open('scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)

# Download files
from google.colab import files
files.download('xgboost_simswap_model.pkl')
files.download('scaler.pkl')
```

Then place both files in the `backend/` directory of this project.

## 🚀 Installation & Setup

### 1. Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

This will install:
- Flask 2.3.3
- XGBoost 2.0.3
- scikit-learn 1.3.2
- pandas, numpy, and other dependencies

### 2. Place Model Files

Copy your model files to the backend directory:
```
backend/
├── xgboost_simswap_model.pkl  ← Place here
├── scaler.pkl                  ← Place here
├── app.py
├── ml_predictor.py
└── requirements.txt
```

### 3. Start the Backend Server

```bash
cd backend
python app.py
```

You should see:
```
✅ Model loaded from xgboost_simswap_model.pkl
✅ Scaler loaded from scaler.pkl
✅ ML Model loaded successfully
 * Running on http://0.0.0.0:5000
```

### 4. Open the Frontend

Open `ml-dashboard.html` in your web browser.

## 🎮 Usage

### Making a Prediction

1. **Fill in the form** with user behavior data:
   - **Distance Change**: How far the user traveled (km)
   - **Time Since SIM Change**: Hours since last SIM swap
   - **Failed Logins**: Number of failed login attempts in 24h
   - **Calls/SMS**: Communication activity in 24h
   - **Data Usage Change**: Percentage change in data usage
   - **Cell Tower Changes**: Number of tower switches
   - **Toggle Flags**: Roaming status, SIM/device changes
   - **Location**: Current and previous cities

2. **Click "Analyze Risk"** to get instant prediction

3. **View Results**:
   - Risk status (SAFE ✅ or SUSPICIOUS 🚨)
   - Confidence score (0-100%)
   - Top risk factors identified
   - Prediction added to history table

4. **Download Report**: Click "Download Report" for detailed text file

### Example Input

```
Distance Change: 450 km
Time Since SIM Change: 2 hours
Failed Logins: 5
Calls (24h): 3
SMS (24h): 1
Data Usage Change: -80%
Cell Tower Changes: 8
Is Roaming: Yes
SIM Change Flag: Yes
Device Change Flag: Yes
Current City: New York
Previous City: Los Angeles
```

This would likely trigger a **SUSPICIOUS** prediction due to:
- Impossible travel (450km in 2 hours = 225 km/h)
- High failed logins
- Recent SIM change
- Device change
- Unusual data usage drop

## 🔧 API Documentation

### POST `/predict`

**Endpoint**: `http://localhost:5000/predict`

**Request Body** (JSON):
```json
{
  "distance_change": 450.0,
  "time_since_sim_change": 2.0,
  "num_failed_logins_last_24h": 5,
  "num_calls_last_24h": 3,
  "num_sms_last_24h": 1,
  "data_usage_change_percent": -80.0,
  "change_in_cell_tower_id": 8,
  "is_roaming": 1,
  "sim_change_flag": 1,
  "device_change_flag": 1,
  "current_city": "New York",
  "previous_city": "Los Angeles"
}
```

**Response** (JSON):
```json
{
  "prediction": 1,
  "confidence": 94.5,
  "risk_factors": [
    "High number of failed logins: 5",
    "Impossible travel detected: 225.0 km/h",
    "Recent SIM card change detected",
    "Device change detected",
    "User is currently roaming"
  ],
  "status": "success"
}
```

## 🎨 Customization

### Color Theme

Edit `ml-dashboard.css` to change colors:

```css
:root {
    --primary-bg: #0a0e27;      /* Main background */
    --accent-blue: #3b82f6;     /* Primary accent */
    --accent-teal: #14b8a6;     /* Secondary accent */
    --accent-red: #ef4444;      /* Danger/suspicious */
    --accent-green: #10b981;    /* Safe/success */
}
```

### Feature Engineering

Modify `backend/ml_predictor.py` to adjust feature engineering:

```python
def engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
    # Add your custom features here
    df['custom_feature'] = ...
    return df
```

## 📊 Project Structure

```
SIMGuard/
├── ml-dashboard.html          # Main dashboard page
├── ml-dashboard.css           # Styling (731 lines)
├── ml-dashboard.js            # Frontend logic (372 lines)
├── ML_DASHBOARD_README.md     # This file
└── backend/
    ├── app.py                 # Flask API with /predict endpoint
    ├── ml_predictor.py        # ML model wrapper class
    ├── requirements.txt       # Python dependencies
    ├── xgboost_simswap_model.pkl  # Your model (place here)
    └── scaler.pkl                  # Your scaler (place here)
```

## 🐛 Troubleshooting

### Model Not Loading

**Error**: `ML model not loaded - prediction endpoint will not work`

**Solution**: Ensure both `.pkl` files are in the `backend/` directory

### CORS Errors

**Error**: `Access to fetch blocked by CORS policy`

**Solution**: Backend already has CORS enabled. Ensure backend is running on port 5000

### Prediction Fails

**Error**: `Prediction failed: ...`

**Solution**: Check that your model expects the same features as defined in `ml_predictor.py`

## 🎓 Academic Presentation Tips

1. **Demo Flow**:
   - Show the clean, professional UI
   - Enter realistic attack scenario data
   - Highlight the real-time prediction
   - Explain the risk factors identified
   - Show the prediction history table
   - Download and display the report

2. **Technical Highlights**:
   - XGBoost model integration
   - Feature engineering pipeline
   - RESTful API architecture
   - Responsive modern UI
   - LocalStorage for persistence

3. **Future Enhancements**:
   - Real-time data streaming
   - Multiple ML models comparison
   - User authentication
   - Database integration
   - Advanced visualizations

## 📞 Support

For issues or questions:
- Check the main `README.md`
- Review `backend/README.md` for API details
- Check browser console for frontend errors
- Check terminal for backend errors

---

**SIMGuard ML Dashboard** - Final Year Project by Thinara | 2025  
Powered by XGBoost Machine Learning
