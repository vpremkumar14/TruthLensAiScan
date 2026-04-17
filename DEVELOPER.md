# Developer Guide - TruthLens AI Scan

## Development Workflow

### Getting Started with Development

#### 1. Environment Setup

**Clone/Pull Repository**
```bash
# or navigate to the project folder
cd /path/to/truth
```

**Backend Development**
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start development server with auto-reload
python app.py
```

**Frontend Development**
```bash
cd frontend

# Install dependencies
npm install

# Start dev server with HMR
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### Project Structure

```
truth/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.jsx          # Navigation bar
│   │   │   ├── FileUpload.jsx      # Drag & drop upload
│   │   │   ├── ResultCard.jsx      # Results display
│   │   │   └── LoadingSpinner.jsx  # Loading animation
│   │   ├── pages/
│   │   │   ├── Home.jsx            # Landing page
│   │   │   ├── ImageDetection.jsx  # Image upload & analysis
│   │   │   ├── VideoDetection.jsx  # Video upload & analysis
│   │   │   └── About.jsx           # Project info
│   │   ├── utils/
│   │   │   └── api.js              # API client (Axios)
│   │   ├── App.jsx                 # Main component
│   │   ├── main.jsx                # App entry point
│   │   └── index.css               # Global styles
│   ├── index.html                  # HTML template
│   ├── package.json                # Dependencies
│   ├── vite.config.js              # Vite config
│   ├── tailwind.config.js          # Tailwind config
│   └── postcss.config.js           # PostCSS config
│
├── backend/
│   ├── app.py                      # Main Flask app
│   ├── config.py                   # Configuration
│   ├── train_model.py              # Training script
│   ├── create_model.py             # Initialize model
│   ├── check_setup.py              # System check
│   ├── test_api.py                 # API tests
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── model_handler.py        # Model loading & inference
│   │   └── preprocessing.py        # Image/video preprocessing
│   ├── data/                       # Training data directory
│   ├── uploads/                    # Uploaded files
│   ├── requirements.txt            # Python dependencies
│   └── .env.example                # Environment template
│
├── models/                         # Trained models
│   └── deepfake_detector.pth      # Main model checkpoint
│
├── README.md                       # Main documentation
├── QUICKSTART.md                   # Quick start guide
├── ARCHITECTURE.md                 # System architecture
├── DEVELOPER.md                    # This file
└── DOCKER.md                       # Docker setup
```

## Code Style & Best Practices

### Frontend (React + JavaScript)

**Component Structure**
```jsx
// src/components/MyComponent.jsx
import { useState } from 'react'
import { motion } from 'framer-motion'

const MyComponent = ({ prop1, prop2 }) => {
  const [state, setState] = useState(null)
  
  const handleClick = () => {
    setState(!state)
  }
  
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="glass rounded-lg p-4"
    >
      {/* Component JSX */}
    </motion.div>
  )
}

export default MyComponent
```

**Naming Conventions**
- Components: PascalCase (MyComponent.jsx)
- Functions: camelCase (handleSubmit)
- Constants: UPPER_SNAKE_CASE (API_BASE_URL)
- CSS classes: kebab-case (glass-effect)

**File Organization**
```
components/
  ├── Common/           # Reusable components
  │   ├── Button.jsx
  │   └── Card.jsx
  ├── Feature/          # Feature-specific
  │   ├── ImageUpload.jsx
  │   └── Results.jsx
  └── Layout/          # Layout components
      ├── Sidebar.jsx
      └── Header.jsx
```

### Backend (Python/Flask)

**Function Documentation**
```python
def detect_image(image_path, model, device='cpu'):
    """
    Predict if image is real or fake.
    
    Args:
        image_path (str): Path to image file
        model: Loaded PyTorch model
        device (str): Device to use ('cpu' or 'cuda')
    
    Returns:
        tuple: (prediction, confidence, explanation)
            - prediction (str): 'Real' or 'Fake'
            - confidence (float): 0.0 to 1.0
            - explanation (str): Human-readable explanation
    
    Raises:
        FileNotFoundError: If image not found
        ValueError: If image cannot be processed
    """
```

**Error Handling**
```python
try:
    image = Image.open(image_path).convert('RGB')
    # Process image
except FileNotFoundError:
    logger.error(f"Image not found: {image_path}")
    return None, 0.5, "File not found"
except Exception as e:
    logger.error(f"Error processing image: {e}")
    return None, 0.5, f"Processing error: {str(e)}"
```

**API Response Format**
```python
# Success response
{
  "status": "success",
  "prediction": "Real",
  "confidence": 0.95,
  "explanation": "...",
  "timestamp": "2024-01-15T10:30:00Z"
}

# Error response
{
  "status": "error",
  "message": "File too large",
  "code": 413
}
```

## Testing

### Frontend Testing

**Test Image Upload**
1. Navigate to `/image`
2. Click upload area
3. Select test image
4. Verify results display

**Test Video Upload**
1. Navigate to `/video`
2. Click upload area
3. Select test video
4. Verify results display

**Test Navigation**
- All navbar links work
- Home page CTA buttons redirect
- Mobile menu responsive

### Backend Testing

