from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.NuevaReserva_services import ReservaService
from app.domain.NuevaReserva_model import ReservaRequest

router = APIRouter(prefix="/api/v1/reservas", tags=["Reservas"])

@router.post("/")
def crear_reserva(request: ReservaRequest, db: Session = Depends(get_db)):
    service = ReservaService(db)
    return service.crear_reserva(request)

@router.get("/{id_reserva}")
def obtener_reserva(id_reserva: int, db: Session = Depends(get_db)):
    service = ReservaService(db)
    return service.obtener_reserva(id_reserva)
