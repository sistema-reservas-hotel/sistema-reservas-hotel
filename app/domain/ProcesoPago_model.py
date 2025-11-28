from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

class PagoBase(BaseModel):
    id_cliente: int
    id_reserva: Optional[int] = None
    monto: float
    metodo: str

class PagoCreacion(PagoBase):
    pass

class PagoRespuesta(BaseModel):
    id_pago: int
    id_reserva: Optional[int]
    monto: float
    metodo: str
    estado_pago: str
    fecha_pago: datetime
    comprobante: Optional[str]

    class Config:
        orm_mode = True
