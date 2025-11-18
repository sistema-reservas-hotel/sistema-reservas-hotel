from pydantic import BaseModel, EmailStr

class InicioRequest(BaseModel):
    email: EmailStr
    password: str

class ClienteToken(BaseModel):
    id_cliente: int
    nombre: str
    email: EmailStr

class InicioResponse(BaseModel):
    token: str
    cliente: ClienteToken