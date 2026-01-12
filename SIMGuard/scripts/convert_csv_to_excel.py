#!/usr/bin/env python3
"""
Convert sample CSV to Excel format
"""

import pandas as pd
import os

# Read CSV
csv_path = 'sample_sl_dataset.csv'
excel_path = 'sample_sl_dataset.xlsx'

if os.path.exists(csv_path):
    print(f"Reading {csv_path}...")
    df = pd.read_csv(csv_path)
    
    print(f"Dataset shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    
    # Save as Excel
    print(f"Saving to {excel_path}...")
    df.to_excel(excel_path, index=False, engine='openpyxl')
    
    print(f"✅ Successfully converted to Excel!")
    print(f"   File: {excel_path}")
    print(f"   Rows: {len(df)}")
    print(f"   Columns: {len(df.columns)}")
else:
    print(f"❌ CSV file not found: {csv_path}")

