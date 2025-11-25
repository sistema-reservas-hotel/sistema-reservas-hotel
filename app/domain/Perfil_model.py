from pydantic import BaseModel, EmailStr
from datetime import datetime

class PerfilResponse(BaseModel):
    id_cliente: int
    nombre: str
    apellido: str
    email: EmailStr
    telefono: str
    direccion: str
    fecha_registro: datetime

    class Config:
        from_attributes = True


class PerfilUpdateRequest(BaseModel):
    nombre: str | None = None
    apellido: str | None = None
    telefono: str | None = None
    direccion: str | None = None