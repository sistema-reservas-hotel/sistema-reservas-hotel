from sqlalchemy.orm import Session
from app.models.ClienteBD import ClienteDB
from app.domain.Registrar_model import ClienteCreate
from datetime import datetime

class ClienteRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_user_by_email(self, email: str) -> ClienteDB:
        return self.db.query(ClienteDB).filter(ClienteDB.email == email).first()
    
    def create_cliente(self, cliente: ClienteCreate, hashed_password: str) -> ClienteDB:
        nuevo = ClienteDB(
            nombre=cliente.nombre,
            apellido=cliente.apellido,
            email=cliente.email,
            password=hashed_password,
            telefono=cliente.telefono, 
            direccion=cliente.direccion,
            fecha_registro=datetime.utcnow()
        )

        nuevo.password = hashed_password

        self.db.add(nuevo)
        self.db.commit()
        self.db.refresh(nuevo)
        return nuevo
