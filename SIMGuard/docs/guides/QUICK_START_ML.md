# 🚀 Quick Start Guide - ML Dashboard

Get the SIMGuard ML Dashboard up and running in 5 minutes!

## ⚡ Prerequisites

- Python 3.8+
- Your trained XGBoost model files:
  - `xgboost_simswap_model.pkl`
  - `scaler.pkl`

## 📦 Step 1: Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

This installs:
- Flask, Flask-CORS
- XGBoost 2.0.3
- scikit-learn 1.3.2
- pandas, numpy
- Other dependencies

## 📁 Step 2: Place Model Files

Copy your model files to the `backend/` directory:

```
backend/
├── xgboost_simswap_model.pkl  ← Your trained model
├── scaler.pkl                  ← Your fitted scaler
├── app.py
├── ml_predictor.py
└── requirements.txt
```

### Getting Model Files from Colab

If you trained in Google Colab:

```python
import pickle

# Save model
with open('xgboost_simswap_model.pkl', 'wb') as f:
    pickle.dump(model, f)

# Save scaler
with open('scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)

# Download
from google.colab import files
files.download('xgboost_simswap_model.pkl')
files.download('scaler.pkl')
```

## ✅ Step 3: Verify Model Files

```bash
cd backend
python check_models.py
```

You should see:
```
✅ Model file: Found (X.XX MB)
✅ Model file: Valid pickle file
✅ Scaler file: Found (X.XX MB)
✅ Scaler file: Valid pickle file
✅ ALL CHECKS PASSED!
```

## 🚀 Step 4: Start Backend Server

```bash
cd backend
python app.py
```

Look for these messages:
```
✅ Model loaded from xgboost_simswap_model.pkl
✅ Scaler loaded from scaler.pkl
✅ ML Model loaded successfully
 * Running on http://0.0.0.0:5000
```

## 🌐 Step 5: Open ML Dashboard

Open `ml-dashboard.html` in your web browser.

You should see:
- Left panel: Input form with all fields
- Right panel: "Ready to Analyze" message
- Dark cybersecurity theme

## 🧪 Step 6: Test with Sample Data

### Test Case 1: Normal Activity (Should be SAFE)

```
Distance Change: 5 km
Time Since SIM Change: 720 hours (30 days)
Failed Logins: 0
Calls (24h): 15
SMS (24h): 8
Data Usage Change: 5%
Cell Tower Changes: 2
Is Roaming: No
SIM Change Flag: No
Device Change Flag: No
Current City: New York
Previous City: New York
```

Click "Analyze Risk" → Should show **SAFE ✅**

### Test Case 2: Suspicious Activity (Should be SUSPICIOUS)

```
Distance Change: 500 km
Time Since SIM Change: 1 hour
Failed Logins: 5
Calls (24h): 2
SMS (24h): 0
Data Usage Change: -80%
Cell Tower Changes: 10
Is Roaming: Yes
SIM Change Flag: Yes
Device Change Flag: Yes
Current City: Los Angeles
Previous City: New York
```

Click "Analyze Risk" → Should show **SUSPICIOUS 🚨**

## 🎯 What You Should See

After clicking "Analyze Risk":

1. **Loading spinner** appears briefly
2. **Risk indicator** shows:
   - SAFE ✅ (green) or SUSPICIOUS 🚨 (red)
   - Confidence percentage
3. **Risk factors** listed (if suspicious)
4. **Prediction added** to history table
5. **Download Report** button enabled

## 🧪 Optional: Run Automated Tests

```bash
cd backend
python test_ml_endpoint.py
```

This runs 4 test cases and shows results.

## 🐛 Troubleshooting

### "ML model not loaded"

**Problem**: Model files not found or invalid

**Solution**:
1. Check files are in `backend/` directory
2. Run `python check_models.py`
3. Verify file names are exactly:
   - `xgboost_simswap_model.pkl`
   - `scaler.pkl`

### "Cannot connect to API"

**Problem**: Backend server not running

**Solution**:
1. Start backend: `cd backend && python app.py`
2. Check terminal for errors
3. Verify port 5000 is not in use

### "CORS Error"

**Problem**: Frontend can't access backend

**Solution**:
- Backend already has CORS enabled
- Make sure backend is running on `http://localhost:5000`
- Check browser console for specific error

### Prediction Always Returns Same Result

**Problem**: Model might not be trained properly

**Solution**:
1. Verify model was trained on correct features
2. Check scaler was fitted on training data
3. Test with extreme values to see if prediction changes

## 📚 Next Steps

1. **Read Full Documentation**: See `ML_DASHBOARD_README.md`
2. **Customize Features**: Edit `backend/ml_predictor.py`
3. **Adjust Styling**: Modify `ml-dashboard.css`
4. **Add More Test Cases**: Update `backend/test_ml_endpoint.py`

## 🎓 For Academic Presentation

### Demo Flow

1. **Show the UI**: Clean, professional interface
2. **Explain Features**: Point out input fields and their meaning
3. **Run Normal Case**: Show SAFE prediction
4. **Run Attack Case**: Show SUSPICIOUS with risk factors
5. **Show History**: Demonstrate localStorage persistence
6. **Download Report**: Show professional text report
7. **Explain Backend**: Show code and ML integration

### Key Points to Highlight

- Real-time ML predictions
- Feature engineering pipeline
- Professional UI/UX
- RESTful API architecture
- Production-ready code
- Comprehensive error handling

## ✅ Success Checklist

- [ ] Dependencies installed
- [ ] Model files in place
- [ ] `check_models.py` passes
- [ ] Backend server starts successfully
- [ ] ML Dashboard opens in browser
- [ ] Test predictions work
- [ ] Results display correctly
- [ ] History table updates
- [ ] Report download works

## 🎉 You're Ready!

Your ML Dashboard is now fully functional and ready for:
- Development and testing
- Academic presentations
- Demo to judges
- Further customization

For detailed documentation, see `ML_DASHBOARD_README.md`

---

**SIMGuard ML Dashboard** - Final Year Project by Thinara | 2025
