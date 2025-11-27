from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.HabitacionPrecio_services import TipoHabitacionService
from app.domain.HabitacionPrecio_model import TipoHabitacionPrecioUpdate

router = APIRouter(prefix="/habitaciones/tipo", tags=["Tipos de Habitación"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.put("/{id}/precio", status_code=status.HTTP_200_OK)
def update_precio(id: int, precio: TipoHabitacionPrecioUpdate, db: Session = Depends(get_db)):
    """
    Actualiza el precio base de un tipo de habitación
    """
    service = TipoHabitacionService(db)
    return service.cambiar_precio(id, precio)