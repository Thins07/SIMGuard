
#!/usr/bin/env python3
"""
Model Files Checker
Verifies that required ML model files are present and valid
"""

import os
import joblib
import sys

def check_file_exists(filepath, description):
    """Check if a file exists and print status"""
    if os.path.exists(filepath):
        size = os.path.getsize(filepath)
        size_mb = size / (1024 * 1024)
        print(f"✅ {description}: Found ({size_mb:.2f} MB)")
        return True
    else:
        print(f"❌ {description}: NOT FOUND")
        print(f"   Expected location: {filepath}")
        return False

def check_pickle_valid(filepath, description):
    """Check if a pickle file can be loaded"""
    try:
        obj = joblib.load(filepath)
        print(f"✅ {description}: Valid pickle file")
        return True, obj
    except Exception as e:
        print(f"❌ {description}: Invalid or corrupted")
        print(f"   Error: {str(e)}")
        return False, None

def main():
    """Main checker function"""
    print("=" * 60)
    print("SIMGuard ML Model Files Checker (Thinker Engine)")
    print("=" * 60)
    print()
    
    # Get absolute path to backend directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define required files (Updated for Thinker Model)
    model_file = os.path.join(base_dir, 'sim_swap_model.pkl') 
    scaler_file = os.path.join(base_dir, 'preprocessor.pkl')       
    
    all_ok = True
    
    # Check model file
    print("1. Checking XGBoost Model File...")
    if check_file_exists(model_file, "sim_swap_model.pkl"):
        valid, model = check_pickle_valid(model_file, "Model")
        if valid:
            print(f"   Model type: {type(model).__name__}")
        else:
            all_ok = False
    else:
        all_ok = False
    print()
    
    # Check scaler file
    print("2. Checking Preprocessor (Scaler) File...")
    if check_file_exists(scaler_file, "preprocessor.pkl"):
        valid, scaler = check_pickle_valid(scaler_file, "Scaler")
        if valid:
            print(f"   Scaler type: {type(scaler).__name__}")
        else:
            all_ok = False
    else:
        all_ok = False
    print()
    
    # Final status
    print("=" * 60)
    if all_ok:
        print("✅ ALL CHECKS PASSED!")
        print("   Your ML model files are correctly installed.")
        print("   Restart the backend to load the new model: python run.py")
    else:
        print("❌ SOME CHECKS FAILED!")
        print("   Please copy your 'sim_swap_model.pkl' and 'preprocessor.pkl'")
        print(f"   into this directory: {base_dir}")
    print("=" * 60)
    
    return 0 if all_ok else 1

if __name__ == '__main__':
    sys.exit(main())
