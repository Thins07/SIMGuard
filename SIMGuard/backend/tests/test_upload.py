#!/usr/bin/env python3
"""
Test the upload endpoint
"""

import requests

# Test if backend is running
try:
    response = requests.get('http://localhost:5000/')
    print(f"✅ Backend is running: {response.status_code}")
except Exception as e:
    print(f"❌ Backend not accessible: {e}")
    exit(1)

# Test upload endpoint
try:
    with open('sample_sl_dataset.xlsx', 'rb') as f:
        files = {'file': ('sample_sl_dataset.xlsx', f, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
        response = requests.post('http://localhost:5000/sl/upload-dataset', files=files)
        
        print(f"\nUpload Response Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ Upload successful!")
            print(f"   Rows: {data.get('total_rows')}")
            print(f"   Columns: {data.get('total_columns')}")
        else:
            print(f"\n❌ Upload failed!")
            
except Exception as e:
    print(f"❌ Error testing upload: {e}")

