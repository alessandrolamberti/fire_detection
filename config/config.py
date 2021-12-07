from os import getenv 
from dotenv import load_dotenv

load_dotenv()

DEVICE = getenv('DEVICE')
MODEL_PATH = "weights/yolo_detector.pt"
DETECTION_THRESHOLD = 0.5
MIN_ROI = 600

ALLOWED_FILE_EXTENSIONS = ['.jpg', '.jpeg', '.png']
LABELS = ['smoke']

