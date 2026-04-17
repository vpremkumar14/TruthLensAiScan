# TruthLens AI Scan - Deepfake Detection

A full-stack AI-powered web application for detecting deepfake and AI-generated media (images and videos) using deep learning.

## Features

✨ **Core Features**
- 🎬 Multi-modal detection for images and videos
- 🤖 Advanced CNN with ResNet50 for accurate classification
- ⚡ Fast inference with GPU support
- 📊 Confidence scores with detailed analysis
- 🎨 Modern, professional UI with dark theme
- ✨ Glassmorphism effects and smooth animations
- 📱 Fully responsive design

🔍 **Detection Capabilities**
- Real vs AI-generated images
- Deepfake video detection
- Frame-by-frame video analysis
- Explainable AI insights

## Tech Stack

### Frontend
- **Framework**: React 18
- **Styling**: Tailwind CSS
- **Animations**: Framer Motion
- **Build Tool**: Vite
- **HTTP Client**: Axios

### Backend
- **Framework**: Flask
- **Language**: Python 3.8+
- **Deep Learning**: PyTorch
- **Computer Vision**: OpenCV
- **CORS**: Flask-CORS

### AI Model
- **Architecture**: ResNet50 with Transfer Learning
- **Input Size**: 224x224 pixels
- **Classes**: Real / Fake
- **Framework**: PyTorch

## Project Structure

```
truth/
├── frontend/                 # React application
│   ├── src/
│   │   ├── components/      # Reusable components
│   │   │   ├── Navbar.jsx
│   │   │   ├── FileUpload.jsx
│   │   │   ├── ResultCard.jsx
│   │   │   └── LoadingSpinner.jsx
│   │   ├── pages/          # Page components
│   │   │   ├── Home.jsx
│   │   │   ├── ImageDetection.jsx
│   │   │   ├── VideoDetection.jsx
│   │   │   └── About.jsx
│   │   ├── utils/
│   │   │   └── api.js      # API calls
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css       # Custom styles
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── postcss.config.js
│
├── backend/                 # Flask application
│   ├── app.py              # Main Flask app
│   ├── train_model.py      # Model training script
│   ├── utils/
│   │   ├── model_handler.py   # Model loading and inference
│   │   └── preprocessing.py   # Image/video preprocessing
│   ├── uploads/            # Uploaded files storage
│   ├── requirements.txt     # Python dependencies
│   └── .env.example
│
├── models/                  # Trained models
│   └── deepfake_detector.pth  # Trained model checkpoint
│
└── README.md
```

## Installation

### Prerequisites
- **Node.js**: 16+
- **Python**: 3.8+
- **npm** or **yarn**

### Backend Setup

1. **Navigate to backend directory**
```bash
cd backend
```

2. **Create virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **(Optional) Train the model**
If you have a dataset organized as:
```
data/
  real/
    *.jpg
  fake/
    *.jpg
```

Train using:
```bash
python train_model.py --epochs 50 --batch-size 32
```

The trained model will be saved to `../models/deepfake_detector.pth`

5. **Start backend server**
```bash
python app.py
```

The backend will run on `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Start development server**
```bash
npm run dev
```

The frontend will run on `http://localhost:3000`

## Usage

1. **Open the application**
   - Navigate to `http://localhost:3000`

2. **Choose detection type**
   - Click "Image Detection" or "Video Detection"

3. **Upload media**
   - Drag and drop or click to select file
   - Supported formats:
     - Images: PNG, JPG, JPEG, GIF, BMP
     - Videos: MP4, AVI, MOV, MKV, FLV, WMV
     - Max size: 100MB

4. **View results**
   - Real/Fake classification
   - Confidence percentage
   - Detailed analysis explanation

## API Endpoints

### Health Check
```
GET /api/health
```
Returns server status and model status

### Image Detection
```
POST /api/detect-image
Content-Type: multipart/form-data

file: <binary image data>
```

**Response:**
```json
{
  "prediction": "Real|Fake",
  "confidence": 0.95,
  "explanation": "...",
  "file": "filename.jpg"
}
```

### Video Detection
```
POST /api/detect-video
Content-Type: multipart/form-data

file: <binary video data>
```

**Response:**
```json
{
  "prediction": "Real|Fake",
  "confidence": 0.87,
  "explanation": "...",
  "file": "filename.mp4"
}
```

## Model Details

### Architecture
- **Base Model**: ResNet50 (pre-trained on ImageNet)
- **Modifications**: Final layer replaced with binary classifier
- **Training**: Transfer learning with frozen early layers
- **Input Normalization**: ImageNet mean/std

### Input Requirements
- **Size**: 224×224 pixels
- **Format**: RGB
- **Preprocessing**: Normalization with ImageNet statistics

### Output
- **Classes**: 0 (Real), 1 (Fake)
- **Confidence**: Probability score (0-1)
- **Processing**:
  - Images: Single-pass inference
  - Videos: Multi-frame analysis with aggregated prediction

## Configuration

### Backend (.env)
```
FLASK_ENV=production
FLASK_DEBUG=False
CORS_ALLOWED_ORIGINS=http://localhost:3000
MAX_FILE_SIZE=104857600
UPLOAD_FOLDER=uploads
MODEL_PATH=models/deepfake_detector.pth
DEVICE=auto
API_HOST=0.0.0.0
API_PORT=5000
```

### Frontend
Update API URL in `src/utils/api.js` if backend runs on different host:
```javascript
const API_BASE_URL = 'http://localhost:5000/api'
```

## Performance

- **Inference Speed**: ~1-2 seconds per image (CPU), <500ms (GPU)
- **Video Analysis**: ~5-10 seconds for 1-minute video
- **Memory**: ~2GB for model + processing
- **Accuracy**: >90% on validation set (with proper training data)

## Troubleshooting

### Backend won't start
```bash
# Check if port 5000 is in use
lsof -i :5000  # macOS/Linux
netstat -ano | findstr :5000  # Windows

# Use different port
python app.py --port 8000
```

### Model not found
```bash
# Ensure model exists at: models/deepfake_detector.pth
# If not, train the model:
python train_model.py
```

### CORS errors
- Ensure backend CORS is configured for frontend origin
- Check `CORS_ALLOWED_ORIGINS` in backend configuration

### Out of memory
- Reduce batch size in model training
- Use GPU: ensure CUDA is properly installed
- Process smaller video chunks

## Future Enhancements

📋 **Planned Features**
- [ ] Live camera scanning
- [ ] Scan history and statistics
- [ ] Heatmap visualization for suspicious regions
- [ ] Batch processing API
- [ ] Model ensemble for improved accuracy
- [ ] Real-time streaming analysis
- [ ] Mobile app (React Native)
- [ ] Advanced explainability features
- [ ] Multi-language support

## Dataset Requirements

For training on custom data, organize as:
```
data/
  real/
    - Authentic photos/videos
  fake/
    - AI-generated or deepfake media
```

Recommended dataset sizes:
- **Minimum**: 500 images per class
- **Optimal**: 5000+ images per class

## License

This project is provided as-is for educational and research purposes.

## Support

For issues and feature requests, please create an issue in the repository.

## Disclaimer

This tool is designed to help detect AI-generated and deepfake content. While it provides high accuracy, no detection system is 100% perfect. Always use critical thinking and multiple verification methods for important decisions.

---

**Built with ❤️ for media authenticity**

**Version**: 1.0.0  
**Last Updated**: 2024
