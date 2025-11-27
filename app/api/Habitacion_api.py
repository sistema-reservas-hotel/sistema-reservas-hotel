from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.Habitacion_service import HabitacionesService
from app.domain.Habitacion_model import HabitacionesResponse, HabitacionResponse, ErrorResponse

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

@router.get(
    "/disponibilidad",
    response_model=HabitacionesResponse | HabitacionResponse | ErrorResponse,
    status_code=status.HTTP_200_OK
)
def obtener_habitaciones_disponibilidad(
    tipoHabitacion: str = Query(None, description="Filtrar por tipo de habitación"),
    db: Session = Depends(get_db)
):
    service = HabitacionesService(db)
    return service.listar_habitaciones(tipoHabitacion)
