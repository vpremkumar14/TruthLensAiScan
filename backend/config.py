"""
Configuration utilities for TruthLens
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""
    
    # Flask
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('FLASK_DEBUG', 'True') == 'True'
    
    # CORS
    CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', 'http://localhost:3000').split(',')
    
    # File Upload
    MAX_FILE_SIZE = int(os.getenv('MAX_FILE_SIZE', 104857600))  # 100MB
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
    
    # Model
    MODEL_PATH = os.getenv('MODEL_PATH', 'models/deepfake_detector.pth')
    DEVICE = os.getenv('DEVICE', 'auto')
    
    # API
    API_HOST = os.getenv('API_HOST', '0.0.0.0')
    API_PORT = int(os.getenv('API_PORT', 5000))
    
    @staticmethod
    def get_device():
        """Get torch device"""
        import torch
        device = Config.DEVICE
        if device == 'auto':
            return torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        return torch.device(device)

def print_config():
    """Print current configuration"""
    print("\n📝 TruthLens Configuration:")
    print(f"  Environment: {Config.FLASK_ENV}")
    print(f"  Debug: {Config.DEBUG}")
    print(f"  CORS Origins: {Config.CORS_ALLOWED_ORIGINS}")
    print(f"  Max File Size: {Config.MAX_FILE_SIZE / 1024 / 1024:.1f}MB")
    print(f"  Upload Folder: {Config.UPLOAD_FOLDER}")
    print(f"  Model Path: {Config.MODEL_PATH}")
    print(f"  Device: {Config.get_device()}")
    print()
