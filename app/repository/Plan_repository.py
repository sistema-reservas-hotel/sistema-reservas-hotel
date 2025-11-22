from sqlalchemy.orm import Session
from app.database import PlanesDB
from typing import List, Optional


class PlanRepository:
    def __init__(self, db: Session):
        self.db = db

    def obtener_planes_activos(self) -> List[PlanesDB]:
        return self.db.query(PlanesDB).filter(PlanesDB.activo == True).all()

    def obtener_plan_por_id(self, idPlan: int) -> Optional[PlanesDB]:
        return self.db.query(PlanesDB).filter(PlanesDB.idPlan == idPlan, PlanesDB.activo == True).first()
