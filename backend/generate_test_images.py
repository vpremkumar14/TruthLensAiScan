"""
Example test image generator for testing the application
Creates simple test images for verification
"""

import numpy as np
from PIL import Image
import os

def create_test_images():
    """Create simple test images"""
    os.makedirs('backend/uploads/test_images', exist_ok=True)
    
    # Create red image (fake indicator)
    fake_img = np.zeros((224, 224, 3), dtype=np.uint8)
    fake_img[:, :, 0] = 255  # Red channel
    fake_img[50:100, 50:100, 1] = 200  # Green spots (pattern)
    Image.fromarray(fake_img).save('backend/uploads/test_images/fake_pattern.jpg')
    print("✓ Created: test_images/fake_pattern.jpg")
    
    # Create natural-looking image (real indicator)
    real_img = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
    # Add some structure to make it look more natural
    for i in range(224):
        real_img[i, :, 0] = int(255 * (i / 224))  # Gradient
    Image.fromarray(real_img).save('backend/uploads/test_images/natural_pattern.jpg')
    print("✓ Created: test_images/natural_pattern.jpg")
    
    # Create gradient image
    grad_img = np.zeros((224, 224, 3), dtype=np.uint8)
    for i in range(224):
        grad_img[i, :, 0] = int(255 * (i / 224))
        grad_img[i, :, 1] = 128
        grad_img[i, :, 2] = 255 - int(255 * (i / 224))
    Image.fromarray(grad_img).save('backend/uploads/test_images/gradient.jpg')
    print("✓ Created: test_images/gradient.jpg")

if __name__ == '__main__':
    create_test_images()
    print("\n✓ Test images created in backend/uploads/test_images/")
    print("  Use these to test the API endpoints")
