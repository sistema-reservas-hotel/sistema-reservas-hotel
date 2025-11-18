from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from datetime import datetime


DATABASE_URL = "sqlite:///./ReservasHotel.db"

engine = create_engine(DATABASE_URL, connect_args=
{"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False,
autoflush=False, bind=engine)

Base = declarative_base()

class ClienteDB(Base):
    __tablename__ = "clientes"
    id_cliente = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    telefono = Column(String)
    direccion = Column(String)
    fecha_registro = Column(DateTime, default=datetime.utcnow)
    password = Column(String, nullable=False)

class ReservasDB(Base):
    __tablename__ = "reservas"
    id_reserva = Column(Integer, primary_key=True)
    id_cliente = Column(Integer, ForeignKey("clientes.id_cliente"), nullabel=False)
    fecha_reserva = Column(DateTime, nullable=False)
    check_in = Column(Date, nullable=False)
    check_out = Column(Date, nullable=False)
    habitacion = Column(String, nullable=False)
    plan = Column(String, nullable=False)
    valor_total = Column(Integer, nullable=False)
    estado = Column(String, nullable=False)

    cliente = relationship("ClienteDB", backref="reservas")



Base.metadata.create_all(bind=engine)
