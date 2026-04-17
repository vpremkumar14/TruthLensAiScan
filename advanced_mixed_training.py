"""
Advanced Mixed Training Script - 3 Dataset Approach
Train ResNet50 on MULTIPLE DATASETS combining images, videos, and synthetic data
Optimized for BEST ACCURACY with limited data

Usage:
    # Quick local training
    python advanced_mixed_training.py --local-only --epochs 30
    
    # With augmentation
    python advanced_mixed_training.py --augment --epochs 50
    
    # Full training with all datasets
    python advanced_mixed_training.py --full --epochs 100
"""

import sys
import os
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader, random_split
from torchvision import transforms, models
import numpy as np
import cv2
from PIL import Image
import matplotlib.pyplot as plt
from tqdm import tqdm
import json
from pathlib import Path
import argparse
import random
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Set seeds for reproducibility
def set_seed(seed=42):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

set_seed(42)

# ============================================================
# DEVICE SETUP
# ============================================================
def get_device():
    """Get torch device (GPU if available, else CPU)"""
    if torch.cuda.is_available():
        device = torch.device('cuda')
        logger.info(f"✓ Using GPU: {torch.cuda.get_device_name(0)}")
    else:
        device = torch.device('cpu')
        logger.info("⚠ Using CPU - Training will be slower")
    return device

# ============================================================
# VIDEO FRAME EXTRACTION
# ============================================================
def extract_frames_from_video(video_path, num_frames=8, target_size=(224, 224)):
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
            cap.set(cv2.CAP_PROP_POS_FRAMES, int(idx))
            ret, frame = cap.read()
            
            if ret:
                # Resize frame
                frame = cv2.resize(frame, target_size)
                # Convert BGR to RGB
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frames.append(frame_rgb)
        
        cap.release()
        return frames
    
    except Exception as e:
        logger.warning(f"Error extracting frames from {video_path}: {e}")
        return []

def convert_videos_to_frames(data_dir, num_frames_per_video=8):
    """
    Convert ALL video files to frames
    Returns path to temporary frames directory
    """
    logger.info("\n🎬 Converting video frames to images...")
    
    data_dir = Path(data_dir)
    temp_dir = data_dir / 'temp_frames'
    temp_dir.mkdir(exist_ok=True)
    
    (temp_dir / 'real').mkdir(exist_ok=True)
    (temp_dir / 'fake').mkdir(exist_ok=True)
    
    frame_count = {'real': 0, 'fake': 0}
    
    # Video extensions to check
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv']
    
    # Process real videos
    real_dir = data_dir / 'real'
    if real_dir.exists():
        for video_file in real_dir.iterdir():
            if video_file.suffix.lower() in video_extensions:
                frames = extract_frames_from_video(video_file, num_frames=num_frames_per_video)
                for i, frame in enumerate(frames):
                    try:
                        frame_img = Image.fromarray(frame)
                        frame_name = f"{video_file.stem}_frame_{i:03d}.jpg"
                        frame_img.save(temp_dir / 'real' / frame_name)
                        frame_count['real'] += 1
                    except Exception as e:
                        logger.warning(f"Error saving frame: {e}")
    
    # Process fake videos
    fake_dir = data_dir / 'fake'
    if fake_dir.exists():
        for video_file in fake_dir.iterdir():
            if video_file.suffix.lower() in video_extensions:
                frames = extract_frames_from_video(video_file, num_frames=num_frames_per_video)
                for i, frame in enumerate(frames):
                    try:
                        frame_img = Image.fromarray(frame)
                        frame_name = f"{video_file.stem}_frame_{i:03d}.jpg"
                        frame_img.save(temp_dir / 'fake' / frame_name)
                        frame_count['fake'] += 1
                    except Exception as e:
                        logger.warning(f"Error saving frame: {e}")
    
    logger.info(f"✓ Video frames extracted: Real={frame_count['real']}, Fake={frame_count['fake']}")
    return temp_dir if (frame_count['real'] > 0 or frame_count['fake'] > 0) else None

