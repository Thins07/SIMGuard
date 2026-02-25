# SIMGuard – Security & User Data Confidentiality

This document describes where user/subscriber data lives in the project and concrete steps to keep it confidential. No code structure changes are required; these are configuration, deployment, and operational practices.

---

## 1. Where User Data Lives (Current Flow)

| Location | Data | Risk if exposed |
|----------|------|------------------|
| **Uploaded files** | `backend/uploads/` — CSV/Excel with user_id, location, timestamps, login status, etc. | High: full telemetry |
| **Training uploads** | Same folder: `uploads/training_data.csv` (overwritten per upload) | High: same as above |
| **In-memory** | `uploaded_data`, `analysis_results` in Flask app (batch analysis + report) | High while server runs |
| **Manual check** | Request body to `/predict` (time since SIM change, distance, data usage %, failed logins, flags) | Medium: single-user snapshot |
| **PDF report** | Only summary counts in current implementation (no per-user PII in PDF) | Low |
| **API responses** | `/results` returns `user_id`, `risk_level`, `flag_reason`; suspicious_activities list | Medium: identifiers + risk |

Your `.gitignore` already excludes `backend/uploads/` and `backend/reports/`, so uploaded files and reports are not committed.

---

## 2. Steps to Keep User Data Confidential

### A. Secrets & configuration

- **SECRET_KEY**  
  - Currently in code (`app.config['SECRET_KEY'] = '...'`).  
  - **Step:** Read from environment, e.g. `os.environ.get('SIMGUARD_SECRET_KEY')` or a `.env` file (with `.env` in `.gitignore`). Use a long, random value in production.

- **API keys / DB URLs**  
  - If you add external services later, keep keys and URLs in environment variables or a secrets manager, never in the repo.

### B. Transport (data in transit)

- **HTTPS**  
  - **Step:** In production, run the app behind a reverse proxy (e.g. Nginx, Caddy) or a cloud load balancer that terminates TLS. Do not send real user data over plain HTTP on the public internet.

- **CORS**  
  - Currently `CORS(app, origins=['*'])`.  
  - **Step:** In production, set `origins` to the exact frontend origin(s), e.g. `['https://your-simguard-domain.com']`, to reduce risk of unauthorized sites calling your API.

### C. Data at rest

- **Upload folder**  
  - **Step:** Ensure `uploads/` (and any folder holding training data) has strict filesystem permissions (e.g. only the app user can read/write).  
  - **Step:** Optionally wipe or overwrite files after analysis/training, or move them to a restricted, encrypted storage location.

- **Training dataset**  
  - Training data in `uploads/training_data.csv` is sensitive. **Step:** Restrict access to the server and, if possible, use encrypted storage or a secure data store for production training pipelines.

### D. Access control

- **No authentication on endpoints**  
  - `/upload`, `/analyze`, `/results`, `/predict`, `/report`, `/upload_train`, `/train` are unauthenticated.  
  - **Step:** For production, add authentication (e.g. API keys, JWT, or session-based auth) and optionally role-based access so only authorized operators can upload data, run analysis, or download reports.  
  - **Step:** Restrict admin-only actions (e.g. training, diagnostics) to a separate role or path.

### E. Logging and monitoring

- **Step:** Avoid logging request/response bodies that contain PII (user_id, locations, timestamps, failed logins, etc.). Log only what’s needed (e.g. endpoint, status code, non-identifying error messages).  
- **Step:** If logs are stored centrally, treat them as confidential and apply the same access and retention policies as for the main dataset.

### F. Deployment and runtime

- **Step:** In production, run with `debug=False` (Flask) so stack traces and internal details are not exposed.  
- **Step:** Bind to a loopback or internal interface (e.g. `127.0.0.1`) when the app is only reached via a reverse proxy; avoid exposing the app directly on `0.0.0.0` to the internet unless necessary and protected.

### G. Data minimization in responses

- **Step:** If you need to share results with third parties, consider returning or exporting only aggregated stats and risk bands, not `user_id` or raw telemetry.  
- **Step:** For the PDF report, the current implementation already limits content to summary-level information; keep that approach and avoid adding per-user PII to reports unless strictly required.

### H. Model and artifact handling

- **Step:** Treat trained models (e.g. `.pkl`) as part of your security boundary: restrict who can deploy or replace them, and store them in a secure, access-controlled location.  
  - If you prefer not to track binary artifacts in git, add `*.pkl` (or your model paths) to `.gitignore` and deliver models via a secure pipeline instead.

---

## 3. Quick checklist (no code structure change)

- [ ] Move `SECRET_KEY` (and any future secrets) to environment variables.
- [ ] Use HTTPS and restrict CORS to the real frontend origin(s) in production.
- [ ] Restrict filesystem permissions on `uploads/` and any training data paths.
- [ ] Add authentication (and optional RBAC) for production API access.
- [ ] Avoid logging PII; secure and restrict access to logs.
- [ ] Run with `debug=False` and bind to a safe host/port behind a reverse proxy.
- [ ] Keep API responses and reports minimal (no unnecessary PII).

These steps keep your existing code structure intact while improving confidentiality and security of user data.
