from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.ReservasBD import ReservasBD
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
        fecha_fin: Optional[date] = None) -> List[ReservasBD]:
       
        query = self.db.query(ReservasBD).filter(ReservasBD.id_cliente == id_cliente)

        if estado:
            query = query.filter(ReservasBD.estado == estado)

        if fecha_inicio:
            query = query.filter(ReservasBD.check_in >= fecha_inicio)

        if fecha_fin:
            query = query.filter(ReservasBD.check_out <= fecha_fin)

        query = query.order_by(ReservasBD.fecha_reserva.desc())

        return query.all()