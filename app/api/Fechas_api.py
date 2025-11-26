# app/api/fechas_api.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.Fechas_service import FechasService

router = APIRouter(prefix="/api/v1/reservas/fechas", tags=["Fechas"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

service = FechasService()

@router.get("/disponibilidad")
def disponibilidad(
    fechaEntrada: str | None = Query(None, description="Fecha de entrada en ISO 8601 (YYYY-MM-DDTHH:MM:SSZ)"),
    fechaSalida: str | None = Query(None, description="Fecha de salida en ISO 8601 (YYYY-MM-DDTHH:MM:SSZ)"),
    db: Session = Depends(get_db)
):
    return service.disponibilidad(db, fechaEntrada, fechaSalida)
