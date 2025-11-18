from sqlalchemy.orm import Session
from database import ClienteDB
from datetime import datetime

class PerfilRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_cliente_by_id(self, id_cliente: int):
        return self.db.query(ClienteDB).filter(ClienteDB.id_cliente == id_cliente).first()
    
    def update_cliente(self, cliente: ClienteDB, Update_data: dict):
        for key, value in Update_data.items():
            setattr(cliente, key, value)

        cliente.updated_at = datetime.utcnow()

        self.db.commit()
        self.db.refresh(cliente)
        return cliente
        