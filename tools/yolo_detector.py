import torch

class YoloDetector():
    def __init__(self, weights, device):
        self.device = torch.device(device)
        self.model = self._load_model(weights)

    def _load_model(self, weights):
        model = torch.hub.load("detection/yolov5", "custom", path=weights,
                               source="local", force_reload=True)
        model.to(self.device)
        print("[INFO] Loaded YOLOv5 model")
        return model
    
    def detect(self, image):
        return self.model(image)