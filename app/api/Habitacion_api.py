from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database import SessionLocal
from services.Habitaciones_service import HabitacionesService
from domain.Habitacion_model import HabitacionesResponse, HabitacionResponse, ErrorResponse


router = APIRouter(prefix="/reservas/habitaciones", tags=["Habitaciones"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/disponibilidad", response_model=HabitacionesResponse | HabitacionResponse | ErrorResponse)
def obtener_habitaciones_disponibilidad(
    tipoHabitacion: str = Query(None, description="Filtrar por tipo de habitacion"),
    db: Session = Depends(get_db)
):
    service = HabitacionesService(db)
    return service.listar_habitaciones(tipoHabitacion)