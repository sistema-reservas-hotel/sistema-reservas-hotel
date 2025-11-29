from sqlalchemy.orm import Session
from app.models.PlanesBD import PlanesDB

class PlanesRepository:

    def obtener_planes(self, db: Session):
        return db.query(PlanesDB).all()

    def agregar_plan(self, db: Session, plan: PlanesDB):
        db.add(plan)
        db.commit()
        db.refresh(plan)
        return plan

    def obtener_por_id(self, db: Session, id_plan: int):
        return db.query(PlanesDB).filter(PlanesDB.id_Plan == id_plan).first()

    def actualizar_plan(self, db: Session, plan: PlanesDB):
        db.commit()
        db.refresh(plan)
        return plan

    def eliminar_plan(self, db: Session, plan: PlanesDB):
        db.delete(plan)
        db.commit()
        return plan