# ============================================================
# SYNTHETIC DATA GENERATION (For augmentation)
# ============================================================
def generate_synthetic_faces(num_samples=100, save_dir=None):
    """
    Generate synthetic training images for data augmentation
    Uses various patterns to create diverse fake samples
    """
    logger.info(f"\n🖼 Generating {num_samples} synthetic images...")
    
    if save_dir:
        Path(save_dir).mkdir(parents=True, exist_ok=True)
    
    synthetic_images = []
    
    for i in range(num_samples):
        # Create varied synthetic patterns
        img_type = i % 5
        img = np.zeros((224, 224, 3), dtype=np.uint8)
        
        if img_type == 0:
            # Gradient pattern
            for j in range(224):
                img[j, :, 0] = int(255 * (j / 224))
                img[j, :, 1] = int(128 * (j / 224))
                img[j, :, 2] = 255 - int(255 * (j / 224))
        
        elif img_type == 1:
            # Noise pattern
            img = np.random.randint(0, 200, (224, 224, 3), dtype=np.uint8)
        
        elif img_type == 2:
            # Circular patterns
            center = (112, 112)
            radius = 50 + (i % 30)
            cv2.circle(img, center, radius, (100 + (i % 155), 50, 200), -1)
        
        elif img_type == 3:
            # Block patterns (mosaic)
            block_size = 8 + (i % 20)
            for x in range(0, 224, block_size):
                for y in range(0, 224, block_size):
                    color = (np.random.randint(0, 256), np.random.randint(0, 256), np.random.randint(0, 256))
                    cv2.rectangle(img, (x, y), (x + block_size, y + block_size), color, -1)
        
        else:
            # Complex patterns
            img = np.zeros((224, 224, 3), dtype=np.uint8)
            for _ in range(20):
                pt1 = (np.random.randint(0, 224), np.random.randint(0, 224))
                pt2 = (np.random.randint(0, 224), np.random.randint(0, 224))
                color = (np.random.randint(0, 256), np.random.randint(0, 256), np.random.randint(0, 256))
                cv2.line(img, pt1, pt2, color, 2)
        
        synthetic_images.append(img)
        
        # Save if directory provided
        if save_dir:
            Image.fromarray(img).save(f"{save_dir}/synthetic_{i:04d}.jpg")
    
    logger.info(f"✓ Generated {num_samples} synthetic images")
    return synthetic_images

# ============================================================
# DATA AUGMENTATION TRANSFORMATIONS
# ============================================================
def get_train_transforms(augment=True):
    """
    Create training transforms with aggressive augmentation
    Better accuracy with limited data
    """
    if augment:
        return transforms.Compose([
            transforms.RandomHorizontalFlip(p=0.5),
            transforms.RandomVerticalFlip(p=0.3),
            transforms.RandomRotation(degrees=15),
            transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1),
            transforms.RandomAffine(degrees=0, translate=(0.1, 0.1)),
            transforms.RandomPerspective(distortion_scale=0.2, p=0.5),
            transforms.GaussianBlur(kernel_size=3, sigma=(0.1, 2.0)),
            transforms.RandomInvert(p=0.1),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                               std=[0.229, 0.224, 0.225])
        ])
    else:
        return transforms.Compose([
            transforms.RandomHorizontalFlip(p=0.5),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                               std=[0.229, 0.224, 0.225])
        ])

def get_val_transforms():
    """Validation transforms (minimal augmentation)"""
    return transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                           std=[0.229, 0.224, 0.225])
    ])

