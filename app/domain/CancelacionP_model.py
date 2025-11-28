from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# --- Modelos de Respuesta ---

class PagoCanceladoResponse(BaseModel):
    """
    Modelo de datos para una respuesta exitosa de cancelación de pago,
    siguiendo la estructura JSON solicitada.
    """
    id_Pago: int = Field(alias="id_pago") # Mapeo del campo interno al campo de salida
    id_Reserva: Optional[int] = Field(alias="id_reserva")
    monto: float
    estado: str = Field(alias="estado_pago")
    fechaCancelacion: datetime
    motivo: str

    class Config:
        # Permite la asignación por nombre de campo (id_pago) y por alias (idPago)
        allow_population_by_field_name = True

class PagoCancelacionSalida(BaseModel):
    """
    Estructura de la respuesta del servicio/API para la cancelación.
    """
    success: bool
    message: str
    data: Optional[PagoCanceladoResponse] = None