from sqlalchemy.orm import Session
from app.models.HabitacionesBD import HabitacionesDB
from datetime import datetime

class TipoHabitacionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, id_tipoHabitacion: int) -> HabitacionesDB:
        return self.db.query(HabitacionesDB).filter(HabitacionesDB.id_tipoHabitacion == id_tipoHabitacion).first()

    def update_precio(self, id_tipoHabitacion: int, nuevo_precio: int) -> dict:
        tipo = self.get_by_id(id_tipoHabitacion)
        if not tipo:
            return None
        
        precio_anterior = tipo.precio_base
        tipo.precio_base = nuevo_precio
        
    
        
        self.db.commit()
        self.db.refresh(tipo)
        return {
            "id_tipoHabitacion": tipo.id_tipoHabitacion,
            "nombre": tipo.nombre,
            "precio_base_anterior": precio_anterior,
            "nuevo_precio": nuevo_precio
        }