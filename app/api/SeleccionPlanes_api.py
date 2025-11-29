from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.SeleccionPlanes_service import PlanesService
from app.database import SessionLocal
from app.domain.SeleccionPlanes_models import PlanCreate, PlanUpdate

router = APIRouter(prefix="/reservas", tags=["Planes"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/planes")
def listar_planes(db: Session = Depends(get_db)):
    service = PlanesService(db)
    return service.obtener_planes()

@router.post("/planes")
def agregar_plan(data: PlanCreate, db: Session = Depends(get_db)):
    service = PlanesService(db)
    try:
        plan = service.agregar_plan(
            data.id_tipoHabitacion,
            data.nombre,
            data.precio,
            data.serviciosIncluidos
        )
        return {"success": True, "mensaje": "Plan agregado correctamente", "data": plan}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/planes/{id_plan}")
def editar_plan(id_plan: int, data: PlanUpdate, db: Session = Depends(get_db)):
    service = PlanesService(db)
    plan = service.editar_plan(
        id_plan,
        data.nombre,
        data.precio,
        data.serviciosIncluidos
    )
    if not plan:
        raise HTTPException(status_code=404, detail="Plan no encontrado")
    return {"success": True, "mensaje": "Plan actualizado correctamente", "data": plan}

@router.delete("/planes/{id_plan}")
def eliminar_plan(id_plan: int, db: Session = Depends(get_db)):
    service = PlanesService(db)
    plan = service.eliminar_plan(id_plan)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan no encontrado")
    return {"success": True, "mensaje": "Plan eliminado correctamente", "data": {"idPlan": plan.id_Plan, "nombre": plan.nombre}}
