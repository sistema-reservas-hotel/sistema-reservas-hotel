from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.services.ActualizarHbtn_services import HabitacionService
from app.domain.ActualizarHbtn_model import ActualizarEstado
from app.database import SessionLocal

router = APIRouter(prefix="/habitaciones", tags=["Habitaciones"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.put("/{id}/estado", status_code=status.HTTP_200_OK)
def update_estado(id: int, estado: ActualizarEstado, db: Session = Depends(get_db)):
    """
    Actualiza el estado de una habitación
    """
    service = HabitacionService(db)
    return service.cambiar_estado(id, estado)