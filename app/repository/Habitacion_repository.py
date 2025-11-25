from sqlalchemy.orm import Session
from app.models import HabitacionesBD, PlanesBD


class HabitacionesRepository:
    def _init_(self, db: Session):
        self.db = db

    def get_all_habitaciones(self):
        return self.db.query(HabitacionesBD).all()
    
    def get_habitacion_by_tipo(self, tipo: str):
        return self.db.query(HabitacionesBD).filter(HabitacionesBD.nombre == tipo).first()
    
    def get_planes_por_habitacion(self, id_tipoHabitacion: int):
        return self.db.query(PlanesBD).filter(PlanesBD.id_tipoHabitacion == id_tipoHabitacion).all()