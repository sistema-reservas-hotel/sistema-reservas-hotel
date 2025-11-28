from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.TipoHabitacion_service import TipoHabitacionService
from app.domain.TipoHabitacion_model import TipoHabitacionCreate, TipoHabitacionResponse

router = APIRouter(prefix="/habitaciones/tipo", tags=["Habitaciones"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=TipoHabitacionResponse, status_code=status.HTTP_201_CREATED)
def create_tipo(tipo: TipoHabitacionCreate, db: Session = Depends(get_db)):
    service = TipoHabitacionService(db)
    return service.create_tipo(tipo)

@router.put("/{id_tipoHabitacion}", response_model=TipoHabitacionResponse)
def update_tipo(id_tipoHabitacion: int, tipo: TipoHabitacionCreate, db: Session = Depends(get_db)):
    service = TipoHabitacionService(db)
    return service.update_tipo(id_tipoHabitacion, tipo)

@router.delete("/{id_tipoHabitacion}")
def delete_tipo(id_tipoHabitacion: int, db: Session = Depends(get_db)):
    """Elimina un tipo de habitación si no tiene reservas activas"""
    service = TipoHabitacionService(db)
    return service.delete_tipo(id_tipoHabitacion)
