from pydantic import BaseModel, EmailStr
from datetime import date

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
    fecha_registro: date

    class Config:
        from_attributes = True
