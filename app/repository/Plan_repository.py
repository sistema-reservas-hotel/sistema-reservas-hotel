from sqlalchemy.orm import Session
from database import PlanDB
from typing import List, Optional


class PlanRepository:
    def __init__(self, db: Session):
        self.db = db

    def obtener_planes_activos(self) -> List[PlanDB]:
        return self.db.query(PlanDB).filter(PlanDB.activo == True).all()

    def obtener_plan_por_id(self, idPlan: int) -> Optional[PlanDB]:
        return self.db.query(PlanDB).filter(PlanDB.idPlan == idPlan, PlanDB.activo == True).first()
