#!/usr/bin/env python3
"""
SIMGuard Backend Startup Script
Simple script to start the Flask application with proper configuration
"""

import os
import sys

# Ensure the current directory (backend/) is in sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

def check_dependencies():
    """Check if all required dependencies are installed"""
    required_packages = [
        'flask', 'flask_cors', 'pandas', 'numpy', 'fpdf', 'sklearn', 'xgboost'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            if package == 'sklearn':
                try:
                    __import__('sklearn')
                except ImportError:
                    missing_packages.append(package)
            else:
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
    directories = ['uploads', 'reports', 'models', 'simswap_detector']
    
    for directory in directories:
        if not os.path.exists(directory):
            try:
                os.makedirs(directory)
                print(f"✅ Created directory: {directory}")
            except Exception:
                pass # Ignore if it exists

def print_startup_info():
    """Print startup information"""
    print("🛡️  SIMGuard Backend API")
    print("=" * 40)
    print(f"🌐 Server: http://localhost:5001")
    print(f"📁 Upload folder: uploads/")
    print(f"📊 Max file size: 16MB")
    print("=" * 40)
    print("Available endpoints:")
    print("  GET  /           - Health check")
    print("  POST /upload     - Upload CSV file")
    print("  POST /analyze    - Analyze data")
    print("  GET  /results    - Get analysis results")
    print("  GET  /report     - Download PDF report")
    print("  POST /predict    - ML Manual Prediction")
    print("  POST /train      - Train ML Model")
    print("=" * 40)
    print("🚀 Starting server...")

def main():
    """Main startup function"""
    # Check dependencies
    if not check_dependencies():
        print("⚠️  Warning: Some dependencies missing. App may crash.")
    
    # Setup directories
    setup_directories()
    
    # Import app with error handling
    try:
        from app import app
        
        # Print startup info
        print_startup_info()
        
        # Start the Flask application
        app.run(
            host='0.0.0.0',
            port=5001,
            debug=True,
            threaded=True
        )
    except ImportError as e:
        print(f"❌ Critical Import Error: {e}")
        print("\nDebug Info:")
        print(f"Current Directory: {os.getcwd()}")
        print(f"Script Directory: {current_dir}")
        print("Directory Contents:")
        try:
            print(os.listdir(current_dir))
        except:
            print("Cannot list directory")
            
        simswap_dir = os.path.join(current_dir, 'simswap_detector')
        if os.path.exists(simswap_dir):
            print("simswap_detector Contents:")
            print(os.listdir(simswap_dir))
        else:
            print("simswap_detector directory NOT found!")
            
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()