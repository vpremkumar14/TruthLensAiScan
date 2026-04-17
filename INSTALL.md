# Installation & First Run Guide

## Prerequisites Checklist

Before starting, ensure you have:

- [ ] **Node.js 16+** - Download from [nodejs.org](https://nodejs.org)
  ```bash
  node --version  # Should show v16.0.0 or higher
  npm --version   # Should show 7.0.0 or higher
  ```

- [ ] **Python 3.8+** - Download from [python.org](https://python.org)
  ```bash
  python --version  # Should show 3.8+
  ```

- [ ] **Git** (Optional) - For version control
  ```bash
  git --version
  ```

---

## Installation Options

### Option 1: Using Setup Script (Easiest)

**Windows**:
```bash
cd truth
setup.bat
```

**macOS/Linux**:
```bash
cd truth
bash setup.sh
```

### Option 2: Manual Installation

#### Step 1: Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create initial model (for testing purposes)
python create_model.py

# You should see: ✓ Placeholder model created at models/deepfake_detector.pth
```

#### Step 2: Frontend Setup

```bash
# Open new terminal, navigate to frontend
cd frontend

# Install dependencies
npm install

# This will download all React, Tailwind, and other packages
# May take 2-5 minutes depending on internet speed
```

#### Step 3: Start the Application

**Terminal 1 - Backend**:
```bash
cd backend

# Activate virtual environment (if not already)
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Start server
python app.py

# You should see:
# 🚀 Starting TruthLens Backend Server...
# 📊 Model loaded on device: cpu
#  * Running on http://0.0.0.0:5000
```

**Terminal 2 - Frontend**:
```bash
cd frontend

# Start development server
npm run dev

# You should see:
# VITE v5.0.0 ready in XXX ms
#   ➜  Local:   http://localhost:3000/
#   ➜  press h to show help
```

#### Step 4: Open Application

Open your browser and navigate to:
```
http://localhost:3000
```

You should see the TruthLens home page with:
- Navigation bar with logo
- Hero section with "Detect Deepfakes with AI Power"
- "Get Started" and "Try Video Detection" buttons
- Features section
- Call-to-action area

---

## Troubleshooting

### Common Issues

#### 1. Port 5000 Already in Use

**Error**: `Address already in use`

**Solution**:
```bash
# Find process using port 5000
# Windows (PowerShell):
Get-Process -Id (Get-NetTCPConnection -LocalPort 5000).OwningProcess

# Kill process:
Stop-Process -Id <PID> -Force

# macOS/Linux:
lsof -i :5000
kill -9 <PID>

# Or use different port:
python app.py --port 8000
```

#### 2. Port 3000 Already in Use

**Error**: `Port 3000 is in use`

**Solution**:
```bash
# Update vite config or use different port
npm run dev -- --port 3001
```

#### 3. Dependencies Installation Fails

**Error**: `pip install` or `npm install` fails

**Solution**:
```bash
# Python: Clear cache and try again
pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt

# Node: Clear cache and try again
npm cache clean --force
npm install
```

#### 4. Model Not Found

**Error**: `Model file not found at models/deepfake_detector.pth`

**Solution**:
```bash
cd backend
python create_model.py
```

#### 5. CUDA Not Found (GPU Support)

**Note**: Application works fine on CPU, but slower

**Solution for GPU**:
```bash
# If you have NVIDIA GPU, install CUDA:
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Verify CUDA availability:
python -c "import torch; print(torch.cuda.is_available())"
```

#### 6. CORS Errors in Browser

**Error**: `Access to XMLHttpRequest blocked by CORS policy`

**Likely cause**: Backend not running

**Solution**:
```bash
# Make sure backend is running on http://localhost:5000
# Check Terminal 1 shows "Running on http://0.0.0.0:5000"
```

#### 7. npm ERR! code ENOENT

**Error**: `npm ERR! enoent ENOENT: no such file or directory`

**Solution**:
```bash
# Make sure you're in the frontend directory
cd frontend

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

#### 8. Python Version Error

**Error**: `Python 3.8 or higher required`

**Solution**:
```bash
# Check Python version
python --version

# If using Python 2, try:
python3 --version

# Use python3 if available:
python3 -m venv venv
```

---

## Verification Steps

### 1. Backend Health Check

```bash
# Terminal 1 should show:
# 🚀 Starting TruthLens Backend Server...
# 📊 Model loaded on device: cpu
#  * Running on http://0.0.0.0:5000
#  * Press CTRL+C to quit

# Test in new terminal:
curl http://localhost:5000/api/health
# Should return: {"status": "healthy", "device": "cpu", "model_loaded": true}
```

### 2. Frontend Build Verification

```bash
# Terminal 2 should show:
# VITE v5.0.0
#   ➜  Local:   http://localhost:3000/
#   ➜  press h to show help
```

### 3. Browser Test

1. Open `http://localhost:3000`
2. You should see:
   - ✓ TruthLens logo in navbar
   - ✓ Hero section with gradient text
   - ✓ Navigation links visible
   - ✓ No console errors (Check DevTools)

### 4. Upload Test

1. Click "Image Detection" or "Video Detection"
2. Try uploading a test file
3. Should show loading spinner
4. After 2-5 seconds, should display results

---

## System Requirements

### Minimum
- CPU: 2 cores
- RAM: 4 GB
- Storage: 2 GB
- Internet: For dependency installation

### Recommended
- CPU: 4+ cores
- RAM: 8 GB
- Storage: 5 GB
- GPU: NVIDIA GTX 1050+ (optional, for faster inference)

### Optimal
- CPU: 8+ cores
- RAM: 16 GB
- Storage: 10 GB
- GPU: NVIDIA RTX 2080+ or better

---

## Quick Reference

### Common Commands

```bash
# Backend operations
cd backend
python -m venv venv              # Create virtual env
source venv/bin/activate         # Activate (macOS/Linux)
venv\Scripts\activate            # Activate (Windows)
pip install -r requirements.txt  # Install dependencies
python app.py                    # Start server
python check_setup.py            # Verify installation
python test_api.py               # Test API endpoints

# Frontend operations
cd frontend
npm install                      # Install dependencies
npm run dev                      # Start dev server
npm run build                    # Build for production
npm run preview                  # Preview production build

# Model operations
cd backend
python create_model.py           # Create initial model
python train_model.py            # Train on custom data
python generate_test_images.py   # Generate test images
```

---

## Next Steps

### 1. First Time Using

1. ✓ Start both servers (Backend + Frontend)
2. ✓ Open `http://localhost:3000`
3. ✓ Click "Image Detection"
4. ✓ Try uploading an image
5. ✓ View the results

### 2. Training Custom Model

If you have real and fake image datasets:
```bash
cd backend

# Organize data:
# data/
#   real/
#   fake/

# Train:
python train_model.py --epochs 50
```

### 3. Deployment

When ready for production:
- See [DOCKER.md](DOCKER.md) for containerization
- See [ARCHITECTURE.md](ARCHITECTURE.md) for deployment options

---

## Support & Help

### System Check Script

```bash
cd backend
python check_setup.py
```

This will verify:
- Python version
- PyTorch installation
- OpenCV installation
- Model file
- Frontend dependencies

### Logs

Check logs for errors:
```bash
# Backend logs appear in Terminal 1

# Frontend logs appear in Browser Console (F12)

# Uploaded files stored in:
backend/uploads/
```

### Get Help

1. Check [README.md](README.md) for detailed documentation
2. Check [API.md](API.md) for API details
3. Check [DEVELOPER.md](DEVELOPER.md) for development info
4. Check console/terminal errors

---

## Environment Variable Setup (Optional)

Create `.env` file in `backend/` directory:

```env
FLASK_ENV=development
FLASK_DEBUG=True
CORS_ALLOWED_ORIGINS=http://localhost:3000
MAX_FILE_SIZE=104857600
UPLOAD_FOLDER=uploads
MODEL_PATH=models/deepfake_detector.pth
DEVICE=auto
```

---

## Performance Tips

1. **Enable GPU** (if available):
   ```bash
   # Install CUDA version of PyTorch
   pip install torch --index-url https://download.pytorch.org/whl/cu118
   ```

2. **Reduce model size**:
   - Use quantization: 50% faster, 75% smaller
   - Use ONNX export: Better performance

3. **Optimize frontend**:
   - Clear browser cache (Ctrl+Shift+Del)
   - Disable browser extensions
   - Close unnecessary tabs

---

## Success Indicators

You'll know everything is working when:

✅ Backend starts without errors
✅ Frontend starts without errors
✅ Browser opens to http://localhost:3000
✅ No red error messages in console
✅ File upload works
✅ Results display correctly
✅ All navigation links work
✅ Mobile responsive design works

---

**Installation Complete!** 🎉

You're ready to use TruthLens AI Scan for detecting deepfakes and AI-generated media.

**Have questions?** Check the documentation files or review the troubleshooting section above.

---

**Version**: 1.0  
**Last Updated**: 2024
