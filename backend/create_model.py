"""
Create a placeholder model for testing
Run this to generate a model without training
"""

import torch
import torch.nn as nn
from torchvision.models import resnet50
import os

class DeepfakeDetector(nn.Module):
    def __init__(self, num_classes=2):
        super(DeepfakeDetector, self).__init__()
        self.resnet = resnet50(pretrained=True)
        num_features = self.resnet.fc.in_features
        self.resnet.fc = nn.Linear(num_features, num_classes)
    
    def forward(self, x):
        return self.resnet(x)

if __name__ == '__main__':
    print("Creating placeholder model...")
    model = DeepfakeDetector(num_classes=2)
    
    os.makedirs('models', exist_ok=True)
    model_path = 'models/deepfake_detector.pth'
    
    torch.save(model.state_dict(), model_path)
    print(f"✓ Placeholder model created at {model_path}")
    print("Note: This is an untrained model for testing only.")
    print("For production use, train with: python train_model.py")
