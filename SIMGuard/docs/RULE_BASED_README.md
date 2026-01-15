# SIMGuard (Rule-Based Final Submission)

This README describes how to run and verify the FINAL rule-based version of SIMGuard for your academic submission.

## 1) Backend Setup
- Python 3.9+ recommended.
- From `backend/`: install dependencies
  - `pip install -r requirements.txt`
  - Ensure `openpyxl` is installed for Excel support.
- Run API
  - `python run.py` (or `python app.py`)
  - The API listens on `http://localhost:5000`.

## 2) Supported Dataset Formats
- File types: `.csv`, `.xlsx`, `.xls`
- Required columns (minimum): `timestamp`, `user_id`, `sim_id`, `device_id`, `location`, and one of `ip` or `ip_address`, and one of `login_status` or `success`.
- Timestamps should be valid datetime strings; locations should be city names (e.g., "New York", "London").

## 3) End-to-End Flow
1. Open `frontend/site/index.html` in your browser (static pages).
2. Go to **Upload** page, select CSV/Excel, click **Upload & Analyze** (this calls `/upload` then `/analyze`).
3. Go to **Dashboard** to view summaries and suspicious users (fetches `/results`).
4. Go to **Report** and click **Download PDF** (calls `/report`).

## 4) What is Included
- Rule-based engine only (ML endpoints are disabled).
- Multi-page web flow: Introduction → Upload → Dashboard → Report.
- PDF report with executive summary, summaries, risk distribution, and suspicious activity table.

## 5) Troubleshooting
- If results are empty, re-upload and run **Upload & Analyze**, then refresh the Dashboard.
- File size limit: 16MB.
- Ensure column names match the required set; see samples in `data/samples/`.

## 6) Clean-Up & Scope
- Legacy heuristic function `analyze_user_behavior` remains documented but is unused; the active path uses the shared rule engine.
- ML functionality is intentionally disabled for this final submission.
