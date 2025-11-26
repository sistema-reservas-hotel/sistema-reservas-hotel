from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.Preferencias_service import PreferenciasService
from app.domain.Preferencias_model import PreferenciasBase

router = APIRouter(prefix="/api/clientes", tags=["Preferencias"])

service = PreferenciasService()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# GET - consultar preferencias
@router.get("/preferencias")
def get_preferencias(
    db: Session = Depends(get_db),
    Authorization: str = Header(...)
):
    token = Authorization.split(" ")[1]
    return service.get_preferencias(db, token)


# PUT - guardar o actualizar preferencias
@router.put("/preferencias")
def update_preferencias(
    preferencias: PreferenciasBase,
    db: Session = Depends(get_db),
    Authorization: str = Header(...)
):
    token = Authorization.split(" ")[1]
    return service.update_preferencias(db, token, preferencias)
