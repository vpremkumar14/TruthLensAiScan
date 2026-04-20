"""
Generate synthetic training dataset (no external downloads needed)
Creates 200 real and 200 fake face-like images
"""

import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import random
from pathlib import Path

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
REAL_DIR = DATA_DIR / "real"
FAKE_DIR = DATA_DIR / "fake"

# Create directories
REAL_DIR.mkdir(parents=True, exist_ok=True)
FAKE_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 60)
print("🚀 Generating Synthetic Training Dataset")
print("=" * 60)

def create_real_face():
    """Create a realistic-looking face image"""
    img = Image.new('RGB', (224, 224), color=(200, 150, 100))
    draw = ImageDraw.Draw(img)
    
    # Face shape (oval)
    face_color = (220 + random.randint(-20, 20), 
                  170 + random.randint(-20, 20), 
                  150 + random.randint(-20, 20))
    draw.ellipse([30, 20, 194, 204], fill=face_color)
    
    # Eyes
    eye_color = (60 + random.randint(-30, 30), 
                 40 + random.randint(-30, 30), 
                 20 + random.randint(-30, 30))
    draw.ellipse([60, 70, 85, 95], fill=eye_color)
    draw.ellipse([139, 70, 164, 95], fill=eye_color)
    
    # Eye whites
    draw.ellipse([62, 72, 83, 93], fill=(240, 240, 240))
    draw.ellipse([141, 72, 162, 93], fill=(240, 240, 240))
    
    # Pupils
    pupil_x1, pupil_y1 = random.randint(65, 80), random.randint(75, 90)
    draw.ellipse([pupil_x1, pupil_y1, pupil_x1+8, pupil_y1+8], fill=(20, 20, 20))
    
    pupil_x2, pupil_y2 = random.randint(144, 159), random.randint(75, 90)
    draw.ellipse([pupil_x2, pupil_y2, pupil_x2+8, pupil_y2+8], fill=(20, 20, 20))
    
    # Nose
    nose_color = (face_color[0] - 20, face_color[1] - 20, face_color[2] - 20)
    draw.polygon([112, 110, 108, 140, 116, 140], fill=nose_color)
    
    # Mouth
    mouth_color = (180 + random.randint(-30, 30), 
                   80 + random.randint(-30, 30), 
                   80 + random.randint(-30, 30))
    draw.arc([90, 130, 134, 160], 0, 180, fill=mouth_color, width=3)
    
    # Hair (simple)
    hair_color = (30 + random.randint(-20, 20),
                  20 + random.randint(-20, 20), 
                  10 + random.randint(-20, 20))
    for i in range(50, 180, 10):
        draw.polygon([(i, 20), (i-3, 0), (i+3, 0)], fill=hair_color)
    
    # Add some texture/noise
    pixels = img.load()
    for _ in range(1000):
        x, y = random.randint(0, 223), random.randint(0, 223)
        noise = random.randint(-20, 20)
        try:
            r, g, b = pixels[x, y]
            pixels[x, y] = (max(0, min(255, r + noise)),
                           max(0, min(255, g + noise)),
                           max(0, min(255, b + noise)))
        except:
            pass
    
    # Blur slightly for realism
    img = img.filter(ImageFilter.GaussianBlur(radius=0.5))
    
    return img

def create_fake_face():
    """Create an AI-like synthetic face"""
    img = Image.new('RGB', (224, 224), color=(180, 130, 100))
    draw = ImageDraw.Draw(img)
    
    # Perfect oval (too perfect = AI indicator)
    face_color = (210 + random.randint(-10, 10), 
                  160 + random.randint(-10, 10), 
                  140 + random.randint(-10, 10))
    draw.ellipse([20, 10, 204, 214], fill=face_color)
    
    # Perfect symmetrical eyes
    eye_color = (50, 30, 10)
    draw.ellipse([50, 60, 85, 95], fill=eye_color)
    draw.ellipse([139, 60, 174, 95], fill=eye_color)
    
    # Too perfect eyes (AI artifact)
    draw.ellipse([55, 65, 80, 90], fill=(240, 240, 240))
    draw.ellipse([144, 65, 169, 90], fill=(240, 240, 240))
    
    # Perfect round pupils
    draw.ellipse([65, 73, 73, 81], fill=(10, 10, 10))
    draw.ellipse([154, 73, 162, 81], fill=(10, 10, 10))
    
    # Nose (too symmetrical)
    draw.polygon([112, 100, 109, 135, 115, 135], fill=(180, 110, 90))
    
    # Mouth (perfect curve)
    mouth_color = (160, 60, 60)
    draw.arc([95, 125, 129, 165], 0, 180, fill=mouth_color, width=4)
    
    # Hair (too uniform)
    hair_color = (20, 10, 5)
    draw.rectangle([0, 0, 224, 35], fill=hair_color)
    
    # Add grid-like artifacts (AI generation indicator)
    for x in range(0, 224, 20):
        draw.line([(x, 0), (x, 224)], fill=(150, 130, 120), width=1)
    for y in range(0, 224, 20):
        draw.line([(0, y), (224, y)], fill=(150, 130, 120), width=1)
    
    # Blur for artifact softening
    img = img.filter(ImageFilter.GaussianBlur(radius=1.5))
    
    return img

# Generate real faces
print("\n📸 Creating 200 realistic faces...")
for i in range(200):
    img = create_real_face()
    img.save(REAL_DIR / f"real_face_{i:04d}.jpg")
    if (i + 1) % 50 == 0:
        print(f"  ✅ Created {i+1} real faces")

# Generate fake faces
print("\n🤖 Creating 200 AI-like synthetic faces...")
for i in range(200):
    img = create_fake_face()
    img.save(FAKE_DIR / f"fake_face_{i:04d}.jpg")
    if (i + 1) % 50 == 0:
        print(f"  ✅ Created {i+1} fake faces")

# Verify
real_count = len(list(REAL_DIR.glob("*.jpg")))
fake_count = len(list(FAKE_DIR.glob("*.jpg")))

print("\n" + "=" * 60)
print("📊 DATASET CREATED")
print("=" * 60)
print(f"✅ Real images: {real_count}")
print(f"✅ Fake images: {fake_count}")
print(f"✅ Total: {real_count + fake_count}")
print("\n🎯 Ready to train! Run:")
print("   python train_model_final.py --epochs 50 --batch-size 16")
print("=" * 60)
