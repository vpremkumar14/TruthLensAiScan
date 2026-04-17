#!/usr/bin/env python3
"""
🚀 QUICK START - Mixed Model Training Setup
Interactive guide for training your deepfake detection model

Run: python quickstart_train.py
"""

import os
import subprocess
import sys
from pathlib import Path

class Colors:
    """ANSI color codes"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    """Print section header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")

def print_success(text):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")

def print_error(text):
    """Print error message"""
    print(f"{Colors.RED}✗ {text}{Colors.END}")

def print_info(text):
    """Print info message"""
    print(f"{Colors.CYAN}ℹ {text}{Colors.END}")

def print_option(num, text, details=""):
    """Print option"""
    if details:
        print(f"{Colors.YELLOW}[{num}]{Colors.END} {text}")
        print(f"    {Colors.CYAN}{details}{Colors.END}")
    else:
        print(f"{Colors.YELLOW}[{num}]{Colors.END} {text}")

def check_dependencies():
    """Check if required packages are installed"""
    print_header("📋 Checking Dependencies")
    
    required = {
        'torch': 'PyTorch (Deep Learning)',
        'torchvision': 'Torchvision (Vision Models)',
        'cv2': 'OpenCV (Video Processing)',
        'PIL': 'Pillow (Image Processing)',
        'numpy': 'NumPy (Numerical Computing)',
        'tqdm': 'tqdm (Progress Bars)'
    }
    
    missing = []
    for module, name in required.items():
        try:
            __import__(module)
            print_success(f"{name} installed")
        except ImportError:
            print_error(f"{name} NOT installed")
            missing.append(module)
    
    if missing:
        print_info("Install missing packages with:")
        print(f"  pip install {' '.join(missing)}")
        return False
    
    return True

def check_data():
    """Check current data status"""
    print_header("📊 Checking Dataset")
    
    data_dir = Path('backend/data')
    real_dir = data_dir / 'real'
    fake_dir = data_dir / 'fake'
    
    real_count = len(list(real_dir.glob('*'))) if real_dir.exists() else 0
    fake_count = len(list(fake_dir.glob('*'))) if fake_dir.exists() else 0
    
    print(f"Real directory: {Colors.CYAN}{real_count} files{Colors.END}")
    print(f"Fake directory: {Colors.CYAN}{fake_count} files{Colors.END}")
    print(f"Total: {Colors.CYAN}{real_count + fake_count} files{Colors.END}")
    
    if real_count + fake_count == 0:
        print_error("No data found!")
        return False
    elif real_count + fake_count < 10:
        print_info("Limited data - will use synthetic augmentation")
    else:
        print_success("Good amount of data")
    
    return True

def choose_scenario():
    """Let user choose training scenario"""
    print_header("🎯 Choose Training Scenario")
    
    print_option(1, "Quick Test (5-10 min)", 
                "Uses synthetic data only - great for setup verification")
    print_option(2, "Quick Training (15-30 min)",
                "Your images + synthetic augmentation - good for initial training")
    print_option(3, "Standard Training (30-60 min)",
                "Full training with videos - recommended for production")
    print_option(4, "Extended Training (1-2+ hours)",
                "Multiple passes, best accuracy - for large datasets")
    print_option(5, "Custom Configuration",
                "Specify your own parameters")
    
    while True:
        choice = input(f"\n{Colors.YELLOW}Choose scenario (1-5): {Colors.END}").strip()
        if choice in ['1', '2', '3', '4', '5']:
            return choice
        print_error("Invalid choice. Please enter 1-5")

def get_training_params(scenario):
    """Get training parameters based on scenario"""
    params = {
        '1': {
            'name': 'Quick Test',
            'epochs': 30,
            'batch_size': 16,
            'augment': True,
            'synthetic': True,
        },
        '2': {
            'name': 'Quick Training',
            'epochs': 50,
            'batch_size': 32,
            'augment': True,
            'synthetic': True,
        },
        '3': {
            'name': 'Standard Training',
            'epochs': 100,
            'batch_size': 32,
            'augment': True,
            'synthetic': True,
        },
        '4': {
            'name': 'Extended Training',
            'epochs': 150,
            'batch_size': 32,
            'augment': True,
            'synthetic': True,
        },
    }
    
    if scenario == '5':
        print_header("⚙️  Custom Configuration")
        epochs = int(input(f"Epochs (default 50): ") or "50")
        batch = int(input(f"Batch size (default 32): ") or "32")
        lr = float(input(f"Learning rate (default 0.001): ") or "0.001")
        return {
            'name': 'Custom',
            'epochs': epochs,
            'batch_size': batch,
            'lr': lr,
            'augment': True,
            'synthetic': True,
        }
    
    return params[scenario]

