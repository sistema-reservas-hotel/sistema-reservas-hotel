from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.Preferencias_service import PreferenciasService
from app.domain.Preferencias_model import PreferenciasBase
from app.utils.jwt_manager import get_current_user_payload 

router = APIRouter(prefix="/api/clientes", tags=["Preferencias"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/preferencias")
def get_preferencias(
    db: Session = Depends(get_db),
    current_user_payload: dict = Depends(get_current_user_payload)
):

    id_cliente = current_user_payload.get("id_cliente")
    service = PreferenciasService(db)
    return service.get_preferencias(id_cliente)


@router.put("/preferencias")
def update_preferencias(
    preferencias: PreferenciasBase,
    db: Session = Depends(get_db),
    current_user_payload: dict = Depends(get_current_user_payload)
):
    
    id_cliente = current_user_payload.get("id_cliente")
    service = PreferenciasService(db) 
    return service.update_preferencias(id_cliente, preferencias)