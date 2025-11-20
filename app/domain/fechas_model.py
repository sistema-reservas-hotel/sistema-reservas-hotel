from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class FechaItem(BaseModel):
    fecha: datetime

class DisponibilidadData(BaseModel):
    rangoConsultado: dict
    disponibilidad: List[FechaItem]
    sugerencias: Optional[List[FechaItem]] = None

class DisponibilidadResponse(BaseModel):
    success: bool
    message: str
    data: Optional[DisponibilidadData] = None
    error_code: Optional[str] = None
    details: Optional[dict] = None
