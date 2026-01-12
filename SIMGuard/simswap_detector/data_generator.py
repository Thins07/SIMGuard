"""
Synthetic Data Generator for SIM Swap Detection Testing
Generates realistic Sri Lankan telecom usage patterns
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from typing import Dict
import config


class SyntheticDataGenerator:
    """Generate synthetic test data for SIM swap detection"""
    
    def __init__(self, num_legitimate=80, num_suspicious=20):
        """
        Initialize data generator
        
        Args:
            num_legitimate: Number of legitimate user records
            num_suspicious: Number of suspicious user records
        """
        self.num_legitimate = num_legitimate
        self.num_suspicious = num_suspicious
        self.total_records = num_legitimate + num_suspicious
        
    def generate_legitimate_user(self, user_id: int) -> Dict:
        """Generate legitimate user activity data"""
        return {
            'user_id': f'USER_{user_id:04d}',
            'phone_number': f'077{random.randint(1000000, 9999999)}',
            'operator': random.choice(config.SRI_LANKAN_OPERATORS),
            
            # SIM and Device
            'hours_since_sim_change': random.randint(200, 2000),  # Old SIM
            'device_changed_after_sim': False,
            'hours_between_sim_device_change': 999,
            
            # Location
            'previous_city': random.choice(config.SRI_LANKAN_CITIES),
            'current_city': None,  # Same city
            'hours_since_location_change': 999,
            
            # Cell Tower
            'cell_tower_changes_24h': random.randint(0, 3),  # Normal movement
            
            # Data Usage (MB)
            'previous_data_usage_mb': random.randint(500, 2000),
            'current_data_usage_mb': None,  # Will set to similar value
            
            # Call Pattern
            'previous_calls_24h': random.randint(5, 20),
            'current_calls_24h': None,  # Will set to similar value
            
            # SMS Pattern
            'previous_sms_24h': random.randint(10, 50),
            'current_sms_24h': None,  # Will set to similar value
            
            # Security
            'failed_logins_24h': random.randint(0, 2),  # Normal failed attempts
            'is_roaming': False,
            
            # Label
            'is_suspicious': 0,
            'label': 'LEGITIMATE'
        }
    
    def generate_suspicious_user(self, user_id: int) -> Dict:
        """Generate suspicious user activity data (SIM swap scenario)"""
        scenario = random.choice([
            'full_sim_swap',
            'sim_swap_with_device_change',
            'sim_swap_with_location_change',
            'sim_swap_with_roaming',
            'sim_swap_with_failed_logins'
        ])
        
        base_data = {
            'user_id': f'USER_{user_id:04d}',
            'phone_number': f'077{random.randint(1000000, 9999999)}',
            'operator': random.choice(config.SRI_LANKAN_OPERATORS),
            'is_suspicious': 1,
            'label': 'SUSPICIOUS'
        }
        
        if scenario == 'full_sim_swap':
            # Complete SIM swap with multiple red flags
            prev_city = random.choice(config.SRI_LANKAN_CITIES)
            curr_city = random.choice([c for c in config.SRI_LANKAN_CITIES if c != prev_city])
            
            base_data.update({
                'hours_since_sim_change': random.randint(1, 48),
                'device_changed_after_sim': True,
                'hours_between_sim_device_change': random.randint(1, 24),
                'previous_city': prev_city,
                'current_city': curr_city,
                'hours_since_location_change': random.uniform(0.5, 2),
                'cell_tower_changes_24h': random.randint(8, 20),
                'previous_data_usage_mb': random.randint(1000, 2000),
                'current_data_usage_mb': random.randint(3000, 8000),
                'previous_calls_24h': random.randint(10, 20),
                'current_calls_24h': random.randint(50, 100),
                'previous_sms_24h': random.randint(20, 40),
                'current_sms_24h': random.randint(100, 200),
                'failed_logins_24h': random.randint(5, 15),
                'is_roaming': False
            })
            
        elif scenario == 'sim_swap_with_device_change':
            # SIM swap + device change
            base_data.update({
                'hours_since_sim_change': random.randint(1, 36),
                'device_changed_after_sim': True,
                'hours_between_sim_device_change': random.randint(1, 12),
                'previous_city': random.choice(config.SRI_LANKAN_CITIES),
                'current_city': None,
                'hours_since_location_change': 999,
                'cell_tower_changes_24h': random.randint(2, 4),
                'previous_data_usage_mb': random.randint(800, 1500),
                'current_data_usage_mb': random.randint(2500, 5000),
                'previous_calls_24h': random.randint(8, 15),
                'current_calls_24h': random.randint(40, 80),
                'previous_sms_24h': random.randint(15, 30),
                'current_sms_24h': random.randint(80, 150),
                'failed_logins_24h': random.randint(4, 10),
                'is_roaming': False
            })
            
        elif scenario == 'sim_swap_with_location_change':
            # SIM swap + sudden location change
            prev_city = 'Colombo'
            curr_city = random.choice(['Jaffna', 'Batticaloa', 'Trincomalee'])
            
            base_data.update({
                'hours_since_sim_change': random.randint(2, 60),
                'device_changed_after_sim': False,
                'hours_between_sim_device_change': 999,
                'previous_city': prev_city,
                'current_city': curr_city,
                'hours_since_location_change': random.uniform(0.5, 1.5),
                'cell_tower_changes_24h': random.randint(10, 25),
                'previous_data_usage_mb': random.randint(1000, 1800),
                'current_data_usage_mb': random.randint(200, 500),
                'previous_calls_24h': random.randint(12, 18),
                'current_calls_24h': random.randint(2, 5),
                'previous_sms_24h': random.randint(25, 35),
                'current_sms_24h': random.randint(3, 8),
                'failed_logins_24h': random.randint(3, 8),
                'is_roaming': False
            })

        elif scenario == 'sim_swap_with_roaming':
            # SIM swap + immediate roaming
            base_data.update({
                'hours_since_sim_change': random.randint(1, 20),
                'device_changed_after_sim': True,
                'hours_between_sim_device_change': random.randint(2, 18),
                'previous_city': random.choice(config.SRI_LANKAN_CITIES),
                'current_city': None,
                'hours_since_location_change': 999,
                'cell_tower_changes_24h': random.randint(6, 12),
                'previous_data_usage_mb': random.randint(900, 1600),
                'current_data_usage_mb': random.randint(3000, 6000),
                'previous_calls_24h': random.randint(10, 18),
                'current_calls_24h': random.randint(45, 90),
                'previous_sms_24h': random.randint(20, 35),
                'current_sms_24h': random.randint(90, 160),
                'failed_logins_24h': random.randint(2, 6),
                'is_roaming': True
            })

        else:  # sim_swap_with_failed_logins
            # SIM swap + many failed login attempts
            base_data.update({
                'hours_since_sim_change': random.randint(1, 40),
                'device_changed_after_sim': True,
                'hours_between_sim_device_change': random.randint(1, 30),
                'previous_city': random.choice(config.SRI_LANKAN_CITIES),
                'current_city': None,
                'hours_since_location_change': 999,
                'cell_tower_changes_24h': random.randint(3, 7),
                'previous_data_usage_mb': random.randint(1000, 1800),
                'current_data_usage_mb': random.randint(2000, 4500),
                'previous_calls_24h': random.randint(8, 16),
                'current_calls_24h': random.randint(35, 75),
                'previous_sms_24h': random.randint(18, 32),
                'current_sms_24h': random.randint(75, 140),
                'failed_logins_24h': random.randint(8, 20),
                'is_roaming': False
            })

        return base_data

    def normalize_data(self, data: Dict) -> Dict:
        """Normalize data (set current = previous if None)"""
        if data['current_city'] is None:
            data['current_city'] = data['previous_city']

        if data['current_data_usage_mb'] is None:
            # Legitimate users have similar data usage (±20%)
            variation = random.uniform(0.8, 1.2)
            data['current_data_usage_mb'] = int(data['previous_data_usage_mb'] * variation)

        if data['current_calls_24h'] is None:
            variation = random.uniform(0.85, 1.15)
            data['current_calls_24h'] = int(data['previous_calls_24h'] * variation)

        if data['current_sms_24h'] is None:
            variation = random.uniform(0.85, 1.15)
            data['current_sms_24h'] = int(data['previous_sms_24h'] * variation)

        return data

    def generate_dataset(self) -> pd.DataFrame:
        """Generate complete dataset with legitimate and suspicious users"""
        all_users = []

        # Generate legitimate users
        for i in range(self.num_legitimate):
            user = self.generate_legitimate_user(i + 1)
            user = self.normalize_data(user)
            all_users.append(user)

        # Generate suspicious users
        for i in range(self.num_suspicious):
            user = self.generate_suspicious_user(self.num_legitimate + i + 1)
            user = self.normalize_data(user)
            all_users.append(user)

        # Shuffle dataset
        random.shuffle(all_users)

        # Create DataFrame
        df = pd.DataFrame(all_users)

        return df

    def save_to_excel(self, filename: str):
        """Generate and save dataset to Excel file"""
        df = self.generate_dataset()
        df.to_excel(filename, index=False, engine='openpyxl')
        print(f"✅ Dataset saved to {filename}")
        print(f"   Total records: {len(df)}")
        print(f"   Legitimate: {len(df[df['is_suspicious'] == 0])}")
        print(f"   Suspicious: {len(df[df['is_suspicious'] == 1])}")
        return df

    def save_to_csv(self, filename: str):
        """Generate and save dataset to CSV file"""
        df = self.generate_dataset()
        df.to_csv(filename, index=False)
        print(f"✅ Dataset saved to {filename}")
        print(f"   Total records: {len(df)}")
        print(f"   Legitimate: {len(df[df['is_suspicious'] == 0])}")
        print(f"   Suspicious: {len(df[df['is_suspicious'] == 1])}")
        return df


if __name__ == '__main__':
    print("\n" + "="*60)
    print("Generating Built-in Excel Test Datasets")
    print("="*60)

    # Create datasets directory
    import os
    datasets_dir = os.path.join(os.path.dirname(__file__), 'datasets')
    os.makedirs(datasets_dir, exist_ok=True)

    # Dataset 1: Standard Test Dataset (100 users)
    print("\n📊 Dataset 1: Standard Test Dataset (100 users)")
    generator1 = SyntheticDataGenerator(num_legitimate=80, num_suspicious=20)
    generator1.save_to_excel(os.path.join(datasets_dir, 'dataset_standard_100users.xlsx'))
    print("   ✅ Saved: dataset_standard_100users.xlsx")

    # Dataset 2: Small Demo Dataset (20 users)
    print("\n📊 Dataset 2: Small Demo Dataset (20 users)")
    generator2 = SyntheticDataGenerator(num_legitimate=15, num_suspicious=5)
    generator2.save_to_excel(os.path.join(datasets_dir, 'dataset_demo_20users.xlsx'))
    print("   ✅ Saved: dataset_demo_20users.xlsx")

    # Dataset 3: Large Test Dataset (500 users)
    print("\n📊 Dataset 3: Large Test Dataset (500 users)")
    generator3 = SyntheticDataGenerator(num_legitimate=400, num_suspicious=100)
    generator3.save_to_excel(os.path.join(datasets_dir, 'dataset_large_500users.xlsx'))
    print("   ✅ Saved: dataset_large_500users.xlsx")

    # Dataset 4: High Risk Scenario (50% suspicious)
    print("\n📊 Dataset 4: High Risk Scenario (50 users, 50% suspicious)")
    generator4 = SyntheticDataGenerator(num_legitimate=25, num_suspicious=25)
    generator4.save_to_excel(os.path.join(datasets_dir, 'dataset_highrisk_50users.xlsx'))
    print("   ✅ Saved: dataset_highrisk_50users.xlsx")

    # Also save to legacy data folder for backward compatibility
    print("\n📊 Legacy: Saving to data/ folder")
    os.makedirs('../data', exist_ok=True)
    generator1.save_to_excel('../data/simswap_test_data.xlsx')
    generator1.save_to_csv('../data/simswap_test_data.csv')
    print("   ✅ Saved: data/simswap_test_data.xlsx")
    print("   ✅ Saved: data/simswap_test_data.csv")

    print("\n" + "="*60)
    print("✅ All built-in datasets generated successfully!")
    print(f"📁 Location: {datasets_dir}")
    print("="*60)

