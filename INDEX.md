# TruthLens AI Scan - Documentation Index

A comprehensive guide to all documentation and resources for the TruthLens AI Scan deepfake detection application.

---

## 📚 Documentation by Use Case

### I want to... 

#### 🚀 Get Started Quickly
- **Start Here**: [QUICKSTART.md](QUICKSTART.md) - 2-minute setup
- **Then Read**: [INSTALL.md](INSTALL.md) - Detailed installation
- **Then Try**: Upload an image at `http://localhost:3000`

#### 💻 Install & Run
- [INSTALL.md](INSTALL.md) - Complete installation guide with troubleshooting
- [QUICKSTART.md](QUICKSTART.md) - Quick start (fastest path)
- [setup.bat](setup.bat) - Automated setup (Windows)
- [setup.sh](setup.sh) - Automated setup (Linux/Mac)

#### 🔌 Use the API
- [API.md](API.md) - Full REST API documentation
- [test_api.py](backend/test_api.py) - API test script
- Endpoints: POST /detect-image, POST /detect-video, GET /health

#### 🏗️ Understand Architecture
- [ARCHITECTURE.md](ARCHITECTURE.md) - System design and deployment
- [Project Structure](#project-structure) - Code organization
- Includes: Tech stack, data flow, performance notes

#### 👨‍💻 Develop Features
- [DEVELOPER.md](DEVELOPER.md) - Development guide
- [API.md](API.md) - API reference
- [backend/utils/](backend/utils/) - Backend utilities

#### 🚢 Deploy to Production
- [ARCHITECTURE.md](ARCHITECTURE.md#deployment-options) - Deployment strategies
- [DOCKER.md](DOCKER.md) - Docker containerization
- Cloud options: Heroku, AWS, GCP, Azure

#### 🤖 Train Custom Model
- [backend/train_model.py](backend/train_model.py) - Training script
- [backend/data/README.md](backend/data/README.md) - Data preparation
- Run: `python train_model.py --epochs 50`

#### 🛠️ Fix Issues
- [INSTALL.md](INSTALL.md#troubleshooting) - Troubleshooting guide
- Run: `python backend/check_setup.py` - System diagnostics
- [backend/test_api.py](backend/test_api.py) - Test backend

---

## 📖 Main Documentation Files

### [README.md](README.md) - Project Overview
- Features overview
- Tech stack
- Project structure
- Installation (brief)
- API endpoints
- Future enhancements

### [QUICKSTART.md](QUICKSTART.md) - Fast Start Guide
- 2-minute installation
- Port information
- File upload instructions
- Troubleshooting table

### [INSTALL.md](INSTALL.md) - Complete Installation
- Prerequisites checklist
- Step-by-step installation
- Troubleshooting with solutions
- System requirements
- Verification steps

### [API.md](API.md) - API Reference
- All endpoints documented
- Request/response examples
- Error handling
- Rate limiting
- Client integration code

### [ARCHITECTURE.md](ARCHITECTURE.md) - System Design
- Architecture diagram
- Tech stack details
- Data flow diagrams
- Deployment options
- Performance optimization
- Cost estimation

### [DEVELOPER.md](DEVELOPER.md) - Development Guide
- Code style guidelines
- Testing procedures
- Adding new features
- Debugging techniques
- Performance tips

### [DOCKER.md](DOCKER.md) - Containerization
- Docker setup
- Docker Compose configuration
- Building images
- Running containers

### [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Completion Report
- Project achievements
- Features checklist
- Technology stack
- Statistics and highlights

---

## 🗂️ Project Structure

```
truth/
├── frontend/                     # React Application
│   ├── src/components/          # UI Components
│   ├── src/pages/               # Page Components
│   ├── src/utils/api.js         # API Client
│   ├── package.json             # Dependencies
│   ├── vite.config.js           # Build Config
│   └── tailwind.config.js       # CSS Config
│
├── backend/                      # Flask Application
│   ├── app.py                   # Main App
│   ├── train_model.py           # Training
│   ├── utils/                   # Utilities
│   ├── data/                    # Training Data
│   ├── uploads/                 # Uploaded Files
│   ├── requirements.txt         # Dependencies
│   └── .env.example             # Config Template
│
├── models/                      # Model Storage
│   └── deepfake_detector.pth   # Trained Model
│
├── Documentation/
│   ├── README.md               # Main Docs
│   ├── QUICKSTART.md          # Fast Start
│   ├── INSTALL.md             # Installation
│   ├── API.md                 # API Docs
│   ├── ARCHITECTURE.md        # Architecture
│   ├── DEVELOPER.md           # Dev Guide
│   ├── DOCKER.md              # Docker
│   └── PROJECT_SUMMARY.md     # Summary
│
└── Setup Scripts/
    ├── setup.bat              # Windows
    ├── setup.sh               # Linux/Mac
    └── INDEX.md               # This File
```

---

## 🎯 Quick Reference

### Common Commands

```bash
# Backend
cd backend && python -m venv venv
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
python app.py             # Start server
python train_model.py     # Train model
python check_setup.py     # Verify setup
python test_api.py        # Test API

# Frontend
cd frontend
npm install               # Install deps
npm run dev              # Start dev server
npm run build            # Production build
```

### File Locations

| Item | Location |
|------|----------|
| Frontend Code | `frontend/src/` |
| Backend Code | `backend/` |
| Model File | `models/deepfake_detector.pth` |
| Uploads | `backend/uploads/` |
| API Docs | [API.md](API.md) |
| Dev Docs | [DEVELOPER.md](DEVELOPER.md) |
| Config | `backend/.env` |

### URLs

| Service | URL |
|---------|-----|
| Frontend | http://localhost:3000 |
| Backend | http://localhost:5000 |
| API Health | http://localhost:5000/api/health |

---

## 📚 Topic Guide

### Installation & Setup
1. [QUICKSTART.md](QUICKSTART.md) - 2 minute setup
2. [INSTALL.md](INSTALL.md) - Detailed guide
3. [backend/check_setup.py](backend/check_setup.py) - Verification script

### Using the Application
1. [QUICKSTART.md](QUICKSTART.md) - How to use
2. [Frontend Code](frontend/src/) - UI components
3. [API.md](API.md) - API endpoints

### API Integration
1. [API.md](API.md) - Complete reference
2. [frontend/src/utils/api.js](frontend/src/utils/api.js) - Client example
3. [backend/test_api.py](backend/test_api.py) - Test script

### Model Training
1. [backend/train_model.py](backend/train_model.py) - Training code
2. [backend/data/README.md](backend/data/README.md) - Data setup
3. [ARCHITECTURE.md](ARCHITECTURE.md#model-training) - Technical details

### Deployment
1. [ARCHITECTURE.md](ARCHITECTURE.md#deployment-options) - Options
2. [DOCKER.md](DOCKER.md) - Docker setup
3. [DEVELOPER.md](DEVELOPER.md) - Dev setup

### Development
1. [DEVELOPER.md](DEVELOPER.md) - Getting started
2. [ARCHITECTURE.md](ARCHITECTURE.md) - Design patterns
3. Code files in `frontend/src/` and `backend/`

---

## 🔍 Finding What You Need

### By Question

**How do I install?**
→ [INSTALL.md](INSTALL.md)

**How do I start?**
→ [QUICKSTART.md](QUICKSTART.md)

**How do I use the API?**
→ [API.md](API.md)

**How do I deploy?**
→ [ARCHITECTURE.md](ARCHITECTURE.md#deployment-options)

**How do I develop?**
→ [DEVELOPER.md](DEVELOPER.md)

**How do I train a model?**
→ [backend/train_model.py](backend/train_model.py) + [backend/data/README.md](backend/data/README.md)

**How do I fix errors?**
→ [INSTALL.md](INSTALL.md#troubleshooting)

**What's the architecture?**
→ [ARCHITECTURE.md](ARCHITECTURE.md)

**What APIs are available?**
→ [API.md](API.md)

---

## 🔧 Utility Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| setup.bat | Windows setup | `setup.bat` |
| setup.sh | Linux/Mac setup | `bash setup.sh` |
| backend/check_setup.py | Verify installation | `python check_setup.py` |
| backend/test_api.py | Test API endpoints | `python test_api.py` |
| backend/create_model.py | Initialize model | `python create_model.py` |
| backend/train_model.py | Train custom model | `python train_model.py` |
| backend/generate_test_images.py | Generate test data | `python generate_test_images.py` |

---

## 📊 Technology Stack

### Frontend
- React 18
- Vite
- Tailwind CSS
- Framer Motion
- Axios

### Backend
- Python 3.8+
- Flask
- PyTorch
- OpenCV
- Pillow

### Infrastructure
- Node.js / npm
- Docker (optional)
- Cloud platforms

---

## 🚀 Getting Help

### Troubleshooting
1. Check [INSTALL.md](INSTALL.md#troubleshooting) - Common issues
2. Run `python backend/check_setup.py` - System check
3. Review console/terminal output - Error messages

### Learning Resources
See [ARCHITECTURE.md](ARCHITECTURE.md#resources) for:
- React documentation
- PyTorch tutorials
- Flask guides
- Transfer learning resources

### Additional Resources
- [README.md](README.md) - Full project description
- [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Completion report
- [backend/utils/](backend/utils/) - Source code

---

## 📝 Document Maintenance

| Document | Last Updated | Maintainer |
|----------|-------------|-----------|
| README.md | 2024 | Project |
| QUICKSTART.md | 2024 | Project |
| INSTALL.md | 2024 | Project |
| API.md | 2024 | Project |
| ARCHITECTURE.md | 2024 | Project |
| DEVELOPER.md | 2024 | Project |
| DOCKER.md | 2024 | Project |
| PROJECT_SUMMARY.md | 2024 | Project |

---

## 🎓 Learning Path

### Beginner (Want to use the app)
1. Read [QUICKSTART.md](QUICKSTART.md)
2. Follow installation steps
3. Try uploading files
4. Check results

### Intermediate (Want to understand)
1. Read [README.md](README.md)
2. Read [ARCHITECTURE.md](ARCHITECTURE.md)
3. Explore source code
4. Read [API.md](API.md)

### Advanced (Want to develop)
1. Read [DEVELOPER.md](DEVELOPER.md)
2. Read [ARCHITECTURE.md](ARCHITECTURE.md)
3. Study source code
4. Add new features
5. Train custom model

### Expert (Want to deploy)
1. Read [ARCHITECTURE.md](ARCHITECTURE.md)
2. Read [DOCKER.md](DOCKER.md)
3. Choose deployment platform
4. Deploy application
5. Monitor performance

---

## 🎉 Success Checklist

- [ ] Installation complete
- [ ] Backend running: http://localhost:5000
- [ ] Frontend running: http://localhost:3000
- [ ] Can access home page
- [ ] Can upload images
- [ ] Can upload videos
- [ ] Results display correctly
- [ ] No errors in console

---

## 📞 Support

For help:
1. Check relevant documentation file
2. Review troubleshooting sections
3. Run diagnostic scripts
4. Check source code comments
5. Review error messages in console

---

## 📄 License & Attribution

TruthLens AI Scan - Deepfake Detection Application
Version 1.0.0
Status: Production Ready

---

**Start Here**: [QUICKSTART.md](QUICKSTART.md)
**Full Guide**: [INSTALL.md](INSTALL.md)
**API Reference**: [API.md](API.md)

Happy coding! 🚀
