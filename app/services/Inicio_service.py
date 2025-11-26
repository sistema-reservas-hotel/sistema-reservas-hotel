from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repository.Inicio_repository import InicioRepository
from app.utils.password import verify_password
from app.utils.jwt_manager import create_access_token
from app.domain.Inicio_model import InicioRequest, InicioResponse, ClienteToken


class InicioService:
    def __init__(self, db: Session):
        self.repository = InicioRepository(db)

    def inicio(self, credentials: InicioRequest):

        if not credentials.email or not credentials.password:
            return {
                "mensaje":"Debe prorcionar correo y contraseña.",
                "data":None,
                "success":False
            }
        
        cliente = self.repository.get_user_by_email(credentials.email)

        if not cliente: 
            return {
                "mensaje":"Credenciales invalidas. verifique su correo o contraseña.",
                "data":None,
                "succcess":False    
            }
        
        if not verify_password(credentials.password, cliente.password):
            return {
                "mensaje": "Contraseña incorrecta, por favor verifique su contraseña.",
                "data": None,
                "success": False
            }
        
        token = create_access_token({
            "id_cliente": cliente.id_cliente 
            })

        cliente_data = ClienteToken(
            id_cliente=cliente.id_cliente,
            nombre=cliente.nombre,
            email=cliente.email
        )

        return {
             "mensaje": "Inicio de sesión exitoso.",
            "data": {
                "token": token,
                "usuario": cliente_data
            },
            "success": True
            }
