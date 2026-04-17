from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import cv2

app = Flask(__name__)
CORS(app)

# =========================
# CONFIG
# =========================
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg'}
ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'avi', 'mov'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# =========================
# DEVICE
# =========================
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print("🚀 Using device:", device)

# =========================
# MODEL CLASS (IMPORTANT FIX)
# =========================
class DeepfakeModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.model = models.resnet50(weights=None)
        self.model.fc = nn.Linear(self.model.fc.in_features, 2)

    def forward(self, x):
        return self.model(x)

# =========================
# LOAD MODEL
# =========================
model = DeepfakeModel()
model.load_state_dict(torch.load('deepfake_detector.pth', map_location=device))
model.to(device)
model.eval()

print("✅ Model Loaded")

# =========================
# TRANSFORM
# =========================
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485,0.456,0.406],
                         [0.229,0.224,0.225])
])

# =========================
# HELPERS
# =========================
def allowed_file(filename, file_type):
    if '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    if file_type == 'image':
        return ext in ALLOWED_IMAGE_EXTENSIONS
    if file_type == 'video':
        return ext in ALLOWED_VIDEO_EXTENSIONS
    return False

# =========================
# PREDICT IMAGE (FINAL)
# =========================
def predict_image(filepath):
    img = Image.open(filepath).convert("RGB")
    img = transform(img).unsqueeze(0).to(device)

    with torch.no_grad():
        output = model(img)
        probs = torch.softmax(output, dim=1)

    real_prob = probs[0][0].item()
    fake_prob = probs[0][1].item()

    print("REAL:", real_prob, "FAKE:", fake_prob)

    # ✅ FINAL CORRECT LOGIC
    if real_prob > fake_prob:
        label = "Real ✅"
        confidence = real_prob
    else:
        label = "Fake ❌"
        confidence = fake_prob

    return label, confidence



def predict_video(filepath):
    cap = cv2.VideoCapture(filepath)
    frames = []

    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    step = max(1, total // 5)

    for i in range(0, total, step):
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frames.append(frame)

    cap.release()

    preds = []

    for frame in frames:
        img = Image.fromarray(frame)
        img = transform(img).unsqueeze(0).to(device)

        with torch.no_grad():
            output = model(img)
            _, pred = torch.max(output, 1)
            preds.append(pred.item())

    avg = sum(preds) / len(preds)

    label = "Fake ❌" if avg > 0.5 else "Real ✅"
    confidence = max(avg, 1 - avg)

    return label, confidence

# =========================
# ROUTES
# =========================
@app.route('/')
def home():
    return "🚀 TruthLens AI Backend Running"

@app.route('/api/detect-image', methods=['POST'])
def detect_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']

    if not allowed_file(file.filename, 'image'):
        return jsonify({'error': 'Invalid image format'}), 400

    filename = secure_filename(file.filename)
    path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(path)

    label, confidence = predict_image(path)

    return jsonify({
        'prediction': label,
        'confidence': float(confidence)
    })


@app.route('/api/detect-video', methods=['POST'])
def detect_video():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']

    if not allowed_file(file.filename, 'video'):
        return jsonify({'error': 'Invalid video format'}), 400

    filename = secure_filename(file.filename)
    path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(path)

    label, confidence = predict_video(path)

    return jsonify({
        'prediction': label,
        'confidence': float(confidence)
    })

# =========================
# MAIN
# =========================
if __name__ == '__main__':
    print("🔥 Starting TruthLens Server...")
    app.run(debug=True, host='0.0.0.0', port=5000)