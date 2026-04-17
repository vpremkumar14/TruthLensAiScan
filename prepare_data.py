"""
Data Preparation Helper Script
Organize, validate, and prepare mixed datasets for training

Usage:
    python prepare_data.py --help
    python prepare_data.py --organize              # Organize existing files
    python prepare_data.py --validate              # Validate dataset
    python prepare_data.py --create-dummy          # Create dummy data for testing
    python prepare_data.py --balance               # Balance real/fake ratio
    python prepare_data.py --sample --count 50    # Create sample dataset
"""

import os
import shutil
import argparse
import json
from pathlib import Path
import numpy as np
from PIL import Image
import cv2
import logging
from tqdm import tqdm

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DatasetManager:
    """Manage deepfake dataset organization and preparation"""
    
    def __init__(self, root_dir='backend/data'):
        self.root_dir = Path(root_dir)
        self.root_dir.mkdir(parents=True, exist_ok=True)
        self.real_dir = self.root_dir / 'real'
        self.fake_dir = self.root_dir / 'fake'
        self.real_dir.mkdir(exist_ok=True)
        self.fake_dir.mkdir(exist_ok=True)
    
    def get_dataset_info(self):
        """Get current dataset statistics"""
        info = {
            'real': {'images': 0, 'videos': 0, 'total_files': 0},
            'fake': {'images': 0, 'videos': 0, 'total_files': 0},
            'total': 0
        }
        
        # Image extensions
        image_exts = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
        video_exts = {'.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv'}
        
        # Count real files
        for file in self.real_dir.iterdir():
            if file.is_file():
                info['real']['total_files'] += 1
                if file.suffix.lower() in image_exts:
                    info['real']['images'] += 1
                elif file.suffix.lower() in video_exts:
                    info['real']['videos'] += 1
        
        # Count fake files
        for file in self.fake_dir.iterdir():
            if file.is_file():
                info['fake']['total_files'] += 1
                if file.suffix.lower() in image_exts:
                    info['fake']['images'] += 1
                elif file.suffix.lower() in video_exts:
                    info['fake']['videos'] += 1
        
        info['total'] = info['real']['total_files'] + info['fake']['total_files']
        return info
    
    def print_dataset_info(self):
        """Print dataset statistics"""
        info = self.get_dataset_info()
        
        logger.info("\n" + "="*60)
        logger.info("📊 DATASET STATISTICS")
        logger.info("="*60)
        
        logger.info(f"\n✓ Real (Authentic) Content:")
        logger.info(f"  Images: {info['real']['images']}")
        logger.info(f"  Videos: {info['real']['videos']}")
        logger.info(f"  Total: {info['real']['total_files']}")
        
        logger.info(f"\n✗ Fake (Deepfake) Content:")
        logger.info(f"  Images: {info['fake']['images']}")
        logger.info(f"  Videos: {info['fake']['videos']}")
        logger.info(f"  Total: {info['fake']['total_files']}")
        
        logger.info(f"\n📈 Total Dataset Size: {info['total']} files")
        
        if info['total'] > 0:
            real_pct = 100 * info['real']['total_files'] / info['total']
            fake_pct = 100 * info['fake']['total_files'] / info['total']
            logger.info(f"  Real: {real_pct:.1f}% | Fake: {fake_pct:.1f}%")
        
        logger.info("="*60 + "\n")
        
        return info
    
    def validate_dataset(self):
        """Validate dataset - check file integrity"""
        logger.info("\n🔍 Validating Dataset...")
        
        issues = []
        
        # Check if directories exist
        if not self.real_dir.exists() or len(list(self.real_dir.iterdir())) == 0:
            issues.append("❌ No files in real/ directory")
        
        if not self.fake_dir.exists() or len(list(self.fake_dir.iterdir())) == 0:
            issues.append("❌ No files in fake/ directory")
        
        # Check image integrity
        for label, dir_path in [('real', self.real_dir), ('fake', self.fake_dir)]:
            for file in dir_path.iterdir():
                if file.suffix.lower() in {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}:
                    try:
                        img = Image.open(file)
                        img.verify()
                    except Exception as e:
                        issues.append(f"❌ Corrupted image: {file.name} ({e})")
                
                elif file.suffix.lower() in {'.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv'}:
                    try:
                        cap = cv2.VideoCapture(str(file))
                        if not cap.isOpened():
                            issues.append(f"❌ Invalid video: {file.name}")
                        else:
                            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                            if frame_count == 0:
                                issues.append(f"❌ Empty video: {file.name}")
                        cap.release()
                    except Exception as e:
                        issues.append(f"❌ Error reading video: {file.name} ({e})")
        
        # Check balance
        info = self.get_dataset_info()
        if info['total'] > 0:
            real_pct = 100 * info['real']['total_files'] / info['total']
            if real_pct < 30 or real_pct > 70:
                issues.append(f"⚠️  Imbalanced data: {real_pct:.1f}% real (target: ~50%)")
        
        # Report
        if issues:
            logger.warning(f"\n⚠️  Found {len(issues)} issues:")
            for issue in issues:
                logger.warning(f"  {issue}")
        else:
            logger.info("✓ Dataset validation passed!")
        
        return len(issues) == 0
    
    def create_dummy_dataset(self, num_real=20, num_fake=20):
        """Create dummy dataset for testing"""
        logger.info(f"\n🖼  Creating dummy dataset...")
        logger.info(f"   Real images: {num_real}, Fake images: {num_fake}")
        
        # Create real images (natural-looking)
        logger.info("\n  Creating real images...")
        for i in tqdm(range(num_real), desc="Real"):
            img = np.random.randint(50, 200, (224, 224, 3), dtype=np.uint8)
            # Add some structure
            for j in range(224):
                img[j, :, 0] = int(255 * (j / 224))
            Image.fromarray(img).save(self.real_dir / f"real_dummy_{i:03d}.jpg")
        
        # Create fake images (artificial-looking)
        logger.info("\n  Creating fake images...")
        for i in tqdm(range(num_fake), desc="Fake"):
            img = np.zeros((224, 224, 3), dtype=np.uint8)
            # Add artificial patterns
            for _ in range(50):
                pt1 = (np.random.randint(0, 224), np.random.randint(0, 224))
                pt2 = (np.random.randint(0, 224), np.random.randint(0, 224))
                color = (np.random.randint(0, 256), np.random.randint(0, 256), np.random.randint(0, 256))
                cv2.line(img, pt1, pt2, color, 2)
            Image.fromarray(img).save(self.fake_dir / f"fake_dummy_{i:03d}.jpg")
        
        logger.info(f"\n✓ Dummy dataset created!")
        self.print_dataset_info()
    
    def organize_files(self, source_dir=None):
        """Organize files from source directory into real/fake structure"""
        if not source_dir:
            logger.error("❌ Please provide source directory: --source-dir /path/to/files")
            return
        
        source_dir = Path(source_dir)
        if not source_dir.exists():
            logger.error(f"❌ Source directory not found: {source_dir}")
            return
        
        logger.info(f"\n📁 Organizing files from: {source_dir}")
        logger.info("   Scan files with 'real' or 'deepfake' in filename...")
        
        organized = {'real': 0, 'fake': 0}
        
        for file in tqdm(source_dir.rglob('*'), desc="Organizing"):
            if not file.is_file():
                continue
            
            filename_lower = file.name.lower()
            
            # Skip if not media file
            if not any(filename_lower.endswith(ext) for ext in 
                      ['.jpg', '.png', '.jpeg', '.mp4', '.avi', '.mov', '.gif', '.mkv']):
                continue
            
            # Detect label from filename
            if 'real' in filename_lower or 'authentic' in filename_lower or 'genuine' in filename_lower:
                dest = self.real_dir / file.name
                organized['real'] += 1
            elif 'fake' in filename_lower or 'deepfake' in filename_lower or 'ai_' in filename_lower:
                dest = self.fake_dir / file.name
                organized['fake'] += 1
            else:
                # Ask user
                logger.warning(f"   Unsure about: {file.name}")
                continue
            
            # Copy file
            try:
                shutil.copy2(file, dest)
            except Exception as e:
                logger.warning(f"   Error copying {file.name}: {e}")
        
        logger.info(f"\n✓ Organization complete!")
        logger.info(f"  Copied to real/: {organized['real']} files")
        logger.info(f"  Copied to fake/: {organized['fake']} files")
    
    def balance_dataset(self, target_ratio=0.5):
        """Balance real/fake ratio"""
        info = self.get_dataset_info()
        
        real_count = info['real']['total_files']
        fake_count = info['fake']['total_files']
        total = real_count + fake_count
        
        if total == 0:
            logger.error("❌ No files in dataset")
            return
        
        logger.info(f"\n⚖️  Balancing dataset...")
        logger.info(f"   Current: {real_count} real, {fake_count} fake")
        
        # Determine which class is larger
        if real_count > fake_count:
            # Remove some real files
            target = int(fake_count / target_ratio) if fake_count > 0 else 0
            to_remove = max(0, real_count - target)
            if to_remove > 0:
                logger.info(f"   Removing {to_remove} real files...")
                files_to_remove = list(self.real_dir.glob('*'))[:to_remove]
                for file in tqdm(files_to_remove, desc="Removing"):
                    file.unlink()
        
        else:
            # Remove some fake files
            target = int(real_count * target_ratio)
            to_remove = max(0, fake_count - target)
            if to_remove > 0:
                logger.info(f"   Removing {to_remove} fake files...")
                files_to_remove = list(self.fake_dir.glob('*'))[:to_remove]
                for file in tqdm(files_to_remove, desc="Removing"):
                    file.unlink()
        
        self.print_dataset_info()
    
    def create_sample_dataset(self, size=50):
        """Create a small sample dataset"""
        logger.info(f"\n📦 Creating {size}-sample dataset...")
        
        real_count = min(size // 2, len(list(self.real_dir.glob('*'))))
        fake_count = min(size // 2, len(list(self.fake_dir.glob('*'))))
        
        logger.info(f"   Real samples: {real_count}")
        logger.info(f"   Fake samples: {fake_count}")
        
        # Create sample directory
        sample_dir = self.root_dir / 'sample'
        (sample_dir / 'real').mkdir(parents=True, exist_ok=True)
        (sample_dir / 'fake').mkdir(parents=True, exist_ok=True)
        
        # Copy random samples
        real_files = list(self.real_dir.glob('*'))
        fake_files = list(self.fake_dir.glob('*'))
        
        for file in tqdm(np.random.choice(real_files, real_count, replace=False), desc="Real"):
            shutil.copy2(file, sample_dir / 'real' / file.name)
        
        for file in tqdm(np.random.choice(fake_files, fake_count, replace=False), desc="Fake"):
            shutil.copy2(file, sample_dir / 'fake' / file.name)
        
        logger.info(f"✓ Sample dataset created in: {sample_dir}")

# ============================================================
# MAIN
# ============================================================
def main():
    parser = argparse.ArgumentParser(
        description='Data Preparation Helper for Deepfake Detection',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python prepare_data.py --info                    # Show dataset stats
  python prepare_data.py --validate                # Validate dataset
  python prepare_data.py --create-dummy            # Create test data
  python prepare_data.py --balance                 # Balance real/fake
  python prepare_data.py --organize --source-dir . # Organize existing files
  python prepare_data.py --sample --count 50       # Create 50-sample subset
        """
    )
    
    parser.add_argument('--data-dir', default='backend/data', help='Data directory')
    parser.add_argument('--info', action='store_true', help='Show dataset info')
    parser.add_argument('--validate', action='store_true', help='Validate dataset')
    parser.add_argument('--create-dummy', action='store_true', help='Create dummy dataset')
    parser.add_argument('--organize', action='store_true', help='Organize existing files')
    parser.add_argument('--balance', action='store_true', help='Balance real/fake ratio')
    parser.add_argument('--sample', action='store_true', help='Create sample dataset')
    parser.add_argument('--source-dir', help='Source directory for organization')
    parser.add_argument('--count', type=int, default=50, help='Number of samples (for --sample)')
    
    args = parser.parse_args()
    
    # Initialize manager
    manager = DatasetManager(args.data_dir)
    
    # Execute commands
    if args.info:
        manager.print_dataset_info()
    
    elif args.validate:
        manager.validate_dataset()
    
    elif args.create_dummy:
        manager.create_dummy_dataset()
        manager.print_dataset_info()
    
    elif args.organize:
        manager.organize_files(args.source_dir)
    
    elif args.balance:
        manager.balance_dataset()
    
    elif args.sample:
        manager.create_sample_dataset(args.count)
    
    else:
        # Default: show info
        manager.print_dataset_info()
        manager.validate_dataset()

if __name__ == '__main__':
    main()
