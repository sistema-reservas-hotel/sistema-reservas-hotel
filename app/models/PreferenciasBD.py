from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from app.models.ClienteBD import ClienteDB
from sqlalchemy.orm import relationship
from app.models.Base import Base

class PreferenciasClienteDB(Base):
    __tablename__ = "preferencias_cliente"
    id_preferencia = Column(Integer, primary_key=True, index=True)
    id_cliente = Column(Integer, ForeignKey("clientes.id_cliente"), nullable=False, unique=True)
    documento = Column(String)
    tipo_habitacion_preferida = Column(String)
    metodo_pago_preferido = Column(String)
    hora_llegada = Column(String)

    cliente = relationship("ClienteDB")
