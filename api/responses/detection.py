from pydantic import BaseModel
from typing import Optional, List

class DetectionBoxModel(BaseModel):
    xmin: float
    ymin: float
    xmax: float
    ymax: float

class DetectionModel(BaseModel):
    detection_boxes: List[DetectionBoxModel]
    detection_classes: List[str]
    detection_scores: List[float]

class ResponseModel(BaseModel):
    success: bool
    detection: Optional[DetectionModel]