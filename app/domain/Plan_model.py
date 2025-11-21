from pydantic import BaseModel
from typing import List, Optional


class PlanResponse(BaseModel):
    idPlan: int
    nombre: str
    descripcion: str
    precio: int
    moneda: str = "COP"
    serviciosIncluidos: List[str]


class ResponsePlanList(BaseModel):
    success: bool
    message: str
    data: List[PlanResponse]


class ResponsePlanDetalle(BaseModel):
    success: bool
    message: str
    data: Optional[PlanResponse] = None
    error_code: Optional[str] = None
    details: Optional[dict] = None
