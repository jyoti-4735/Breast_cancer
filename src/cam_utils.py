import torch 
import torch.nn.functional as F 
import numpy as np 
import cv2

class GradCAM: 
    def init(self, model, target_layer): 
        self.model = model.eval() 
        self.target_layer = target_layer
        self.gradients = None
        self.activations = None

    
        self.target_layer.register_forward_hook(self.save_activation)
        self.target_layer.register_full_backward_hook(self.save_gradient)

def save_activation(self, module, input, output):
    self.activations = output.detach()

def save_gradient(self, module, grad_input, grad_output):
    self.gradients = grad_output[0].detach()

def generate(self, input_tensor, class_idx=None):
    output = self.model(input_tensor)

    if class_idx is None:
        class_idx = output.argmax(dim=1).item()

    self.model.zero_grad()
    class_score = output[0, class_idx]
    class_score.backward()

    # Global Average Pooling
    pooled_gradients = torch.mean(self.gradients, dim=[0, 2, 3])

    # Weight the activations
    for i in range(self.activations.shape[1]):
        self.activations[:, i, :, :] *= pooled_gradients[i]

    # Compute the heatmap
    heatmap = torch.mean(self.activations, dim=1).squeeze()
    heatmap = torch.nn.functional.relu(heatmap)
    heatmap /= torch.max(heatmap)
    return heatmap.cpu().numpy()
def overlay_heatmap_on_image(heatmap, image_np, alpha=0.5, colormap=cv2.COLORMAP_JET): 
    heatmap = cv2.resize(heatmap, (image_np.shape[1], image_np.shape[0])) 
    heatmap = np.uint8(255 * heatmap) 
    heatmap_color = cv2.applyColorMap(heatmap, colormap) 
    overlay = cv2.addWeighted(image_np, 1 - alpha, heatmap_color, alpha, 0) 
    return overlay