import cv2 
import numpy as np
import time
from yolo_detector import YoloDetector
from config import *

model = YoloDetector(MODEL_PATH)

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

def run_detector(image, threshold, min_roi):
    start = time.time()
    results = model.detect(image)
    print("Detection time: {}".format(time.time() - start))

    boxes = []
    scores = []
    labels = []

    for detection in results.xyxy[0]:
        *bbox, confidence, label = detection
        ROI_area = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1])

        bbox = normalize_bbox(bbox, image.shape[:2])

        if confidence > threshold and ROI_area > min_area:
            box = {"xmin": float(bbox[0]), "ymin": float(bbox[1]),
                   "xmax": float(bbox[2]), "ymax": float(bbox[3])}
            boxes.append(box)
            scores.append(float(confidence))
            labels.append(ORGANIZATIONS[int(label)])
        
    print(f"Found {len(boxes)} objects")
    
    return boxes, labels, scores