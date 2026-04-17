"""
Test script for TruthLens API endpoints
"""

import requests
import json
from pathlib import Path

BASE_URL = 'http://localhost:5000/api'

def test_health():
    """Test health endpoint"""
    print("🔍 Testing /api/health...")
    try:
        response = requests.get(f'{BASE_URL}/health')
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False

def test_image_detection(image_path):
    """Test image detection endpoint"""
    print(f"\n🔍 Testing /api/detect-image...")
    
    if not Path(image_path).exists():
        print(f"   ✗ Image not found: {image_path}")
        return False
    
    try:
        with open(image_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(f'{BASE_URL}/detect-image', files=files)
        
        print(f"   Status: {response.status_code}")
        result = response.json()
        print(f"   Response: {json.dumps(result, indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False

def test_video_detection(video_path):
    """Test video detection endpoint"""
    print(f"\n🔍 Testing /api/detect-video...")
    
    if not Path(video_path).exists():
        print(f"   ✗ Video not found: {video_path}")
        return False
    
    try:
        with open(video_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(f'{BASE_URL}/detect-video', files=files)
        
        print(f"   Status: {response.status_code}")
        result = response.json()
        print(f"   Response: {json.dumps(result, indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False

def main():
    print("="*50)
    print("🧪 TruthLens API - Test Suite")
    print("="*50)
    
    # Test health
    health_ok = test_health()
    
    if not health_ok:
        print("\n✗ Backend is not running!")
        print("   Please start the backend: python app.py")
        return
    
    print("\n✅ Backend is running!")
    
    # You can manually test with image/video files
    print("\n📝 To test image detection:")
    print("   Place an image in uploads/ and provide the path")
    print("\n📝 To test video detection:")
    print("   Place a video in uploads/ and provide the path")
    print("\n💡 Example:")
    print("   test_image_detection('uploads/test.jpg')")
    print("   test_video_detection('uploads/test.mp4')")

if __name__ == '__main__':
    main()
