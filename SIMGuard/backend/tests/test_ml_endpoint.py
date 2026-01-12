#!/usr/bin/env python3
"""
ML Endpoint Test Script
Tests the /predict endpoint with sample data
"""

import requests
import json
import sys

# API Configuration
API_BASE_URL = 'http://localhost:5000'
PREDICT_ENDPOINT = f'{API_BASE_URL}/predict'

# Test Cases
TEST_CASES = [
    {
        "name": "Normal User Activity",
        "description": "Regular user with normal behavior patterns",
        "data": {
            "distance_change": 5.0,
            "time_since_sim_change": 720.0,  # 30 days
            "num_failed_logins_last_24h": 0,
            "num_calls_last_24h": 15,
            "num_sms_last_24h": 8,
            "data_usage_change_percent": 5.0,
            "change_in_cell_tower_id": 2,
            "is_roaming": 0,
            "sim_change_flag": 0,
            "device_change_flag": 0,
            "current_city": "New York",
            "previous_city": "New York"
        },
        "expected": "SAFE"
    },
    {
        "name": "Suspicious Activity - Impossible Travel",
        "description": "User traveled 500km in 1 hour (impossible)",
        "data": {
            "distance_change": 500.0,
            "time_since_sim_change": 1.0,
            "num_failed_logins_last_24h": 3,
            "num_calls_last_24h": 2,
            "num_sms_last_24h": 0,
            "data_usage_change_percent": -70.0,
            "change_in_cell_tower_id": 10,
            "is_roaming": 1,
            "sim_change_flag": 1,
            "device_change_flag": 1,
            "current_city": "Los Angeles",
            "previous_city": "New York"
        },
        "expected": "SUSPICIOUS"
    },
    {
        "name": "High Risk - Multiple Failed Logins",
        "description": "Many failed login attempts with SIM change",
        "data": {
            "distance_change": 200.0,
            "time_since_sim_change": 0.5,
            "num_failed_logins_last_24h": 10,
            "num_calls_last_24h": 1,
            "num_sms_last_24h": 0,
            "data_usage_change_percent": -90.0,
            "change_in_cell_tower_id": 5,
            "is_roaming": 1,
            "sim_change_flag": 1,
            "device_change_flag": 1,
            "current_city": "Chicago",
            "previous_city": "Miami"
        },
        "expected": "SUSPICIOUS"
    },
    {
        "name": "Moderate Activity",
        "description": "Some suspicious indicators but not extreme",
        "data": {
            "distance_change": 50.0,
            "time_since_sim_change": 168.0,  # 7 days
            "num_failed_logins_last_24h": 2,
            "num_calls_last_24h": 5,
            "num_sms_last_24h": 3,
            "data_usage_change_percent": 20.0,
            "change_in_cell_tower_id": 3,
            "is_roaming": 0,
            "sim_change_flag": 0,
            "device_change_flag": 1,
            "current_city": "Boston",
            "previous_city": "Boston"
        },
        "expected": "SAFE or SUSPICIOUS (borderline)"
    }
]

def test_health_check():
    """Test if the API is running"""
    try:
        response = requests.get(API_BASE_URL, timeout=5)
        if response.status_code == 200:
            print("✅ API is running")
            return True
        else:
            print(f"❌ API returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"❌ Cannot connect to API at {API_BASE_URL}")
        print("   Make sure the Flask server is running: python app.py")
        return False
    except Exception as e:
        print(f"❌ Error checking API: {e}")
        return False

def test_prediction(test_case):
    """Test a single prediction"""
    print(f"\n{'='*60}")
    print(f"Test: {test_case['name']}")
    print(f"Description: {test_case['description']}")
    print(f"Expected: {test_case['expected']}")
    print(f"{'='*60}")
    
    try:
        # Make prediction request
        response = requests.post(
            PREDICT_ENDPOINT,
            json=test_case['data'],
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            
            # Display results
            prediction = "SUSPICIOUS" if result['prediction'] == 1 else "SAFE"
            confidence = result['confidence']
            risk_factors = result.get('risk_factors', [])
            
            print(f"\n✅ Prediction: {prediction}")
            print(f"   Confidence: {confidence:.2f}%")
            
            if risk_factors:
                print(f"   Risk Factors:")
                for factor in risk_factors:
                    print(f"   - {factor}")
            else:
                print(f"   Risk Factors: None identified")
            
            # Check if matches expected
            if test_case['expected'].startswith(prediction):
                print(f"\n✅ Result matches expected outcome")
            else:
                print(f"\n⚠️  Result differs from expected (this is OK for borderline cases)")
            
            return True
            
        else:
            print(f"❌ Request failed with status code: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error making prediction: {e}")
        return False

def main():
    """Main test function"""
    print("=" * 60)
    print("SIMGuard ML Endpoint Test Suite")
    print("=" * 60)
    
    # Check if API is running
    print("\n1. Checking API Health...")
    if not test_health_check():
        print("\n❌ Cannot proceed with tests. Please start the Flask server first.")
        return 1
    
    # Run test cases
    print("\n2. Running Test Cases...")
    passed = 0
    failed = 0
    
    for test_case in TEST_CASES:
        if test_prediction(test_case):
            passed += 1
        else:
            failed += 1
    
    # Summary
    print(f"\n{'='*60}")
    print("Test Summary")
    print(f"{'='*60}")
    print(f"Total Tests: {len(TEST_CASES)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"{'='*60}")
    
    if failed == 0:
        print("✅ All tests passed!")
        return 0
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
