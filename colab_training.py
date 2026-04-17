"""
TruthLens AI Scan - Model Training Script for Google Colab
Run this in Google Colab for free GPU-powered training
"""

import sys
import os
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, models
import numpy as np
import cv2
from PIL import Image
import matplotlib.pyplot as plt
from tqdm import tqdm
import json
from pathlib import Path
import requests
from zipfile import ZipFile
import shutil

# ============================================================
# STEP 0: Install Requirements (Run in Colab)
# ============================================================
def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    os.system('pip install torch torchvision opencv-python pillow requests tqdm -q')
    print("✓ All packages installed!")

# ============================================================
# STEP 1: Download Dataset
# ============================================================
def download_celebdf_lite():
    """
    Download CelebDF Lite Dataset (smaller version for quick training)
    Alternative: Use FaceForensics++ (larger, better quality)
    """
    print("\n📥 Downloading CelebDF Lite Dataset...")
    
    dataset_path = Path('/content/celebdf_dataset')
    dataset_path.mkdir(exist_ok=True)
    
    # For Colab, we'll use a pre-processed mini dataset
    # You can replace with actual FaceForensics++ or DFDC dataset
    
    print("⚠️  NOTE: Using sample dataset structure")
    print("For production, use FaceForensics++ from Kaggle")
    
    return dataset_path

def prepare_sample_dataset():
    """
    Create sample dataset structure for demo
    In production, download FaceForensics++ or DFDC
    """
    print("\n📁 Preparing sample dataset structure...")
    
    data_dir = Path('/content/dataset')
    (data_dir / 'real').mkdir(parents=True, exist_ok=True)
    (data_dir / 'fake').mkdir(parents=True, exist_ok=True)
    
    print(f"✓ Dataset directories created at {data_dir}")
    return data_dir

# ============================================================
# STEP 2: Custom Dataset Class
# ============================================================
class DeepfakeDataset(Dataset):
    """Custom dataset for deepfake detection"""
    
    def __init__(self, data_dir, split='train', transform=None):
        self.data_dir = Path(data_dir)
        self.transform = transform
        self.split = split
        self.images = []
        self.labels = []
        
        # Load real images (label 0)
        real_dir = self.data_dir / 'real'
        if real_dir.exists():
            for img_file in real_dir.glob('*.jpg'):
                self.images.append(str(img_file))
                self.labels.append(0)
            for img_file in real_dir.glob('*.png'):
                self.images.append(str(img_file))
                self.labels.append(0)
        
        # Load fake images (label 1)
        fake_dir = self.data_dir / 'fake'
        if fake_dir.exists():
            for img_file in fake_dir.glob('*.jpg'):
                self.images.append(str(img_file))
                self.labels.append(1)
            for img_file in fake_dir.glob('*.png'):
                self.images.append(str(img_file))
                self.labels.append(1)
        
        print(f"✓ Loaded {len(self.images)} images")
        print(f"  Real: {self.labels.count(0)}, Fake: {self.labels.count(1)}")
    
    def __len__(self):
        return len(self.images)
    
    def __getitem__(self, idx):
        try:
            img_path = self.images[idx]
            label = self.labels[idx]
            
            # Load image
            img = Image.open(img_path).convert('RGB')
            
            # Apply transforms
            if self.transform:
                img = self.transform(img)
            
            return img, label
        except Exception as e:
            print(f"Error loading {self.images[idx]}: {e}")
            # Return a dummy image
            dummy = torch.randn(3, 224, 224)
            return dummy, self.labels[idx]

# ============================================================
# STEP 3: Model Definition
# ============================================================
class DeepfakeDetector(nn.Module):
    """ResNet50 for deepfake detection"""
    
    def __init__(self, pretrained=True):
        super(DeepfakeDetector, self).__init__()
        
        # Load pre-trained ResNet50
        self.model = models.resnet50(pretrained=pretrained)
        
        # Modify final layer for binary classification
        num_ftrs = self.model.fc.in_features
        self.model.fc = nn.Linear(num_ftrs, 2)
    
    def forward(self, x):
        return self.model(x)

