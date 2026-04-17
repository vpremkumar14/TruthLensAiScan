#!/usr/bin/env python3
"""
Quick setup and test script for TruthLens
Verifies all components are working correctly
"""

import os
import sys
import torch
import cv2
import numpy as np

def check_python_version():
    """Check Python version"""
    print("🔍 Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"   ✓ Python {version.major}.{version.minor} OK")
        return True
    else:
        print(f"   ✗ Python 3.8+ required (found {version.major}.{version.minor})")
        return False

def check_pytorch():
    """Check PyTorch installation"""
    print("🔍 Checking PyTorch...")
    try:
        print(f"   ✓ PyTorch {torch.__version__} installed")
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        print(f"   ✓ Device: {device}")
        
        # Test tensor operations
        x = torch.randn(1, 3, 224, 224)
        print(f"   ✓ Tensor shape: {x.shape}")
        return True
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False

def check_opencv():
    """Check OpenCV installation"""
    print("🔍 Checking OpenCV...")
    try:
        print(f"   ✓ OpenCV {cv2.__version__} installed")
        return True
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False

def check_model():
    """Check model file"""
    print("🔍 Checking model...")
    model_path = 'models/deepfake_detector.pth'
    if os.path.exists(model_path):
        size_mb = os.path.getsize(model_path) / 1024 / 1024
        print(f"   ✓ Model found: {model_path} ({size_mb:.1f}MB)")
        return True
    else:
        print(f"   ✗ Model not found: {model_path}")
        print(f"   💡 Run: python create_model.py")
        return False

def check_frontend():
    """Check frontend dependencies"""
    print("🔍 Checking Frontend...")
    if os.path.exists('../frontend/package.json'):
        print(f"   ✓ package.json found")
        node_modules = os.path.exists('../frontend/node_modules')
        if node_modules:
            print(f"   ✓ node_modules found")
            return True
        else:
            print(f"   ✗ node_modules not found")
            print(f"   💡 Run: cd frontend && npm install")
            return False
    else:
        print(f"   ✗ Frontend not found")
        return False

def main():
    print("\n" + "="*50)
    print("🔧 TruthLens - System Check")
    print("="*50 + "\n")
    
    checks = [
        check_python_version(),
        check_pytorch(),
        check_opencv(),
        check_model(),
        check_frontend(),
    ]
    
    print("\n" + "="*50)
    if all(checks):
        print("✅ All systems operational!")
        print("\n📝 Next steps:")
        print("   1. python app.py          (start backend)")
        print("   2. npm run dev             (start frontend)")
        print("   3. Open http://localhost:3000")
    else:
        print("⚠️  Some components need attention")
        print("   Please fix the issues above and try again")
    print("="*50 + "\n")

if __name__ == '__main__':
    os.chdir('backend')
    main()
