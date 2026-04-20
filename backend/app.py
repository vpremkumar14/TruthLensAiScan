from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import cv2
import numpy as np

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print("🚀 Using device:", device)

# ================= MODEL =================
class DeepfakeModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.model = models.resnet50(weights=None)
        self.model.fc = nn.Linear(self.model.fc.in_features, 2)

    def forward(self, x):
        return self.model(x)

model = DeepfakeModel()
model.load_state_dict(torch.load('deepfake_detector.pth', map_location=device))
model.to(device)
model.eval()

print("✅ Model Loaded")

# ================= TRANSFORM =================
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485,0.456,0.406],
                         [0.229,0.224,0.225])
])

# ================= GRADCAM =================
class GradCAM:
    def __init__(self, model, target_layer):
        self.model = model
        self.gradients = None
        self.activations = None

        target_layer.register_forward_hook(self.forward_hook)
        target_layer.register_backward_hook(self.backward_hook)

    def forward_hook(self, module, input, output):
        self.activations = output

    def backward_hook(self, module, grad_input, grad_output):
        self.gradients = grad_output[0]

    def generate(self, x, class_idx):
        self.model.zero_grad()
        output = self.model(x)
        output[0, class_idx].backward()

        grads = self.gradients[0]
        acts = self.activations[0]

        weights = torch.mean(grads, dim=(1,2))
        cam = torch.zeros(acts.shape[1:], dtype=torch.float32)

        for i, w in enumerate(weights):
            cam += w * acts[i]

        cam = cam.detach().cpu().numpy()
        cam = np.maximum(cam, 0)
        cam = cv2.resize(cam, (224,224))

        if cam.max() != 0:
            cam = cam / cam.max()

        return cam

gradcam = GradCAM(model.model, model.model.layer4)

# ================= EXPLANATION =================
def generate_explanation(label, confidence):
    text = []

    if confidence > 0.9:
        text.append("The model is highly confident in its prediction.")
    else:
        text.append("The model has moderate confidence.")

    if label == "Fake":
        text.append("Manipulation patterns detected in facial regions such as eyes, mouth, and texture.")
        text.append("These inconsistencies are typical of AI-generated or deepfake content.")
    else:
        text.append("No manipulation patterns detected.")
        text.append("Facial features and textures appear natural and consistent.")

    return " ".join(text)

# ================= IMAGE =================
def predict_image(path, filename):
    img = Image.open(path).convert("RGB")
    tensor = transform(img).unsqueeze(0).to(device)

    output = model(tensor)
    probs = torch.softmax(output, dim=1)

    real = probs[0][0].item()
    fake = probs[0][1].item()

    if real > fake:
        label = "Real"
        conf = real
        idx = 0
    else:
        label = "Fake"
        conf = fake
        idx = 1

    cam = gradcam.generate(tensor, idx)

    heatmap = cv2.applyColorMap(np.uint8(255 * cam), cv2.COLORMAP_JET)

    original = cv2.imread(path)
    original = cv2.resize(original, (224,224))

    overlay = heatmap * 0.4 + original

    out_path = f"uploads/explain_{filename}"
    cv2.imwrite(out_path, overlay)

    explanation = generate_explanation(label, conf)

    return label, conf, out_path, explanation

# ================= VIDEO =================
def predict_video(path, filename):
    cap = cv2.VideoCapture(path)

    frames = []
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if total == 0:
        return "Error", 0.0, None, None

    step = max(1, total // 5)

    for i in range(0, total, step):
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        ret, frame = cap.read()

        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frames.append(frame)

    cap.release()

    if len(frames) == 0:
        return "Error", 0.0, None, None

    best_frame = None
    best_tensor = None
    best_conf = 0
    best_idx = 0

    real_scores = []
    fake_scores = []

    for frame in frames:
        img = Image.fromarray(frame)
        tensor = transform(img).unsqueeze(0).to(device)

        with torch.no_grad():
            output = model(tensor)
            probs = torch.softmax(output, dim=1)

        real = probs[0][0].item()
        fake = probs[0][1].item()

        real_scores.append(real)
        fake_scores.append(fake)

        conf = max(real, fake)

        if conf > best_conf:
            best_conf = conf
            best_frame = frame
            best_tensor = tensor
            best_idx = 0 if real > fake else 1

    avg_real = sum(real_scores) / len(real_scores)
    avg_fake = sum(fake_scores) / len(fake_scores)

    final_label = "Real" if avg_real > avg_fake else "Fake"
    final_conf = max(avg_real, avg_fake)

    cam = gradcam.generate(best_tensor, best_idx)

    heatmap = cv2.applyColorMap(np.uint8(255 * cam), cv2.COLORMAP_JET)

    frame_bgr = cv2.cvtColor(best_frame, cv2.COLOR_RGB2BGR)
    frame_bgr = cv2.resize(frame_bgr, (224,224))

    overlay = heatmap * 0.4 + frame_bgr

    out_path = f"uploads/video_explain_{filename}.jpg"
    cv2.imwrite(out_path, overlay)

    explanation = generate_explanation(final_label, final_conf)

    return final_label, final_conf, out_path, explanation

# ================= ROUTES =================
@app.route('/')
def home():
    return "🚀 TruthLens AI Backend Running"

@app.route('/uploads/<filename>')
def serve_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/api/detect-image', methods=['POST'])
def detect_image():
    file = request.files['file']
    filename = secure_filename(file.filename)
    path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(path)

    label, conf, img_path, explanation = predict_image(path, filename)

    return jsonify({
        "prediction": label,
        "confidence": float(conf),
        "explanation": explanation,
        "explanation_image": img_path
    })

@app.route('/api/detect-video', methods=['POST'])
def detect_video():
    file = request.files['file']
    filename = secure_filename(file.filename)
    path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(path)

    label, conf, img_path, explanation = predict_video(path, filename)

    return jsonify({
        "prediction": label,
        "confidence": float(conf),
        "explanation": explanation,
        "explanation_image": img_path
    })

# ================= MAIN =================
if __name__ == '__main__':
    print("🔥 Starting TruthLens Server...")
    app.run(debug=True)