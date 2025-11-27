from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.Preferencias_service import PreferenciasService
from app.domain.Preferencias_model import PreferenciasBase, PreferenciasResponse

router = APIRouter(prefix="/api/v1/cliente/preferencias", tags=["Preferencias Cliente"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=PreferenciasResponse)
def obtener_preferencias(id_cliente: int, db: Session = Depends(get_db)):
    service = PreferenciasService(db)
    return service.get_preferencias(id_cliente)

@router.put("/", response_model=PreferenciasResponse)
def guardar_preferencias(id_cliente: int, preferencias: PreferenciasBase, db: Session = Depends(get_db)):
    service = PreferenciasService(db)
    return service.save_preferencias(id_cliente, preferencias)
