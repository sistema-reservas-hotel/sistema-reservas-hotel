from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repository.Registro_repository import ClienteRepository
from app.domain.Registro_model import ClienteCreate,ClienteResponse
from app.utils.password import hash_password, verify_password


class ClienteService:
    def __init__(self, db: Session):
        self.repository = ClienteRepository(db)

    def registrar_cliente(self, data: ClienteCreate):

        if self.repository.get_by_email(data.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El correo electronico ya esta registrado."
            )
        
        hashed = hash_password(data.password)

        cliente =self.repository.create_cliente(data, hashed)

        return {
            "mensaje": "Registro exitoso. Bienvenido a la plataforma.",
            "data": ClienteResponse.from_orm(cliente),
            "success": True
        }

