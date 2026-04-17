# 🔍 TruthLens AI Scan - Complete Installation & Setup Guide

Welcome to **TruthLens AI Scan** - A powerful full-stack application for detecting deepfake and AI-generated media!

---

## ⚡ Quick Start (5 Minutes)

### Option 1: Automated Setup (Recommended)

**Windows**:
```bash
python install.py
```

**macOS/Linux**:
```bash
python3 install.py
```

**Then start the servers** (in separate terminals):
```bash
# Terminal 1
cd backend && source venv/bin/activate && python app.py

# Terminal 2
cd frontend && npm run dev

# Open: http://localhost:3000
```

### Option 2: Manual Setup

**Backend**:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
python create_model.py
python app.py
```

**Frontend** (new terminal):
```bash
cd frontend
npm install
npm run dev
```

**Then open browser**: `http://localhost:3000`

---

## 📋 Requirements

- **Python**: 3.8 or higher
- **Node.js**: 16 or higher
- **npm**: 7 or higher
- **RAM**: 4GB minimum, 8GB recommended
- **Disk**: 2GB free space

**Check versions**:
```bash
python --version
node --version
npm --version
```

---

## 📚 Documentation

Find what you need:

| Need | Document |
|------|----------|
| 2-minute quickstart | [QUICKSTART.md](QUICKSTART.md) |
| Complete installation | [INSTALL.md](INSTALL.md) |
| API reference | [API.md](API.md) |
| System architecture | [ARCHITECTURE.md](ARCHITECTURE.md) |
| Development guide | [DEVELOPER.md](DEVELOPER.md) |
| Docker setup | [DOCKER.md](DOCKER.md) |
| Full overview | [README.md](README.md) |
| **Documentation index** | **[INDEX.md](INDEX.md)** ← Start here! |

---

## 🎯 Features

✨ **Modern UI**
- Dark theme with glassmorphism effects
- Smooth animations with Framer Motion
- Fully responsive design (mobile, tablet, desktop)
- Professional interface

🤖 **AI Detection**
- ResNet50 CNN with transfer learning
- Real vs Fake classification
- Confidence scores (0-100%)
- Multi-frame video analysis

📁 **Multi-Modal Support**
- Image detection (PNG, JPG, GIF, BMP)
- Video detection (MP4, AVI, MOV, MKV, FLV, WMV)
- Up to 100MB file size
- Fast processing with GPU support

📊 **Detailed Results**
- Real/Fake prediction
- Confidence percentage
- Human-readable explanations
- Analysis insights

---

## 🚀 First Time Running

1. **Run setup**:
   ```bash
   python install.py  # Automated setup
   ```

2. **Start backend** (Terminal 1):
   ```bash
   cd backend && source venv/bin/activate && python app.py
   ```

3. **Start frontend** (Terminal 2):
   ```bash
   cd frontend && npm run dev
   ```

4. **Open browser**:
   ```
   http://localhost:3000
   ```

5. **Try it**:
   - Click "Image Detection" or "Video Detection"
   - Upload a file
   - See results in 2-5 seconds!

---

## 🆘 Troubleshooting

### Issue: Port already in use
```bash
# Find process using port
lsof -i :5000  # macOS/Linux
netstat -ano | findstr :5000  # Windows

# Kill process or use different port
python app.py --port 8000
```

### Issue: Module not found
```bash
cd backend
pip install -r requirements.txt  # Reinstall dependencies
```

### Issue: npm dependencies fail
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Issue: Backend says model not found
```bash
cd backend
python create_model.py
```

