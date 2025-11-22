from sqlalchemy.orm import Session
from app.database import HabitacionesDB, PlanesDB


class HabitacionesRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_habitaciones(self):
        return self.db.query(HabitacionesDB).all()
    
    def get_habitacion_by_tipo(self, tipo: str):
        return self.db.query(HabitacionesDB).filter(HabitacionesDB.nombre == tipo).first()
    
    def get_planes_por_habitacion(self, id_tipoHabitacion: int):
        return self.db.query(PlanesDB).filter(PlanesDB.id_tipoHabitacion == id_tipoHabitacion).all()
    
    