# app/domain/NuevaReserva_model.py
from pydantic import BaseModel
from datetime import datetime

class ReservaRequest(BaseModel):
    id_cliente: int
    id_tipoHabitacion: int
    check_in: datetime
    check_out: datetime
    habitacion: str
    plan: str
