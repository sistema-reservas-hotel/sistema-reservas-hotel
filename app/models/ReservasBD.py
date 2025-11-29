from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from datetime import datetime
from sqlalchemy.orm import relationship
from app.models.Base import Base


class ReservasDB(Base):
    _tablename_ = "reservas"

    id_reserva = Column(Integer, primary_key=True)
    id_cliente = Column(Integer, ForeignKey("clientes.id_cliente"), nullable=False)
    id_tipoHabitacion = Column(Integer, ForeignKey("habitaciones.id_tipoHabitacion"), nullable=False)  
    fecha_reserva = Column(DateTime, default=datetime.utcnow, nullable=False)
    check_in = Column(DateTime, nullable=False)
    check_out = Column(DateTime, nullable=False)
    habitacion = Column(String, nullable=False)  # nombre interno o código
    plan = Column(String, nullable=False)
    estado_reserva = Column(String, nullable=False)
    num_personas = Column(Integer, nullable=False)

    cliente = relationship("ClienteDB", back_populates="reservas")
