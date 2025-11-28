from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.models.Base import Base  

class AuditoriaBD(Base):
    __tablename__ = "auditoria"

    id_log = Column(Integer, primary_key=True, autoincrement=True)
    usuario = Column(String, nullable=True)
    accion = Column(String, nullable=False)
    detalle = Column(String, nullable=True)
    fecha_evento = Column(DateTime, default=datetime.utcnow, nullable=False)
    referencia_id = Column(String, nullable=True)  # puede ser id_pago, id_reserva, id_factura…