**Unit Tests**
```bash
cd backend

# Test model loading
python -c "from utils.model_handler import load_model; load_model()"

# Test API health
python test_api.py
```

**Integration Tests**
```bash
# With actual image
python test_api.py
# Then in test_api.py:
# test_image_detection('path/to/image.jpg')

# Start server
python app.py

# In another terminal
curl http://localhost:5000/api/health
```

**Load Testing**
```bash
# Using Apache Bench
ab -n 100 -c 10 http://localhost:5000/api/health

# Using wrk
wrk -t4 -c100 -d30s http://localhost:5000/api/health
```

## Adding New Features

### Adding a New API Endpoint

1. **Add route in app.py**
```python
@app.route('/api/new-endpoint', methods=['POST'])
def new_endpoint():
    try:
        # Implementation
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

2. **Add API client in frontend**
```javascript
// src/utils/api.js
export const newEndpoint = async (data) => {
  const response = await axios.post(
    `${API_BASE_URL}/new-endpoint`,
    data
  )
  return response.data
}
```

3. **Use in component**
```jsx
const handleClick = async () => {
  const result = await newEndpoint(data)
  setResult(result)
}
```

### Adding a New Page

1. **Create component**
```jsx
// src/pages/NewPage.jsx
import { motion } from 'framer-motion'

const NewPage = () => {
  return <div>New Page</div>
}

export default NewPage
```

2. **Add route**
```jsx
// src/App.jsx
import NewPage from './pages/NewPage'

<Route path="/new-page" element={<NewPage />} />
```

3. **Add navigation**
```jsx
// src/components/Navbar.jsx
<NavLink to="/new-page" label="New Page" />
```

### Adding a New Model

1. **Implement model class**
```python
# utils/models/new_model.py
import torch.nn as nn

class NewModel(nn.Module):
    def __init__(self):
        super().__init__()
        # Implementation
```

2. **Update model_handler.py**
```python
def load_model(model_type='resnet50', device='cpu'):
    if model_type == 'new_model':
        model = NewModel()
    # Load weights
    return model
```

3. **Update inference functions**
```python
def predict_image(image_path, model_type='resnet50'):
    model = load_model(model_type)
    # Predict with new model
```

## Debugging

### Frontend Debugging

**React DevTools**
- Install React Developer Tools browser extension
- Inspect component hierarchy
- View props and state

**Console Logging**
```javascript
console.log('Data:', data)      // Log objects
console.table(data)              // Log as table
console.error('Error:', error)  // Log errors
console.time('label')            // Measure performance
```

**Browser DevTools**
- Network tab: Monitor API calls
- Application tab: Check localStorage/cookies
- Console tab: Execute JavaScript

### Backend Debugging

**Python Debugging**
```python
import pdb; pdb.set_trace()  # Breakpoint

# Or use debugger in Flask
if __name__ == '__main__':
    app.run(debug=True)  # Auto-reload, debug mode
```

**Logging**
```python
import logging

logger = logging.getLogger(__name__)
logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
```

**Print Debugging**
```python
print(f"Image shape: {image.shape}")
print(f"Model output: {outputs}")
print(f"Prediction: {prediction}")
```

## Performance Optimization

### Frontend Optimization

**Code Splitting**
```javascript
const HeavyComponent = lazy(() => import('./HeavyComponent'))
```

**Memoization**
```javascript
const MyComponent = memo(({ data }) => {
  return <div>{data}</div>
})
```

**Image Optimization**
- Compress images
- Use WebP format
- Lazy load images

### Backend Optimization

**Model Optimization**
```python
# Quantization
model = torch.quantization.quantize_dynamic(
    model, {torch.nn.Linear}, dtype=torch.qint8
)

# Half precision
model.half()

# ONNX export
torch.onnx.export(model, dummy_input, 'model.onnx')
```

**Batch Processing**
```python
# Process multiple images at once
batch = torch.cat([img1, img2, img3])
predictions = model(batch)
```

## Common Issues & Solutions

| Problem | Solution |
|---------|----------|
| Module not found | Check PYTHONPATH, install requirements |
| Port already in use | Kill process or change port |
| CUDA OOM | Reduce batch size, use CPU |
| Slow model loading | Use GPU, quantize model |
| CORS errors | Check backend config |
| API timeout | Increase timeout, optimize inference |

## Resources

### Documentation
- [React Docs](https://react.dev)
- [PyTorch Docs](https://pytorch.org/docs)
- [Flask Docs](https://flask.palletsprojects.com)
- [Tailwind CSS](https://tailwindcss.com)
- [Framer Motion](https://www.framer.com/motion)

### Tutorials
- [ResNet50 Architecture](https://arxiv.org/abs/1512.03385)
- [Transfer Learning Guide](https://pytorch.org/tutorials/beginner/transfer_learning_tutorial.html)
- [Flask RESTful](https://flask-restful.readthedocs.io)
- [React Router](https://reactrouter.com)

### Tools
- [Visual Studio Code](https://code.visualstudio.com)
- [Chrome DevTools](https://developer.chrome.com/docs/devtools)
- [Postman](https://www.postman.com) - API Testing
- [PyCharm](https://www.jetbrains.com/pycharm) - Python IDE

---

**Happy coding!** 🚀
