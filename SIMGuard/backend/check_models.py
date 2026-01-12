#!/usr/bin/env python3
"""
Model Files Checker
Verifies that required ML model files are present and valid
"""

import os
import pickle
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
        print(f"   Expected location: {os.path.abspath(filepath)}")
        return False

def check_pickle_valid(filepath, description):
    """Check if a pickle file can be loaded"""
    try:
        with open(filepath, 'rb') as f:
            obj = pickle.load(f)
        print(f"✅ {description}: Valid pickle file")
        return True, obj
    except Exception as e:
        print(f"❌ {description}: Invalid or corrupted")
        print(f"   Error: {str(e)}")
        return False, None

def main():
    """Main checker function"""
    print("=" * 60)
    print("SIMGuard ML Model Files Checker")
    print("=" * 60)
    print()
    
    # Define required files
    model_file = 'xgboost_simswap_model.pkl'
    scaler_file = 'scaler.pkl'
    
    all_ok = True
    
    # Check model file
    print("1. Checking XGBoost Model File...")
    if check_file_exists(model_file, "Model file"):
        valid, model = check_pickle_valid(model_file, "Model file")
        if valid:
            print(f"   Model type: {type(model).__name__}")
        else:
            all_ok = False
    else:
        all_ok = False
    print()
    
    # Check scaler file
    print("2. Checking Scaler File...")
    if check_file_exists(scaler_file, "Scaler file"):
        valid, scaler = check_pickle_valid(scaler_file, "Scaler file")
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
        print("   Your ML model files are ready to use.")
        print("   You can now start the Flask server with: python app.py")
    else:
        print("❌ SOME CHECKS FAILED!")
        print()
        print("📋 To fix this:")
        print("   1. Train your model in Google Colab or locally")
        print("   2. Save the model and scaler using pickle:")
        print()
        print("      import pickle")
        print("      with open('xgboost_simswap_model.pkl', 'wb') as f:")
        print("          pickle.dump(model, f)")
        print("      with open('scaler.pkl', 'wb') as f:")
        print("          pickle.dump(scaler, f)")
        print()
        print("   3. Download the files from Colab:")
        print()
        print("      from google.colab import files")
        print("      files.download('xgboost_simswap_model.pkl')")
        print("      files.download('scaler.pkl')")
        print()
        print("   4. Place both files in the backend/ directory")
        print()
        print(f"   Expected location: {os.path.abspath('.')}")
    print("=" * 60)
    
    return 0 if all_ok else 1

if __name__ == '__main__':
    sys.exit(main())
