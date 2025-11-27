from sqlalchemy.orm import Session
from app.models.HabitacionesBD import HabitacionesDB
from app.models.ReservasBD import ReservasDB
from app.domain.TipoHabitacion_model import TipoHabitacionCreate

class TipoHabitacionRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_tipo(self, tipo_data: TipoHabitacionCreate) -> HabitacionesDB:
        tipo = HabitacionesDB(
            nombre=tipo_data.nombre,
            descripcion=tipo_data.descripcion,
            descripcion_plan=tipo_data.descripcion_plan,
            plan_incluido=tipo_data.plan_incluido,
            precio_base=tipo_data.precio_base,
            capacidad=tipo_data.capacidad
        )
        self.db.add(tipo)
        self.db.commit()
        self.db.refresh(tipo)
        return tipo

    def get_by_id(self, id_tipoHabitacion: int) -> HabitacionesDB:
        return self.db.query(HabitacionesDB).filter(HabitacionesDB.id_tipoHabitacion == id_tipoHabitacion).first()

    def get_by_nombre(self, nombre: str) -> HabitacionesDB:
        return self.db.query(HabitacionesDB).filter(HabitacionesDB.nombre == nombre).first()

    def update_tipo(self, id_tipoHabitacion: int, tipo_data: dict) -> HabitacionesDB:
        tipo = self.get_by_id(id_tipoHabitacion)
        for key, value in tipo_data.items():
            setattr(tipo, key, value)
        self.db.commit()
        self.db.refresh(tipo)
        return tipo

    def delete_tipo(self, id_tipoHabitacion: int) -> bool:
        tipo = self.get_by_id(id_tipoHabitacion)
        reservas = self.db.query(ReservasDB).filter(ReservasDB.id_tipoHabitacion == id_tipoHabitacion).count()
        if reservas > 0:
            return False
        self.db.delete(tipo)
        self.db.commit()
        return True
