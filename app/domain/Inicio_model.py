from pydantic import BaseModel, EmailStr

class InicioRequest(BaseModel):
    email: EmailStr
    password: str

class InicioClienteData(BaseModel):
    id_cliente: int
    nombre: str
    email: EmailStr

class InicioResponse(BaseModel):
    mensaje: str
    data: dict | None
    success: bool