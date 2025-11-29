from pydantic import BaseModel

class PlanCreate(BaseModel):
    id_tipoHabitacion: int
    nombre: str
    precio: int
    serviciosIncluidos: str


class PlanUpdate(BaseModel):
    nombre: str
    precio: int
    serviciosIncluidos: str


class PlanResponse(BaseModel):
    id_Plan: int
    id_tipoHabitacion: int
    nombre: str
    precio: int
    serviciosIncluidos: str

    class Config:
        orm_mode = True
