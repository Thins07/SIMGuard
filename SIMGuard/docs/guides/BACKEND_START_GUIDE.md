# 🚀 Backend Server Start Guide

## ✅ Fixed Issues

1. ✅ **File upload double-click bug** - FIXED in `sl-ml-dashboard.js`
2. ✅ **Backend syntax error** - FIXED in `backend/sl_ml_handler.py`

---

## 🔧 Start Backend Server

### Method 1: PowerShell (Recommended)

```powershell
# Navigate to project directory
cd C:\Users\Thinara\Documents\augment-projects\SIMGuard

# Start backend
python backend/app.py
```

### Method 2: Command Prompt

```cmd
cd C:\Users\Thinara\Documents\augment-projects\SIMGuard
python backend\app.py
```

### Method 3: VS Code Terminal

1. Open VS Code
2. Open Terminal (Ctrl + `)
3. Run:
```bash
python backend/app.py
```

---

## ✅ Expected Output

When backend starts successfully, you should see:

```
INFO:__main__:Starting SIMGuard Backend API...
INFO:__main__:Upload folder: uploads
INFO:__main__:Max file size: 16.0MB
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.x.x:5000
INFO:werkzeug:Press CTRL+C to quit
WARNING:werkzeug: * Debugger is active!
INFO:werkzeug: * Debugger PIN: xxx-xxx-xxx
```

**Note**: You may see a warning about ML model not found - this is OK! The Sri Lankan endpoints will still work.

---

## 🧪 Test Backend is Running

### Option 1: Browser Test

Open browser and go to:
```
http://localhost:5000
```

You should see:
```json
{
  "status": "success",
  "message": "SIMGuard Backend API is running",
  "version": "1.0.0"
}
```

### Option 2: PowerShell Test

```powershell
Invoke-WebRequest -Uri http://localhost:5000 -Method GET
```

### Option 3: Python Test

```python
import requests
response = requests.get('http://localhost:5000')
print(response.json())
```

---

## 🌐 Open Dashboard

Once backend is running:

1. Open `sl-ml-dashboard.html` in browser
2. Click "Select Excel File" → Opens **ONCE** ✅
3. Select `sample_sl_dataset.xlsx`
4. Click "Analyze File"
5. Dataset should load successfully

---

## 🐛 Troubleshooting

### Problem: "Address already in use"

**Cause**: Port 5000 is already in use

**Solution**:
```powershell
# Find process using port 5000
netstat -ano | findstr :5000

# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F

# Restart backend
python backend/app.py
```

### Problem: "ModuleNotFoundError"

**Cause**: Missing Python packages

**Solution**:
```powershell
cd backend
pip install -r requirements.txt
```

### Problem: Backend starts but dashboard can't connect

**Cause**: Firewall blocking connection

**Solution**:
1. Check Windows Firewall settings
2. Allow Python through firewall
3. Try accessing `http://127.0.0.1:5000` instead of `localhost`

### Problem: "Failed to fetch" in dashboard

**Cause**: Backend not running or wrong URL

**Solution**:
1. Verify backend is running (check terminal)
2. Check browser console (F12) for errors
3. Verify API URL in `sl-ml-dashboard.js` line 7:
   ```javascript
   const API_BASE_URL = 'http://localhost:5000';
   ```

---

## 📊 Complete Test Workflow

### Step 1: Start Backend
```powershell
python backend/app.py
```

Wait for: `Running on http://127.0.0.1:5000`

### Step 2: Test Backend
Open browser: `http://localhost:5000`

Should see: `"status": "success"`

### Step 3: Open Dashboard
Open `sl-ml-dashboard.html` in browser

### Step 4: Test File Upload
1. Click "Select Excel File" → Opens **ONCE** ✅
2. Select `sample_sl_dataset.xlsx`
3. File info displays ✅

### Step 5: Test Analysis
1. Click "Analyze File" button
2. Wait 2-5 seconds
3. Dataset preview appears ✅
4. Shows: "51 rows" ✅

### Step 6: Test Model Training
1. Keep "XGBoost Classifier" selected
2. Click "Train Model"
3. Wait 5-10 seconds
4. Results appear ✅
5. Accuracy: ~95-98% ✅

### Step 7: Test Prediction
1. Fill in prediction form
2. Select cities from dropdowns
3. Click "Predict"
4. Result appears: SAFE ✅ or SUSPICIOUS 🚨

---

## ✅ Success Indicators

Backend is working if:
- ✅ Terminal shows "Running on http://127.0.0.1:5000"
- ✅ Browser shows API response at `http://localhost:5000`
- ✅ No error messages in terminal

Dashboard is working if:
- ✅ File explorer opens **ONCE** when clicking button
- ✅ File info displays after selection
- ✅ "Analyze File" button appears
- ✅ Dataset loads successfully
- ✅ Model trains successfully
- ✅ Predictions work

---

## 🎯 Quick Commands

```powershell
# Start backend
python backend/app.py

# Test backend (in another terminal)
curl http://localhost:5000

# Stop backend
# Press Ctrl+C in terminal
```

---

## 📝 Notes

1. **Keep backend running** while using dashboard
2. **Don't close terminal** where backend is running
3. **Refresh dashboard** (F5) if connection fails
4. **Check terminal** for error messages
5. **Use sample_sl_dataset.xlsx** for testing

---

**Backend is ready! Now test the dashboard with the fixed file upload!** 🎉