# ============================================================
# STEP 4: Training Function
# ============================================================
def train_model(model, train_loader, val_loader, epochs=20, device='cuda'):
    """Train the deepfake detection model"""
    
    print(f"\n🚀 Starting training on {device}...")
    
    # Loss and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=5, gamma=0.1)
    
    # Training metrics
    history = {
        'train_loss': [],
        'train_acc': [],
        'val_loss': [],
        'val_acc': []
    }
    
    best_acc = 0.0
    
    for epoch in range(epochs):
        print(f"\n{'='*60}")
        print(f"Epoch {epoch+1}/{epochs}")
        print('='*60)
        
        # ===== Train Phase =====
        model.train()
        train_loss = 0.0
        train_correct = 0
        train_total = 0
        
        for batch_idx, (images, labels) in enumerate(tqdm(train_loader, desc='Training')):
            images = images.to(device)
            labels = labels.to(device)
            
            # Forward pass
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            
            # Backward pass
            loss.backward()
            optimizer.step()
            
            # Calculate accuracy
            _, predicted = torch.max(outputs.data, 1)
            train_total += labels.size(0)
            train_correct += (predicted == labels).sum().item()
            train_loss += loss.item()
        
        # Calculate epoch metrics
        train_loss /= len(train_loader)
        train_acc = 100 * train_correct / train_total
        
        # ===== Validation Phase =====
        model.eval()
        val_loss = 0.0
        val_correct = 0
        val_total = 0
        
        with torch.no_grad():
            for images, labels in tqdm(val_loader, desc='Validating'):
                images = images.to(device)
                labels = labels.to(device)
                
                outputs = model(images)
                loss = criterion(outputs, labels)
                
                _, predicted = torch.max(outputs.data, 1)
                val_total += labels.size(0)
                val_correct += (predicted == labels).sum().item()
                val_loss += loss.item()
        
        # Calculate validation metrics
        val_loss /= len(val_loader)
        val_acc = 100 * val_correct / val_total
        
        # Store history
        history['train_loss'].append(train_loss)
        history['train_acc'].append(train_acc)
        history['val_loss'].append(val_loss)
        history['val_acc'].append(val_acc)
        
        # Print metrics
        print(f"Train Loss: {train_loss:.4f} | Train Acc: {train_acc:.2f}%")
        print(f"Val Loss: {val_loss:.4f} | Val Acc: {val_acc:.2f}%")
        
        # Save best model
        if val_acc > best_acc:
            best_acc = val_acc
            torch.save(model.state_dict(), '/content/deepfake_detector_best.pth')
            print("💾 Best model saved!")
        
        scheduler.step()
    
    return model, history

# ============================================================
# STEP 5: Data Transformation
# ============================================================
def get_transforms():
    """Get data transforms for training and validation"""
    
    # ImageNet statistics
    mean = [0.485, 0.456, 0.406]
    std = [0.229, 0.224, 0.225]
    
    train_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomRotation(15),
        transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
        transforms.ToTensor(),
        transforms.Normalize(mean=mean, std=std)
    ])
    
    val_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=mean, std=std)
    ])
    
    return train_transform, val_transform

