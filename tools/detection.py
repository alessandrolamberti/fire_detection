import cv2 
import numpy as np
import time
from config import *
import torch
from os import environ

class YoloDetector():
    def __init__(self, weights, device):
        environ["CUDA_VISIBLE_DEVICES"] = "-1"
        self.device = torch.device('cpu')
        self.model = self._load_model(weights)

    def _load_model(self, weights):
        model = torch.hub.load("detection/yolov5", "custom", path=weights,
                               source="local", force_reload=True)
        model.to('cpu')
        print("[INFO] Loaded YOLOv5 model")
        return model
    
    def detect(self, image):
        return self.model(image)

model = YoloDetector(MODEL_PATH, DEVICE)

def preprocess(image, size=(320, 320)):
    start = time.time()
    original_image = cv2.imdecode(np.frombuffer(image, np.uint8), cv2.IMREAD_COLOR)
    resized_image = cv2.resize(original_image, size)
    print("Preprocess time: {}".format(time.time() - start))
    return resized_image

def normalize_bbox(bbox, size):
    xmin, ymin, xmax, ymax = bbox
    xmin = xmin / size[0]
    xmax = xmax / size[0]
    ymin = ymin / size[1]
    ymax = ymax / size[1]
    return xmin, ymin, xmax, ymax

def run_detector(image, threshold, min_area):
    start = time.time()
    results = model.detect(image)
    print("Detection time: {}".format(time.time() - start))

    boxes = []
    scores = []
    classes = []

    for detection in results.xyxy[0]:
        *bbox, confidence, label = detection
        ROI_area = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1])

        bbox = normalize_bbox(bbox, image.shape[:2])

        if confidence > threshold and ROI_area > min_area:
            box = {"xmin": float(bbox[0]), "ymin": float(bbox[1]),
                   "xmax": float(bbox[2]), "ymax": float(bbox[3])}
            boxes.append(box)
            scores.append(float(confidence))
            classes.append(ORGANIZATIONS[int(label)])
        
    print(f"Found {len(boxes)} objects")
    
    return boxes, classes, scores