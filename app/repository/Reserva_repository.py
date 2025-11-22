from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import ReservasDB
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
        fecha_fin: Optional[date] = None
    ) -> List[ReservasDB]:
       
        query = self.db.query(ReservasDB).filter(ReservasDB.id_cliente == id_cliente)

        if estado:
            query = query.filter(ReservasDB.estado == estado)

        if fecha_inicio:
            query = query.filter(ReservasDB.check_in >= fecha_inicio)

        if fecha_fin:
            query = query.filter(ReservasDB.check_out <= fecha_fin)

        query = query.order_by(ReservasDB.fecha_reserva.desc())

        return query.all()