# ============================================================
# STEP 6: Main Training Pipeline
# ============================================================
def main():
    """Main training function"""
    
    print("="*60)
    print("TruthLens AI Scan - Model Training")
    print("="*60)
    
    # Configuration
    BATCH_SIZE = 32
    EPOCHS = 20
    DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
    
    print(f"\n🖥️  Device: {DEVICE}")
    print(f"📊 Batch Size: {BATCH_SIZE}")
    print(f"🔢 Epochs: {EPOCHS}")
    
    # Install requirements
    install_requirements()
    
    # Prepare dataset
    data_dir = prepare_sample_dataset()
    print("\n⚠️  IMPORTANT:")
    print("1. Upload your images to 'dataset/real/' and 'dataset/fake/' folders")
    print("2. Use at least 50+ images in each folder")
    print("3. Re-run this cell after uploading images")
    
    # Get transforms
    train_transform, val_transform = get_transforms()
    
    # Create dataset
    full_dataset = DeepfakeDataset(data_dir, transform=train_transform)
    
    if len(full_dataset) == 0:
        print("\n❌ No images found! Please upload images first.")
        print("Upload structure:")
        print("  dataset/")
        print("    ├── real/   (authentic images)")
        print("    └── fake/   (AI-generated images)")
        return
    
    # Split dataset (80% train, 20% val)
    train_size = int(0.8 * len(full_dataset))
    val_size = len(full_dataset) - train_size
    train_dataset, val_dataset = torch.utils.data.random_split(
        full_dataset, 
        [train_size, val_size]
    )
    
    # Create dataloaders
    train_loader = DataLoader(
        train_dataset,
        batch_size=BATCH_SIZE,
        shuffle=True,
        num_workers=2
    )
    
    val_loader = DataLoader(
        val_dataset,
        batch_size=BATCH_SIZE,
        shuffle=False,
        num_workers=2
    )
    
    print(f"\n📊 Dataset split:")
    print(f"  Train: {len(train_dataset)} images")
    print(f"  Val: {len(val_dataset)} images")
    
    # Create model
    print("\n🧠 Creating ResNet50 model...")
    model = DeepfakeDetector(pretrained=True)
    model = model.to(DEVICE)
    print("✓ Model created and moved to device")
    
    # Count parameters
    total_params = sum(p.numel() for p in model.parameters())
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"📈 Total parameters: {total_params:,}")
    print(f"📈 Trainable parameters: {trainable_params:,}")
    
    # Train model
    model, history = train_model(
        model,
        train_loader,
        val_loader,
        epochs=EPOCHS,
        device=DEVICE
    )
    
    # Save final model
    print("\n💾 Saving final model...")
    torch.save(model.state_dict(), '/content/deepfake_detector_final.pth')
    
    # Save training history
    with open('/content/training_history.json', 'w') as f:
        json.dump(history, f, indent=2)
    print("✓ Training history saved")
    
    # Plot results
    plot_training_results(history)
    
    print("\n" + "="*60)
    print("✅ Training Complete!")
    print("="*60)
    print("\n📥 Download these files:")
    print("1. deepfake_detector_best.pth (Best model)")
    print("2. deepfake_detector_final.pth (Final model)")
    print("3. training_history.json (Metrics)")
    print("\n💡 Place the .pth file in: backend/models/deepfake_detector.pth")

# ============================================================
# STEP 7: Plot Results
# ============================================================
def plot_training_results(history):
    """Plot training and validation metrics"""
    
    print("\n📊 Plotting training results...")
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Plot loss
    axes[0].plot(history['train_loss'], label='Train Loss', marker='o')
    axes[0].plot(history['val_loss'], label='Val Loss', marker='s')
    axes[0].set_xlabel('Epoch')
    axes[0].set_ylabel('Loss')
    axes[0].set_title('Training and Validation Loss')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # Plot accuracy
    axes[1].plot(history['train_acc'], label='Train Accuracy', marker='o')
    axes[1].plot(history['val_acc'], label='Val Accuracy', marker='s')
    axes[1].set_xlabel('Epoch')
    axes[1].set_ylabel('Accuracy (%)')
    axes[1].set_title('Training and Validation Accuracy')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/content/training_results.png', dpi=100, bbox_inches='tight')
    print("✓ Results saved to training_results.png")
    plt.show()

# ============================================================
# Run Training
# ============================================================
if __name__ == "__main__":
    main()
