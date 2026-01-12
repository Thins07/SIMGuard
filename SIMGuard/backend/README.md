# SIMGuard Backend API

Flask-based backend API for the SIMGuard SIM swap detection tool. This API provides endpoints for file upload, analysis, and report generation for detecting suspicious SIM swapping activities.

## Features

- **File Upload**: Accept and validate CSV files containing user activity logs
- **SIM Swap Detection**: Analyze user behavior patterns to detect suspicious activities
- **Real-time Analysis**: Process uploaded data and identify potential SIM swap attacks
- **PDF Report Generation**: Create comprehensive investigation reports
- **RESTful API**: Clean, well-documented API endpoints
- **CORS Enabled**: Support for frontend integration
- **Error Handling**: Comprehensive error handling and validation

## API Endpoints

### 1. Health Check
```
GET /
```
Returns API status and available endpoints.

### 2. File Upload
```
POST /upload
```
Upload CSV file for analysis.

**Request**: Multipart form data with 'file' field
**Response**: Upload confirmation with file metadata

### 3. Data Analysis
```
POST /analyze
```
Perform SIM swap detection analysis on uploaded data.

**Response**: Analysis summary with statistics

### 4. Get Results
```
GET /results
```
Retrieve detailed analysis results and suspicious activities.

**Response**: Complete analysis results with flagged activities

### 5. Generate Report
```
GET /report
```
Download PDF investigation report.

**Response**: PDF file download

### 6. System Status
```
GET /status
```
Get current system status and data state.

### 7. Clear Data
```
POST /clear
```
Clear uploaded data and analysis results.

## CSV File Format

The uploaded CSV file must contain the following columns:

| Column | Description | Example |
|--------|-------------|---------|
| `timestamp` | Activity timestamp | `2025-01-10 14:30:15` |
| `user_id` | Unique user identifier | `USR0001` |
| `sim_id` | SIM card identifier | `SIM12345` |
| `device_id` | Device identifier | `DEV001` |
| `ip` | IP address | `192.168.1.100` |
| `location` | User location | `New York` |
| `login_status` | Login success/failure | `success` or `failed` |

### Sample CSV Data
```csv
timestamp,user_id,sim_id,device_id,ip,location,login_status
2025-01-10 14:30:15,USR0001,SIM12345,DEV001,192.168.1.100,New York,success
2025-01-10 14:35:12,USR0001,SIM54321,DEV003,203.0.113.45,Miami,success
```

## Detection Algorithms

The system analyzes the following patterns to detect SIM swap attacks:

### 1. SIM ID Changes
- Detects when a user's SIM ID changes between sessions
- **Risk Level**: High

### 2. Impossible Travel
- Identifies location changes that are physically impossible
- **Criteria**: >500km distance in <2 hours
- **Risk Level**: High

### 3. Suspicious Location Changes
- Flags rapid location changes that are unusual
- **Criteria**: >100km distance in <30 minutes
- **Risk Level**: Medium

### 4. Device Changes
- Detects when user switches to a different device
- **Risk Level**: Medium

### 5. IP Address Changes
- Identifies suspicious IP address changes
- **Criteria**: Different network ranges
- **Risk Level**: Medium

### 6. Failed Logins After Changes
- Flags failed login attempts following suspicious activities
- **Risk Level**: High

### 7. Rapid Successive Changes
- Detects multiple changes occurring within short time periods
- **Criteria**: Multiple flags within 6 minutes
- **Risk Level**: High

## Installation and Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation Steps

1. **Clone the repository**
```bash
git clone <repository-url>
cd SIMGuard/backend
```

2. **Create virtual environment** (recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
python app.py
```

The API will be available at `http://localhost:5000`

### Docker Setup (Optional)

Create a `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["python", "app.py"]
```

Build and run:
```bash
docker build -t simguard-backend .
docker run -p 5000:5000 simguard-backend
```

## Configuration

### Environment Variables
- `FLASK_ENV`: Set to `development` for debug mode
- `FLASK_PORT`: Custom port (default: 5000)
- `MAX_FILE_SIZE`: Maximum upload file size in bytes

### File Upload Limits
- Maximum file size: 16MB
- Supported formats: CSV only
- Temporary storage in `uploads/` directory

## API Usage Examples

### Upload File
```bash
curl -X POST -F "file=@sample_logs.csv" http://localhost:5000/upload
```

### Analyze Data
```bash
curl -X POST http://localhost:5000/analyze
```

### Get Results
```bash
curl -X GET http://localhost:5000/results
```

### Download Report
```bash
curl -X GET http://localhost:5000/report -o investigation_report.pdf
```

## Response Format

All API responses follow this format:

```json
{
  "status": "success|error",
  "message": "Description of the result",
  "data": { ... }
}
```

### Error Responses
```json
{
  "status": "error",
  "message": "Error description"
}
```

## Security Considerations

- File type validation prevents malicious uploads
- File size limits prevent DoS attacks
- Temporary file cleanup prevents disk space issues
- Input validation on all endpoints
- CORS configured for specific origins in production

## Performance

- Supports concurrent requests through threading
- Memory-efficient CSV processing with pandas
- Optimized analysis algorithms for large datasets
- PDF generation in memory to avoid disk I/O

## Testing

### Sample Test Data
Use the provided `sample_logs.csv` file for testing:

```bash
# Upload sample data
curl -X POST -F "file=@../sample_logs.csv" http://localhost:5000/upload

# Run analysis
curl -X POST http://localhost:5000/analyze

# Get results
curl -X GET http://localhost:5000/results
```

### Expected Results
The sample data contains several suspicious activities:
- SIM ID changes for user USR0001
- Location changes from New York to Miami
- Device changes
- IP address changes

## Troubleshooting

### Common Issues

1. **File Upload Fails**
   - Check file format (must be CSV)
   - Verify file size (<16MB)
   - Ensure required columns are present

2. **Analysis Errors**
   - Verify data was uploaded successfully
   - Check CSV column names match requirements
   - Ensure timestamp format is valid

3. **Report Generation Fails**
   - Ensure analysis was completed first
   - Check available disk space
   - Verify fpdf2 is installed correctly

### Logging
The application logs important events and errors. Check console output for debugging information.

## Development

### Code Structure
```
backend/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── uploads/           # Temporary file storage
└── README.md          # This file
```

### Adding New Detection Rules
To add new detection algorithms, modify the `analyze_user_behavior()` function in `app.py`:

```python
def analyze_user_behavior(user_data):
    # Add your custom detection logic here
    pass
```

## License

This project is developed for educational purposes as part of a final year cybersecurity project.

## Support

For questions or issues, please contact the development team or create an issue in the project repository.

---

**SIMGuard Backend** - Protecting against SIM swapping attacks through intelligent detection and analysis.
