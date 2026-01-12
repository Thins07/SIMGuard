# 📥 Downloadable Sample Excel Datasets

## 🎯 Ready-to-Use Excel Files for Demonstration

All sample datasets are **pre-generated** and stored in the project for immediate use.

---

## 📊 Available Datasets

### 1. **Demo Dataset (20 Users)** - RECOMMENDED FOR DEMO

**File**: `simswap_detector/datasets/dataset_demo_20users.xlsx`

**Contents**:
- Total Users: 20
- Legitimate Users: 15 (75%)
- Suspicious Users: 5 (25%)

**Use Case**: Quick demonstration, presentations, testing

**Expected Results**:
- 🚨 HIGH Risk: ~5 users
- ⚠️ MEDIUM Risk: ~0 users
- ✅ LOW Risk: ~15 users

**Download Location**: Already in project at `simswap_detector/datasets/dataset_demo_20users.xlsx`

---

### 2. **Standard Dataset (100 Users)** - RECOMMENDED FOR TESTING

**File**: `simswap_detector/datasets/dataset_standard_100users.xlsx`

**Contents**:
- Total Users: 100
- Legitimate Users: 80 (80%)
- Suspicious Users: 20 (20%)

**Use Case**: Standard testing, validation, academic evaluation

**Expected Results**:
- 🚨 HIGH Risk: ~20 users
- ⚠️ MEDIUM Risk: ~0 users
- ✅ LOW Risk: ~80 users

**Download Location**: Already in project at `simswap_detector/datasets/dataset_standard_100users.xlsx`

---

### 3. **Large Dataset (500 Users)** - FOR PERFORMANCE TESTING

**File**: `simswap_detector/datasets/dataset_large_500users.xlsx`

**Contents**:
- Total Users: 500
- Legitimate Users: 400 (80%)
- Suspicious Users: 100 (20%)

**Use Case**: Performance testing, scalability demonstration

**Expected Results**:
- 🚨 HIGH Risk: ~100 users
- ⚠️ MEDIUM Risk: ~0 users
- ✅ LOW Risk: ~400 users

**Download Location**: Already in project at `simswap_detector/datasets/dataset_large_500users.xlsx`

---

### 4. **High-Risk Scenario (50 Users)** - FOR ATTACK SIMULATION

**File**: `simswap_detector/datasets/dataset_highrisk_50users.xlsx`

**Contents**:
- Total Users: 50
- Legitimate Users: 25 (50%)
- Suspicious Users: 25 (50%)

**Use Case**: High-risk scenario simulation, attack wave demonstration

**Expected Results**:
- 🚨 HIGH Risk: ~25 users
- ⚠️ MEDIUM Risk: ~0 users
- ✅ LOW Risk: ~25 users

**Download Location**: Already in project at `simswap_detector/datasets/dataset_highrisk_50users.xlsx`

---

## 📋 Dataset Structure

All datasets contain the following columns:

| Column Name | Data Type | Description | Example |
|-------------|-----------|-------------|---------|
| user_id | String | Unique user identifier | USER_0001 |
| phone_number | String | Phone number | +94771234567 |
| operator | String | Telecom operator | Dialog, Mobitel, Hutch, Airtel |
| hours_since_sim_change | Float | Hours since SIM changed | 24.5 |
| device_changed_after_sim | Boolean | Device changed after SIM | TRUE/FALSE |
| hours_between_sim_device_change | Float | Hours between changes | 12.0 |
| previous_city | String | Previous location | Colombo |
| current_city | String | Current location | Kandy |
| hours_since_location_change | Float | Hours since location changed | 2.5 |
| cell_tower_changes_24h | Integer | Cell tower changes in 24h | 8 |
| previous_data_usage_mb | Float | Previous data usage (MB) | 1024.5 |
| current_data_usage_mb | Float | Current data usage (MB) | 3500.2 |
| previous_calls_24h | Integer | Previous calls in 24h | 15 |
| current_calls_24h | Integer | Current calls in 24h | 45 |
| previous_sms_24h | Integer | Previous SMS in 24h | 20 |
| current_sms_24h | Integer | Current SMS in 24h | 80 |
| failed_logins_24h | Integer | Failed logins in 24h | 5 |
| is_roaming | Boolean | Currently roaming | TRUE/FALSE |
| is_suspicious | Integer | Label (0=legitimate, 1=suspicious) | 0 or 1 |
| label | String | Human-readable label | Legitimate / Suspicious |

---

## 🔍 How to Access Datasets

### Method 1: Use Built-in Datasets in Dashboard (EASIEST)

