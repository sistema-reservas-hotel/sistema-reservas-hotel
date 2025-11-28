from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.Base import Base 

class FacturaBD(Base):
    __tablename__ = "facturas"

    id_factura = Column(Integer, primary_key=True, autoincrement=True)
    id_pago = Column(Integer, ForeignKey("pagos.id_pago"), nullable=False)
    fecha_emision = Column(DateTime, default=datetime.utcnow, nullable=False)
    total = Column(Integer, nullable=False)
    url_pdf = Column(String, nullable=True)
    numero_factura = Column(String, unique=True, nullable=True)

    # Relación con pagos (opcional)
    pago = relationship("PagosDB", backref="factura")
