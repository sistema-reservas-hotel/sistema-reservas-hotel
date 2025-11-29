from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.ReservasBD import ReservasDB
from datetime import datetime, date

class ReservaRepository:
    # Clase que agrupa las consultas a la tabla reservas

    def __init__(self, db: Session):
        self.db = db

    def obtener_reservas_por_cliente(
        self,
        id_cliente: int,
        estado: Optional[str] = None,
        fecha_inicio: Optional[date] = None,
        fecha_fin: Optional[date] = None) -> List[ReservasDB]:
       
        query = self.db.query(ReservasDB).filter(ReservasDB.id_cliente == id_cliente)

        if estado:
            query = query.filter(ReservasDB.estado == estado)

        if fecha_inicio:
            query = query.filter(ReservasDB.check_in >= fecha_inicio)

        if fecha_fin:
            query = query.filter(ReservasDB.check_out <= fecha_fin)

        query = query.order_by(ReservasDB.fecha_reserva.desc())

        return query.all()
    
    def obtener_reserva(self, id_reserva: int) -> Optional[ReservasDB]:
        """Obtiene una reserva por su ID"""
        return self.db.query(ReservasDB).filter(ReservasDB.id_reserva == id_reserva).first()

    def actualizar_estado(self, id_reserva: int, nuevo_estado: str) -> Optional[ReservasDB]:
        """Actualiza el estado de una reserva"""
        reserva = self.obtener_reserva(id_reserva)
        if not reserva:
            return None
        reserva.estado = nuevo_estado
        self.db.commit()
        self.db.refresh(reserva)
        return reserva

    def horas_antes_checkin(self, id_reserva: int) -> Optional[int]:
        """Devuelve cuántas horas faltan para el check-in de la reserva"""
        reserva = self.obtener_reserva(id_reserva)
        if not reserva:
            return None
        ahora = datetime.utcnow()
        diferencia = reserva.check_in - ahora
        return int(diferencia.total_seconds() // 3600)