
from fastapi import APIRouter, Depends
from app.database import get_db
from app.services.Habitacion_service import HabitacionesService

router = APIRouter(prefix="/api/v1/reservas/habitaciones", tags=["Habitaciones"])

@router.get("/disponibilidad")
def disponibilidad(tipoHabitacion: str = None, db=Depends(get_db)):
    service = HabitacionesService(db)
    return service.listar_habitaciones(tipoHabitacion)
