from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
# from database import SessionLocal # Importación necesaria
from app.services.NuevaReserva_services import ReservaService
from app.domain.NuevaReserva_model import ReservaCreacion, ReservaCreacionSalida

router = APIRouter(prefix="/reservas", tags=["Reservas"])

# Asumiendo que get_db está disponible:
def get_db():
    db = SessionLocal() # Define SessionLocal en tu entorno
    try:
        yield db
    finally:
        db.close()

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=ReservaCreacionSalida,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": dict},
        status.HTTP_409_CONFLICT: {"model": dict},
        status.HTTP_204_NO_CONTENT: {"model": dict},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": dict},
    }
)
def crear_reserva(reserva: ReservaCreacion, db: Session = Depends(get_db)):
    """
    ➕ **[POST /reservas]**
    Crea una nueva reserva validando fechas, capacidad y disponibilidad en el inventario.
    """
    try:
        service = ReservaService(db)
        return service.crear_nueva_reserva(reserva)
    except HTTPException as e:
        raise e