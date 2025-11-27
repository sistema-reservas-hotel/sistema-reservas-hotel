from sqlalchemy.orm import Session
from app.models import TipoHabitacionDB, ReservaDB
from app.domain.TipoHabitacion_model import TipoHabitacionCreate

class TipoHabitacionRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_tipo(self, tipo_data: TipoHabitacionCreate) -> TipoHabitacionDB:
        tipo = TipoHabitacionDB(
            nombre=tipo_data.nombre,
            descripcion=tipo_data.descripcion,
            descripcion_plan=tipo_data.descripcion_plan,
            plan=tipo_data.plan,
            precio_base=tipo_data.precio_base,
            capacidad=tipo_data.capacidad
        )
        self.db.add(tipo)
        self.db.commit()
        self.db.refresh(tipo)
        return tipo

    def get_by_id(self, id_tipo: int) -> TipoHabitacionDB:
        return self.db.query(TipoHabitacionDB).filter(TipoHabitacionDB.id_tipo == id_tipo).first()

    def get_by_nombre(self, nombre: str) -> TipoHabitacionDB:
        return self.db.query(TipoHabitacionDB).filter(TipoHabitacionDB.nombre == nombre).first()

    def update_tipo(self, id_tipo: int, tipo_data: dict) -> TipoHabitacionDB:
        tipo = self.get_by_id(id_tipo)
        for key, value in tipo_data.items():
            setattr(tipo, key, value)
        self.db.commit()
        self.db.refresh(tipo)
        return tipo

    def delete_tipo(self, id_tipo: int) -> bool:
        tipo = self.get_by_id(id_tipo)
        reservas = self.db.query(ReservaDB).filter(ReservaDB.id_tipoHabitacion == id_tipo).count()
        if reservas > 0:
            return False
        self.db.delete(tipo)
        self.db.commit()
        return True
