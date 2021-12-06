from os import getenv 
from dotenv import load_dotenv

load_dotenv()

DEVICE = getenv('DEVICE')
MODEL_PATH = "weights/yolov5_m.pt"
DETECTION_THRESHOLD = 0.5
MIN_ROI = 600
