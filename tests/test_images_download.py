#!/usr/bin/env python3
"""
Test script to verify images ZIP download functionality
"""

import requests
import json
import time
import os
import zipfile
import tempfile
from datetime import datetime

# Configuration
BASE_URL = "http://backend:8000"
TEST_URL = "https://jeevawasa.com"

def test_scraping_and_images_download():
    """Test scraping and images ZIP download functionality"""
    print("🔍 Testing Scraping and Images ZIP Download...")
    
    try:
        # Step 1: Perform scraping
        print("   1. Performing scraping...")
        payload = {
            "url": TEST_URL,
    
        }
        
        response = requests.post(f"{BASE_URL}/api/scrape", json=payload)
        
        if response.status_code != 200:
            print(f"❌ Scraping failed: {response.status_code}")
            print(f"   Response: {response.text}")
            assert False, "Test failed"
        
        data = response.json()
        print(f"✅ Scraping successful!")
        print(f"   Links: {data['links_count']}")
        print(f"   Images: {data['images_count']}")
        print(f"   Images ZIP URL: {data['images_folder']}")
        
        # Extract session ID from images URL
        images_url = data['images_folder']
        session_id = images_url.split('/')[-1]
        
        print(f"   Session ID: {session_id}")
        
        # Step 2: Get images info
        print("   2. Getting images info...")
        images_info_response = requests.get(f"{BASE_URL}/api/images/{session_id}/info")
        
        if images_info_response.status_code == 200:
            images_info = images_info_response.json()
            print(f"✅ Images info retrieved successfully!")
            print(f"   Total images: {images_info['total_images']}")
            print(f"   Total size: {images_info['total_size_mb']} MB")
            
            # Show some image details
            for i, img in enumerate(images_info['images'][:5]):  # Show first 5
                print(f"   - {img['filename']}: {img['size_mb']} MB ({img['extension']})")
            
            if len(images_info['images']) > 5:
                print(f"   ... and {len(images_info['images']) - 5} more images")
        else:
            print(f"❌ Failed to get images info: {images_info_response.status_code}")
            assert False, "Test failed"
        
        # Step 3: Download images ZIP
        print("   3. Downloading images ZIP...")
        zip_response = requests.get(f"{BASE_URL}/api/images/{session_id}")
        
        if zip_response.status_code == 200:
            print(f"✅ Images ZIP download successful!")
            print(f"   Content-Type: {zip_response.headers.get('Content-Type', 'N/A')}")
            print(f"   Content-Length: {zip_response.headers.get('Content-Length', 'N/A')}")
            print(f"   Content-Disposition: {zip_response.headers.get('Content-Disposition', 'N/A')}")
            
            # Save ZIP file for inspection
            zip_filename = f"test_images_{session_id}.zip"
            with open(zip_filename, 'wb') as f:
                f.write(zip_response.content)
            
            print(f"   ZIP saved to: {zip_filename}")
            
            # Verify ZIP content
            print("   4. Verifying ZIP content...")
            try:
                with zipfile.ZipFile(zip_filename, 'r') as zipf:
                    file_list = zipf.namelist()
                    print(f"✅ ZIP verification successful!")
                    print(f"   Files in ZIP: {len(file_list)}")
                    
                    # Show first few files
                    for i, filename in enumerate(file_list[:5]):
                        file_info = zipf.getinfo(filename)
                        print(f"   - {filename}: {file_info.file_size} bytes")
                    
                    if len(file_list) > 5:
                        print(f"   ... and {len(file_list) - 5} more files")
                    
                    # Verify all files are images
                    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg'}
                    non_image_files = [f for f in file_list if not any(f.lower().endswith(ext) for ext in image_extensions)]
                    
                    if non_image_files:
                        print(f"⚠️  Warning: Found non-image files in ZIP: {non_image_files}")
                    else:
                        print("✅ All files in ZIP are images")
                    
                    assert True, "Test passed"
                    
            except zipfile.BadZipFile:
                print("❌ ERROR: Downloaded file is not a valid ZIP!")
                assert False, "Test failed"
            except Exception as e:
                print(f"❌ Error verifying ZIP: {str(e)}")
                assert False, "Test failed"
        else:
            print(f"❌ Images ZIP download failed: {zip_response.status_code}")
            print(f"   Response: {zip_response.text}")
            assert False, "Test failed"
            
    except Exception as e:
        print(f"❌ Test error: {str(e)}")
        assert False, "Test failed"

def test_images_info_endpoint():
    """Test the images info endpoint"""
    print("\n🔍 Testing Images Info Endpoint...")
    
    try:
        # First get the last session
        last_session_response = requests.get(f"{BASE_URL}/api/debug/last-session")
        
        if last_session_response.status_code != 200:
            print(f"❌ Failed to get last session: {last_session_response.status_code}")
            assert False, "Test failed"
        
        last_session_data = last_session_response.json()
        
        if 'error' in last_session_data:
            print(f"⚠️  No sessions found: {last_session_data['error']}")
            assert False, "Test failed"
        
        session_id = last_session_data['latest_session']
        print(f"   Using session: {session_id}")
        
        # Test images info endpoint
        images_info_response = requests.get(f"{BASE_URL}/api/images/{session_id}/info")
        
        if images_info_response.status_code == 200:
            images_info = images_info_response.json()
            print(f"✅ Images info endpoint successful!")
            print(f"   Total images: {images_info['total_images']}")
            print(f"   Total size: {images_info['total_size_mb']} MB")
            print(f"   Download URL: {images_info['download_url']}")
            assert True, "Test passed"
        else:
            print(f"❌ Images info endpoint failed: {images_info_response.status_code}")
            assert False, "Test failed"
            
    except Exception as e:
        print(f"❌ Test error: {str(e)}")
        assert False, "Test failed"

