from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repository.Registrar_repository import ClienteRepository
from app.domain.Registrar_model import ClienteCreate, ClienteResponse
from app.utils.password import hash_password

class ClienteService:
    def __init__(self, db: Session):
        self.repository = ClienteRepository(db)

    def registrar_cliente(self, data: ClienteCreate) -> dict:
        # Validar si el correo ya existe
        if self.repository.get_user_by_email(data.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El correo electrónico ya está registrado."
            )
        
        # Hashear la contraseña
        hashed = hash_password(data.password)

        # Crear el cliente en la base de datos
        cliente = self.repository.create_cliente(data, hashed)

        # Retornar respuesta limpia usando ClienteResponse
        return {
            "mensaje": "Registro exitoso. Bienvenido a la plataforma.",
            "data": ClienteResponse.from_orm(cliente),
            "success": True
        }
