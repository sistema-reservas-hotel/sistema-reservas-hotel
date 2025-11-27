from pydantic import BaseModel
from typing import Optional

class PerfilUpdateRequest(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None

    class Config:
        from_attributes = True

class PerfilResponse(BaseModel):
    mensaje: str
    data: Optional[PerfilUpdateRequest] = None
    success: bool
