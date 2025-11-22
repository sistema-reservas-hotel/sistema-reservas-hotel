from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.fechas_service import FechasService


router = APIRouter(prefix="/api/v1/reservas/fechas", tags=["Fechas"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/disponibilidad")
def disponibilidad_fechas(
    fechaEntrada: str | None = Query(None, description="Formato ISO 8601: YYYY-MM-DDTHH:MM:SSZ"),
    fechaSalida: str | None = Query(None, description="Formato ISO 8601: YYYY-MM-DDTHH:MM:SSZ"),
    db: Session = Depends(get_db)
):
    """
    Endpoint para consultar disponibilidad por rango de fechas.
    Si no se envían parámetros, devuelve calendario general (próximos 90 días).
    """
    service = FechasService(db)
    resultado = service.buscar_disponibilidad(fechaEntrada, fechaSalida)

   
    if resultado.get("error_code") == "RES_400":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=resultado)

   
    if resultado.get("error_code") == "RES_503":
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=resultado)

  
    return resultado
