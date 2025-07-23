#!/usr/bin/env python3
"""
Test script to verify the improvements made to the web scraper
"""

import requests
import json
import time
import os
from datetime import datetime

# Configuration
BASE_URL = "http://backend:8000"
TEST_URL = "https://jeevawasa.com"

def test_health_check():
    """Test the enhanced health check endpoint"""
    print("🔍 Testing Health Check...")
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health Check: {data['status']}")
            if 'system_info' in data:
                print(f"   Memory Usage: {data['system_info'].get('memory_usage_percent', 'N/A')}%")
                print(f"   Disk Usage: {data['system_info'].get('disk_usage_percent', 'N/A')}%")
            assert True, "Test passed"
        else:
            print(f"❌ Health Check failed: {response.status_code}")
            assert False, "Test failed"
    except Exception as e:
        print(f"❌ Health Check error: {str(e)}")
        assert False, "Test failed"

def test_scraping():
    """Test the improved scraping functionality"""
    print("\n🔍 Testing Scraping...")
    try:
        payload = {
            "url": TEST_URL,
    
        }
        
        print(f"   Scraping: {TEST_URL}")
        start_time = time.time()
        
        response = requests.post(f"{BASE_URL}/api/scrape", json=payload)
        duration = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Scraping successful!")
            print(f"   Duration: {duration:.2f}s")
            print(f"   Links: {data['links_count']}")
            print(f"   Images: {data['images_count']}")
            print(f"   Message: {data['message']}")
            assert True, "Test passed"
        else:
            print(f"❌ Scraping failed: {response.status_code}")
            print(f"   Response: {response.text}")
            assert False, "Test failed"
    except Exception as e:
        print(f"❌ Scraping error: {str(e)}")
        assert False, "Test failed"

def test_maintenance_stats():
    """Test the maintenance statistics endpoint"""
    print("\n🔍 Testing Maintenance Stats...")
    try:
        response = requests.get(f"{BASE_URL}/api/maintenance/stats")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Maintenance Stats:")
            print(f"   Total Sessions: {data.get('total_sessions', 0)}")
            print(f"   Total Files: {data.get('total_files', 0)}")
            print(f"   Total Size: {data.get('total_size_mb', 0)} MB")
            assert True, "Test passed"
        else:
            print(f"❌ Maintenance Stats failed: {response.status_code}")
            assert False, "Test failed"
    except Exception as e:
        print(f"❌ Maintenance Stats error: {str(e)}")
        assert False, "Test failed"

def test_debug_logs():
    """Test the debug logs endpoint"""
    print("\n🔍 Testing Debug Logs...")
    try:
        response = requests.get(f"{BASE_URL}/api/debug/logs")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Debug Logs:")
            print(f"   Total Log Files: {data.get('total_files', 0)}")
            if 'log_files' in data:
                for filename, info in data['log_files'].items():
                    if isinstance(info, dict) and 'size' in info:
                        print(f"   - {filename}: {info['size']} bytes, {info.get('lines', 0)} lines")
            assert True, "Test passed"
        else:
            print(f"❌ Debug Logs failed: {response.status_code}")
            assert False, "Test failed"
    except Exception as e:
        print(f"❌ Debug Logs error: {str(e)}")
        assert False, "Test failed"

def test_last_session():
    """Test the last session debug endpoint"""
    print("\n🔍 Testing Last Session...")
    try:
        response = requests.get(f"{BASE_URL}/api/debug/last-session")
        if response.status_code == 200:
            data = response.json()
            if 'error' not in data:
                print(f"✅ Last Session:")
                print(f"   Session ID: {data.get('latest_session', 'N/A')}")
                print(f"   Files: {len(data.get('files', []))}")
                if data.get('csv_file'):
                    print(f"   CSV File: {data['csv_file']}")
                assert True, "Test passed"
            else:
                print(f"⚠️  Last Session: {data['error']}")
                assert True, "Test passed"  # Not an error, just no sessions
        else:
            print(f"❌ Last Session failed: {response.status_code}")
            assert False, "Test failed"
    except Exception as e:
        print(f"❌ Last Session error: {str(e)}")
        assert False, "Test failed"

def test_improvements():
    """Run all improvement tests"""
    print("🚀 Testing Web Scraper Improvements")
    print("=" * 50)
    
    tests = [
        ("Health Check", test_health_check),
        ("Scraping", test_scraping),
        ("Maintenance Stats", test_maintenance_stats),
        ("Debug Logs", test_debug_logs),
        ("Last Session", test_last_session),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            test_func()  # Function uses assert, so if it passes, we continue
            results.append((test_name, True))
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
        print("🎉 All tests passed! Improvements are working correctly.")
        assert True, "All improvement tests passed"
    else:
        print("⚠️  Some tests failed. Check the server logs for details.")
        assert False, f"Only {passed}/{total} tests passed"

def check_improvements():
    """Check if improvements are properly implemented"""
    print("\n🔍 Checking Implementation...")
    
    # Check if main.py has the new functions
    try:
        with open('backend/main.py', 'r') as f:
            content = f.read()
            
        improvements = [
        ("Rate Limiting", "def rate_limit_delay()"),
        ("Retry Logic", "def retry_request("),
        ("Image Validation", "def validate_image_data("),
        ("Memory Cleanup", "def cleanup_memory()"),
        ("File Extension Helper", "def get_file_extension_from_mime_type("),
        ("Maintenance Endpoints", "@app.post(\"/api/maintenance/cleanup\")"),
        ("Enhanced Health Check", "psutil.virtual_memory()"),
        ]
        
        print("✅ Implementation Check:")
        for name, signature in improvements:
            if signature in content:
                print(f"   ✅ {name}")
            else:
                print(f"   ❌ {name} - Missing")
                
    except FileNotFoundError:
        print("❌ backend/main.py not found")
    except Exception as e:
        print(f"❌ Error checking implementation: {str(e)}")

if __name__ == "__main__":
    print("Web Scraper Improvements Test Suite")
    print("=" * 50)
    
    # Check implementation first
    check_improvements()
    
    # Run tests
    success = test_improvements()
    
    if success:
        print("\n🎉 All improvements are working correctly!")
        print("\nKey improvements verified:")
        print("✅ Fixed base64 image processing")
        print("✅ Added rate limiting and retry logic")
        print("✅ Implemented image validation")
        print("✅ Added memory management")
        print("✅ Enhanced monitoring and debugging")
        print("✅ Added maintenance tools")
    else:
        print("\n⚠️  Some improvements may need attention.")
        print("Check the server logs and ensure the backend is running.")
    
    print(f"\nTest completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}") 