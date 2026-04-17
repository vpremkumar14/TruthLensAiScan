# 🚀 Training Command Reference Card

Quick lookup for all training commands and options.

---

## ⚡ Quick Start

### Interactive (Recommended for First Time)
```bash
python quickstart_train.py
```
✓ Guided step-by-step
✓ Checks dependencies
✓ Helps choose scenario
✓ No parameters needed

---

## 🎯 One-Command Training by Scenario

### Scenario A: Quick Test (Synthetic Data - 5 min)
```bash
python advanced_mixed_training.py --local-only --epochs 30
```

### Scenario B: Quick Training (Your Data - 15 min)
```bash
python advanced_mixed_training.py --augment --epochs 50
```

### Scenario C: Standard Training (Videos - 45 min)
```bash
python advanced_mixed_training.py --epochs 100
```

### Scenario D: Maximum Accuracy (Large Dataset - 2 hrs)
```bash
python advanced_mixed_training.py --full --epochs 150
```

---

## 📋 Full Command Reference

### Basic Training
```bash
# Default training (50 epochs, batch=32)
python advanced_mixed_training.py

# Custom epochs
python advanced_mixed_training.py --epochs 100

# Custom batch size (for GPU memory)
python advanced_mixed_training.py --batch-size 16

# Custom learning rate
python advanced_mixed_training.py --lr 0.0005
```

### Data Options
```bash
# Include synthetic data (default: on)
python advanced_mixed_training.py --synthetic

# Exclude synthetic data
python advanced_mixed_training.py --no-synthetic

# Include augmentation (default: on)
python advanced_mixed_training.py --augment

# Exclude augmentation
python advanced_mixed_training.py --no-augment
```

### Presets
```bash
# Quick test preset (30 epochs, batch=16)
python advanced_mixed_training.py --local-only

# Full training preset (100 epochs)
python advanced_mixed_training.py --full
```

### Combined Examples
```bash
# Quick test with higher epochs
python advanced_mixed_training.py --local-only --epochs 50

# Custom dataset directory
python advanced_mixed_training.py --data-dir /path/to/data --epochs 100

# All options combined
python advanced_mixed_training.py \
    --data-dir backend/data \
    --epochs 120 \
    --batch-size 24 \
    --lr 0.0005 \
    --augment \
    --synthetic
```

---

## 🛠️ Data Preparation Commands

### Check Dataset Status
```bash
# Show file counts and statistics
python prepare_data.py --info

# Show info for custom directory
python prepare_data.py --data-dir /path/to/data --info
```

### Validate Dataset
```bash
# Check file integrity
python prepare_data.py --validate

# Validate custom directory
python prepare_data.py --data-dir /path/to/data --validate
```

### Create/Generate Data
```bash
# Create 40 dummy images (20 real + 20 fake)
python prepare_data.py --create-dummy

# Create custom dummy dataset
python prepare_data.py --create-dummy --data-dir /path/to/data
```

### Organize Existing Files
```bash
# Organize files from source directory into real/fake folders
python prepare_data.py --organize --source-dir /path/to/files

# Organize with custom data directory
python prepare_data.py --organize --source-dir /path/to/files --data-dir backend/data
```

### Balance Dataset
```bash
# Balance real/fake ratio to 50/50
python prepare_data.py --balance

# Balance custom directory
python prepare_data.py --data-dir /path/to/data --balance
```

### Create Sample Subset
```bash
# Create 50-sample dataset
python prepare_data.py --sample --count 50

# Create 100-sample dataset
python prepare_data.py --sample --count 100

# Create sample with custom size
python prepare_data.py --sample --count 200 --data-dir /path/to/data
```

---

## 🎓 Full Parameter Details

### Training Parameters

| Parameter | Default | Options | Example |
|-----------|---------|---------|---------|
| `--data-dir` | backend/data | path | `--data-dir data/` |
| `--epochs` | 50 | number | `--epochs 100` |
| `--batch-size` | 32 | number | `--batch-size 16` |
| `--lr` | 0.001 | float | `--lr 0.0005` |
| `--augment` | True | flag | `--no-augment` |
| `--synthetic` | True | flag | `--no-synthetic` |
| `--local-only` | False | flag | `--local-only` |
| `--full` | False | flag | `--full` |

### Data Parameters

