from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from services.Plan_service import PlanService
from domain.Plan_model import ResponsePlanList, ResponsePlanDetalle

router = APIRouter(prefix="/reservas", tags=["Planes"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/planes", response_model=ResponsePlanList)
def obtener_planes(db: Session = Depends(get_db)):
    service = PlanService(db)
    return service.listar_planes()


@router.get("/planes/{idPlan}", response_model=ResponsePlanDetalle)
def obtener_plan_por_id(idPlan: int, db: Session = Depends(get_db)):
    service = PlanService(db)
    return service.obtener_plan_por_id(idPlan)
