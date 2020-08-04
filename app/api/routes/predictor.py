import base64
from typing import Any

import cv2
from fastapi import APIRouter, HTTPException, Body
import joblib
from loguru import logger

from core.errors import PredictException
from helpers import string_to_image
from models.prediction import HealthResponse, MachineLearningResponse, Stickman, DoodleResponse
from services.stickman import Stick
from services.mobilenet import model


router = APIRouter()


# @router.post("/stickman")
# async def stickman(stickman: Stickman):
#     if not stickman:
#         raise HTTPException(
#             status_code=404, detail=f"'data_input' argument invalid!")
#     try:
#         data_input = stickman.data_input
#         img = string_to_image(data_input)
#         stick = Stick()
#         stick.get_image(img)
#         await stick.process()
#         string = base64.b64encode(cv2.imencode(
#             '.jpg', stick.output)[1]).decode()

#     except Exception as e:
#         print(e)
#         raise HTTPException(status_code=500, detail=f"Exception: {e}")

#     return {
#         string
#     }


@router.post("/predict")
async def predict(doodle: Stickman):
    if not doodle:
        raise HTTPException(
            status_code=404, detail=f"'data_input' argument invalid!")
    try:
        data_input = doodle.data_input
        img = string_to_image(data_input)

        result, confident = model.predict(img)

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Exception: {e}")

    return DoodleResponse(result=result, confident=confident)


@router.get(
    "/health", response_model=HealthResponse, name="health:get-data",
)
async def health():
    is_health = False
    try:
        get_prediction("lorem ipsum")
        is_health = True
        return HealthResponse(status=is_health)
    except Exception:
        raise HTTPException(status_code=404, detail="Unhealthy")