def prepare_data_prompt():
    """Ask user if they want to prepare data first"""
    print_header("📁 Data Preparation")
    
    print_option(1, "Use synthetic data (no files needed)",
                "Creates artificial training data automatically")
    print_option(2, "Create dummy dataset for testing",
                "Generates 40 dummy images for quick testing")
    print_option(3, "Validate existing dataset",
                "Check if your data is organized correctly")
    print_option(4, "Skip - I'll add data manually",
                "Continue to training")
    
    choice = input(f"\n{Colors.YELLOW}Choose (1-4): {Colors.END}").strip()
    
    if choice == '1':
        return None
    elif choice == '2':
        subprocess.run([sys.executable, 'prepare_data.py', '--create-dummy'])
        return None
    elif choice == '3':
        subprocess.run([sys.executable, 'prepare_data.py', '--validate'])
        return None
    
    return None

def display_training_summary(params):
    """Display training configuration"""
    print_header("📊 Training Configuration")
    
    print(f"Scenario: {Colors.CYAN}{params['name']}{Colors.END}")
    print(f"Epochs: {Colors.CYAN}{params['epochs']}{Colors.END}")
    print(f"Batch Size: {Colors.CYAN}{params['batch_size']}{Colors.END}")
    print(f"Learning Rate: {Colors.CYAN}{params.get('lr', 0.001)}{Colors.END}")
    print(f"Augmentation: {Colors.CYAN}{'Yes' if params['augment'] else 'No'}{Colors.END}")
    print(f"Synthetic Data: {Colors.CYAN}{'Yes' if params['synthetic'] else 'No'}{Colors.END}")

def run_training(params):
    """Run the training script"""
    print_header("🚀 Starting Training")
    
    cmd = [
        sys.executable,
        'advanced_mixed_training.py',
        '--epochs', str(params['epochs']),
        '--batch-size', str(params['batch_size']),
    ]
    
    if not params['augment']:
        cmd.append('--no-augment')
    
    if not params['synthetic']:
        cmd.append('--no-synthetic')
    
    if 'lr' in params:
        cmd.extend(['--lr', str(params['lr'])])
    
    print_info("Training command:")
    print(f"{Colors.CYAN}{' '.join(cmd)}{Colors.END}\n")
    
    print_info("Training started... This may take a while.")
    print_info("Watch for accuracy improvements and model checkpoints.\n")
    
    try:
        result = subprocess.run(cmd, check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print_error(f"Training failed: {e}")
        return False

def show_next_steps():
    """Show what to do after training"""
    print_header("✅ Training Complete!")
    
    print_success("Your model has been trained and saved!")
    print(f"\nModel location: {Colors.CYAN}models/deepfake_detector_mixed.pth{Colors.END}")
    print(f"Training history: {Colors.CYAN}models/training_history.json{Colors.END}")
    print(f"Accuracy plot: {Colors.CYAN}models/training_history.png{Colors.END}")
    
    print_info("\n📊 Training Results:")
    print("  Check models/training_history.png for accuracy/loss curves")
    print("  Higher accuracy = better model")
    
    print_info("\n🎬 Next Steps:")
    print_option(1, "Test the model on new images",
                "python backend/test_api.py")
    print_option(2, "Deploy to production",
                "Update backend/app.py model path")
    print_option(3, "Retrain with more data",
                "Add more images/videos and run again")
    print_option(4, "Use in your app",
                "The model is ready for inference!")
    
    print_info("\n💡 Tips:")
    print("  • Add more images/videos for better accuracy")
    print("  • Mix real images, real videos, and deepfake videos")
    print("  • Train for longer (100+ epochs) for best results")
    print("  • Use data augmentation for limited data")

def main():
    """Main quickstart flow"""
    print(f"{Colors.BOLD}{Colors.BLUE}")
    print("""
╔══════════════════════════════════════════════════════════╗
║  🚀 TRUTHLENS - MIXED MODEL TRAINING QUICKSTART 🚀      ║
║                                                          ║
║  Train a powerful deepfake detector with 3 datasets     ║
║  Images + Videos + Synthetic Data = Best Accuracy ✨    ║
╚══════════════════════════════════════════════════════════╝
    """)
    print(Colors.END)
    
    # Step 1: Check dependencies
    if not check_dependencies():
        print_error("Please install missing packages and run again")
        sys.exit(1)
    
    # Step 2: Check data
    has_data = check_data()
    
    # Step 3: Prepare data if needed
    if not has_data or input(f"\n{Colors.YELLOW}Prepare/validate data? (y/n): {Colors.END}").lower() == 'y':
        prepare_data_prompt()
    
    # Step 4: Choose scenario
    scenario = choose_scenario()
    params = get_training_params(scenario)
    
    # Step 5: Display summary
    display_training_summary(params)
    
    # Step 6: Confirm and start
    confirm = input(f"\n{Colors.YELLOW}Start training? (y/n): {Colors.END}").strip().lower()
    if confirm != 'y':
        print_info("Training cancelled")
        sys.exit(0)
    
    # Step 7: Run training
    success = run_training(params)
    
    # Step 8: Show next steps
    if success:
        show_next_steps()
    else:
        print_error("Training failed. Check error messages above.")

if __name__ == '__main__':
    main()
