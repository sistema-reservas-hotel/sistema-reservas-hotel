from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class FechaQuery(BaseModel):
    fechaEntrada: Optional[str] = None
    dechaSalida: Optional[str] = None

class FechaItem(BaseModel):
    fecha: str

class RangoConsultado(BaseModel):
    inicio: str
    fin: str

class FechasDisponibilidadResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    error_code: Optional[str] = None
