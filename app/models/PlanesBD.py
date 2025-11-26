from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from sqlalchemy.orm import relationship

Base = declarative_base()


class PlanesDB(Base):
    __tablename__ = "planes"
    id_Plan = Column(Integer, primary_key=True, index=True)
    id_tipoHabitacion = Column(Integer, ForeignKey("habitaciones.id_tipoHabitacion"),nullable=False)
    nombre = Column(String, nullable=False)  
    precio = Column(Integer, nullable=False)
    serviciosIncluidos = Column(String, nullable=False)  
    id_tipoHabitacion = Column(Integer, ForeignKey("habitaciones.id_tipoHabitacion"))
    habitacion = relationship("HabitacionesDB", back_populates="planes")
