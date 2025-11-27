from pydantic import BaseModel
from typing import Optional

class PreferenciasBase(BaseModel):
    documento: Optional[str] = None
    tipo_habitacion_preferida: Optional[str] = None
    metodo_pago_preferido: Optional[str] = None
    hora_llegada: Optional[str] = None

    class Config:
        from_attributes = True  # <- Esto permite from_orm

class PreferenciasResponse(BaseModel):
    mensaje: str
    data: Optional[PreferenciasBase] = None
    success: bool
