from sqlalchemy.orm import Session
from app.models.ClienteBD import ClienteDB

class PerfilRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_cliente(self, id_cliente: int):
        return self.db.query(ClienteDB).filter_by(id_cliente=id_cliente).first()

    def update_cliente(self, id_cliente: int, data: dict):
        cliente = self.get_by_cliente(id_cliente)
        if not cliente:
            return None
        for key, value in data.items():
            setattr(cliente, key, value)
        self.db.commit()
        self.db.refresh(cliente)
        return cliente
