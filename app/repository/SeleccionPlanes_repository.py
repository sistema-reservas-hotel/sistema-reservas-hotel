# app/repository/Plan_repository.py
from sqlalchemy.orm import Session
from app.models.PlanesBD import PlanesDB

class PlanesRepository:
    def __init__(self, db: Session):
        self.db = db

    def listar_planes(self):
        """
        Retorna todos los planes activos
        """
        return self.db.query(PlanesDB).filter(PlanesDB.activo == True).all()
