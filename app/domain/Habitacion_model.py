from pydantic import BaseModel
from typing import List, Optional, Dict

class PlanIncluido(BaseModel):
    plan: str
    precio: int
    serviciosIncluidos: List[str]

class HabitacionBase(BaseModel):
    idTipoHabitacion: int
    nombre: str
    descripcion: str
    capacidad: int
    precioPorNoche: int
    imagen: Optional[str]
    disponible: bool
    habitacionesDisponibles: int
    planes: List[PlanIncluido] = []

class HabitacionesResponse(BaseModel):
    success: bool
    message: str
    data: List[HabitacionBase] = []

class HabitacionResponse(BaseModel):
    success: bool
    message: str
    data: HabitacionBase

class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    error_code: str
    details: Dict = {}
