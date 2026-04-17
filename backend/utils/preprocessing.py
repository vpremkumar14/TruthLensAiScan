import cv2
import numpy as np
from PIL import Image
import torchvision.transforms as transforms

def preprocess_image(image_path, target_size=(224, 224)):
    """Load and preprocess image"""
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, target_size)
    
    # Normalize
    image = image.astype('float32') / 255.0
    
    return image

def extract_video_frames(video_path, num_frames=10, target_size=(224, 224)):
    """Extract frames from video"""
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        raise ValueError(f"Cannot open video: {video_path}")
    
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    if total_frames == 0:
        raise ValueError("Video has no frames")
    
    # Sample frames evenly
    frame_indices = np.linspace(0, total_frames - 1, num_frames, dtype=int)
    
    frames = []
    for frame_idx in frame_indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = cap.read()
        
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, target_size)
            frames.append(frame)
    
    cap.release()
    
    return np.array(frames)

def normalize_image(image_array):
    """Normalize image using ImageNet statistics"""
    image = image_array.astype('float32')
    
    # ImageNet normalization
    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])
    
    image = (image / 255.0 - mean) / std
    
    return image

def augment_image(image_array, augment=False):
    """Apply data augmentation"""
    if not augment:
        return image_array
    
    # Random flip
    if np.random.random() > 0.5:
        image_array = np.fliplr(image_array)
    
    # Random rotation
    if np.random.random() > 0.5:
        angle = np.random.uniform(-10, 10)
        center = (image_array.shape[0] // 2, image_array.shape[1] // 2)
        matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
        image_array = cv2.warpAffine(image_array, matrix, (image_array.shape[1], image_array.shape[0]))
    
    return image_array
