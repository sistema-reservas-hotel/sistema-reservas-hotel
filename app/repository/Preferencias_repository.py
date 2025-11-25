from sqlalchemy.orm import Session
from app.models.preferencias import PreferenciasCliente

class PreferenciasRepository:

    def get_by_cliente(self, db: Session, id_cliente: int):
        return db.query(PreferenciasCliente).filter_by(id_cliente=id_cliente).first()

    def save_or_update(self, db: Session, id_cliente: int, data: dict):
        preferencias = self.get_by_cliente(db, id_cliente)

        if preferencias:
            for key, value in data.items():
                setattr(preferencias, key, value)
        else:
            preferencias = PreferenciasCliente(id_cliente=id_cliente, **data)
            db.add(preferencias)

        db.commit()
        db.refresh(preferencias)
        return preferencias
