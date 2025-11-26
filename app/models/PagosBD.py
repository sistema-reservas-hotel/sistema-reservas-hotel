from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.Base import Base

class PagosDB(Base):
    __tablename__ = "pagos"

    id_pago = Column(Integer, primary_key=True, index=True)
    id_cliente = Column(Integer, ForeignKey("clientes.id_cliente"), nullable=False)
    id_reserva = Column(Integer, ForeignKey("reservas.id_reserva"), nullable=True)  # opcional si vinculado a reserva
    fecha_pago = Column(DateTime, default=datetime.utcnow, nullable=False)
    monto = Column(Float, nullable=False)
    metodo = Column(String, nullable=False)  # Ej: "Tarjeta", "Efectivo", "Transferencia"
    estado = Column(String, nullable=False, default="Pendiente")  # Pendiente, Completado, Cancelado
    comprobante = Column(String, nullable=True)  # URL o nombre de archivo del comprobante

    # Relaciones
    cliente = relationship("ClienteDB", back_populates="pagos")
    reserva = relationship("ReservasDB", back_populates="pagos")