# ============================================================
# MIXED DATASET CLASS
# ============================================================
class MixedDeepfakeDataset(Dataset):
    """
    Custom dataset combining:
    1. Images (real/fake)
    2. Video frames (extracted)
    3. Synthetic images
    """
    
    def __init__(self, data_dir, temp_frames_dir=None, synthetic_dir=None, 
                 transform=None, include_synthetic=True):
        self.data_dir = Path(data_dir)
        self.temp_frames_dir = Path(temp_frames_dir) if temp_frames_dir else None
        self.synthetic_dir = Path(synthetic_dir) if synthetic_dir else None
        self.transform = transform
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
            for img_file in real_dir.glob('*.jpeg'):
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
            for img_file in fake_dir.glob('*.jpeg'):
                self.images.append(str(img_file))
                self.labels.append(1)
        
        # Load real video frames
        if self.temp_frames_dir and (self.temp_frames_dir / 'real').exists():
            for frame_file in (self.temp_frames_dir / 'real').glob('*.jpg'):
                self.images.append(str(frame_file))
                self.labels.append(0)
        
        # Load fake video frames
        if self.temp_frames_dir and (self.temp_frames_dir / 'fake').exists():
            for frame_file in (self.temp_frames_dir / 'fake').glob('*.jpg'):
                self.images.append(str(frame_file))
                self.labels.append(1)
        
        # Load synthetic images
        if include_synthetic and self.synthetic_dir:
            if (self.synthetic_dir / 'real').exists():
                for frame_file in (self.synthetic_dir / 'real').glob('*.jpg'):
                    self.images.append(str(frame_file))
                    self.labels.append(0)
            if (self.synthetic_dir / 'fake').exists():
                for frame_file in (self.synthetic_dir / 'fake').glob('*.jpg'):
                    self.images.append(str(frame_file))
                    self.labels.append(1)
        
        logger.info(f"✓ Dataset loaded: {len(self.images)} samples")
        real_count = self.labels.count(0)
        fake_count = self.labels.count(1)
        logger.info(f"  Real: {real_count} ({100*real_count/len(self.images):.1f}%)")
        logger.info(f"  Fake: {fake_count} ({100*fake_count/len(self.images):.1f}%)")
    
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
            logger.warning(f"Error loading {self.images[idx]}: {e}")
            # Return random valid sample
            valid_idx = np.random.randint(0, len(self.images))
            return self.__getitem__(valid_idx)

# ============================================================
# ADVANCED MODEL WITH DROPOUT & BATCH NORM
# ============================================================
class AdvancedDeepfakeDetector(nn.Module):
    """
    ResNet50 + Custom layers for better generalization
    Includes dropout and advanced pooling
    """
    
    def __init__(self, num_classes=2, dropout_rate=0.3):
        super(AdvancedDeepfakeDetector, self).__init__()
        
        # Load pretrained ResNet50
        self.resnet = models.resnet50(pretrained=True)
        
        # Freeze early layers for better transfer learning
        for param in self.resnet.layer1.parameters():
            param.requires_grad = False
        for param in self.resnet.layer2.parameters():
            param.requires_grad = False
        
        # Modify final layers with bottleneck
        num_features = self.resnet.fc.in_features
        
        # Add custom layers
        self.resnet.fc = nn.Sequential(
            nn.Linear(num_features, 512),
            nn.BatchNorm1d(512),
            nn.ReLU(),
            nn.Dropout(dropout_rate),
            nn.Linear(512, 256),
            nn.BatchNorm1d(256),
            nn.ReLU(),
            nn.Dropout(dropout_rate),
            nn.Linear(256, num_classes)
        )
    
    def forward(self, x):
        return self.resnet(x)

# ============================================================
# TRAINING LOOP
# ============================================================
def train_epoch(model, dataloader, criterion, optimizer, device, scaler=None):
    """Train for one epoch"""
    model.train()
    total_loss = 0
    correct = 0
    total = 0
    
    pbar = tqdm(dataloader, desc="Training")
    for images, labels in pbar:
        images, labels = images.to(device), labels.to(device)
        
        optimizer.zero_grad()
        
        # Forward pass
        outputs = model(images)
        loss = criterion(outputs, labels)
        
        # Backward pass
        loss.backward()
        optimizer.step()
        
        # Statistics
        total_loss += loss.item()
        _, predicted = outputs.max(1)
        correct += predicted.eq(labels).sum().item()
        total += labels.size(0)
        
        pbar.set_postfix({'loss': total_loss/(pbar.n+1), 'acc': 100*correct/total})
    
    return total_loss / len(dataloader), 100 * correct / total

