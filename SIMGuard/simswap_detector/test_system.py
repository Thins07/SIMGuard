"""
Test script to validate the SIM Swap Detection System
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data_ingestion import DataIngestion
from rule_engine import RuleEngine
import pandas as pd


def test_data_loading():
    """Test data loading functionality"""
    print("\n" + "="*60)
    print("TEST 1: Data Loading")
    print("="*60)
    
    try:
        loader = DataIngestion()
        
        # Test Excel loading
        data = loader.load_data('../data/simswap_test_data.xlsx')
        print(f"✅ Excel file loaded: {len(data)} records")
        
        # Validate data
        loader.validate_data()
        print("✅ Data validation passed")
        
        # Get summary
        summary = loader.get_summary()
        print(f"✅ Summary: {summary['total_records']} total, "
              f"{summary['legitimate_count']} legitimate, "
              f"{summary['suspicious_count']} suspicious")
        
        return True
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


def test_rule_engine():
    """Test rule engine functionality"""
    print("\n" + "="*60)
    print("TEST 2: Rule Engine")
    print("="*60)
    
    try:
        engine = RuleEngine()
        
        # Test with suspicious user data
        suspicious_user = {
            'user_id': 'TEST_001',
            'hours_since_sim_change': 24,
            'device_changed_after_sim': True,
            'hours_between_sim_device_change': 12,
            'previous_city': 'Colombo',
            'current_city': 'Jaffna',
            'hours_since_location_change': 1.5,
            'cell_tower_changes_24h': 15,
            'previous_data_usage_mb': 1000,
            'current_data_usage_mb': 5000,
            'previous_calls_24h': 10,
            'current_calls_24h': 60,
            'previous_sms_24h': 20,
            'current_sms_24h': 120,
            'failed_logins_24h': 8,
            'is_roaming': False
        }
        
        result = engine.evaluate_user(suspicious_user)
        
        print(f"✅ User evaluated: {result['user_id']}")
        print(f"   Risk Score: {result['risk_score']}")
        print(f"   Alert Level: {result['alert_level']}")
        print(f"   Rules Triggered: {result['total_rules_triggered']}")
        
        if result['risk_score'] > 60:
            print("✅ Correctly identified as HIGH risk")
        else:
            print(f"⚠️ Expected HIGH risk, got {result['alert_level']}")
        
        # Test with legitimate user data
        legitimate_user = {
            'user_id': 'TEST_002',
            'hours_since_sim_change': 500,
            'device_changed_after_sim': False,
            'hours_between_sim_device_change': 999,
            'previous_city': 'Colombo',
            'current_city': 'Colombo',
            'hours_since_location_change': 999,
            'cell_tower_changes_24h': 2,
            'previous_data_usage_mb': 1000,
            'current_data_usage_mb': 1100,
            'previous_calls_24h': 10,
            'current_calls_24h': 11,
            'previous_sms_24h': 20,
            'current_sms_24h': 22,
            'failed_logins_24h': 1,
            'is_roaming': False
        }
        
        result2 = engine.evaluate_user(legitimate_user)
        
        print(f"\n✅ User evaluated: {result2['user_id']}")
        print(f"   Risk Score: {result2['risk_score']}")
        print(f"   Alert Level: {result2['alert_level']}")
        print(f"   Rules Triggered: {result2['total_rules_triggered']}")
        
        if result2['risk_score'] <= 30:
            print("✅ Correctly identified as LOW risk")
        else:
            print(f"⚠️ Expected LOW risk, got {result2['alert_level']}")
        
        return True
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_end_to_end():
    """Test complete end-to-end workflow"""
    print("\n" + "="*60)
    print("TEST 3: End-to-End Workflow")
    print("="*60)
    
    try:
        # Load data
        loader = DataIngestion()
        loader.load_data('../data/simswap_test_data.xlsx')
        user_records = loader.get_user_records()
        
        # Process all users
        engine = RuleEngine()
        results = []
        
        for user_data in user_records:
            result = engine.evaluate_user(user_data)
            results.append(result)
        
        print(f"✅ Processed {len(results)} users")
        
        # Analyze results
        high_risk = [r for r in results if r['alert_level'] == 'HIGH']
        medium_risk = [r for r in results if r['alert_level'] == 'MEDIUM']
        low_risk = [r for r in results if r['alert_level'] == 'LOW']
        
        print(f"\nResults Summary:")
        print(f"   🚨 HIGH Risk: {len(high_risk)} users")
        print(f"   ⚠️ MEDIUM Risk: {len(medium_risk)} users")
        print(f"   ✅ LOW Risk: {len(low_risk)} users")
        
        # Show sample high-risk user
        if high_risk:
            sample = high_risk[0]
            print(f"\nSample HIGH Risk User: {sample['user_id']}")
            print(f"   Risk Score: {sample['risk_score']}")
            print(f"   Triggered Rules:")
            for rule in sample['triggered_rules']:
                print(f"      • {rule['rule']}: {rule['reason']}")
        
        return True
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("SIM SWAP DETECTION SYSTEM - TEST SUITE")
    print("="*60)
    
    tests = [
        test_data_loading,
        test_rule_engine,
        test_end_to_end
    ]
    
    results = []
    for test in tests:
        result = test()
        results.append(result)
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Tests Passed: {passed}/{total}")
    
    if passed == total:
        print("\n✅ ALL TESTS PASSED - System is ready!")
    else:
        print(f"\n⚠️ {total - passed} test(s) failed - Please review errors above")
    
    print("="*60)


if __name__ == '__main__':
    main()

