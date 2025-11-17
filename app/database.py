from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from sqlalchemy import DateTime

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


Base.metadata.create_all(bind=engine)
