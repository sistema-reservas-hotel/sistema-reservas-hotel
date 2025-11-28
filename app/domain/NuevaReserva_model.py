from pydantic import BaseModel, validator, Field
from datetime import date
from typing import Optional

class ReservaCreacion(BaseModel):
    id_cliente: int
    id_tipoHabitacion: int # Usamos el tipo para buscar una habitación disponible
    fecha_entrada: date
    fecha_salida: date
    num_personas: int
    plan: str = "Alojamiento y Desayuno" # Campo adicional de tu tabla
    
    @validator('fecha_salida')
    def validate_dates(cls, v, values):
        if 'fecha_entrada' in values and v <= values['fecha_entrada']:
            raise ValueError("La fecha de salida debe ser estrictamente posterior a la fecha de entrada.")
        return v

class ReservaDetalle(BaseModel):
    id_reserva_unico: str
    id_cliente: int
    id_habitacion: int = Field(alias="id_habitacion_fk") # ID de instancia de habitación
    tipoHabitacion: str # Nombre del tipo de habitación
    fecha_entrada: date
    fecha_salida: date
    num_personas: int
    estado: str = Field(alias="estado_reserva")

class ReservaCreacionSalida(BaseModel):
    mensaje: str
    data: Optional[ReservaDetalle] = None
    success: bool