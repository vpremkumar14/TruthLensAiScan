import torch
import cv2
import numpy as np

class GradCAM:
    def __init__(self, model, target_layer):
        self.model = model
        self.target_layer = target_layer
        self.gradients = None
        self.feature_maps = None

        target_layer.register_forward_hook(self.forward_hook)
        target_layer.register_backward_hook(self.backward_hook)

    def forward_hook(self, module, input, output):
        self.feature_maps = output

    def backward_hook(self, module, grad_input, grad_output):
        self.gradients = grad_output[0]

    def generate(self, input_tensor, class_idx):
        self.model.zero_grad()

        output = self.model(input_tensor)
        output[0, class_idx].backward()

        gradients = self.gradients[0]
        feature_maps = self.feature_maps[0]

        weights = torch.mean(gradients, dim=(1, 2))

        cam = torch.zeros(feature_maps.shape[1:], dtype=torch.float32)

        for i, w in enumerate(weights):
            cam += w * feature_maps[i]

        cam = cam.detach().cpu().numpy()
        cam = np.maximum(cam, 0)
        cam = cv2.resize(cam, (224, 224))

        if cam.max() != 0:
            cam = cam / cam.max()

        return cam