def validate_epoch(model, dataloader, criterion, device):
    """Validate for one epoch"""
    model.eval()
    total_loss = 0
    correct = 0
    total = 0
    
    with torch.no_grad():
        pbar = tqdm(dataloader, desc="Validating")
        for images, labels in pbar:
            images, labels = images.to(device), labels.to(device)
            
            outputs = model(images)
            loss = criterion(outputs, labels)
            
            total_loss += loss.item()
            _, predicted = outputs.max(1)
            correct += predicted.eq(labels).sum().item()
            total += labels.size(0)
            
            pbar.set_postfix({'loss': total_loss/(pbar.n+1), 'acc': 100*correct/total})
    
    return total_loss / len(dataloader), 100 * correct / total

# ============================================================
# MAIN TRAINING FUNCTION
# ============================================================
def train_mixed_model(data_dir, epochs=50, batch_size=32, learning_rate=0.001, 
                      augment=True, include_synthetic=True, device=None):
    """
    Main training function for mixed dataset
    """
    
    if device is None:
        device = get_device()
    
    logger.info("\n" + "="*60)
    logger.info("🚀 ADVANCED MIXED TRAINING - 3 DATASET APPROACH")
    logger.info("="*60)
    
    # Prepare data
    logger.info("\n📊 Step 1: Preparing Datasets...")
    
    # Convert videos to frames
    temp_frames_dir = convert_videos_to_frames(data_dir, num_frames_per_video=8)
    
    # Generate synthetic data
    synthetic_dir = None
    if include_synthetic:
        synthetic_dir = Path(data_dir) / 'synthetic'
        (synthetic_dir / 'real').mkdir(parents=True, exist_ok=True)
        (synthetic_dir / 'fake').mkdir(parents=True, exist_ok=True)
        
        # Generate synthetic samples
        real_synthetic = generate_synthetic_faces(num_samples=50, 
                                                 save_dir=(synthetic_dir / 'real'))
        fake_synthetic = generate_synthetic_faces(num_samples=50, 
                                                 save_dir=(synthetic_dir / 'fake'))
    
    # Create dataset
    logger.info("\n📁 Step 2: Loading Dataset...")
    train_transform = get_train_transforms(augment=augment)
    val_transform = get_val_transforms()
    
    dataset = MixedDeepfakeDataset(
        data_dir=data_dir,
        temp_frames_dir=temp_frames_dir,
        synthetic_dir=synthetic_dir,
        transform=train_transform,
        include_synthetic=include_synthetic
    )
    
    # Split dataset
    if len(dataset) == 0:
        logger.error("❌ No training data found! Please add images/videos to data/real and data/fake")
        return None
    
    train_size = int(0.8 * len(dataset))
    val_size = len(dataset) - train_size
    train_dataset, val_dataset = random_split(dataset, [train_size, val_size])
    
    # Update val_dataset transform
    val_dataset.dataset.transform = val_transform
    
    # Create dataloaders
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, 
                             num_workers=0, pin_memory=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False, 
                           num_workers=0, pin_memory=True)
    
    logger.info(f"✓ Training samples: {len(train_dataset)}")
    logger.info(f"✓ Validation samples: {len(val_dataset)}")
    
    # Setup model
    logger.info("\n🧠 Step 3: Creating Model...")
    model = AdvancedDeepfakeDetector(num_classes=2, dropout_rate=0.3).to(device)
    logger.info(f"✓ Model created and moved to {device}")
    
    # Setup training
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate, weight_decay=1e-5)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='max', factor=0.5, 
                                                     patience=3, verbose=True)
    
    # Training loop
    logger.info(f"\n🎓 Step 4: Training (Epochs: {epochs}, Batch: {batch_size})...")
    logger.info("="*60)
    
    best_val_acc = 0
    best_model_path = "models/deepfake_detector_mixed.pth"
    Path("models").mkdir(exist_ok=True)
    
    history = {'train_loss': [], 'train_acc': [], 'val_loss': [], 'val_acc': []}
    
    for epoch in range(epochs):
        logger.info(f"\n📍 Epoch {epoch+1}/{epochs}")
        
        # Train
        train_loss, train_acc = train_epoch(model, train_loader, criterion, optimizer, device)
        
        # Validate
        val_loss, val_acc = validate_epoch(model, val_loader, criterion, device)
        
        # Record history
        history['train_loss'].append(train_loss)
        history['train_acc'].append(train_acc)
        history['val_loss'].append(val_loss)
        history['val_acc'].append(val_acc)
        
        logger.info(f"Train Loss: {train_loss:.4f} | Train Acc: {train_acc:.2f}%")
        logger.info(f"Val Loss: {val_loss:.4f} | Val Acc: {val_acc:.2f}%")
        
        # Save best model
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            torch.save(model.state_dict(), best_model_path)
            logger.info(f"✓ Best model saved (Acc: {val_acc:.2f}%)")
        
        # Scheduler step
        scheduler.step(val_acc)
    
    logger.info("\n" + "="*60)
    logger.info(f"✓ Training Complete!")
    logger.info(f"✓ Best Validation Accuracy: {best_val_acc:.2f}%")
    logger.info(f"✓ Model saved to: {best_model_path}")
    logger.info("="*60)
    
    # Plot results
    plot_training_history(history)
    
    # Save history
    with open("models/training_history.json", "w") as f:
        json.dump(history, f, indent=2)
    
    return model

