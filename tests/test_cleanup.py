#!/usr/bin/env python3
"""
Test script for cleanup functionality
Tests various cleanup scenarios and endpoints
"""

import os
import time
import uuid
import requests
import json
from datetime import datetime, timedelta

# Configuration
BASE_URL = "http://backend:8000"
OUTPUT_DIR = "output"

def create_test_session():
    """Create a test session folder with some files"""
    session_id = str(uuid.uuid4())
    session_path = os.path.join(OUTPUT_DIR, session_id)
    
    # Create session directory
    os.makedirs(session_path, exist_ok=True)
    
    # Create some test files
    test_files = [
        ("test_links.csv", "url,text,title\nhttps://example.com,Example,Example Title"),
        ("test_image.jpg", b"fake image data"),
        ("test_data.txt", "Some test data")
    ]
    
    for filename, content in test_files:
        file_path = os.path.join(session_path, filename)
        if isinstance(content, bytes):
            with open(file_path, 'wb') as f:
                f.write(content)
        else:
            with open(file_path, 'w') as f:
                f.write(content)
    
    print(f"✅ Created test session: {session_id}")
    return session_id

def test_cleanup_endpoints():
    """Test various cleanup endpoints"""
    print("\n🧹 Testing Cleanup Endpoints...")
    
    # Test 1: Get maintenance stats
    print("\n1. Testing maintenance stats...")
    try:
        response = requests.get(f"{BASE_URL}/api/maintenance/stats")
        if response.status_code == 200:
            stats = response.json()
            print(f"   ✅ Stats: {stats['total_sessions']} sessions, {stats['total_size_mb']} MB")
        else:
            print(f"   ❌ Failed to get stats: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error getting stats: {e}")
    
    # Test 2: Create test session and clean it up
    print("\n2. Testing specific session cleanup...")
    session_id = create_test_session()
    
    try:
        response = requests.post(f"{BASE_URL}/api/maintenance/cleanup/{session_id}")
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Cleaned up session: {result['message']}")
        else:
            print(f"   ❌ Failed to cleanup session: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error cleaning up session: {e}")
    
    # Test 3: Test scheduled cleanup
    print("\n3. Testing scheduled cleanup...")
    try:
        response = requests.post(f"{BASE_URL}/api/maintenance/cleanup?older_than_hours=1")
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Scheduled cleanup: {result['cleaned_sessions']} sessions cleaned")
        else:
            print(f"   ❌ Failed scheduled cleanup: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error in scheduled cleanup: {e}")

def test_auto_cleanup_scenario():
    """Test auto-cleanup after download scenario"""
    print("\n🔄 Testing Auto-Cleanup Scenario...")
    
    # Create test session
    session_id = create_test_session()
    
    # Simulate download (this should trigger auto-cleanup)
    print(f"\n📥 Simulating download for session: {session_id}")
    
    try:
        # Try to download a file (this should trigger cleanup)
        response = requests.get(f"{BASE_URL}/api/download/{session_id}/test_links.csv")
        print(f"   Download response: {response.status_code}")
        
        # Wait a bit for cleanup to happen
        time.sleep(2)
        
        # Check if session still exists
        session_path = os.path.join(OUTPUT_DIR, session_id)
        if os.path.exists(session_path):
            print(f"   ⚠️  Session folder still exists: {session_path}")
        else:
            print(f"   ✅ Session folder cleaned up automatically")
            
    except Exception as e:
        print(f"   ❌ Error in download test: {e}")

def test_cleanup_all():
    """Test cleanup all sessions (use with caution)"""
    print("\n🗑️  Testing Cleanup All Sessions...")
    
    # Create multiple test sessions
    session_ids = []
    for i in range(3):
        session_id = create_test_session()
        session_ids.append(session_id)
    
    print(f"   Created {len(session_ids)} test sessions")
    
    # Test cleanup all
    try:
        response = requests.post(f"{BASE_URL}/api/maintenance/cleanup-all")
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Cleanup all: {result['cleaned_sessions']} sessions cleaned")
        else:
            print(f"   ❌ Failed cleanup all: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error in cleanup all: {e}")

def check_output_directory():
    """Check the current state of output directory"""
    print("\n📁 Checking Output Directory...")
    
    if not os.path.exists(OUTPUT_DIR):
        print("   ❌ Output directory does not exist")
        return
    
    sessions = [d for d in os.listdir(OUTPUT_DIR) if os.path.isdir(os.path.join(OUTPUT_DIR, d))]
    
    if not sessions:
        print("   ✅ Output directory is clean (no sessions)")
        return
    
    print(f"   📊 Found {len(sessions)} session(s):")
    for session in sessions:
        session_path = os.path.join(OUTPUT_DIR, session)
        creation_time = datetime.fromtimestamp(os.path.getctime(session_path))
        age = datetime.now() - creation_time
        
        # Calculate size
        total_size = 0
        file_count = 0
        for dirpath, dirnames, filenames in os.walk(session_path):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                total_size += os.path.getsize(file_path)
                file_count += 1
        
        print(f"      - {session[:8]}... | Age: {age.total_seconds()/3600:.1f}h | Files: {file_count} | Size: {total_size/1024:.1f}KB")

def main():
    """Main test function"""
    print("🧪 Cleanup Functionality Test")
    print("=" * 50)
    
    # Check if backend is running
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        if response.status_code == 200:
            print("✅ Backend is running")
        else:
            print("❌ Backend is not responding properly")
            return
    except Exception as e:
        print(f"❌ Cannot connect to backend: {e}")
        print("   Make sure the backend is running on http://localhost:8001")
        return
    
    # Run tests
    check_output_directory()
    test_cleanup_endpoints()
    test_auto_cleanup_scenario()
    test_cleanup_all()
    
    # Final check
    print("\n" + "=" * 50)
    print("🏁 Final Check:")
    check_output_directory()
    
    print("\n✅ Cleanup tests completed!")

if __name__ == "__main__":
    main() 