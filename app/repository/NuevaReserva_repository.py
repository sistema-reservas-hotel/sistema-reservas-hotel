from sqlalchemy.orm import Session
from app.models.ReservasBD import ReservasDB
from datetime import date
from app.models.HabitacionesBD import HabitacionesDB

class ReservaRepository:

    def __init__(self, db: Session):
        self.db = db

    def buscar_disponibilidad(self, id_tipoHabitacion: int):
        """
        Retorna una habitación libre según el campo habitacionesDisponibles
        """
        habitacion = (
            self.db.query(HabitacionesDB)
            .filter(
                HabitacionesDB.id_tipoHabitacion == id_tipoHabitacion,
                HabitacionesDB.habitacionesDisponibles > 0
            )
            .first()
        )
        return habitacion

    def crear_reserva(self, reserva: ReservasDB):
        # Al crear la reserva, decrementamos habitacionesDisponibles
        habitacion = self.db.query(HabitacionesDB).filter(HabitacionesDB.id_tipoHabitacion == reserva.id_tipoHabitacion).first()
        if habitacion:
            habitacion.habitacionesDisponibles -= 1
            self.db.add(reserva)
            self.db.commit()
            self.db.refresh(reserva)
            return reserva
        return None

    def obtener_reserva(self, id_reserva: int):
        return self.db.query(ReservasDB).filter(ReservasDB.id_reserva == id_reserva).first()
