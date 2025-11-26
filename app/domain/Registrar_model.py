from pydantic import BaseModel, EmailStr
from datetime import datetime

class ClienteCreate(BaseModel):
    nombre: str
    apellido: str
    email: EmailStr
    password: str
    telefono: str
    direccion: str

class ClienteResponse(BaseModel):
    id_cliente: int
    nombre: str
    apellido: str
    email: str
    telefono: str
    direccion: str
    fecha_registro: datetime

    class Config:
        from_attributes = True