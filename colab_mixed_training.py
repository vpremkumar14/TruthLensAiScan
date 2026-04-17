"""
TruthLens AI Scan - Mixed Image & Video Training Script
Train ResNet50 on BOTH images and video frames for better detection
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
# STEP 1: Video Frame Extraction
# ============================================================
def extract_frames_from_video(video_path, num_frames=5):
    """
    Extract evenly spaced frames from video
    Returns list of frame arrays
    """
    try:
        cap = cv2.VideoCapture(str(video_path))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        if total_frames == 0:
            return []
        
        # Calculate frame indices to extract
        frame_indices = np.linspace(0, total_frames - 1, num_frames, dtype=int)
        
        frames = []
        for idx in frame_indices:
            cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
            ret, frame = cap.read()
            
            if ret:
                # Convert BGR to RGB
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frames.append(frame_rgb)
        
        cap.release()
        return frames
    
    except Exception as e:
        print(f"Error extracting frames from {video_path}: {e}")
        return []

def convert_video_frames_to_images(data_dir, num_frames_per_video=5):
    """
    Convert video frames to images for training
    Creates temporary images from videos
    """
    print("\n🎬 Converting video frames to images...")
    
    data_dir = Path(data_dir)
    temp_dir = data_dir / 'temp_frames'
    temp_dir.mkdir(exist_ok=True)
    
    (temp_dir / 'real').mkdir(exist_ok=True)
    (temp_dir / 'fake').mkdir(exist_ok=True)
    
    frame_count = {'real': 0, 'fake': 0}
    
    # Process real videos
    real_dir = data_dir / 'real'
    if real_dir.exists():
        for video_file in real_dir.glob('*.mp4'):
            frames = extract_frames_from_video(video_file, num_frames=num_frames_per_video)
            for i, frame in enumerate(frames):
                try:
                    frame_img = Image.fromarray(frame)
                    frame_name = f"{video_file.stem}_frame_{i}.jpg"
                    frame_img.save(temp_dir / 'real' / frame_name)
                    frame_count['real'] += 1
                except Exception as e:
                    print(f"Error saving frame: {e}")
        
        for video_file in real_dir.glob('*.avi'):
            frames = extract_frames_from_video(video_file, num_frames=num_frames_per_video)
            for i, frame in enumerate(frames):
                try:
                    frame_img = Image.fromarray(frame)
                    frame_name = f"{video_file.stem}_frame_{i}.jpg"
                    frame_img.save(temp_dir / 'real' / frame_name)
                    frame_count['real'] += 1
                except Exception as e:
                    print(f"Error saving frame: {e}")
    
    # Process fake videos
    fake_dir = data_dir / 'fake'
    if fake_dir.exists():
        for video_file in fake_dir.glob('*.mp4'):
            frames = extract_frames_from_video(video_file, num_frames=num_frames_per_video)
            for i, frame in enumerate(frames):
                try:
                    frame_img = Image.fromarray(frame)
                    frame_name = f"{video_file.stem}_frame_{i}.jpg"
                    frame_img.save(temp_dir / 'fake' / frame_name)
                    frame_count['fake'] += 1
                except Exception as e:
                    print(f"Error saving frame: {e}")
        
        for video_file in fake_dir.glob('*.avi'):
            frames = extract_frames_from_video(video_file, num_frames=num_frames_per_video)
            for i, frame in enumerate(frames):
                try:
                    frame_img = Image.fromarray(frame)
                    frame_name = f"{video_file.stem}_frame_{i}.jpg"
                    frame_img.save(temp_dir / 'fake' / frame_name)
                    frame_count['fake'] += 1
                except Exception as e:
                    print(f"Error saving frame: {e}")
    
    print(f"✓ Video frames extracted:")
    print(f"  Real frames: {frame_count['real']}")
    print(f"  Fake frames: {frame_count['fake']}")
    
    return temp_dir

# ============================================================
# STEP 2: Mixed Dataset Class (Images + Video Frames)
# ============================================================
class MixedDeepfakeDataset(Dataset):
    """Custom dataset combining images and video frames"""
    
    def __init__(self, data_dir, temp_frames_dir, split='train', transform=None):
        self.data_dir = Path(data_dir)
        self.temp_frames_dir = Path(temp_frames_dir) if temp_frames_dir else None
        self.transform = transform
        self.split = split
        self.images = []
        self.labels = []
        
        # Load real images
        real_dir = self.data_dir / 'real'
        if real_dir.exists():
            for img_file in real_dir.glob('*.jpg'):
                self.images.append(str(img_file))
                self.labels.append(0)
            for img_file in real_dir.glob('*.png'):
                self.images.append(str(img_file))
                self.labels.append(0)
        
        # Load fake images
        fake_dir = self.data_dir / 'fake'
        if fake_dir.exists():
            for img_file in fake_dir.glob('*.jpg'):
                self.images.append(str(img_file))
                self.labels.append(1)
            for img_file in fake_dir.glob('*.png'):
                self.images.append(str(img_file))
                self.labels.append(1)
        
        # Load real video frames (if available)
        if self.temp_frames_dir and (self.temp_frames_dir / 'real').exists():
            for frame_file in (self.temp_frames_dir / 'real').glob('*.jpg'):
                self.images.append(str(frame_file))
                self.labels.append(0)
        
        # Load fake video frames (if available)
        if self.temp_frames_dir and (self.temp_frames_dir / 'fake').exists():
            for frame_file in (self.temp_frames_dir / 'fake').glob('*.jpg'):
                self.images.append(str(frame_file))
                self.labels.append(1)
        
        print(f"✓ Loaded {len(self.images)} total samples (images + video frames)")
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
            dummy = torch.randn(3, 224, 224)
            return dummy, self.labels[idx]

# ============================================================
# STEP 3: Model Definition
# ============================================================
class DeepfakeDetector(nn.Module):
    """ResNet50 for mixed image & video deepfake detection"""
    
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
# STEP 4: Data Augmentation & Transforms
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
        transforms.RandomAffine(degrees=0, translate=(0.1, 0.1)),
        transforms.GaussianBlur(kernel_size=3, sigma=(0.1, 2.0)),
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
# STEP 5: Training Function
# ============================================================
def train_model(model, train_loader, val_loader, epochs=20, device='cuda'):
    """Train the mixed dataset model"""
    
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
        'val_acc': [],
        'train_real_acc': [],
        'train_fake_acc': [],
        'val_real_acc': [],
        'val_fake_acc': []
    }
    
    best_acc = 0.0
    
    for epoch in range(epochs):
        print(f"\n{'='*70}")
        print(f"Epoch {epoch+1}/{epochs}")
        print('='*70)
        
        # ===== Train Phase =====
        model.train()
        train_loss = 0.0
        train_correct = 0
        train_total = 0
        train_real_correct = 0
        train_real_total = 0
        train_fake_correct = 0
        train_fake_total = 0
        
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
            
            # Per-class accuracy
            for i in range(len(labels)):
                if labels[i] == 0:  # Real
                    train_real_total += 1
                    if predicted[i] == 0:
                        train_real_correct += 1
                else:  # Fake
                    train_fake_total += 1
                    if predicted[i] == 1:
                        train_fake_correct += 1
        
        # Calculate epoch metrics
        train_loss /= len(train_loader)
        train_acc = 100 * train_correct / train_total
        train_real_acc = 100 * train_real_correct / train_real_total if train_real_total > 0 else 0
        train_fake_acc = 100 * train_fake_correct / train_fake_total if train_fake_total > 0 else 0
        
        # ===== Validation Phase =====
        model.eval()
        val_loss = 0.0
        val_correct = 0
        val_total = 0
        val_real_correct = 0
        val_real_total = 0
        val_fake_correct = 0
        val_fake_total = 0
        
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
                
                # Per-class accuracy
                for i in range(len(labels)):
                    if labels[i] == 0:  # Real
                        val_real_total += 1
                        if predicted[i] == 0:
                            val_real_correct += 1
                    else:  # Fake
                        val_fake_total += 1
                        if predicted[i] == 1:
                            val_fake_correct += 1
        
        # Calculate validation metrics
        val_loss /= len(val_loader)
        val_acc = 100 * val_correct / val_total
        val_real_acc = 100 * val_real_correct / val_real_total if val_real_total > 0 else 0
        val_fake_acc = 100 * val_fake_correct / val_fake_total if val_fake_total > 0 else 0
        
        # Store history
        history['train_loss'].append(train_loss)
        history['train_acc'].append(train_acc)
        history['val_loss'].append(val_loss)
        history['val_acc'].append(val_acc)
        history['train_real_acc'].append(train_real_acc)
        history['train_fake_acc'].append(train_fake_acc)
        history['val_real_acc'].append(val_real_acc)
        history['val_fake_acc'].append(val_fake_acc)
        
        # Print metrics
        print(f"\nTrain Loss: {train_loss:.4f} | Train Acc: {train_acc:.2f}%")
        print(f"  → Real accuracy: {train_real_acc:.2f}% | Fake accuracy: {train_fake_acc:.2f}%")
        print(f"\nVal Loss: {val_loss:.4f} | Val Acc: {val_acc:.2f}%")
        print(f"  → Real accuracy: {val_real_acc:.2f}% | Fake accuracy: {val_fake_acc:.2f}%")
        
        # Save best model
        if val_acc > best_acc:
            best_acc = val_acc
            torch.save(model.state_dict(), '/content/deepfake_detector_best.pth')
            print("\n💾 Best model saved!")
        
        scheduler.step()
    
    return model, history

# ============================================================
# STEP 6: Visualization
# ============================================================
def plot_training_results(history):
    """Plot comprehensive training results"""
    
    print("\n📊 Plotting training results...")
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # Plot loss
    axes[0, 0].plot(history['train_loss'], label='Train Loss', marker='o')
    axes[0, 0].plot(history['val_loss'], label='Val Loss', marker='s')
    axes[0, 0].set_xlabel('Epoch')
    axes[0, 0].set_ylabel('Loss')
    axes[0, 0].set_title('Training and Validation Loss')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    # Plot overall accuracy
    axes[0, 1].plot(history['train_acc'], label='Train Accuracy', marker='o')
    axes[0, 1].plot(history['val_acc'], label='Val Accuracy', marker='s')
    axes[0, 1].set_xlabel('Epoch')
    axes[0, 1].set_ylabel('Accuracy (%)')
    axes[0, 1].set_title('Overall Accuracy')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    
    # Plot real accuracy
    axes[1, 0].plot(history['train_real_acc'], label='Train Real Acc', marker='o')
    axes[1, 0].plot(history['val_real_acc'], label='Val Real Acc', marker='s')
    axes[1, 0].set_xlabel('Epoch')
    axes[1, 0].set_ylabel('Real Accuracy (%)')
    axes[1, 0].set_title('Real Image Detection Accuracy')
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)
    
    # Plot fake accuracy
    axes[1, 1].plot(history['train_fake_acc'], label='Train Fake Acc', marker='o')
    axes[1, 1].plot(history['val_fake_acc'], label='Val Fake Acc', marker='s')
    axes[1, 1].set_xlabel('Epoch')
    axes[1, 1].set_ylabel('Fake Accuracy (%)')
    axes[1, 1].set_title('Fake Image Detection Accuracy')
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/content/training_results.png', dpi=100, bbox_inches='tight')
    print("✓ Results saved to training_results.png")
    plt.show()

# ============================================================
# STEP 7: Main Training Pipeline
# ============================================================
def main():
    """Main training function"""
    
    print("="*70)
    print("TruthLens AI Scan - Mixed Image & Video Training")
    print("="*70)
    
    # Configuration
    BATCH_SIZE = 32
    EPOCHS = 20
    NUM_FRAMES_PER_VIDEO = 5
    DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
    
    print(f"\n🖥️  Device: {DEVICE}")
    print(f"📊 Batch Size: {BATCH_SIZE}")
    print(f"🔢 Epochs: {EPOCHS}")
    print(f"🎬 Frames per video: {NUM_FRAMES_PER_VIDEO}")
    
    # Install requirements
    print("\n📦 Installing required packages...")
    os.system('pip install torch torchvision opencv-python pillow requests tqdm -q')
    print("✓ All packages installed!")
    
    # Prepare dataset
    data_dir = Path('/content/dataset')
    data_dir.mkdir(exist_ok=True)
    (data_dir / 'real').mkdir(exist_ok=True)
    (data_dir / 'fake').mkdir(exist_ok=True)
    
    print("\n" + "="*70)
    print("📁 DATASET STRUCTURE")
    print("="*70)
    print("\nUpload files in this structure:")
    print("""
    /content/dataset/
    ├── real/
    │   ├── photo1.jpg          (authentic photo)
    │   ├── photo2.png          (authentic photo)
    │   ├── video1.mp4          (authentic video)
    │   └── video2.avi          (authentic video)
    └── fake/
        ├── generated1.jpg      (AI-generated image)
        ├── deepfake1.mp4       (deepfake video)
        └── generated2.png      (AI image)
    """)
    print("Minimum: 50+ images/frames per class for good accuracy")
    print("="*70)
    
    # Count images
    real_images = len(list((data_dir / 'real').glob('*.jpg'))) + \
                  len(list((data_dir / 'real').glob('*.png')))
    fake_images = len(list((data_dir / 'fake').glob('*.jpg'))) + \
                  len(list((data_dir / 'fake').glob('*.png')))
    real_videos = len(list((data_dir / 'real').glob('*.mp4'))) + \
                  len(list((data_dir / 'real').glob('*.avi')))
    fake_videos = len(list((data_dir / 'fake').glob('*.mp4'))) + \
                  len(list((data_dir / 'fake').glob('*.avi')))
    
    print(f"\n📊 Dataset Summary:")
    print(f"  Real images: {real_images}")
    print(f"  Real videos: {real_videos}")
    print(f"  Fake images: {fake_images}")
    print(f"  Fake videos: {fake_videos}")
    
    total_samples = real_images + fake_images
    
    if total_samples == 0:
        print("\n❌ No images found!")
        print("Please upload images to continue.")
        return
    
    # Get transforms
    train_transform, val_transform = get_transforms()
    
    # Extract video frames
    temp_frames_dir = None
    if real_videos > 0 or fake_videos > 0:
        temp_frames_dir = convert_video_frames_to_images(data_dir, NUM_FRAMES_PER_VIDEO)
    
    # Create dataset
    full_dataset = MixedDeepfakeDataset(
        data_dir, 
        temp_frames_dir, 
        transform=train_transform
    )
    
    if len(full_dataset) == 0:
        print("❌ No samples found!")
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
    
    print(f"\n📊 Using {len(full_dataset)} total samples:")
    print(f"  Train: {len(train_dataset)} samples")
    print(f"  Val: {len(val_dataset)} samples")
    
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
    
    print("\n" + "="*70)
    print("✅ Training Complete!")
    print("="*70)
    print("\n📥 Download these files:")
    print("1. deepfake_detector_best.pth ⭐ (Best model - USE THIS!)")
    print("2. deepfake_detector_final.pth (Final model)")
    print("3. training_history.json (Metrics)")
    print("4. training_results.png (Graphs)")
    print("\n💡 Place deepfake_detector_best.pth in: backend/models/deepfake_detector.pth")

# ============================================================
# Run Training
# ============================================================
if __name__ == "__main__":
    main()
