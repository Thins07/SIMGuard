# 🚀 Quick Start Guide - SIM Swap Detection System

## ⚡ 5-Minute Setup

### Step 1: Install Dependencies (1 minute)

```bash
cd simswap_detector
pip install -r requirements.txt
```

### Step 2: Run Dashboard (30 seconds)

```bash
streamlit run dashboard.py
```

Browser opens automatically at `http://localhost:8501`

### Step 3: Upload Test Data (30 seconds)

1. Click **"Browse files"** in sidebar
2. Navigate to `data/simswap_test_data.xlsx`
3. Click **"Open"**
4. Wait for ✅ "Loaded 100 records"

### Step 4: Run Detection (1 minute)

1. Click **"Run Detection"** button in sidebar
2. Wait for analysis (~2-3 seconds)
3. See ✅ "Detection complete!"

### Step 5: View Results (2 minutes)

**Summary Metrics** (top of page):
- Total Users: 100
- 🚨 High Risk: ~20
- ⚠️ Medium Risk: ~0-5
- ✅ Low Risk: ~75-80

**Filter Results**:
- Select alert levels: HIGH, MEDIUM, LOW
- Adjust minimum risk score slider

**Detailed Analysis**:
- Select a user from dropdown
- View triggered rules
- See risk score breakdown

**Export Results**:
- Scroll to bottom
- Click "📥 Download Results (CSV)"

---

## 🎯 Expected Results

### High Risk Users (Score 61-100)

Example: **USER_0085**
```
Risk Score: 95
Alert Level: 🚨 HIGH

Triggered Rules:
✅ Recent SIM change (20 points)
✅ Device changed after SIM (25 points)
✅ Sudden location change (15 points)
✅ Abnormal cell tower changes (10 points)
✅ Data usage increased 350% (10 points)
✅ Failed login attempts: 12 (20 points)
```

### Low Risk Users (Score 0-30)

Example: **USER_0001**
```
Risk Score: 0
Alert Level: ✅ LOW

Triggered Rules:
❌ No suspicious activity detected
```

---

## 📊 Dashboard Features

### 1. Summary Metrics
- Total users analyzed
- Count by alert level (HIGH/MEDIUM/LOW)

### 2. Filter Options
- **Alert Level**: Select HIGH, MEDIUM, or LOW
- **Minimum Risk Score**: Slider from 0-100

### 3. Results Table
- User ID
- Risk Score
- Alert Level (with emoji)
- Number of rules triggered
- Rule details

### 4. Detailed Analysis
- Select individual user
- View all triggered rules
- See rule weights and reasons

### 5. Export
- Download results as CSV
- Includes all users and details

---

## 🔧 Customization

### Change Rule Thresholds

Edit `config.py`:

```python
# Make detection more strict
SIM_CHANGE_HOURS_THRESHOLD = 48  # Default: 72
FAILED_LOGIN_COUNT_THRESHOLD = 2  # Default: 3

# Make detection more lenient
LOCATION_DISTANCE_KM_THRESHOLD = 200  # Default: 100
```

### Change Risk Weights

Edit `config.py`:

```python
RISK_WEIGHTS = {
    'recent_sim_change': 30,  # Increase importance
    'failed_login_attempts': 25,  # Increase importance
    # ... other weights
}
```

### Generate More Test Data

```bash
python data_generator.py
```

Edit `data_generator.py` to change:
- Number of users
- Suspicious vs legitimate ratio
- Scenario types

---

## 🐛 Troubleshooting

### Dashboard won't start

```bash
# Check streamlit installation
streamlit --version

# Reinstall if needed
pip install streamlit==1.29.0

# Try running again
streamlit run dashboard.py
```

### "File not found" error

```bash
# Regenerate test data
python data_generator.py

# Check data folder exists
ls ../data/
```

### Import errors

```bash
# Reinstall all dependencies
pip install -r requirements.txt --force-reinstall
```

---

## 📝 Command Reference

```bash
# Install dependencies
pip install -r requirements.txt

# Run dashboard
streamlit run dashboard.py

# Generate test data
python data_generator.py

# Check Python version
python --version  # Should be 3.8+

# Check installed packages
pip list
```

---

## ✅ Verification Checklist

Before demo:

- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Test data exists (`data/simswap_test_data.xlsx`)
- [ ] Dashboard starts (`streamlit run dashboard.py`)
- [ ] Data uploads successfully
- [ ] Detection runs without errors
- [ ] Results display correctly
- [ ] Export works (CSV download)

---

## 🎓 Demo Script

**For Academic Presentation**:

1. **Introduction** (1 min)
   - "This is a rule-based SIM swap detection system"
   - "Uses 9 behavioral rules to detect attacks"

2. **Upload Data** (30 sec)
   - "I'll upload our test dataset with 100 users"
   - "80 legitimate, 20 suspicious"

3. **Run Detection** (30 sec)
   - "Click Run Detection"
   - "System evaluates all 9 rules for each user"

4. **Show Results** (2 min)
   - "20 high-risk users detected"
   - "Let's look at USER_0085 in detail"
   - "6 rules triggered, risk score 95"

5. **Explain Rules** (2 min)
   - "Recent SIM change: 20 hours ago"
   - "Device changed 5 hours after SIM"
   - "Location jumped 300km in 1 hour"
   - "12 failed login attempts"

6. **Show Legitimate User** (1 min)
   - "USER_0001 has risk score 0"
   - "No suspicious patterns detected"

7. **Export** (30 sec)
   - "Results can be exported for further analysis"

**Total Time**: ~7 minutes

---

## 🎉 You're Ready!

Your SIM swap detection system is now:
- ✅ Fully functional
- ✅ Tested with realistic data
- ✅ Ready for demonstration
- ✅ Ready for academic evaluation

**Good luck with your final year project!** 🎓

