# API Documentation - TruthLens AI Scan

## Base URL
```
http://localhost:5000/api
```

## Authentication
Currently, the API does not require authentication. Implement OAuth2/JWT if needed for production.

---

## Endpoints

### 1. Health Check

**Endpoint**: `GET /health`

**Description**: Check if the backend server and model are running properly.

**Response**:
```json
{
  "status": "healthy",
  "device": "cuda",
  "model_loaded": true
}
```

**Status Codes**:
- 200: Server is healthy and ready

**Example Request**:
```bash
curl http://localhost:5000/api/health
```

---

### 2. Image Detection

**Endpoint**: `POST /detect-image`

**Description**: Upload an image and get AI detection results.

**Content-Type**: `multipart/form-data`

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| file | File | Yes | Image file (PNG, JPG, JPEG, GIF, BMP) |

**Request Example**:
```bash
curl -X POST \
  -F "file=@/path/to/image.jpg" \
  http://localhost:5000/api/detect-image
```

**Response** (Success):
```json
{
  "prediction": "Real",
  "confidence": 0.95,
  "explanation": "This image appears to be authentic with very high confidence (95.0%). No significant signs of AI manipulation or deepfake artifacts were detected in the analysis.",
  "file": "image.jpg"
}
```

**Response** (Failure):
```json
{
  "message": "Invalid file type. Allowed: PNG, JPG, JPEG, GIF, BMP"
}
```

**Status Codes**:
- 200: Success
- 400: Bad request (missing file, invalid type)
- 413: File too large (>100MB)
- 500: Server error

**Response Fields**:
| Field | Type | Description |
|-------|------|-------------|
| prediction | string | "Real" or "Fake" |
| confidence | float | 0.0 to 1.0 (confidence score) |
| explanation | string | Human-readable analysis result |
| file | string | Original filename |

**Supported Image Formats**:
- JPEG (JPG, JPEG)
- PNG
- GIF
- BMP
- WebP

**File Size Limits**:
- Maximum: 100 MB

---

### 3. Video Detection

**Endpoint**: `POST /detect-video`

**Description**: Upload a video and get AI detection results by analyzing multiple frames.

**Content-Type**: `multipart/form-data`

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| file | File | Yes | Video file (MP4, AVI, MOV, MKV, FLV, WMV) |

**Request Example**:
```bash
curl -X POST \
  -F "file=@/path/to/video.mp4" \
  http://localhost:5000/api/detect-video
```

**Response** (Success):
```json
{
  "prediction": "Fake",
  "confidence": 0.87,
  "explanation": "This video is likely AI-generated or a deepfake (87.0% confidence). Several indicators suggest the presence of synthetic or manipulated content.",
  "file": "video.mp4"
}
```

**Response** (Failure):
```json
{
  "message": "Invalid file type. Allowed: MP4, AVI, MOV, MKV, FLV, WMV"
}
```

**Status Codes**:
- 200: Success
- 400: Bad request (missing file, invalid type)
- 413: File too large (>100MB)
- 500: Server error

**Response Fields**:
Same as Image Detection

**Supported Video Formats**:
- MP4 (H.264, H.265)
- AVI
- MOV
- MKV
- FLV
- WMV

**Processing Details**:
- Extracts 10 frames at regular intervals
- Processes each frame independently
- Aggregates predictions (average)
- Total processing time: 5-15 seconds

---

## Response Format

### Success Response
```json
{
  "prediction": "Real|Fake",
  "confidence": 0.0-1.0,
  "explanation": "Detailed explanation...",
  "file": "filename"
}
```

### Error Response
```json
{
  "message": "Error description",
  "status": "error",
  "code": 400
}
```

---

## Error Handling

### Common Error Codes

| Status | Message | Solution |
|--------|---------|----------|
| 400 | No file provided | Ensure file is attached |
| 400 | No file selected | Select a file before uploading |
| 400 | Invalid file type | Check file format |
| 413 | File too large | Use file <100MB |
| 500 | Error processing image/video | Check file integrity, retry |

---

## Rate Limiting

Currently not implemented. For production, implement:
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)
```

---

## CORS Configuration

**Allowed Origins** (Configurable in `.env`):
```
CORS_ALLOWED_ORIGINS=http://localhost:3000,https://yourdomain.com
```

**Allowed Methods**: GET, POST, OPTIONS

**Allowed Headers**: Content-Type, Authorization

---

## Request/Response Examples

### Example 1: Image Detection

**Request**:
```bash
curl -X POST \
  -F "file=@photo.jpg" \
  -H "Accept: application/json" \
  http://localhost:5000/api/detect-image \
  -v
