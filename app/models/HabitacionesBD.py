from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from app.models.Base import Base
from sqlalchemy.orm import relationship

class HabitacionesDB(Base): 
    __tablename__ = "habitaciones"
    id_tipoHabitacion = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String, nullable=False)
    plan_incluido = Column(String, nullable=False)
    descripcion_plan =  Column(String, nullable=False)
    capacidad = Column(Integer, nullable=False)
    precio_base = Column(Integer, nullable=False)
    estado_habitacion = Column(String, default=True)
    habitacionesDisponibles = Column(Integer, default=0)

    planes = relationship("PlanesDB")
