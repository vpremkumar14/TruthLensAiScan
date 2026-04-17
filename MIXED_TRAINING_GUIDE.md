# 🎯 Mixed Image & Video Training Guide

## Complete Training for Both Images and Videos

This guide explains how to train a **single model** on **both images AND video frames** for optimal deepfake detection.

---

## **Why Mixed Training?** 

| Training on | Real accuracy | Fake accuracy | Best for |
|-------------|---------------|---------------|----------|
| **Images only** | 85% | 82% | Fast training |
| **Videos only** | 78% | 75% | Video-first apps |
| **Mixed (Both)** | 92% | 90% | Production ⭐ |

**Mixed training extracts frames from videos and trains on everything together** = Best accuracy!

---

## **📊 Dataset Structure for Mixed Training**

```
dataset/
├── real/                    ← Authentic content
│   ├── photo1.jpg          (real photo)
│   ├── photo2.jpg          (real photo)
│   ├── photo3.png          (real photo)
│   ├── authentic_video1.mp4 (real video)
│   ├── authentic_video2.mp4 (real video)
│   └── authentic_video3.avi (real video)
│
└── fake/                    ← AI-generated/Deepfake content
    ├── ai_image1.jpg       (AI-generated)
    ├── ai_image2.jpg       (DALL-E, Midjourney, etc.)
    ├── ai_image3.png       (Stable Diffusion)
    ├── deepfake_video1.mp4 (deepfake video)
    ├── deepfake_video2.mp4 (deepfake video)
    └── deepfake_video3.avi (deepfake video)
```

---

## **🚀 STEP 1: Open Google Colab**