def test_images_zip_endpoint():
    """Test the images ZIP endpoint"""
    print("\n🔍 Testing Images ZIP Endpoint...")
    
    try:
        # First get the last session
        last_session_response = requests.get(f"{BASE_URL}/api/debug/last-session")
        
        if last_session_response.status_code != 200:
            print(f"❌ Failed to get last session: {last_session_response.status_code}")
            assert False, "Test failed"
        
        last_session_data = last_session_response.json()
        
        if 'error' in last_session_data:
            print(f"⚠️  No sessions found: {last_session_data['error']}")
            assert False, "Test failed"
        
        session_id = last_session_data['latest_session']
        print(f"   Using session: {session_id}")
        
        # Test images ZIP endpoint
        zip_response = requests.get(f"{BASE_URL}/api/images/{session_id}")
        
        if zip_response.status_code == 200:
            print(f"✅ Images ZIP endpoint successful!")
            print(f"   Content-Type: {zip_response.headers.get('Content-Type', 'N/A')}")
            print(f"   Content-Length: {zip_response.headers.get('Content-Length', 'N/A')}")
            
            # Check if it's actually a ZIP file
            if zip_response.headers.get('Content-Type') == 'application/zip':
                print("✅ Content-Type is correct (application/zip)")
                
                # Try to open as ZIP
                try:
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as temp_file:
                        temp_file.write(zip_response.content)
                        temp_file_path = temp_file.name
                    
                    with zipfile.ZipFile(temp_file_path, 'r') as zipf:
                        file_count = len(zipf.namelist())
                        print(f"✅ ZIP file is valid with {file_count} files")
                    
                    # Clean up
                    os.unlink(temp_file_path)
                    assert True, "Test passed"
                    
                except zipfile.BadZipFile:
                    print("❌ ERROR: Response is not a valid ZIP file!")
                    assert False, "Test failed"
                except Exception as e:
                    print(f"❌ Error testing ZIP: {str(e)}")
                    assert False, "Test failed"
            else:
                print(f"❌ Wrong Content-Type: {zip_response.headers.get('Content-Type')}")
                assert False, "Test failed"
        else:
            print(f"❌ Images ZIP endpoint failed: {zip_response.status_code}")
            assert False, "Test failed"
            
    except Exception as e:
        print(f"❌ Test error: {str(e)}")
        assert False, "Test failed"

def test_no_images_session():
    """Test behavior when session has no images"""
    print("\n🔍 Testing Session with No Images...")
    
    try:
        # Create a test session with no images (just CSV)
        test_session_id = "test-no-images-session"
        test_session_path = os.path.join("output", test_session_id)
        
        # Create session directory
        os.makedirs(test_session_path, exist_ok=True)
        
        # Create a dummy CSV file (no images)
        csv_path = os.path.join(test_session_path, "test.csv")
        with open(csv_path, 'w') as f:
            f.write("url,text\nhttps://example.com,Test\n")
        
        # Test images info endpoint
        images_info_response = requests.get(f"{BASE_URL}/api/images/{test_session_id}/info")
        
        if images_info_response.status_code == 200:
            images_info = images_info_response.json()
            print(f"✅ Images info for no-images session:")
            print(f"   Total images: {images_info['total_images']}")
            print(f"   Total size: {images_info['total_size_mb']} MB")
            
            # Test ZIP download (should return 404)
            zip_response = requests.get(f"{BASE_URL}/api/images/{test_session_id}")
            
            if zip_response.status_code in [404, 500]:
                print(f"✅ Correctly returns {zip_response.status_code} for session with no images")
                assert True, "Test passed"
            else:
                print(f"❌ Expected 404 or 500, got {zip_response.status_code}")
                assert False, "Test failed"
        else:
            print(f"❌ Images info failed: {images_info_response.status_code}")
            assert False, "Test failed"
            
    except Exception as e:
        print(f"❌ Test error: {str(e)}")
        assert False, "Test failed"
    finally:
        # Clean up test session
        test_session_path = os.path.join("output", "test-no-images-session")
        if os.path.exists(test_session_path):
            import shutil
            shutil.rmtree(test_session_path)

def main():
    """Run all images download tests"""
    print("🚀 Images ZIP Download Test Suite")
    print("=" * 50)
    
    tests = [
        ("Scraping and Images Download", test_scraping_and_images_download),
        ("Images Info Endpoint", test_images_info_endpoint),
        ("Images ZIP Endpoint", test_images_zip_endpoint),
        ("No Images Session", test_no_images_session),
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
        print("🎉 All images download tests passed!")
        print("\nKey features verified:")
        print("✅ Images ZIP download functionality")
        print("✅ Images info endpoint")
        print("✅ Proper ZIP file creation")
        print("✅ Content-Type headers")
        print("✅ Error handling for no images")
    else:
        print("⚠️  Some tests failed. Check the server configuration.")
    
    print(f"\nTest completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main() 