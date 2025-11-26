from pydantic import BaseModel
from typing import List, Optional


class PlanIncluido(BaseModel):
    id_plan: int
    nombre: str
    precio: float
    descripcion: Optional[str]

    class Config:
        from_attributes = True


class HabitacionBase(BaseModel):
    id_tipoHabitacion: int
    nombre: str
    descripcion: str
    capacidad: int
    precioPorNoche: float
    imagen: Optional[str]
    disponible: bool
    HabitacionDisponibles: int

    class Config:
        from_attributes = True


class HabitacionConPlanesResponse(BaseModel):
    habitacion: HabitacionBase
    planes: List[PlanIncluido]


class ErrorResponse(BaseModel):
    succes: bool = False
    message: str
    error_code: str
    details: dict = {}
