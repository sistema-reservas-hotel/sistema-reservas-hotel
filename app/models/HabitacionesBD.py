from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from sqlalchemy.orm import relationship

Base = declarative_base()

class HabitacionesDB(Base): 
    __tablename__ = "habitaciones"
    id_tipoHabitacion = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String, nullable=False)
    capacidad = Column(Integer, nullable=False)
    precioPorNoche = Column(Integer, nullable=False)
    imagen = Column(String, nullable=True)
    disponible = Column(Boolean, default=True)
    habitacionesDisponibles = Column(Integer, default=0)
    planes = relationship("PlanesDB", back_populates="habitacion")
