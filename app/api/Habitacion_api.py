from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.Habitacion_service import HabitacionesService
from app.domain.Habitacion_model import HabitacionBase, HabitacionConPlanesResponse


router = APIRouter(
    prefix="/api/v1/reservas/habitaciones",
    tags=["Habitaciones"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.get("/", response_model=list[HabitacionBase] | HabitacionBase)
def obtener_habitaciones(
    tipoHabitacion: str | None = Query(None),
    db: Session = Depends(get_db)
):
    service = HabitacionesService(db)
    return service.listar_habitaciones(tipoHabitacion)


@router.get("/planes", response_model=HabitacionConPlanesResponse)
def obtener_planes(
    tipoHabitacion: str = Query(..., description="Nombre del tipo de habitación"),
    db: Session = Depends(get_db)
):
    service = HabitacionesService(db)
    return service.obtener_planes(tipoHabitacion)
