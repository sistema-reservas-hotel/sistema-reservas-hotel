from pydantic import BaseModel
from typing import Optional

class TipoHabitacionCreate(BaseModel):
    nombre: str
    descripcion: str
    plan_incluido: Optional[str] = "null"
    descripcion_plan: Optional[str] = "Esta habitación no cuenta con planes incluidos"
    precio_base: int
    capacidad: int

class TipoHabitacionResponse(BaseModel):
    id_tipoHabitacion: int
    nombre: str
    descripcion: str
    plan_incluido: Optional[str] = None
    descripcion_plan: Optional[str] = None
    precio_base: int
    capacidad: int

    class Config:
        from_attributes = True
