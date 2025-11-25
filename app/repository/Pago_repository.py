from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class PagoDetalle(BaseModel):
    id_pago: int
    fecha_pago: datetime
    monto: int
    metodo: str
    estado: str
    comprobante: Optional[str] = None

class ResponsePagos(BaseModel):
    success: bool
    mensaje: str
    data: dict = {"pagos": []}
    error_code: Optional[str] = None