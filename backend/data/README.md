# Sample data directory structure for model training

This directory should contain your training data organized as:

```
data/
  real/
    - Authentic photos and videos frames
    - Real images from real-world scenarios
    - Examples: photo123.jpg, photo124.png, etc.
    
  fake/
    - AI-generated images
    - Deepfake images
    - Synthetic content
    - Examples: generated001.jpg, deepfake001.png, etc.
```

## Dataset Setup Instructions

1. **Gather Data**
   - Collect authentic images and put in `real/` folder
   - Collect AI-generated/deepfake images and put in `fake/` folder

2. **Organize Structure**
   ```
   data/
   ├── real/
   │   ├── img1.jpg
   │   ├── img2.png
   │   └── ... (more real images)
   └── fake/
       ├── fake1.jpg
       ├── fake2.png
       └── ... (more fake images)
   ```

3. **Training**
   ```bash
   cd ..
   python train_model.py --epochs 50 --batch-size 32
   ```

## Dataset Recommendations

- **Minimum**: 500 images per class
- **Recommended**: 2000+ images per class
- **Optimal**: 5000+ images per class

## Data Formats Supported

- Images: JPG, PNG, GIF, BMP
- Videos: MP4, AVI, MOV (videos will be converted to frames)

## Tips for Better Results

1. **Balance**: Keep similar number of real and fake images
2. **Diversity**: Include various image types and qualities
3. **Cleanliness**: Remove corrupted or irrelevant images
4. **Labeling**: Double-check classification accuracy
5. **Augmentation**: The training script includes random flipping and rotation

## Public Datasets

You can download datasets from:
- **FaceForensics++**: https://github.com/ondyari/FaceForensics
- **Celeb-DF**: https://www.cs.albany.edu/~lsw/celeb-deepfakeforensics/
- **DFDC**: https://www.kaggle.com/c/deepfake-detection-challenge
- **COCO**: https://cocodataset.org/ (for real images)

---

Start by adding your images to this directory structure, then run training!
