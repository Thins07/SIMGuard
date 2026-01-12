# 🔧 Troubleshooting Guide - SIM Swap Detection System

## Common Issues and Solutions

---

## 🚨 Issue 1: File Upload Failed

### Symptoms
- Error message when uploading Excel file
- "Failed to fetch" error
- File upload button not working

### Solution ✅

**The file upload issue has been FIXED!** The system now uses session state management.

**Steps to verify fix**:

1. **Restart dashboard**:
   ```bash
   cd simswap_detector
   streamlit run dashboard.py
   ```

2. **Clear browser cache**: Press `Ctrl + F5` (hard refresh)

3. **Try uploading**:
   - Select "Upload Excel File"
   - Upload any `.xlsx` file from `datasets/` folder
   - Click "Run Detection"
   - Should work! ✅

**If still failing**:
- Check file format (must be `.xlsx` or `.xls`)
- Check file size (should be < 200MB)
- Check file has required columns (see README)
- Use built-in datasets instead (no upload needed)

---

## 🚨 Issue 2: Dashboard Won't Start

### Symptoms
- `streamlit: command not found`
- `ModuleNotFoundError: No module named 'streamlit'`
- Dashboard doesn't open in browser

### Solution ✅

**Step 1: Install dependencies**
```bash
cd simswap_detector
pip install -r requirements.txt
```

**Step 2: Verify installation**
```bash
python -c "import streamlit; import pandas; import openpyxl; print('✅ All OK')"
```

**Step 3: Try again**
```bash
streamlit run dashboard.py
```

**If still failing**:
- Check Python version: `python --version` (should be 3.8+)
- Upgrade pip: `python -m pip install --upgrade pip`
- Reinstall streamlit: `pip install streamlit==1.29.0`

---

## 🚨 Issue 3: No Built-in Datasets Found

### Symptoms
- "No built-in datasets found" message
- Empty dropdown in dashboard
- Can't select built-in datasets

### Solution ✅

**Generate datasets**:
```bash
cd simswap_detector
python data_generator.py
```

**Expected output**:
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

**Verify datasets exist**:
```bash
dir simswap_detector\datasets  # Windows
ls simswap_detector/datasets   # Linux/Mac
```

Should see 4 `.xlsx` files.

---

## 🚨 Issue 4: Port 8501 Already in Use

### Symptoms
- `Address already in use`
- `Port 8501 is already in use`
- Dashboard won't start

### Solution ✅

**Option 1: Use different port**
```bash
streamlit run dashboard.py --server.port 8502
```

**Option 2: Kill existing process**

Windows:
```powershell
netstat -ano | findstr :8501
taskkill /PID <PID> /F
```

Linux/Mac:
```bash
lsof -ti:8501 | xargs kill -9
```

**Option 3: Restart computer**

---

## 🚨 Issue 5: Detection Not Running

### Symptoms
- "Run Detection" button doesn't work
- No results displayed
- Spinner keeps spinning

### Solution ✅

**Check data loaded**:
- Ensure you see "✅ Loaded X records" in sidebar
- If not, reload data source

**Check for errors**:
- Look for red error messages
- Check browser console (F12 → Console tab)

**Try different dataset**:
- Switch to "Demo 20Users" (smallest dataset)
- Click "Run Detection"

**Restart dashboard**:
```bash
# Press Ctrl+C in terminal
# Then restart:
streamlit run dashboard.py
```

---

## 🚨 Issue 6: Report Generation Failed

### Symptoms
- "Generate Report" button doesn't work
- Download button not appearing
- Error when generating report

### Solution ✅

**Ensure detection completed**:
- Must run detection first
- Wait for "✅ Detection complete!" message

**Check file permissions**:
- Ensure you have write permissions in current directory
- Try running as administrator (Windows)

**Try different format**:
- If Excel fails, try CSV
- If CSV fails, try Excel

**Check disk space**:
- Ensure you have enough disk space
- Reports are typically < 1MB

---

## 🚨 Issue 7: Excel File Won't Open

### Symptoms
- "File is corrupted" error
- Excel won't open generated datasets
- "File format not recognized"

### Solution ✅

**Regenerate datasets**:
```bash
cd simswap_detector
python data_generator.py
```

**Check file extension**:
- Must be `.xlsx` (not `.xls` or `.csv`)

**Try different Excel viewer**:
- Microsoft Excel
- LibreOffice Calc
- Google Sheets (upload to Drive)

