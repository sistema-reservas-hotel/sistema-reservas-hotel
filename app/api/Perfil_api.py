from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.utils.jwt_manager import get_current_user_payload 
from app.database import SessionLocal
from app.services.Perfil_service import PerfilService
from app.domain.Perfil_model import PerfilUpdateRequest

router = APIRouter(
    prefix="/api/v1/cliente",
    tags=["Perfil"]
)

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()


@router.get("/perfil", status_code=status.HTTP_200_OK)
def obtener_perfil(
    current_user_payload: dict = Depends(get_current_user_payload), 
    db: Session = Depends(get_db)
):
    
    id_cliente = current_user_payload.get("id_cliente")
    service = PerfilService(db)
    return service.obtener_perfil(id_cliente)




@router.put("/perfil", status_code=status.HTTP_200_OK)
def actualizar_perfil(
    data: PerfilUpdateRequest,
    current_user_payload: dict = Depends(get_current_user_payload),
    db: Session = Depends(get_db)
):
    id_cliente = current_user_payload.get("id_cliente")
    service = PerfilService(db)
    return service.actualizar_perfil(id_cliente, data)