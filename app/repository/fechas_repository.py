from sqlalchemy.orm import Session
from typing import List
from datetime import date, datetime, timedelta
from app.database import ReservasDB, HabitacionesDB

class FechasRepository:
    """
    Repositorio para consultas relacionadas con disponibilidad por fechas.
    Nota: Este código asume que ReservasDB tiene la columna id_tipoHabitacion (FK a HabitacionesDB).
    """

    def __init__(self, db: Session):
        self.db = db

    def reservas_entre_rango_para_tipo(self, id_tipo: int, check_in: date, check_out: date) -> List[ReservasDB]:
        """
        Devuelve las reservas que se solapan con el rango [check_in, check_out).
        Consideramos que una reserva se solapa si:
        reserva.check_in < fecha_fin AND reserva.check_out > fecha_inicio
        """
        return (
            self.db.query(ReservasDB)
            .filter(ReservasDB.id_tipoHabitacion == id_tipo)
            .filter(ReservasDB.check_in < check_out)
            .filter(ReservasDB.check_out > check_in)
            .all()
        )

    def obtener_tipos_habitacion(self):
        """
        Retorna todos los tipos de habitación (tabla habitaciones).
        HabitacionesDB debe tener: id_tipoHabitacion, nombre, capacidad, precioPorNoche, habitacionesDisponibles, disponible, imagen, etc.
        """
        return self.db.query(HabitacionesDB).all()

    def obtener_tipo_por_nombre(self, nombre: str):
        return self.db.query(HabitacionesDB).filter(HabitacionesDB.nombre == nombre).first()
