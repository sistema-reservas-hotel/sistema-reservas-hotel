from pydantic import BaseModel
from typing import List, Optional

class PlanIncluido(BaseModel):
    plan: str
    precio: int
    serviciosIncluidos: List[str]

class HabitacionBase(BaseModel):
    id_tipoHabitacion: int
    nombre: str
    descripcion: str
    capacidad: int
    precioPorNoche: int
    imagen: Optional[str]
    disponible: bool
    HabitacionDisponibles: int
    planes: List[PlanIncluido] = []

class HabitacionesResponse(BaseModel):
    success: bool
    message: str
    data: List[HabitacionBase] = []

class HabitacionResponse(HabitacionBase):
    succes: bool
    message: str

class ErrorResponse(BaseModel):
    succes: bool = False
    message: str
    error_code: str
    details: dict = {}