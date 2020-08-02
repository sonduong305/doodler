from pydantic import BaseModel
from typing import Optional


class MachineLearningResponse(BaseModel):
    prediction: float


class HealthResponse(BaseModel):
    status: bool

class Stickman(BaseModel):
    data_input: str