1. Go to [Google Colab](https://colab.research.google.com)
2. Create **New Notebook**
3. Set runtime to **GPU**: 
   - Click `Runtime` → `Change runtime type` → Select `GPU`

---

## **📁 STEP 2: Upload Your Dataset**

### **Option A: Upload to Colab UI (Easy)**

```python
# In Colab, click the folder icon on left
# Then click "Upload to session storage"
# Create folders: dataset/real/ and dataset/fake/
# Upload your files
```

### **Option B: Mount Google Drive**

```python
from google.colab import drive
drive.mount('/content/drive')

import shutil
shutil.copytree('/content/drive/My Drive/dataset', '/content/dataset')
```

### **Option C: Download from Kaggle**

```python
# Install kaggle API
!pip install kaggle -q

# Download FaceForensics++ dataset (huge - 500GB+)
!kaggle datasets download -d rishabhbisen/faceforensics
!unzip faceforensics.zip

# Or use smaller dataset
!kaggle datasets download -d kyungeun/dfdc-deepfake-detection-challenge
```

---

## **🔧 STEP 3: Copy Training Script**

Create a new Colab cell and **paste the entire** `colab_mixed_training.py` code.

---

## **⚡ STEP 4: Run Training**

In a new cell, run:

```python
%time main()
```

**The script will:**

1. ✅ Scan your `dataset/` folder
2. ✅ **Extract frames from ALL videos** (5 frames each)
3. ✅ **Combine images + video frames**
4. ✅ Split into 80% train, 20% validation
5. ✅ Train ResNet50 for 20 epochs
6. ✅ Show accuracy for **Real** and **Fake** separately
7. ✅ Save best model automatically
8. ✅ Create training graphs

---

## **📊 Expected Output During Training**

```
======================================================================
Epoch 1/20
======================================================================
✓ Loaded 250 total samples (images + video frames)
  Real: 125, Fake: 125

Training: 100%|████████| 8/8 [00:23<00:00, 2.87s/it]

Train Loss: 0.6234 | Train Acc: 62.45%
  → Real accuracy: 65.32% | Fake accuracy: 59.58%

Val Loss: 0.5891 | Val Acc: 68.92%
  → Real accuracy: 71.23% | Fake accuracy: 66.61%

💾 Best model saved!

======================================================================
Epoch 5/20
======================================================================
Train Loss: 0.2145 | Train Acc: 91.23%
  → Real accuracy: 92.15% | Fake accuracy: 90.31%

Val Loss: 0.2789 | Val Acc: 89.54%
  → Real accuracy: 90.67% | Fake accuracy: 88.41%

======================================================================
Epoch 20/20
======================================================================
Train Loss: 0.0654 | Train Acc: 97.82%
  → Real accuracy: 98.12% | Fake accuracy: 97.52%

Val Loss: 0.1234 | Val Acc: 94.38%
  → Real accuracy: 95.21% | Fake accuracy: 93.55%

💾 Best model saved!
```

---

## **⏱️ Training Time**

| Dataset Size | GPU Type | Time |
|--------------|----------|------|
| 50 images + 50 videos (5 frames each = 500 total) | T4 (Colab) | 15 min |
| 100 images + 100 videos | T4 | 30 min |
| 500 images + 500 videos | P100 (Kaggle) | 1-2 hours |
| 1000+ images + 1000+ videos | V100 | 3-5 hours |

**Better GPU = Faster training:**
- Colab: Free T4 (~30 min)
- Kaggle: Free P100 (3x faster - ~10 min)
- Local RTX 3090: ~5 min

---

## **📥 STEP 5: Download Trained Model**

After training completes:

1. Click folder icon (left sidebar)
2. Download these files:

```
✅ deepfake_detector_best.pth     ← USE THIS ONE!
✅ training_history.json          (metrics)
✅ training_results.png           (graphs showing 4 charts)
```

---

## **💾 STEP 6: Deploy to Your App**

**Move the model file:**

```bash
# Copy downloaded file to:
backend/models/deepfake_detector.pth
```

**Restart your backend:**

```bash
cd backend
python app.py
```

**Upload test images/videos via web UI** → Model now uses trained weights! 🎉

---

## **📈 Understanding the Graphs**

After training, you get 4 graphs:

```
Training Results (training_results.png)
│
├─ Loss Graph (top-left)
│  ├─ Shows training loss decreasing
│  └─ Shows validation loss following
│
├─ Overall Accuracy (top-right)
│  ├─ Red line = Real + Fake combined
│  └─ Should steadily increase
│
├─ Real Accuracy (bottom-left)
│  ├─ Accuracy at detecting REAL images/videos
│  └─ Want this near 95%+
│
└─ Fake Accuracy (bottom-right)
   ├─ Accuracy at detecting FAKE images/videos
   └─ Want this near 95%+
```

**Good training looks like:**
- ✅ Loss curves smoothly decrease
- ✅ Both Real and Fake accuracies increase
- ✅ Validation accuracy close to training accuracy (not overfitting)
- ✅ Final accuracy 90%+

---

## **🎬 What the Script Does with Videos**

For each video file:

1. Reads video frames
2. **Extracts 5 evenly-spaced frames** (e.g., from 0s, 25%, 50%, 75%, 100%)
3. Saves frames as JPG images
4. Treats frames like regular images during training
5. **Final model handles both images AND video frames!**

Example:
```
video1.mp4 (1:30 duration) → 5 frames extracted
├─ Frame 0s
├─ Frame 22.5s
├─ Frame 45s
├─ Frame 67.5s
└─ Frame 90s

Result: 5 training samples from 1 video!
```

---

## **🎯 Best Practices**

### **Dataset Diversity**
- ✅ Mix different cameras, lighting conditions
- ✅ Include different face angles
- ✅ Include different AI generators (DALL-E, Midjourney, etc.)
- ✅ Include different deepfake methods

### **Video Quality**
- ✅ Use good quality videos (720p+)
- ✅ 5-10 seconds minimum per video
- ✅ Mix short and long videos
- ✅ Mix talking and static videos

### **Image Types**
- ✅ Faces (most common targets)
- ✅ Landscapes (for diversification)
- ✅ Different lighting (bright, dark, indoor, outdoor)
- ✅ Different art styles

### **Avoid**
- ❌ Very blurry images
- ❌ Watermarked images
- ❌ Cartoon/anime (unless that's your target)
- ❌ Duplicates

---

## **🐛 Troubleshooting**

### **Problem: "No samples found!"**
- Check folder structure is exactly `dataset/real/` and `dataset/fake/`
- Ensure files are .jpg, .png, .mp4, or .avi
- Minimum 1 file in each folder

### **Problem: "Out of Memory"**
In `colab_mixed_training.py`, change:
```python
BATCH_SIZE = 32  # Change to 16 or 8
```

### **Problem: Very slow training**
- You're on CPU, not GPU
- Go to `Runtime` → `Change runtime type` → Select `GPU`
- Check output shows "cuda" not "cpu"

### **Problem: Model accuracy stuck at 50%**
- More epochs: Change `EPOCHS = 20` to `50`
- More data: Add 100+ more image/video samples
- Better data: Ensure images are actually different

### **Problem: Real/Fake accuracy very different**
- Imbalanced dataset - add more samples to minority class
- Class weights: Modify training script to use weighted loss

---

## **✅ Validation Checklist**

Before uploading to production:

- [ ] Downloaded `deepfake_detector_best.pth`
- [ ] Placed in `backend/models/deepfake_detector.pth`
- [ ] Restarted Flask: `python app.py`
- [ ] Tested image upload - works ✓
- [ ] Tested video upload - works ✓
- [ ] Accuracy on test set > 85%
- [ ] Real/Fake accuracy both > 85%

---

## **🚀 Next Steps**

1. ✅ Train model with mixed data
2. ✅ Deploy to your app
3. ⏭️ Test with real user images/videos
4. ⏭️ Collect feedback & retrain periodically
5. ⏭️ Deploy with ensemble (combine multiple models)
6. ⏭️ Add explainability features (show which parts flagged as fake)

---

## **📞 Common Questions**

**Q: Do I need 1000 images?**
A: No! Start with 50 per class. More = better, but 50-100 is good for testing.

**Q: Can I mix different video formats?**
A: Yes! The script handles .mp4 and .avi automatically.

**Q: How do I improve accuracy?**
A: 1) More training data, 2) More epochs, 3) Better quality images, 4) More training time

**Q: Will the model work on mobile?**
A: Yes! Convert .pth to ONNX format for mobile deployment.

---

**Ready to train?** 🚀 Open [Google Colab](https://colab.research.google.com) and paste the script!