**More help**: See [INSTALL.md](INSTALL.md#troubleshooting)

---

## 📂 Project Structure

```
truth/
├── frontend/              # React Web App
│   ├── src/components/   # UI Components
│   ├── src/pages/        # Page Components
│   ├── package.json
│   └── vite.config.js
├── backend/               # Flask API
│   ├── app.py            # Main application
│   ├── utils/            # Utilities
│   ├── train_model.py    # Model training
│   └── requirements.txt
├── models/                # AI Models
│   └── deepfake_detector.pth
├── Documentation/
│   ├── README.md
│   ├── QUICKSTART.md
│   ├── INSTALL.md
│   ├── API.md
│   └── ... (7 docs total)
└── Setup Scripts/
    ├── install.py
    ├── setup.bat
    └── setup.sh
```

---

## 🔗 How It Works

```
User Upload (Image/Video)
    ↓
Frontend sends to Backend API
    ↓
Backend preprocesses file
    ↓
AI Model (ResNet50) analyzes
    ↓
Returns prediction + confidence
    ↓
Frontend displays beautify results
    ↓
User sees Real/Fake + explanation
```

---

## 🌐 API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/health` | GET | Check server status |
| `/api/detect-image` | POST | Analyze image |
| `/api/detect-video` | POST | Analyze video |

**Example**:
```bash
curl -X POST -F "file=@image.jpg" http://localhost:5000/api/detect-image
```

Response:
```json
{
  "prediction": "Real",
  "confidence": 0.95,
  "explanation": "This image appears to be authentic..."
}
```

---

## 🎓 Learning Resources

**Frontend**: React, Tailwind CSS, Framer Motion
**Backend**: Flask, PyTorch, OpenCV
**AI/ML**: ResNet50, Transfer Learning, CNN

See [DEVELOPER.md](DEVELOPER.md#resources) for links.

---

## 🚢 Deployment

Ready to deploy? Options include:
- **Docker** (see [DOCKER.md](DOCKER.md))
- **Heroku** (git push heroku main)
- **AWS** (Lambda + API Gateway)
- **GCP** (Cloud Run)
- **Azure** (App Service)

See [ARCHITECTURE.md](ARCHITECTURE.md#deployment-options) for details.

---

## 📊 Performance

| Metric | Value |
|--------|-------|
| Image Processing | 1-2 seconds |
| Video Processing | 5-10 seconds per minute |
| Model Accuracy | >90% (with training) |
| Max File Size | 100 MB |
| Supported Formats | 10+ formats |

---

## ✅ Verification Checklist

After setup, verify everything works:

- [ ] Backend starts (terminal shows "Running on http://0.0.0.0:5000")
- [ ] Frontend starts (terminal shows "Local: http://localhost:3000")
- [ ] Browser opens to http://localhost:3000
- [ ] Can upload images
- [ ] Can upload videos
- [ ] Results display correctly
- [ ] No error messages in console

---

## 🎯 Next Steps

1. ✅ **Setup** - Run `python install.py`
2. ✅ **Start** - Run backend and frontend
3. ✅ **Test** - Upload an image or video
4. ✅ **Explore** - Try different features
5. ✅ **Develop** - Add new features (see [DEVELOPER.md](DEVELOPER.md))
6. ✅ **Deploy** - Put on cloud (see [ARCHITECTURE.md](ARCHITECTURE.md))

---

## 📞 Need Help?

1. **Check existing docs** - [INDEX.md](INDEX.md) has all documentation
2. **Run diagnostics** - `python backend/check_setup.py`
3. **Review errors** - Check terminal output and browser console
4. **Test API** - `python backend/test_api.py`

---

## 🏆 What's Included

✅ Complete React frontend with multiple pages
✅ Flask backend with REST APIs
✅ ResNet50 AI model (pre-trained)
✅ Training script for custom models
✅ 7 comprehensive documentation files
✅ Setup and test scripts
✅ Docker configuration
✅ Error handling and validation
✅ Professional UI/UX design
✅ Production-ready code

---

## 📈 Tech Stack

**Frontend**
- React 18
- Vite
- Tailwind CSS
- Framer Motion
- Axios

**Backend**
- Python 3.8+
- Flask
- PyTorch
- OpenCV
- Pillow

---

## 🎓 Development

Want to add features? Start with [DEVELOPER.md](DEVELOPER.md):
- Code style guidelines
- Testing procedures
- Adding new features
- Debugging tips

---

## 🚀 Ready to Start?

```bash
python install.py
```

Then follow the on-screen instructions!

---

## 📄 Quick Links

| What | Where |
|------|-------|
| Start here | This file ← You are here |
| 2-min quickstart | [QUICKSTART.md](QUICKSTART.md) |
| Full setup | [INSTALL.md](INSTALL.md) |
| All documentation | [INDEX.md](INDEX.md) |
| API reference | [API.md](API.md) |
| Project overview | [README.md](README.md) |
| Development | [DEVELOPER.md](DEVELOPER.md) |
| Deployment | [ARCHITECTURE.md](ARCHITECTURE.md) |

---

**Version**: 1.0.0  
**Status**: ✅ Production Ready  
**Created**: 2024

**Let's detect deepfakes!** 🔍