# ============================================================
# PLOTTING
# ============================================================
def plot_training_history(history):
    """Plot training history"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Loss plot
    axes[0].plot(history['train_loss'], label='Train Loss', marker='o')
    axes[0].plot(history['val_loss'], label='Val Loss', marker='s')
    axes[0].set_xlabel('Epoch')
    axes[0].set_ylabel('Loss')
    axes[0].set_title('Training & Validation Loss')
    axes[0].legend()
    axes[0].grid(True)
    
    # Accuracy plot
    axes[1].plot(history['train_acc'], label='Train Acc', marker='o')
    axes[1].plot(history['val_acc'], label='Val Acc', marker='s')
    axes[1].set_xlabel('Epoch')
    axes[1].set_ylabel('Accuracy (%)')
    axes[1].set_title('Training & Validation Accuracy')
    axes[1].legend()
    axes[1].grid(True)
    
    plt.tight_layout()
    plt.savefig('models/training_history.png', dpi=150, bbox_inches='tight')
    logger.info("✓ Training plots saved to: models/training_history.png")
    plt.show()

# ============================================================
# CLI
# ============================================================
def main():
    parser = argparse.ArgumentParser(
        description='Advanced Mixed Training for Deepfake Detection',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python advanced_mixed_training.py --local-only --epochs 30
  python advanced_mixed_training.py --augment --epochs 50
  python advanced_mixed_training.py --full --epochs 100
        """
    )
    
    parser.add_argument('--data-dir', default='backend/data', help='Data directory')
    parser.add_argument('--epochs', type=int, default=30, help='Number of epochs')
    parser.add_argument('--batch-size', type=int, default=32, help='Batch size')
    parser.add_argument('--lr', type=float, default=0.001, help='Learning rate')
    parser.add_argument('--augment', action='store_true', default=True, help='Use data augmentation')
    parser.add_argument('--no-augment', dest='augment', action='store_false', help='Disable data augmentation')
    parser.add_argument('--synthetic', action='store_true', default=True, help='Include synthetic data')
    parser.add_argument('--no-synthetic', dest='synthetic', action='store_false', help='Disable synthetic data')
    parser.add_argument('--local-only', action='store_true', help='Quick local training')
    parser.add_argument('--full', action='store_true', help='Full training with all data')
    
    args = parser.parse_args()
    
    # Preset configurations
    if args.local_only:
        args.epochs = 30
        args.batch_size = 16
        logger.info("Using QUICK LOCAL training preset")
    elif args.full:
        args.epochs = 100
        args.batch_size = 32
        logger.info("Using FULL training preset")
    
    # Train
    device = get_device()
    model = train_mixed_model(
        data_dir=args.data_dir,
        epochs=args.epochs,
        batch_size=args.batch_size,
        learning_rate=args.lr,
        augment=args.augment,
        include_synthetic=args.synthetic,
        device=device
    )

if __name__ == '__main__':
    main()
