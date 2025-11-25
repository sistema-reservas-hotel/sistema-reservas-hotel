from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from sqlalchemy.orm import relationship

Base = declarative_base()

class ReservasDB(Base):
    tablename = "reservas"
    id_reserva = Column(Integer, primary_key=True)
    id_cliente = Column(Integer, ForeignKey("clientes.id_cliente"), nullable=False)
    fecha_reserva = Column(DateTime, nullable=False)
    check_in = Column(Date, nullable=False)
    check_out = Column(Date, nullable=False)
    habitacion = Column(String, nullable=False)
    plan = Column(String, nullable=False)
    valor_total = Column(Integer, nullable=False)
    estado = Column(String, nullable=False)
    cliente = relationship("ClienteDB", backref="reservas")
    