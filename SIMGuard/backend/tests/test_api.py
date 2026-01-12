#!/usr/bin/env python3
"""
SIMGuard Backend API Test Script
Test script to demonstrate API functionality and validate endpoints
"""

import requests
import json
import time
import os

# Configuration
API_BASE_URL = "http://localhost:5000"
SAMPLE_CSV_PATH = "../sample_logs.csv"

def test_health_check():
    """Test the health check endpoint"""
    print("🔍 Testing health check endpoint...")
    try:
        response = requests.get(f"{API_BASE_URL}/")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_file_upload():
    """Test file upload endpoint"""
    print("\n📤 Testing file upload endpoint...")
    
    if not os.path.exists(SAMPLE_CSV_PATH):
        print(f"❌ Sample CSV file not found: {SAMPLE_CSV_PATH}")
        return False
    
    try:
        with open(SAMPLE_CSV_PATH, 'rb') as file:
            files = {'file': ('sample_logs.csv', file, 'text/csv')}
            response = requests.post(f"{API_BASE_URL}/upload", files=files)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_analysis():
    """Test analysis endpoint"""
    print("\n🔬 Testing analysis endpoint...")
    try:
        response = requests.post(f"{API_BASE_URL}/analyze")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_results():
    """Test results endpoint"""
    print("\n📊 Testing results endpoint...")
    try:
        response = requests.get(f"{API_BASE_URL}/results")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Analysis Summary:")
            print(f"  - Total Records: {data['summary']['total_records']}")
            print(f"  - Suspicious Activities: {data['summary']['suspicious_count']}")
            print(f"  - Clean Records: {data['summary']['clean_count']}")
            print(f"  - Users Analyzed: {data['summary']['users_analyzed']}")
            
            if data['suspicious_activities']:
                print(f"\nFirst few suspicious activities:")
                for i, activity in enumerate(data['suspicious_activities'][:3]):
                    print(f"  {i+1}. User: {activity['user_id']}, Risk: {activity['risk_level']}, Reason: {activity['flag_reason']}")
        else:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_report_generation():
    """Test report generation endpoint"""
    print("\n📄 Testing report generation endpoint...")
    try:
        response = requests.get(f"{API_BASE_URL}/report")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            # Save the PDF report
            report_filename = f"test_report_{int(time.time())}.pdf"
            with open(report_filename, 'wb') as f:
                f.write(response.content)
            print(f"✅ Report saved as: {report_filename}")
            print(f"Report size: {len(response.content)} bytes")
        else:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_status():
    """Test status endpoint"""
    print("\n📈 Testing status endpoint...")
    try:
        response = requests.get(f"{API_BASE_URL}/status")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_clear_data():
    """Test clear data endpoint"""
    print("\n🗑️ Testing clear data endpoint...")
    try:
        response = requests.post(f"{API_BASE_URL}/clear")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_error_handling():
    """Test error handling"""
    print("\n⚠️ Testing error handling...")
    
    # Test invalid endpoint
    try:
        response = requests.get(f"{API_BASE_URL}/invalid-endpoint")
        print(f"Invalid endpoint - Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error testing invalid endpoint: {e}")
    
    # Test analysis without upload
    try:
        response = requests.post(f"{API_BASE_URL}/analyze")
        print(f"Analysis without upload - Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error testing analysis without upload: {e}")

def run_full_test_suite():
    """Run complete test suite"""
    print("🚀 Starting SIMGuard Backend API Test Suite")
    print("=" * 50)
    
    tests = [
        ("Health Check", test_health_check),
        ("File Upload", test_file_upload),
        ("Data Analysis", test_analysis),
        ("Get Results", test_results),
        ("Report Generation", test_report_generation),
        ("System Status", test_status),
        ("Error Handling", test_error_handling),
        ("Clear Data", test_clear_data)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            success = test_func()
            results.append((test_name, success))
            if success:
                print(f"✅ {test_name} passed")
            else:
                print(f"❌ {test_name} failed")
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
        
        time.sleep(1)  # Brief pause between tests
    
    # Summary
    print(f"\n{'='*50}")
    print("📋 TEST SUMMARY")
    print(f"{'='*50}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name:<20} {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 All tests passed! API is working correctly.")
    else:
        print("⚠️ Some tests failed. Check the API server and try again.")

def interactive_test():
    """Interactive test mode"""
    print("🔧 SIMGuard API Interactive Test Mode")
    print("Available commands:")
    print("1. health - Test health check")
    print("2. upload - Test file upload")
    print("3. analyze - Test analysis")
    print("4. results - Test results")
    print("5. report - Test report generation")
    print("6. status - Test status")
    print("7. clear - Test clear data")
    print("8. errors - Test error handling")
    print("9. full - Run full test suite")
    print("0. quit - Exit")
    
    commands = {
        '1': test_health_check,
        '2': test_file_upload,
        '3': test_analysis,
        '4': test_results,
        '5': test_report_generation,
        '6': test_status,
        '7': test_clear_data,
        '8': test_error_handling,
        '9': run_full_test_suite
    }
    
    while True:
        try:
            choice = input("\nEnter command (1-9, 0 to quit): ").strip()
            
            if choice == '0':
                print("👋 Goodbye!")
                break
            elif choice in commands:
                commands[choice]()
            else:
                print("❌ Invalid command. Please try again.")
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        interactive_test()
    else:
        run_full_test_suite()
