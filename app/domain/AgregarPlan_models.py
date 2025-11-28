from pydantic import BaseModel, Field
from typing import List, Optional, Annotated

class PlanBase(BaseModel):
    id_tipoHabitacion: int
    nombre: str
    precio: Annotated[int, Field(gt=0)]
    serviciosIncluidos: List[str]

class PlanCreate(PlanBase):
    pass

class PlanUpdate(BaseModel):
    nombre: Optional[str] = None
    precio: Optional[Annotated[int, Field(gt=0)]] = None
    serviciosIncluidos: Optional[List[str]] = None

class PlanResponse(BaseModel):
    success: bool
    mensaje: str
    data: Optional[PlanBase] = None

class ErrorResponse(BaseModel):
    success: bool
    error_code: str
    mensaje: str
    details: Optional[dict] = None
