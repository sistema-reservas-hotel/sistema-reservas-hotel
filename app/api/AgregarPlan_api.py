from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.AgregarPlan_service import PlanesService
from app.domain.AgregarPlan_models import PlanCreate, PlanUpdate

router = APIRouter(prefix="/planes", tags=["Planes"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", status_code=status.HTTP_201_CREATED)
def agregar_plan(plan: PlanCreate, db: Session = Depends(get_db)):
    service = PlanesService(db)
    return service.agregar_plan(plan)

@router.put("/{id_Plan}", status_code=status.HTTP_200_OK)
def editar_plan(id_Plan: int, plan: PlanUpdate, db: Session = Depends(get_db)):
    service = PlanesService(db)
    return service.editar_plan(id_Plan, plan)

@router.delete("/{id_Plan}", status_code=status.HTTP_200_OK)
def eliminar_plan(id_Plan: int, db: Session = Depends(get_db)):
    service = PlanesService(db)
    return service.eliminar_plan(id_Plan)
