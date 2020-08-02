import base64
from typing import Any

import cv2
from fastapi import APIRouter, HTTPException, Body
import joblib
from loguru import logger

from core.errors import PredictException
from helpers import string_to_image
from models.prediction import HealthResponse, MachineLearningResponse, Stickman
from services.predict import MachineLearningModelHandlerScore as model
from services.stickman import Stick


router = APIRouter()

# TODO: Change 'load_wrapper' and 'method'  based on your model.pkl.
get_prediction = lambda data_input: MachineLearningResponse(
    model.predict(data_input, load_wrapper=joblib.load, method="predict_proba")
)


@router.get("/predict", response_model=MachineLearningResponse, name="predict:get-data")
async def predict(data_input: Any = None):
    if not data_input:
        raise HTTPException(status_code=404, detail=f"'data_input' argument invalid!")
    try:
        prediction = get_prediction(data_input)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Exception: {e}")

    return MachineLearningResponse(prediction=prediction)

@router.post("/stickman")
async def stickman(stickman: Stickman):
    if not stickman:
        raise HTTPException(status_code=404, detail=f"'data_input' argument invalid!")
    try:
        data_input = stickman.data_input
        pil_img = string_to_image(data_input)
        stick = Stick()
        stick.get_image(pil_img)
        await stick.process()
        string = base64.b64encode(cv2.imencode('.jpg', stick.output)[1]).decode()
        
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Exception: {e}")

    return {
        string
    }

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
