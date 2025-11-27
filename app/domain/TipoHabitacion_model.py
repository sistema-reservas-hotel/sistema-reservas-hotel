from pydantic import BaseModel
from typing import Optional

class TipoHabitacionCreate(BaseModel):
    nombre: str
    descripcion: str
    descripcion_plan: Optional[str] = "Esta habitación no cuenta con planes incluidos"
    plan: Optional[str] = None
    precio_base: float
    capacidad: int

class TipoHabitacionResponse(BaseModel):
    id_tipo: int
    nombre: str
    descripcion: str
    descripcion_plan: Optional[str] = None
    plan: Optional[str] = None
    precio_base: float
    capacidad: int

    class Config:
        from_attributes = True
