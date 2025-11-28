# app/domain/Plan_model.py
from pydantic import BaseModel
from typing import List

class PlanResponse(BaseModel):
    idPlan: int
    nombre: str
    precio: int
    serviciosIncluidos: List[str]

class PlanesResponse(BaseModel):
    success: bool
    message: str
    data: List[PlanResponse] = []

class ErrorResponse(BaseModel):
    success: bool
    error_code: str
    message: str
    details: dict = {}
