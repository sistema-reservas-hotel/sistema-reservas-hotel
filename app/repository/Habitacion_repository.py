from sqlalchemy.orm import Session
from app.models.HabitacionesBD import HabitacionesDB
from app.models.PlanesBD import PlanesDB

class HabitacionesRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_habitaciones(self):
       
        return self.db.query(HabitacionesDB).all()

    def get_habitacion_by_tipo(self, tipo: str):
       
        return self.db.query(HabitacionesDB).filter(HabitacionesDB.nombre == tipo).first()
