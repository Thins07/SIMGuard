#!/usr/bin/env python3
"""
SIMGuard Setup Script
Automated setup and installation script for the SIMGuard project
"""

import os
import sys
import subprocess
import platform
import venv
from pathlib import Path

def print_banner():
    """Print SIMGuard banner"""
    banner = """
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║   🛡️  SIMGuard - AI-Powered SIM Swap Detection Tool      ║
    ║                                                           ║
    ║   Setup and Installation Script                           ║
    ║   Final Year Cybersecurity Project                        ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_python_version():
    """Check if Python version is compatible"""
    print("🔍 Checking Python version...")
    
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        print("   Please upgrade Python and try again")
        return False
    
    print(f"✅ Python {sys.version.split()[0]} detected")
    return True

def check_system_requirements():
    """Check system requirements"""
    print("\n🔍 Checking system requirements...")
    
    # Check operating system
    os_name = platform.system()
    print(f"✅ Operating System: {os_name}")
    
    # Check if pip is available
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], 
                      check=True, capture_output=True)
        print("✅ pip is available")
    except subprocess.CalledProcessError:
        print("❌ Error: pip is not available")
        return False
    
    return True

def create_virtual_environment():
    """Create Python virtual environment"""
    print("\n🔧 Setting up virtual environment...")
    
    backend_dir = Path("backend")
    venv_dir = backend_dir / "venv"
    
    if venv_dir.exists():
        print("⚠️  Virtual environment already exists")
        response = input("   Do you want to recreate it? (y/N): ").lower()
        if response == 'y':
            import shutil
            shutil.rmtree(venv_dir)
            print("🗑️  Removed existing virtual environment")
        else:
            print("📁 Using existing virtual environment")
            return True
    
    try:
        print("📦 Creating virtual environment...")
        venv.create(venv_dir, with_pip=True)
        print("✅ Virtual environment created successfully")
        return True
    except Exception as e:
        print(f"❌ Error creating virtual environment: {e}")
        return False

def get_venv_python():
    """Get path to virtual environment Python executable"""
    backend_dir = Path("backend")
    venv_dir = backend_dir / "venv"
    
    if platform.system() == "Windows":
        return venv_dir / "Scripts" / "python.exe"
    else:
        return venv_dir / "bin" / "python"

def install_dependencies():
    """Install Python dependencies"""
    print("\n📦 Installing Python dependencies...")
    
    backend_dir = Path("backend")
    requirements_file = backend_dir / "requirements.txt"
    
    if not requirements_file.exists():
        print("❌ Error: requirements.txt not found")
        return False
    
    venv_python = get_venv_python()
    
    try:
        print("⬇️  Installing packages...")
        subprocess.run([
            str(venv_python), "-m", "pip", "install", "-r", str(requirements_file)
        ], check=True, cwd=backend_dir)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating project directories...")
    
    directories = [
        "backend/uploads",
        "backend/logs",
        "docs"
    ]
    
    for directory in directories:
        dir_path = Path(directory)
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"✅ Created directory: {directory}")
        else:
            print(f"📁 Directory already exists: {directory}")

def test_installation():
    """Test the installation"""
    print("\n🧪 Testing installation...")
    
    venv_python = get_venv_python()
    backend_dir = Path("backend")
    
    try:
        # Test importing required modules
        test_script = """
import flask
import pandas
import numpy
import fpdf
print("All modules imported successfully")
"""
        
        result = subprocess.run([
            str(venv_python), "-c", test_script
        ], check=True, capture_output=True, text=True, cwd=backend_dir)
        
        print("✅ All dependencies are working correctly")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error testing installation: {e}")
        print("   Some dependencies may not be installed correctly")
        return False

def print_next_steps():
    """Print next steps for the user"""
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next Steps:")
    print("=" * 50)
    
    if platform.system() == "Windows":
        activate_cmd = "backend\\venv\\Scripts\\activate"
    else:
        activate_cmd = "source backend/venv/bin/activate"
    
    print(f"""
1. 🚀 Start the backend server:
   cd backend
   {activate_cmd}
   python app.py

2. 🌐 Open the frontend:
   Open index.html in your web browser
   
3. 📊 Test with sample data:
   Upload the sample_logs.csv file
   
4. 📖 Read the documentation:
   - README.md for overview
   - backend/README.md for API docs
   - docs/DEPLOYMENT.md for deployment

5. 🧪 Run tests:
   cd backend
   python test_api.py
""")
    
    print("=" * 50)
    print("🛡️  SIMGuard is ready to detect SIM swap attacks!")
    print("📞 For support, check the documentation or create an issue on GitHub")

def main():
    """Main setup function"""
    print_banner()
    
    # Check requirements
    if not check_python_version():
        sys.exit(1)
    
    if not check_system_requirements():
        sys.exit(1)
    
    # Setup process
    steps = [
        ("Creating virtual environment", create_virtual_environment),
        ("Installing dependencies", install_dependencies),
        ("Creating directories", create_directories),
        ("Testing installation", test_installation)
    ]
    
    for step_name, step_function in steps:
        if not step_function():
            print(f"\n❌ Setup failed at step: {step_name}")
            print("   Please check the error messages above and try again")
            sys.exit(1)
    
    # Success
    print_next_steps()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error during setup: {e}")
        sys.exit(1)
