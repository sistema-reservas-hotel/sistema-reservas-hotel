from sqlalchemy.orm import Session
from app.models.PlanesDB import PlanesDB

class PlanesRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_plan(self, plan_data: dict):
        plan = PlanesDB(**plan_data)
        self.db.add(plan)
        self.db.commit()
        self.db.refresh(plan)
        return plan

    def get_plan_by_id(self, id_Plan: int):
        return self.db.query(PlanesDB).filter(PlanesDB.id_Plan == id_Plan).first()

    def update_plan(self, id_Plan: int, data: dict):
        plan = self.get_plan_by_id(id_Plan)
        if not plan:
            return None
        for key, value in data.items():
            setattr(plan, key, value)
        self.db.commit()
        self.db.refresh(plan)
        return plan

    def delete_plan(self, id_Plan: int):
        plan = self.get_plan_by_id(id_Plan)
        if not plan:
            return None
        self.db.delete(plan)
        self.db.commit()
        return plan
