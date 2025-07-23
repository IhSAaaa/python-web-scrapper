#!/usr/bin/env python3
"""
Test script to verify CSV download functionality
"""

import requests
import json
import time
import os
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8001"
TEST_URL = "https://jeevawasa.com"

def test_scraping_and_download():
    """Test scraping and CSV download functionality"""
    print("🔍 Testing Scraping and CSV Download...")
    
    try:
        # Step 1: Perform scraping
        print("   1. Performing scraping...")
        payload = {
            "url": TEST_URL,
            "login_enabled": False
        }
        
        response = requests.post(f"{BASE_URL}/api/scrape", json=payload)
        
        if response.status_code != 200:
            print(f"❌ Scraping failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
        
        data = response.json()
        print(f"✅ Scraping successful!")
        print(f"   Links: {data['links_count']}")
        print(f"   Images: {data['images_count']}")
        print(f"   CSV URL: {data['excel_file']}")
        
        # Extract session ID from CSV URL
        csv_url = data['excel_file']
        session_id = csv_url.split('/')[-2]
        csv_filename = csv_url.split('/')[-1]
        
        print(f"   Session ID: {session_id}")
        print(f"   CSV Filename: {csv_filename}")
        
        # Step 2: List session files
        print("   2. Listing session files...")
        files_response = requests.get(f"{BASE_URL}/api/files/{session_id}")
        
        if files_response.status_code == 200:
            files_data = files_response.json()
            print(f"✅ Files listed successfully!")
            print(f"   Total files: {files_data['total_files']}")
            print(f"   Total size: {files_data['total_size_mb']} MB")
            
            for file_info in files_data['files']:
                print(f"   - {file_info['filename']}: {file_info['size_mb']} MB")
        else:
            print(f"❌ Failed to list files: {files_response.status_code}")
        
        # Step 3: Download CSV file
        print("   3. Downloading CSV file...")
        csv_response = requests.get(f"{BASE_URL}/api/download/{session_id}/{csv_filename}")
        
        if csv_response.status_code == 200:
            print(f"✅ CSV download successful!")
            print(f"   Content-Type: {csv_response.headers.get('Content-Type', 'N/A')}")
            print(f"   Content-Length: {csv_response.headers.get('Content-Length', 'N/A')}")
            print(f"   Content-Disposition: {csv_response.headers.get('Content-Disposition', 'N/A')}")
            
            # Check CSV content
            csv_content = csv_response.text
            print(f"   CSV Content Length: {len(csv_content)} characters")
            
            # Check if content is actually CSV (not HTML)
            if csv_content.startswith('<!DOCTYPE html>') or '<html' in csv_content:
                print("❌ ERROR: CSV contains HTML instead of data!")
                print("   First 200 characters:")
                print(f"   {csv_content[:200]}")
                return False
            else:
                print("✅ CSV content is valid (not HTML)")
                print("   First 200 characters:")
                print(f"   {csv_content[:200]}")
                
                # Save CSV for inspection
                test_csv_path = f"test_download_{session_id}.csv"
                with open(test_csv_path, 'w', encoding='utf-8') as f:
                    f.write(csv_content)
                print(f"   CSV saved to: {test_csv_path}")
                
                return True
        else:
            print(f"❌ CSV download failed: {csv_response.status_code}")
            print(f"   Response: {csv_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Test error: {str(e)}")
        return False

def test_csv_endpoint():
    """Test the dedicated CSV endpoint"""
    print("\n🔍 Testing Dedicated CSV Endpoint...")
    
    try:
        # First get the last session
        last_session_response = requests.get(f"{BASE_URL}/api/debug/last-session")
        
        if last_session_response.status_code != 200:
            print(f"❌ Failed to get last session: {last_session_response.status_code}")
            return False
        
        last_session_data = last_session_response.json()
        
        if 'error' in last_session_data:
            print(f"⚠️  No sessions found: {last_session_data['error']}")
            return False
        
        session_id = last_session_data['latest_session']
        print(f"   Using session: {session_id}")
        
        # Test dedicated CSV endpoint
        csv_response = requests.get(f"{BASE_URL}/api/csv/{session_id}")
        
        if csv_response.status_code == 200:
            print(f"✅ Dedicated CSV endpoint successful!")
            print(f"   Content-Type: {csv_response.headers.get('Content-Type', 'N/A')}")
            
            csv_content = csv_response.text
            if csv_content.startswith('<!DOCTYPE html>') or '<html' in csv_content:
                print("❌ ERROR: CSV contains HTML instead of data!")
                return False
            else:
                print("✅ CSV content is valid")
                return True
        else:
            print(f"❌ Dedicated CSV endpoint failed: {csv_response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Test error: {str(e)}")
        return False

def test_direct_file_access():
    """Test direct file access to check if files exist"""
    print("\n🔍 Testing Direct File Access...")
    
    try:
        # Get last session
        last_session_response = requests.get(f"{BASE_URL}/api/debug/last-session")
        
        if last_session_response.status_code != 200:
            print(f"❌ Failed to get last session: {last_session_response.status_code}")
            return False
        
        last_session_data = last_session_response.json()
        
        if 'error' in last_session_data:
            print(f"⚠️  No sessions found: {last_session_data['error']}")
            return False
        
        session_id = last_session_data['latest_session']
        session_path = last_session_data['session_path']
        
        print(f"   Session ID: {session_id}")
        print(f"   Session Path: {session_path}")
        
        # Check if files exist on disk
        if os.path.exists(session_path):
            files = os.listdir(session_path)
            print(f"✅ Session directory exists with {len(files)} files:")
            
            for filename in files:
                file_path = os.path.join(session_path, filename)
                file_size = os.path.getsize(file_path)
                print(f"   - {filename}: {file_size} bytes")
                
                # Check if CSV file has proper content
                if filename.endswith('.csv'):
                    with open(file_path, 'r', encoding='utf-8-sig') as f:
                        content = f.read(200)  # Read first 200 chars
                        if '<html' in content or content.startswith('<!DOCTYPE'):
                            print(f"   ❌ WARNING: {filename} contains HTML!")
                        else:
                            print(f"   ✅ {filename} has valid CSV content")
            
            return True
        else:
            print(f"❌ Session directory does not exist: {session_path}")
            return False
            
    except Exception as e:
        print(f"❌ Test error: {str(e)}")
        return False

def main():
    """Run all CSV download tests"""
    print("🚀 CSV Download Test Suite")
    print("=" * 50)
    
    tests = [
        ("Scraping and Download", test_scraping_and_download),
        ("Dedicated CSV Endpoint", test_csv_endpoint),
        ("Direct File Access", test_direct_file_access),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} crashed: {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All CSV download tests passed!")
    else:
        print("⚠️  Some tests failed. Check the server configuration.")
    
    print(f"\nTest completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main() 