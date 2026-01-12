# SIMGuard Deployment Guide

This guide covers various deployment options for the SIMGuard application, from local development to production environments.

## 📋 Prerequisites

- Python 3.8 or higher
- Git
- Modern web browser
- (Optional) Docker for containerized deployment

## 🚀 Local Development Deployment

### Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/SIMGuard.git
cd SIMGuard
```

2. **Set up Python environment**
```bash
cd backend
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Start the backend server**
```bash
python app.py
```

5. **Open the frontend**
```bash
# Navigate back to project root
cd ..
# Open index.html in your browser
```

### Development Configuration

For development, you can modify these settings in `backend/app.py`:

```python
# Development settings
app.run(
    host='127.0.0.1',  # Localhost only
    port=5000,
    debug=True,        # Enable debug mode
    threaded=True
)
```

## 🌐 Production Deployment

### Option 1: Traditional Server Deployment

#### 1. Server Setup (Ubuntu/Debian)

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3 python3-pip python3-venv nginx -y

# Create application user
sudo useradd -m -s /bin/bash simguard
sudo su - simguard
```

#### 2. Application Setup

```bash
# Clone repository
git clone https://github.com/yourusername/SIMGuard.git
cd SIMGuard

# Set up Python environment
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Install production WSGI server
pip install gunicorn
```

#### 3. Create Gunicorn Configuration

Create `backend/gunicorn.conf.py`:
```python
bind = "127.0.0.1:5000"
workers = 4
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 30
keepalive = 2
preload_app = True
```

#### 4. Create Systemd Service

Create `/etc/systemd/system/simguard.service`:
```ini
[Unit]
Description=SIMGuard Flask Application
After=network.target

[Service]
User=simguard
Group=simguard
WorkingDirectory=/home/simguard/SIMGuard/backend
Environment=PATH=/home/simguard/SIMGuard/backend/venv/bin
ExecStart=/home/simguard/SIMGuard/backend/venv/bin/gunicorn -c gunicorn.conf.py app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

#### 5. Configure Nginx

Create `/etc/nginx/sites-available/simguard`:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Frontend static files
    location / {
        root /home/simguard/SIMGuard;
        index index.html;
        try_files $uri $uri/ =404;
    }

    # Backend API
    location /api/ {
        proxy_pass http://127.0.0.1:5000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # File upload size limit
    client_max_body_size 16M;
}
```

#### 6. Enable and Start Services

```bash
# Enable Nginx site
sudo ln -s /etc/nginx/sites-available/simguard /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Enable and start SIMGuard service
sudo systemctl enable simguard
sudo systemctl start simguard
sudo systemctl status simguard
```

### Option 2: Docker Deployment

#### 1. Create Dockerfile

Create `backend/Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create uploads directory
RUN mkdir -p uploads

# Expose port
EXPOSE 5000

# Run application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]
```

#### 2. Create Docker Compose

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  simguard-backend:
    build: ./backend
    ports:
      - "5000:5000"
    volumes:
      - ./backend/uploads:/app/uploads
    environment:
      - FLASK_ENV=production
    restart: unless-stopped

  simguard-frontend:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./:/usr/share/nginx/html
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
    depends_on:
      - simguard-backend
    restart: unless-stopped
```

#### 3. Create Nginx Configuration for Docker

Create `nginx.conf`:
```nginx
server {
    listen 80;
    server_name localhost;

    location / {
        root /usr/share/nginx/html;
        index index.html;
        try_files $uri $uri/ =404;
    }

    location /api/ {
        proxy_pass http://simguard-backend:5000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    client_max_body_size 16M;
}
```

#### 4. Deploy with Docker

```bash
# Build and start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 🔒 Security Considerations

### Production Security Checklist

- [ ] **HTTPS Configuration**: Use SSL/TLS certificates
- [ ] **CORS Configuration**: Restrict origins to your domain
- [ ] **File Upload Security**: Validate file types and sizes
- [ ] **Rate Limiting**: Implement API rate limiting
- [ ] **Input Validation**: Sanitize all user inputs
- [ ] **Error Handling**: Don't expose sensitive information
- [ ] **Logging**: Implement comprehensive logging
- [ ] **Firewall**: Configure server firewall rules

### Environment Variables

Create `.env` file for production:
```bash
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
MAX_CONTENT_LENGTH=16777216
CORS_ORIGINS=https://your-domain.com
```

Update `app.py` to use environment variables:
```python
import os
from dotenv import load_dotenv

load_dotenv()

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key')
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH', 16777216))
```

## 📊 Monitoring and Logging

### Application Logging

Configure logging in `app.py`:
```python
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    file_handler = RotatingFileHandler('logs/simguard.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
```

### Health Check Endpoint

The application includes a health check endpoint at `/` for monitoring.

### Performance Monitoring

Consider integrating:
- **Application Performance Monitoring (APM)** tools
- **Log aggregation** services
- **Uptime monitoring** services
- **Resource usage** monitoring

## 🔄 Updates and Maintenance

### Updating the Application

```bash
# Pull latest changes
git pull origin main

# Update dependencies
cd backend
source venv/bin/activate
pip install -r requirements.txt

# Restart services
sudo systemctl restart simguard
```

### Backup Strategy

- **Code**: Use Git for version control
- **Data**: Backup any persistent data (if added)
- **Configuration**: Backup server configuration files
- **Logs**: Archive application logs regularly

## 🐛 Troubleshooting

### Common Issues

1. **Port Already in Use**
```bash
# Find process using port 5000
sudo lsof -i :5000
# Kill the process
sudo kill -9 <PID>
```

2. **Permission Denied**
```bash
# Fix file permissions
sudo chown -R simguard:simguard /home/simguard/SIMGuard
sudo chmod -R 755 /home/simguard/SIMGuard
```

3. **Module Not Found**
```bash
# Ensure virtual environment is activated
source venv/bin/activate
# Reinstall requirements
pip install -r requirements.txt
```

### Log Locations

- **Application logs**: `backend/logs/simguard.log`
- **Nginx logs**: `/var/log/nginx/`
- **System logs**: `/var/log/syslog`
- **Service logs**: `journalctl -u simguard`

## 📞 Support

For deployment issues:
1. Check the troubleshooting section
2. Review application logs
3. Create an issue on GitHub
4. Contact the development team

---

This deployment guide should help you get SIMGuard running in various environments. Choose the deployment method that best fits your needs and infrastructure.