1. Start dashboard: `streamlit run dashboard.py`
2. Select "Built-in Datasets"
3. Choose dataset from dropdown
4. Click "Run Detection"

**No download needed!** Datasets are already in the project.

### Method 2: Open Excel File Directly

1. Navigate to: `simswap_detector/datasets/`
2. Double-click any `.xlsx` file
3. Opens in Excel/LibreOffice
4. View data structure and contents

### Method 3: Upload to Dashboard

1. Copy dataset file to any location
2. Start dashboard: `streamlit run dashboard.py`
3. Select "Upload Excel File"
4. Browse and select the `.xlsx` file
5. Click "Run Detection"

---

## 🎬 Demo Workflow with Sample Dataset

### Quick Demo (2 Minutes)

```bash
# Step 1: Start dashboard
cd simswap_detector
streamlit run dashboard.py

# Step 2: In browser
# - Data Source: "Built-in Datasets"
# - Select: "Demo 20Users"
# - Click: "Run Detection"

# Step 3: View results
# - See 5 HIGH risk users
# - Select a user for details
# - Generate Excel report
```

---

## 📊 Sample Data Examples

### Legitimate User Example

```
user_id: USER_0001
phone_number: +94771234567
operator: Dialog
hours_since_sim_change: 720.0 (30 days)
device_changed_after_sim: FALSE
previous_city: Colombo
current_city: Colombo
cell_tower_changes_24h: 2
failed_logins_24h: 0
is_suspicious: 0
label: Legitimate

Risk Score: 0
Alert Level: LOW ✅
```

### Suspicious User Example (SIM Swap Attack)

```
user_id: USER_0085
phone_number: +94777654321
operator: Mobitel
hours_since_sim_change: 18.0 (18 hours)
device_changed_after_sim: TRUE
hours_between_sim_device_change: 3.0
previous_city: Colombo
current_city: Jaffna (300km away)
hours_since_location_change: 1.5
cell_tower_changes_24h: 15
previous_data_usage_mb: 1000
current_data_usage_mb: 4500 (350% increase)
failed_logins_24h: 8
is_roaming: FALSE
is_suspicious: 1
label: Suspicious

Risk Score: 95
Alert Level: HIGH 🚨

Triggered Rules:
1. Recent SIM change (20 points)
2. Device changed after SIM (25 points)
3. Sudden location change (15 points)
4. Abnormal cell tower changes (10 points)
5. Abnormal data usage (10 points)
6. Failed login attempts (20 points)
```

---

## 🔄 Regenerate Datasets

If you need to regenerate datasets with different parameters:

```bash
cd simswap_detector
python data_generator.py
```

**Customization**: Edit `data_generator.py` to change:
- Number of users
- Legitimate vs suspicious ratio
- Attack scenarios
- Sri Lankan cities and operators

---

## ✅ Dataset Validation

All datasets are validated to ensure:

- ✅ All required columns present
- ✅ Correct data types
- ✅ Realistic Sri Lankan telecom patterns
- ✅ Valid city names (25 Sri Lankan districts)
- ✅ Valid operators (Dialog, Mobitel, Hutch, Airtel)
- ✅ Logical data relationships
- ✅ Both legitimate and suspicious scenarios

---

## 📥 Download for External Use

To share datasets externally:

1. **Copy from project**:
   ```
   simswap_detector/datasets/dataset_demo_20users.xlsx
   ```

2. **Share via**:
   - Email attachment
   - Cloud storage (Google Drive, OneDrive)
   - USB drive
   - Network share

3. **Recipients can**:
   - Open in Excel/LibreOffice
   - Upload to dashboard
   - Use for testing
   - Analyze data structure

---

## 🎓 Academic Use

These datasets are suitable for:

- ✅ Final year project demonstrations
- ✅ Academic presentations
- ✅ Research validation
- ✅ Algorithm testing
- ✅ System evaluation
- ✅ Performance benchmarking

**Citation**: If using in academic work, cite as:
```
SIM Swap Detection System - Synthetic Test Dataset
Generated using rule-based scenario simulation
Sri Lankan telecom context (2024)
```

---

## 🎉 Ready to Use!

All sample datasets are:
- ✅ Pre-generated and ready
- ✅ Stored in project
- ✅ Accessible via dashboard
- ✅ Downloadable for external use
- ✅ Validated and tested
- ✅ Demo-ready

**Start using**: `streamlit run dashboard.py` → Select "Built-in Datasets" → Choose dataset → Run Detection!

---

**Last Updated**: December 21, 2024  
**Dataset Version**: 1.0.0

