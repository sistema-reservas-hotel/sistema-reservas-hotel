from pydantic import BaseModel
from datetime import date, datetime
from typing import List, Optional


class ReservaItem(BaseModel):
    id_reserva: int
    fecha_reserva: datetime
    check_in: date
    check_out: date
    habitacion: str
    plan: str
    valor_total: int
    estado: str

    class Config:
        orm_mode = True


class ReservasData(BaseModel):
    reservas: List[ReservaItem]


class ReservasResponse(BaseModel):
    mensaje: str
    data: Optional[ReservasData] = None
    success: bool
