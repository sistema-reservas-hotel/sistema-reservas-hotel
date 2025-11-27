from sqlalchemy.orm import Session
from app.models.HabitacionesBD import HabitacionesDB
from app.models.ReservasBD import ReservasDB

class ActualizarRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, id_tipoHabitacion: int) -> HabitacionesDB:
        return self.db.query(HabitacionesDB).filter(HabitacionesDB.id_tipoHabitacion == id_tipoHabitacion).first()

    def update_estado(self, id_tipoHabitacion: int, nuevo_estado: str) -> dict:
        habitacion = self.get_by_id(id_tipoHabitacion)
        if not habitacion:
            return None

    
        if nuevo_estado == "Disponible":
            reservas_activas = self.db.query(ReservasDB).filter(
                ReservasDB.id_tipoHabitacion == id_tipoHabitacion,
                ReservasDB.estado_reserva == "Activa"
            ).count()
            if reservas_activas > 0:
                return False  

        estado_anterior = habitacion.estado_habitacion
        habitacion.estado_habitacion = nuevo_estado
        self.db.commit()
        self.db.refresh(habitacion)
        return {
            "id_tipoHabitacion": habitacion.id_tipoHabitacion,
            "estado_anterior": estado_anterior,
            "estado_nuevo": nuevo_estado
        }