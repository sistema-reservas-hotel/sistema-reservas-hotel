from pydantic import BaseModel
from typing import Optional

class PreferenciasBase(BaseModel):
    documento: Optional[str] = None
    tipo_habitacion_preferida: Optional[str] = None
    metodo_pago_preferido: Optional[str] = None
    hora_llegada: Optional[str] = None


class PreferenciasResponse(PreferenciasBase):
    id_cliente: int

    class Config:
        orm_mode = True
