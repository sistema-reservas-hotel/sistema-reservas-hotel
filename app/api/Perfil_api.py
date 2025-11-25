from fastapi import APIRouter, Depends, Header, status
from sqlalchemy.orm import Session
from app.models import SessionLocal
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

@router.get("/perfi", status_code=status.HTTP_200_OK)
def obtener_perfil(authorization: str = Header(None), db: Session = Depends(get_db)):
    if not authorization:
        return {
            "mensaje": "Token invalido o sesion expirada.",
            "data": None,
            "success": False,
            "error_code": "AUTH_401"
        }
    
    token = authorization.replace("Bearer ", "")
    service = PerfilService(db)
    return service.obtener_perfil(token)


@router.put("/perfil", status_code=status.HTTP_200_OK)
def actualizar_perfil(
    data: PerfilUpdateRequest,
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    if not authorization:
        return {
            "mensaje": "Token inválido o sesión expirada.",
            "data": None,
            "success": False,
            "error_code": "AUTH_401"
        }
    
    token = authorization.replace("Bearer ", "")
    service = PerfilService(db)
    return service.actualizar_perfil(token, data)