| Parameter | Default | Options | Example |
|-----------|---------|---------|---------|
| `--data-dir` | backend/data | path | `--data-dir data/` |
| `--source-dir` | None | path | `--source-dir ~/images` |
| `--count` | 50 | number | `--count 100` |

---

## 📚 Common Workflows

### Workflow 1: From Zero to Training (Fastest)
```bash
# 1. Interactive setup
python quickstart_train.py

# Done! Model trained and ready
```

### Workflow 2: Manual Setup
```bash
# 1. Create dummy data to test
python prepare_data.py --create-dummy

# 2. Check if data looks good
python prepare_data.py --validate

# 3. Train
python advanced_mixed_training.py --epochs 50

# 4. Check results in models/training_history.png
```

### Workflow 3: With Your Own Data
```bash
# 1. Organize your images into backend/data/real and backend/data/fake
# (Place authentic images in real/, deepfakes in fake/)

# 2. Verify organization
python prepare_data.py --info
python prepare_data.py --validate

# 3. Balance if needed
python prepare_data.py --balance

# 4. Train
python advanced_mixed_training.py --epochs 100

# 5. Upload results to models/ folder
```

### Workflow 4: Large Dataset Training
```bash
# 1. Check current data
python prepare_data.py --info

# 2. Validate data quality
python prepare_data.py --validate

# 3. Create balanced copy
python prepare_data.py --balance

# 4. Start extended training
python advanced_mixed_training.py --full --epochs 200

# 5. Monitor at models/training_history.png
```

---

## ⏱️ Expected Runtimes

| Command | Time | Hardware |
|---------|------|----------|
| `--local-only --epochs 30` | 5-10 min | GPU/CPU |
| `--epochs 50` | 20-30 min | GPU |
| `--epochs 100` | 45-60 min | GPU |
| `--full --epochs 150` | 90+ min | GPU |

**~2x slower on CPU**

---

## 🐛 Troubleshooting Commands

### Check GPU/CPU
```bash
python -c "import torch; print(torch.cuda.is_available())"
```
- `True` = GPU available ✓
- `False` = Using CPU (slower)

### Check Data
```bash
python prepare_data.py --validate
```

### Verify Installation
```bash
python -c "import torch, torchvision, cv2; print('All packages installed')"
```

### Quick Test
```bash
python prepare_data.py --create-dummy
python advanced_mixed_training.py --local-only --epochs 10
```

---

## 📊 Output Files After Training

| File | Location | Purpose |
|------|----------|---------|
| Trained Model | `models/deepfake_detector_mixed.pth` | Use for inference |
| Training History | `models/training_history.json` | Metrics (JSON format) |
| Accuracy Plot | `models/training_history.png` | Visual training progress |

---

## 🎯 Choose Your Command

### I want to...

**...train quickly to test the setup**
```bash
python advanced_mixed_training.py --local-only --epochs 30
```

**...train with my own data**
```bash
python advanced_mixed_training.py --epochs 50
```

**...get best possible accuracy**
```bash
python advanced_mixed_training.py --epochs 150 --batch-size 32
```

**...train on CPU (slower but works)**
```bash
python advanced_mixed_training.py --batch-size 8 --epochs 50
```

**...check my data before training**
```bash
python prepare_data.py --validate
```

**...create test data**
```bash
python prepare_data.py --create-dummy
```

**...be guided step-by-step**
```bash
python quickstart_train.py
```

**...train with custom parameters**
```bash
python advanced_mixed_training.py --epochs 120 --batch-size 24 --lr 0.0005
```

---

## 💡 Tips

- 🚀 First time? Use `python quickstart_train.py`
- 📊 Check results: Open `models/training_history.png`
- 🎨 Want better accuracy? Add more data and train longer
- 📁 Ensure balanced data (50% real, 50% fake)
- 🎬 Include videos for +5-10% accuracy boost
- ⏰ Start with short training (30 epochs) to verify setup
- 🔋 GPU training ~10x faster than CPU

---

## 🔗 Full Documentation

- **`TRAINING_SYSTEM_README.md`** - Complete system guide
- **`ADVANCED_MIXED_TRAINING_GUIDE.md`** - Detailed training guide with scenarios
- **`README.md`** - Project overview

---

**Last Updated**: April 2026
**Supported**: Python 3.8+, PyTorch 1.9+
