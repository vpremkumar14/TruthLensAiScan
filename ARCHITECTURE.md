# TruthLens AI Scan - Architecture & Deployment Guide

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   Frontend (React + Vite)                   │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │     Home     │  │   Image      │  │    Video     │      │
│  │     Page     │  │  Detection   │  │  Detection   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │   Navbar    │  │  ResultCard │  │  FileUpload │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
│                                                              │
│           Tailwind CSS + Framer Motion                      │
└──────────────────────────────────────────────────────────────┘
                            ↓ (Axios)
┌─────────────────────────────────────────────────────────────┐
│                  Backend (Flask + Python)                   │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │            Flask REST API                            │  │
│  │  - /api/health                                       │  │
│  │  - /api/detect-image                                 │  │
│  │  - /api/detect-video                                 │  │
│  └──────────────────────────────────────────────────────┘  │
│                            ↓                                 │
│  ┌──────────────────────────────────────────────────────┐  │
│  │        Model Handler & Inference Engine             │  │
│  │  - Model Loading                                    │  │
│  │  - Preprocessing                                    │  │
│  │  - Batch Inference                                  │  │
│  │  - Post-processing                                  │  │
│  └──────────────────────────────────────────────────────┘  │
│                            ↓                                 │
│  ┌──────────────────────────────────────────────────────┐  │
│  │           Deep Learning Model                        │  │
│  │                                                      │  │
│  │  ┌────────────────────────────────────────────────┐ │  │
│  │  │        ResNet50 (Pre-trained)                 │ │  │
│  │  │                                                │ │  │
│  │  │  Input: 224×224×3 RGB Image                  │ │  │
│  │  │  Layers: 50 convolutional + batch norm       │ │  │
│  │  │  Output: 2-class softmax (Real/Fake)         │ │  │
│  │  │                                                │ │  │
│  │  │  Features:                                     │ │  │
│  │  │  - Transfer learning (ImageNet pre-trained)  │ │  │
│  │  │  - Frozen early layers                        │ │  │
│  │  │  - Fine-tuned final layer                     │ │  │
│  │  └────────────────────────────────────────────────┘ │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                 │
│  │  OpenCV  │  │ PyTorch  │  │  PIL    │                 │
│  │  Video   │  │  Model   │  │  Image  │                 │
│  │ Processing│  │ Inference│  │Processing│                │
│  └──────────┘  └──────────┘  └──────────┘                 │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                   Storage & Files                           │
│                                                              │
│  /uploads          - Temporary uploaded files              │
│  /models           - Trained model checkpoints             │
│  /data             - Training dataset                      │
└─────────────────────────────────────────────────────────────┘
```

## Technology Stack Details

### Frontend (Client-side)

**React 18**
- Component-based UI with JSX
- React Router for page navigation
- Hooks for state management (useState, useEffect)

**Vite**
- Lightning-fast build tool
- HMR (Hot Module Replacement) for development
- Optimized production builds

**Tailwind CSS**
- Utility-first CSS framework
- Dark theme configuration
- Responsive design utilities
- Custom animations and effects

**Framer Motion**
- Animation library for React
- Smooth transitions and keyframe animations
- Gesture support
- Stagger animations

**Axios**
- HTTP client for API requests
- Built-in error handling
- Request/response interceptors
- FormData support for file uploads

### Backend (Server-side)

**Flask**
- Lightweight WSGI web framework
- RESTful API endpoints
- Middleware and hooks
- Built-in development server

**Flask-CORS**
- Cross-Origin Resource Sharing
- Allow frontend from different origin
- Configurable allowed origins

**PyTorch**
- Deep learning framework
- GPU acceleration support
- Model loading and inference
- Tensor operations and optimization

**OpenCV**
- Computer vision library
- Video frames extraction
- Image manipulation
- Frame rate control

**Pillow (PIL)**
- Image processing
- Format conversion
- Resizing and transformations

### AI Model

**ResNet50**
- 50-layer residual neural network
- Pre-trained on ImageNet (14M images)
- Transfer learning approach
- Superior feature extraction

**Model Specifications**
```
Input:  224×224×3 RGB Image
Layers: 
  - Conv2d (7×7, stride 2) → ReLU
  - BatchNorm, MaxPool
  - Residual blocks (4 stages)
  - Global Average Pooling
  - Fully Connected (1000 → 2)
  - Softmax
Output: [P(Real), P(Fake)]
```

## Data Flow

### Image Detection Flow

```
User Upload
    ↓
Frontend FileUpload Component
    ↓
FormData with file
    ↓
axios POST /api/detect-image
    ↓
Backend receives FormData
    ↓
Save file to /uploads
    ↓
Load image with PIL
    ↓
Resize to 224×224
    ↓
Normalize (ImageNet stats)
    ↓
Convert to torch.Tensor
    ↓
ResNet50 Inference
    ↓
softmax(logits) → [0.8, 0.2]
    ↓
argmax → prediction (0=Real)
    ↓
Generate explanation
    ↓
JSON response
    ↓
Display in ResultCard
```

### Video Detection Flow

```
User Upload (MP4, AVI, etc.)
    ↓
Save file to /uploads
    ↓
OpenCV VideoCapture
    ↓
Calculate total frames
    ↓
Sample 10 frames evenly
    ↓
Loop through frames:
  - Read frame (BGR)
  - Convert to RGB
  - Resize to 224×224
  - Normalize
  - Model inference
  - Collect predictions
    ↓
