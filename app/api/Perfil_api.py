from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.database import SessionLocal
from app.services.Perfil_service import PerfilService
from app.domain.Perfil_model import PerfilUpdateRequest
from app.utils.jwt_manager import decode_token

router = APIRouter(
    prefix="/api/v1/cliente",
    tags=["Perfil"]
)

security = HTTPBearer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/perfil", status_code=status.HTTP_200_OK)
def obtener_perfil(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    payload = decode_token(token)
    id_cliente = int(payload.get("sub"))

    service = PerfilService(db)
    return service.obtener_perfil(id_cliente)


@router.put("/perfil", status_code=status.HTTP_200_OK)
def actualizar_perfil(
    data: PerfilUpdateRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    payload = decode_token(token)
    id_cliente = int(payload.get("sub"))

    service = PerfilService(db)
    return service.actualizar_perfil(id_cliente, data)