**Check openpyxl version**:
```bash
pip install openpyxl==3.1.2
```

---

## 🚨 Issue 8: Browser Not Opening Automatically

### Symptoms
- Dashboard starts but browser doesn't open
- Terminal shows URL but nothing happens

### Solution ✅

**Manual open**:
1. Look for this in terminal:
   ```
   Local URL: http://localhost:8501
   ```
2. Copy URL
3. Open browser manually
4. Paste URL in address bar

**Check default browser**:
- Set default browser in Windows/Mac settings
- Try different browser (Chrome, Firefox, Edge)

**Use network URL**:
- Look for "Network URL" in terminal
- Try that URL instead

---

## 🚨 Issue 9: Slow Performance

### Symptoms
- Dashboard is slow
- Detection takes too long
- Browser freezes

### Solution ✅

**Use smaller dataset**:
- Switch to "Demo 20Users" instead of "Large 500Users"
- Upload smaller Excel files

**Close other tabs**:
- Close unused browser tabs
- Close other applications

**Restart dashboard**:
```bash
# Press Ctrl+C
streamlit run dashboard.py
```

**Check system resources**:
- Task Manager (Windows) / Activity Monitor (Mac)
- Ensure enough RAM available
- Close memory-intensive apps

---

## 🚨 Issue 10: Import Errors

### Symptoms
- `ModuleNotFoundError`
- `ImportError`
- Missing dependencies

### Solution ✅

**Reinstall all dependencies**:
```bash
cd simswap_detector
pip install -r requirements.txt --force-reinstall
```

**Check Python version**:
```bash
python --version
```
Should be 3.8 or higher.

**Create virtual environment** (recommended):
```bash
# Create venv
python -m venv venv

# Activate venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

---

## 🛠️ General Debugging Steps

### 1. Check Terminal Output
- Look for error messages in terminal
- Read full error traceback
- Note line numbers

### 2. Check Browser Console
- Press F12 in browser
- Go to Console tab
- Look for JavaScript errors

### 3. Clear Cache
- Browser: Ctrl + F5 (hard refresh)
- Streamlit: Delete `.streamlit` folder

### 4. Restart Everything
```bash
# Stop dashboard (Ctrl+C)
# Restart dashboard
cd simswap_detector
streamlit run dashboard.py
```

### 5. Check File Paths
- Ensure you're in correct directory
- Use `cd simswap_detector` before running commands
- Check file paths are correct

---

## 📞 Quick Fixes Checklist

Before asking for help, try these:

- [ ] Restart dashboard (Ctrl+C, then `streamlit run dashboard.py`)
- [ ] Clear browser cache (Ctrl + F5)
- [ ] Reinstall dependencies (`pip install -r requirements.txt`)
- [ ] Regenerate datasets (`python data_generator.py`)
- [ ] Check Python version (`python --version` → should be 3.8+)
- [ ] Try different dataset (use "Demo 20Users")
- [ ] Check terminal for errors
- [ ] Check browser console (F12)
- [ ] Use built-in datasets instead of upload
- [ ] Restart computer

---

## 🎯 Still Having Issues?

### Collect This Information:

1. **Error message** (full text)
2. **Terminal output** (copy/paste)
3. **Browser console errors** (F12 → Console)
4. **Python version** (`python --version`)
5. **Operating system** (Windows/Mac/Linux)
6. **What you were trying to do**
7. **Steps to reproduce**

### Check Documentation:

- `START_HERE.md` - Quick start guide
- `MVP_SETUP_GUIDE.md` - Complete setup
- `README_SIMSWAP_DETECTOR.md` - Full documentation
- `FILE_UPLOAD_FIX_SUMMARY.md` - File upload fix details

---

## ✅ System Health Check

Run this to verify everything is working:

```bash
# 1. Check Python
python --version

# 2. Check dependencies
python -c "import streamlit; import pandas; import openpyxl; print('✅ All OK')"

# 3. Check datasets
dir simswap_detector\datasets  # Windows
ls simswap_detector/datasets   # Linux/Mac

# 4. Run tests
python simswap_detector/test_system.py

# 5. Start dashboard
cd simswap_detector
streamlit run dashboard.py
```

If all steps pass, system is healthy! ✅

---

**Last Updated**: December 21, 2024  
**Version**: MVP 1.0.0  
**Status**: File upload issue FIXED ✅

