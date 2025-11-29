from app.models.ReservasBD import ReservasDB
from app.models.HabitacionesBD import HabitacionesDB
from sqlalchemy.orm import Session

class ReservaRepository:

    def __init__(self, db: Session):
        self.db = db

    def buscar_disponibilidad(self, id_tipoHabitacion: int):
        # Busca la primera habitación disponible de ese tipo
        return self.db.query(HabitacionesDB).filter(
            HabitacionesDB.id_tipoHabitacion == id_tipoHabitacion,
            HabitacionesDB.estado == "Disponible"
        ).first()

    def crear_reserva(self, reserva: ReservasDB):
        self.db.add(reserva)
        self.db.commit()
        self.db.refresh(reserva)
        return reserva

    def obtener_reserva(self, id_reserva: int):
        return self.db.query(ReservasDB).filter(
            ReservasDB.id_reserva == id_reserva
        ).first()
