from pydantic import BaseModel
from typing import Literal

class ActualizarEstado(BaseModel):
    nuevo_estado: Literal["Disponible", "Ocupada", "Limpieza", "Fuera de servicio"]
    