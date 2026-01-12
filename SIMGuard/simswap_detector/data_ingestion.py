"""
Data Ingestion Module
Handles loading and preprocessing of user activity data
"""

import pandas as pd
import os
from typing import List, Dict


class DataIngestion:
    """Load and preprocess user activity data from Excel/CSV files"""
    
    def __init__(self):
        self.data = None
        self.file_path = None
    
    def load_excel(self, file_path: str) -> pd.DataFrame:
        """
        Load data from Excel file
        
        Args:
            file_path: Path to Excel file
            
        Returns:
            DataFrame with user activity data
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        try:
            self.data = pd.read_excel(file_path, engine='openpyxl')
            self.file_path = file_path
            print(f"✅ Loaded {len(self.data)} records from {file_path}")
            return self.data
        except Exception as e:
            raise Exception(f"Error loading Excel file: {e}")
    
    def load_csv(self, file_path: str) -> pd.DataFrame:
        """
        Load data from CSV file
        
        Args:
            file_path: Path to CSV file
            
        Returns:
            DataFrame with user activity data
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        try:
            self.data = pd.read_csv(file_path)
            self.file_path = file_path
            print(f"✅ Loaded {len(self.data)} records from {file_path}")
            return self.data
        except Exception as e:
            raise Exception(f"Error loading CSV file: {e}")
    
    def load_data(self, file_path: str) -> pd.DataFrame:
        """
        Auto-detect file type and load data
        
        Args:
            file_path: Path to data file (Excel or CSV)
            
        Returns:
            DataFrame with user activity data
        """
        file_extension = os.path.splitext(file_path)[1].lower()
        
        if file_extension in ['.xlsx', '.xls']:
            return self.load_excel(file_path)
        elif file_extension == '.csv':
            return self.load_csv(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}. Use .xlsx, .xls, or .csv")
    
    def get_user_records(self) -> List[Dict]:
        """
        Convert DataFrame to list of user dictionaries
        
        Returns:
            List of user records as dictionaries
        """
        if self.data is None:
            raise ValueError("No data loaded. Call load_data() first.")
        
        return self.data.to_dict('records')
    
    def get_summary(self) -> Dict:
        """
        Get summary statistics of loaded data
        
        Returns:
            Dictionary with summary statistics
        """
        if self.data is None:
            raise ValueError("No data loaded. Call load_data() first.")
        
        summary = {
            'total_records': len(self.data),
            'columns': list(self.data.columns),
            'num_columns': len(self.data.columns)
        }
        
        # Count suspicious vs legitimate if label exists
        if 'is_suspicious' in self.data.columns:
            summary['legitimate_count'] = len(self.data[self.data['is_suspicious'] == 0])
            summary['suspicious_count'] = len(self.data[self.data['is_suspicious'] == 1])
        
        if 'label' in self.data.columns:
            summary['label_distribution'] = self.data['label'].value_counts().to_dict()
        
        return summary
    
    def validate_data(self) -> bool:
        """
        Validate that required columns exist
        
        Returns:
            True if data is valid, raises exception otherwise
        """
        if self.data is None:
            raise ValueError("No data loaded. Call load_data() first.")
        
        required_columns = [
            'user_id',
            'hours_since_sim_change',
            'device_changed_after_sim',
            'previous_city',
            'current_city',
            'cell_tower_changes_24h',
            'previous_data_usage_mb',
            'current_data_usage_mb',
            'previous_calls_24h',
            'current_calls_24h',
            'previous_sms_24h',
            'current_sms_24h',
            'failed_logins_24h',
            'is_roaming'
        ]
        
        missing_columns = [col for col in required_columns if col not in self.data.columns]
        
        if missing_columns:
            raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")
        
        print("✅ Data validation passed")
        return True