Aggregate predictions (average)
    ↓
Final prediction & confidence
    ↓
Generate explanation
    ↓
JSON response
    ↓
Display in ResultCard with video preview
```

## Installation & Deployment

### Local Development Setup

**Backend**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

**Frontend**
```bash
cd frontend
npm install
npm run dev
```

### Production Deployment

**Option 1: Docker Compose**
```bash
docker-compose up -d
```

**Option 2: Cloud Platforms**

**Heroku**
```bash
git push heroku main
```

**AWS Lambda + API Gateway**
- Serverless Flask with Zappa
- S3 bucket for file storage
- CloudFront for frontend CDN

**Google Cloud Run**
- Container-based deployment
- Auto-scaling
- Load balancing

**Azure**
- App Service for Flask backend
- Azure Storage for uploads
- Static Web Apps for React frontend

### Environment Variables

**Backend (.env)**
```
FLASK_ENV=production
FLASK_DEBUG=False
CORS_ALLOWED_ORIGINS=https://yourdomain.com
MAX_FILE_SIZE=104857600
UPLOAD_FOLDER=/tmp/uploads
MODEL_PATH=/models/deepfake_detector.pth
DEVICE=cuda
API_PORT=5000
```

**Frontend (.env.local)**
```
VITE_API_URL=https://api.yourdomain.com
```

## Model Training

### Dataset Preparation

```
data/
  real/
    ├── img_001.jpg (authentic images)
    ├── img_002.jpg
    └── ... (500+ images)
  fake/
    ├── gen_001.jpg (AI-generated images)
    ├── gen_002.jpg
    └── ... (500+ images)
```

### Training Process

```bash
python train_model.py \
  --epochs 50 \
  --batch-size 32 \
  --lr 0.001 \
  --data-dir data
```

**Configuration**
- Optimizer: Adam (lr=0.001)
- Loss: CrossEntropyLoss
- Scheduler: StepLR (step=10, gamma=0.1)
- Augmentation: Random flip, rotation (±10°)
- Train/Val Split: 80/20

**Output**
- Model: `models/deepfake_detector.pth`
- History: `models/deepfake_detector_history.json`

## Performance Optimization

### Backend Optimization

**Model Inference**
- Batch processing support
- GPU acceleration (CUDA)
- Half precision (FP16) for faster inference
- Model quantization option

**Caching**
- Cache preprocessed images
- Cache model predictions
- Redis for distributed caching

**Scaling**
- Gunicorn workers (multiprocessing)
- Load balancing
- Horizontal scaling with multiple instances

### Frontend Optimization

**Bundle Size**
- Code splitting with React.lazy
- Tree shaking (unused code removal)
- Minification and compression
- Image optimization

**Performance**
- Lazy loading components
- Memoization (React.memo)
- Virtualization for large lists
- Service workers for offline support

## Security Considerations

### Backend Security

**Input Validation**
- File type validation (magic number check)
- File size limits (100MB max)
- Filename sanitization
- Content-Type verification

**API Security**
- CORS configuration
- Rate limiting
- Request timeout
- SQL injection prevention (N/A for this app)

**Model Security**
- Model integrity verification
- Adversarial attack resistance
- Input bounds checking

### Frontend Security

**Output Sanitization**
- XSS prevention
- Safe DOM manipulation
- Content Security Policy headers

**Data Protection**
- HTTPS only in production
- Secure cookie handling
- No sensitive data in localStorage

## Monitoring & Logging

### Backend Logging

```python
import logging

logger = logging.getLogger(__name__)
logger.info(f"Processing file: {filename}")
logger.error(f"Model error: {e}")
```

### Metrics to Track

- Request count per endpoint
- Average inference time
- Model accuracy
- Error rates
- File upload sizes
- GPU memory usage

### Observability Stack

**Option 1: Open Source**
- Prometheus (metrics)
- Grafana (visualization)
- ELK Stack (logging)

**Option 2: Cloud Services**
- CloudWatch (AWS)
- Application Insights (Azure)
- Stackdriver (GCP)

## Cost Estimation

### Infrastructure (Monthly)

| Component | Cost |
|-----------|------|
| Server (2 vCPU, 4GB RAM) | $10-20 |
| GPU (optional) | $50-200 |
| Storage (uploads) | $1-5 |
| Bandwidth | $0.00-10 |
| **Total** | **$11-235** |

### Optimization Tips

- Use spot instances for training
- S3 lifecycle policies for cleanup
- CDN for frontend caching
- Lambda for occasional tasks

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Port in use | Change port or kill process |
| CUDA OOM | Reduce batch size or use CPU |
| Slow inference | Enable GPU, check model size |
| CORS errors | Update CORS_ALLOWED_ORIGINS |
| Model not found | Run `python create_model.py` |
| Dependencies missing | `pip install -r requirements.txt` |

## Future Enhancements

1. **Ensemble Models**
   - Combine multiple models
   - Majority voting
   - Stacking

2. **Real-time Processing**
   - WebSocket for live updates
   - Streaming video analysis
   - Progressive results

3. **Advanced Features**
   - Heatmap visualization
   - Attention maps
   - Feature extraction
   - Similarity search

4. **Scalability**
   - Message queue (Celery)
   - Distributed training
   - Model serving (TorchServe)
   - Microservices architecture

---

**Document Version**: 1.0  
**Last Updated**: 2024
