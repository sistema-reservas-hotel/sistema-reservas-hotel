from sqlalchemy.orm import Session
from app.models.PreferenciasBD import PreferenciasClienteDB

class PreferenciasRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_cliente(self, id_cliente: int):
        return self.db.query(PreferenciasClienteDB).filter_by(id_cliente=id_cliente).first()

    def save_or_update(self, id_cliente: int, data: dict):
        preferencias = self.get_by_cliente(id_cliente)

        if preferencias:
            for key, value in data.items():
                setattr(preferencias, key, value)
        else:
            preferencias = PreferenciasClienteDB(id_cliente=id_cliente, **data)
            self.db.add(preferencias)

        self.db.commit()
        self.db.refresh(preferencias)
        return preferencias
