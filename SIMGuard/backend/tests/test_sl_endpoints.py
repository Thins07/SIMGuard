#!/usr/bin/env python3
"""
Test script for Sri Lankan ML endpoints
"""

import requests
import json
import os

API_BASE_URL = 'http://localhost:5000'

def test_upload_dataset():
    """Test dataset upload"""
    print("\n" + "="*60)
    print("TEST 1: Upload Sri Lankan Dataset")
    print("="*60)
    
    # Path to sample dataset
    dataset_path = '../sample_sl_dataset.csv'
    
    if not os.path.exists(dataset_path):
        print(f"❌ Sample dataset not found: {dataset_path}")
        return False
    
    try:
        with open(dataset_path, 'rb') as f:
            files = {'file': ('sample_sl_dataset.csv', f, 'text/csv')}
            response = requests.post(f'{API_BASE_URL}/sl/upload-dataset', files=files)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Dataset uploaded successfully")
            print(f"   Total rows: {result['total_rows']}")
            print(f"   Total columns: {result['total_columns']}")
            print(f"   Class distribution: {result['distribution']}")
            return True
        else:
            print(f"❌ Upload failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_train_model():
    """Test model training"""
    print("\n" + "="*60)
    print("TEST 2: Train XGBoost Model")
    print("="*60)
    
    try:
        data = {
            'model_type': 'xgboost',
            'test_size': 0.2
        }
        
        response = requests.post(
            f'{API_BASE_URL}/sl/train-model',
            json=data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            result = response.json()
            if result['status'] == 'success':
                print(f"✅ Model trained successfully")
                print(f"   Model type: {result['model_type']}")
                print(f"   Accuracy: {result['metrics']['accuracy']*100:.2f}%")
                print(f"   Precision: {result['metrics']['precision']*100:.2f}%")
                print(f"   Recall: {result['metrics']['recall']*100:.2f}%")
                print(f"   F1 Score: {result['metrics']['f1_score']*100:.2f}%")
                print(f"   Train size: {result['train_size']}")
                print(f"   Test size: {result['test_size']}")
                return True
            else:
                print(f"❌ Training failed: {result.get('message', 'Unknown error')}")
                return False
        else:
            print(f"❌ Request failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_prediction():
    """Test prediction"""
    print("\n" + "="*60)
    print("TEST 3: Make Prediction")
    print("="*60)
    
    # Test case: Suspicious activity (Colombo to Galle in 1.5 hours)
    test_data = {
        'distance_change': 450.5,
        'time_since_sim_change': 1.5,
        'num_failed_logins_last_24h': 5,
        'num_calls_last_24h': 2,
        'num_sms_last_24h': 0,
        'data_usage_change_percent': -80.5,
        'change_in_cell_tower_id': 10,
        'is_roaming': 1,
        'sim_change_flag': 1,
        'device_change_flag': 1,
        'current_city': 'Galle',
        'previous_city': 'Colombo'
    }
    
    try:
        response = requests.post(
            f'{API_BASE_URL}/sl/predict',
            json=test_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            result = response.json()
            if result['status'] == 'success':
                prediction = "SUSPICIOUS 🚨" if result['prediction'] == 1 else "SAFE ✅"
                confidence = result['confidence'] * 100
                print(f"✅ Prediction successful")
                print(f"   Input: {test_data['previous_city']} → {test_data['current_city']}")
                print(f"   Result: {prediction}")
                print(f"   Confidence: {confidence:.2f}%")
                return True
            else:
                print(f"❌ Prediction failed: {result.get('message', 'Unknown error')}")
                return False
        else:
            print(f"❌ Request failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_download_model():
    """Test model download"""
    print("\n" + "="*60)
    print("TEST 4: Download Model")
    print("="*60)
    
    try:
        response = requests.get(f'{API_BASE_URL}/sl/download-model')
        
        if response.status_code == 200:
            # Save model file
            output_path = 'downloaded_model.pkl'
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
            file_size = os.path.getsize(output_path)
            print(f"✅ Model downloaded successfully")
            print(f"   File: {output_path}")
            print(f"   Size: {file_size / 1024:.2f} KB")
            
            # Clean up
            os.remove(output_path)
            return True
        else:
            print(f"❌ Download failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run all tests"""
    print("="*60)
    print("🇱🇰 Sri Lankan ML Dashboard - API Test Suite")
    print("="*60)
    
    # Check if server is running
    try:
        response = requests.get(API_BASE_URL, timeout=2)
        print("✅ Backend server is running")
    except:
        print("❌ Backend server is not running!")
        print("   Please start the server: cd backend && python app.py")
        return
    
    # Run tests
    results = []
    results.append(("Upload Dataset", test_upload_dataset()))
    results.append(("Train Model", test_train_model()))
    results.append(("Make Prediction", test_prediction()))
    results.append(("Download Model", test_download_model()))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Dashboard is ready for use.")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")

if __name__ == '__main__':
    main()
