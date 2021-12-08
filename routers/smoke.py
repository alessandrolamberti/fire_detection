from typing import Optional
from starlette.requests import Request
from fastapi.param_functions import Query
from fastapi import APIRouter, File, HTTPException

from responses import ResponseModel
from tools import preprocess, run_detector
from config import *

router = APIRouter()

@router.post("/smoke", response_model=ResponseModel)
async def detect_smoke(request: Request, image: bytes = File(..., description="Image to be analyzed"),
                        detection_threshold: Optional[float] = Query(DETECTION_THRESHOLD, description="Detection threshold"),
                        min_area: Optional[int] = Query(MIN_ROI, description="Minimum area of ROI")):
    """
    Detects if smoke is present in the image.
    """

    data = {"success": False}
    if request.method == "POST":
        content_type = request._form['image'].content_type
        if content_type not in ALLOWED_FILE_EXTENSIONS:
            data["message"] = "File must be one of {}".format(", ".join(ALLOWED_FILE_EXTENSIONS))
            raise HTTPException(
                status_code=400, detail=data)
        
    resized_image = preprocess(image, width=320)
    boxes, classes, scores = run_detector(resized_image, threshold=detection_threshold, min_area=min_area)

    detection = {
        "detection_boxes": boxes,
        "detection_classes": classes,
        "detection_scores": scores
    }

    data["detection"] = detection

    data["success"] = True

    return data