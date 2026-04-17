# 🚀 Google Colab Model Training Guide

## Complete Step-by-Step Instructions

### **Prerequisites:**
- Google account (free)
- Internet connection
- Real and fake images (50+ each)

---

## **OPTION 1: Using Google Colab (RECOMMENDED) ⭐**

### **Step 1: Open Google Colab**

1. Go to [Google Colab](https://colab.research.google.com)
2. Click **"New Notebook"**

### **Step 2: Upload Training Script**

In the first cell, run:

```python
# Download the training script
import urllib.request
urllib.request.urlretrieve(
    'https://raw.githubusercontent.com/your-repo/colab_training.py',
    'colab_training.py'
)

# Or paste the full code directly in a cell
```

### **Step 3: Upload Your Dataset**

**Option A: Upload Folders in Colab UI**

1. Click folder icon (left sidebar)
2. Click **"Upload to session"**
3. Create this structure:
   ```
   /content/
   └── dataset/
       ├── real/   (50+ authentic images)
       └── fake/   (50+ AI-generated images)
   ```

**Option B: Mount Google Drive**

```python
from google.colab import drive
drive.mount('/content/drive')

# If images are in Drive:
import shutil
shutil.copytree('/content/drive/My Drive/dataset', '/content/dataset')
```

### **Step 4: Run Training**

Create a new cell and paste the full `colab_training.py` code, then run:

```python
%time main()
```

This will:
- ✅ Check GPU availability
- ✅ Load and process images
- ✅ Train ResNet50 for 20 epochs
- ✅ Save best model automatically

### **Step 5: Download Trained Model**

After training completes:

1. In left sidebar, click folder icon
2. Find and download:
   - `deepfake_detector_best.pth` ⭐ (Use this one!)
   - `training_history.json`
   - `training_results.png`

### **Step 6: Use Model Locally**

Copy downloaded `.pth` file to:
```
backend/models/deepfake_detector.pth
```

Restart backend:
```bash
python app.py
```

---

## **OPTION 2: Kaggle Notebooks (Free GPU)**

### **Step 1: Create Kaggle Account**
- Go to [Kaggle.com](https://kaggle.com)
- Sign up (free)

### **Step 2: Find Datasets**

Search and add these datasets to notebook:
- **FaceForensics++** (best quality)
- **DFDC - Deepfake Detection Challenge**
- **CelebDF** (smallest)

### **Step 3: Create New Notebook**

1. Click **Create → Notebook**
2. Add dataset (search for above)
3. Paste `colab_training.py` code
4. Run cells

### **Step 4: Download Model**

After training, output files appear in sidebar.

---

## **OPTION 3: Local Training (If You Have GPU)**

If you have NVIDIA GPU locally:

```bash
cd backend
venv\Scripts\activate
python train_model.py --epochs 20 --batch-size 16
```

**Required disk space:** 
- Small dataset: ~2GB
- Medium: ~50GB
- FaceForensics++: ~500GB

---

## **⚡ Quick Training Tips**

### **For Fast Training (5-10 minutes):**
- Use **50-100 images** per class
- Set `--epochs 10`
- Set `--batch-size 32`

```python
# In colab_training.py, modify:
BATCH_SIZE = 32
EPOCHS = 10
```

### **For Best Accuracy (1-2 hours):**
- Use **1000+ images** per class
- Set `--epochs 50`
- Set `--batch-size 16`

```python
BATCH_SIZE = 16
EPOCHS = 50
```

### **GPU Performance:**
- **Colab T4 GPU:** ~30 min for 50 epochs
- **Kaggle P100 GPU:** ~15 min for 50 epochs
- **Local RTX 3090:** ~5 min for 50 epochs

---

## **📊 Expected Results**

After training:

```
Epoch 1/20
Train Loss: 0.6532 | Train Acc: 58.23%
Val Loss: 0.5284 | Val Acc: 72.15%

Epoch 5/20
Train Loss: 0.2134 | Train Acc: 91.45%
Val Loss: 0.2891 | Val Acc: 88.32%

Epoch 20/20
Train Loss: 0.0892 | Train Acc: 96.78%
Val Loss: 0.1456 | Val Acc: 92.47%
```

You should see:
- ✅ Train accuracy increases
- ✅ Validation accuracy follows
- ✅ Loss decreases smoothly

---

## **🐛 Troubleshooting**

### **"No images found!"**
- Check folder structure is exactly: `dataset/real/` and `dataset/fake/`
- Images must be `.jpg` or `.png`
- Need at least 1 image per class

### **"Out of Memory"**
- Reduce `BATCH_SIZE` to 16 or 8
- Use fewer images
- Clear Colab cache: Runtime → Factory Reset

### **"Training is very slow"**
- You're on CPU, not GPU
- In Colab: Runtime → Change runtime type → GPU
- Should see "GPU: NVIDIA T4" at top

### **"Model accuracy is 50%"**
- Need more training data
- Add 100+ images per class
- Increase epochs to 50
- Dataset might be too easy/hard

---

## **📂 File Structure After Training**

Your downloads should include:

```
├── deepfake_detector_best.pth      ← Use this!
├── deepfake_detector_final.pth
├── training_history.json           (metrics data)
└── training_results.png            (accuracy/loss graphs)
```

---

## **✅ Final Steps**

1. **Download** `deepfake_detector_best.pth`
2. **Place** in `backend/models/` folder
3. **Restart** Flask: `python app.py`
4. **Upload** test images via web UI
5. **Check** improved accuracy! 🎉

---

## **💡 Pro Tips**

1. **Use data augmentation** in Colab script (already included)
2. **Monitor validation loss** - if it increases, model is overfitting
3. **Save multiple checkpoints** to compare performance
4. **Use GPU TPU** in Colab for 2x speed boost
5. **Create dataset with diverse lighting** for better generalization

---

## **🎯 Next Steps**

After successful training:

1. ✅ Deploy to production
2. ✅ Test with real videos
3. ✅ Integrate with other deepfake detection tools
4. ✅ Fine-tune for specific use cases
5. ✅ Consider model ensemble for higher accuracy

---

**Questions?** Check [training script comments](colab_training.py) for details.
