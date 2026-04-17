# Quick Start Guide

## Installation & Setup (2 minutes)

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start server
python app.py
```

✓ Backend running on `http://localhost:5000`

### 2. Frontend Setup (New Terminal)

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

✓ Frontend running on `http://localhost:3000`

### 3. Open Application

Navigate to `http://localhost:3000` in your browser

## File Uploads

### Supported Formats
- **Images**: PNG, JPG, JPEG, GIF, BMP (up to 100MB)
- **Videos**: MP4, AVI, MOV, MKV, FLV, WMV (up to 100MB)

### Usage
1. Click "Image Detection" or "Video Detection"
2. Drag & drop or click to upload
3. Wait for AI analysis
4. View results with confidence score

## Training Custom Model

If you have a dataset of real and fake images:

```bash
cd backend

# Organize data:
# data/
#   real/ (authentic images)
#   fake/ (AI-generated images)

# Train model:
python train_model.py --epochs 50 --batch-size 32

# Model saved to: models/deepfake_detector.pth
```

## Ports

- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:5000

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Port 5000 in use | Kill process: `lsof -i :5000` (macOS/Linux) |
| Model not found | Run: `python train_model.py` |
| CORS errors | Check backend is running on port 5000 |
| npm not found | Install Node.js from nodejs.org |

## Features

✨ Modern UI with dark theme and glassmorphism
🎬 Multi-modal detection (images & videos)
📊 Confidence scores and detailed analysis
⚡ Fast inference with GPU support
📱 Fully responsive design

---

**Ready to detect deepfakes!** 🔍
