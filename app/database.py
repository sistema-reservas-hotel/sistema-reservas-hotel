from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from datetime import datetime


DATABASE_URL = "sqlite:///./ReservasHotel.db"

engine = create_engine(DATABASE_URL, connect_args=
{"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False,
autoflush=False, bind=engine)