```

**Response Headers**:
```
HTTP/1.1 200 OK
Content-Type: application/json
Access-Control-Allow-Origin: http://localhost:3000
Content-Length: 285
```

**Response Body**:
```json
{
  "prediction": "Real",
  "confidence": 0.92,
  "explanation": "This image is likely authentic (92.0% confidence), though some minor artifacts were detected. Further manual inspection may be recommended.",
  "file": "photo.jpg"
}
```

---

### Example 2: Video Detection

**Request**:
```bash
curl -X POST \
  -F "file=@video.mp4" \
  http://localhost:5000/api/detect-video \
  -v
```

**Response**:
```json
{
  "prediction": "Real",
  "confidence": 0.85,
  "explanation": "This video is likely authentic (85.0% confidence). The analysis shows minimal indicators of AI generation or manipulation.",
  "file": "video.mp4"
}
```

---

## Client Integration

### JavaScript (Fetch API)

```javascript
async function detectImage(file) {
  const formData = new FormData()
  formData.append('file', file)
  
  const response = await fetch(
    'http://localhost:5000/api/detect-image',
    {
      method: 'POST',
      body: formData
    }
  )
  
  if (!response.ok) {
    throw new Error('Detection failed')
  }
  
  return await response.json()
}

// Usage
const input = document.querySelector('input[type="file"]')
const file = input.files[0]

detectImage(file)
  .then(result => console.log('Result:', result))
  .catch(error => console.error('Error:', error))
```

### JavaScript (Axios)

```javascript
import axios from 'axios'

const API_URL = 'http://localhost:5000/api'

async function detectImage(file) {
  const formData = new FormData()
  formData.append('file', file)
  
  const response = await axios.post(
    `${API_URL}/detect-image`,
    formData,
    {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    }
  )
  
  return response.data
}

// Usage
try {
  const result = await detectImage(file)
  console.log('Prediction:', result.prediction)
  console.log('Confidence:', result.confidence)
} catch (error) {
  console.error('Error:', error.response?.data?.message)
}
```

### Python (Requests)

```python
import requests

API_URL = 'http://localhost:5000/api'

def detect_image(image_path):
    with open(image_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(
            f'{API_URL}/detect-image',
            files=files
        )
    
    return response.json()

# Usage
result = detect_image('image.jpg')
print(f"Prediction: {result['prediction']}")
print(f"Confidence: {result['confidence']:.2%}")
```

### Python (cURL)

```bash
# Image
curl -X POST \
  -F "file=@image.jpg" \
  http://localhost:5000/api/detect-image | jq

# Video
curl -X POST \
  -F "file=@video.mp4" \
  http://localhost:5000/api/detect-video | jq \
  '.confidence'  # Extract just confidence
```

---

## Performance Notes

- **Image Processing**: 1-2 seconds per image (CPU), <500ms (GPU)
- **Video Processing**: 5-10 seconds per minute of video
- **Model Size**: ~100MB
- **GPU Memory**: ~2GB (with batch processing)
- **CPU Requirements**: 2+ cores, 4GB RAM recommended

---

## Versioning

**Current Version**: 1.0.0

**API Version in URL** (Future):
```
/api/v1/detect-image
/api/v2/detect-image
```

---

## Security Best Practices

1. **Always use HTTPS in production**
2. **Implement rate limiting**
3. **Validate file types (magic number check)**
4. **Sanitize filenames**
5. **Set appropriate CORS policies**
6. **Use authentication/authorization**
7. **Log all API requests**
8. **Implement request timeout**

---

## Changelog

### v1.0.0 (Initial Release)
- Image detection endpoint
- Video detection endpoint
- Health check endpoint
- CORS support
- Error handling

### Future Features
- Batch processing endpoint
- API key authentication
- Request signature verification
- Webhook notifications
- Result export formats (CSV, JSON)

---

## Support

For issues or questions:
- Check logs: `backend/logs/`
- Run diagnostics: `python check_setup.py`
- Test API: `python test_api.py`

---

**API Documentation Version**: 1.0  
**Last Updated**: 2024
