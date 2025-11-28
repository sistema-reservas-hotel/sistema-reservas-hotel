# app/repository/Plan_repository.py
from sqlalchemy.orm import Session
from app.models.PlanesBD import PlanesDB

class PlanesRepository:
    def __init__(self, db: Session):
        self.db = db

    def listar_planes(self):
        return self.db.query(PlanesDB).filter(PlanesDB.activo == True).all()

    def obtener_plan_por_id(self, id_plan: int):
        return self.db.query(PlanesDB).filter(PlanesDB.id_Plan == id_plan).first()

    def agregar_plan(self, plan: PlanesDB):
        self.db.add(plan)
        self.db.commit()
        self.db.refresh(plan)
        return plan

    def editar_plan(self, plan: PlanesDB):
        self.db.commit()
        self.db.refresh(plan)
        return plan

    def eliminar_plan(self, plan: PlanesDB):
        self.db.delete(plan)
        self.db.commit()
        return plan
