from pydantic import BaseModel
from datetime import datetime

class ReservaRequest(BaseModel):
    id_cliente: int
    id_tipoHabitacion: int
    capacidad: int
    check_in: datetime
    check_out: datetime
    plan_incluido: str

