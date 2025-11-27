# app/api/Plan_api.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.SeleccionPlanes_service import PlanesService
from app.database import SessionLocal

router = APIRouter(prefix="/reservas", tags=["Planes"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/planes")
def listar_planes(db: Session = Depends(get_db)):
    service = PlanesService(db)
    return service.obtener_planes()
