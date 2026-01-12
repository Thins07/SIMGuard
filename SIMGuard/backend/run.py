#!/usr/bin/env python3
"""
SIMGuard Backend Startup Script
Simple script to start the Flask application with proper configuration
"""

import os
import sys
from app import app, logger

def check_dependencies():
    """Check if all required dependencies are installed"""
    required_packages = [
        'flask', 'flask_cors', 'pandas', 'numpy', 'fpdf'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\nPlease install missing packages:")
        print("pip install -r requirements.txt")
        return False
    
    return True

def setup_directories():
    """Create necessary directories"""
    directories = ['uploads', 'reports']
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Created directory: {directory}")

def print_startup_info():
    """Print startup information"""
    print("🛡️  SIMGuard Backend API")
    print("=" * 40)
    print(f"🌐 Server: http://localhost:5000")
    print(f"📁 Upload folder: uploads/")
    print(f"📊 Max file size: 16MB")
    print(f"🔧 Debug mode: {'ON' if app.debug else 'OFF'}")
    print("=" * 40)
    print("Available endpoints:")
    print("  GET  /           - Health check")
    print("  POST /upload     - Upload CSV file")
    print("  POST /analyze    - Analyze data")
    print("  GET  /results    - Get analysis results")
    print("  GET  /report     - Download PDF report")
    print("  GET  /status     - System status")
    print("  POST /clear      - Clear data")
    print("=" * 40)
    print("🚀 Starting server...")

def main():
    """Main startup function"""
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Setup directories
    setup_directories()
    
    # Print startup info
    print_startup_info()
    
    # Start the Flask application
    try:
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=True,
            threaded=True
        )
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
