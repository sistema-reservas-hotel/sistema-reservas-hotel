from fastapi import APIRouter, Depends, Header, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.Reserva_service import ReservaService
from app.utils.jwt_manager import get_current_user_payload as jwt_verify

router = APIRouter(prefix="/api/cliente", tags=["Reservas"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def verificar_token(token_data: dict = Depends(jwt_verify)):
    id_cliente = token_data.get("id_cliente")

    if not id_cliente:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "mensaje": "No tiene permisos para acceder a esta información.",
                "success": False,
                "error_code": "AUTH_401"
            }
        )
    
    return id_cliente

@router.get("/reservas")
def obtener_reservas_cliente(
    estado: str | None = Query(None),
    fecha_inicio: str | None = Query(None, description="Formato YYYY-MM-DD"),
    fecha_fin: str | None = Query(None, description="Formato YYYY-MM-DD"),
    cliente_id: dict = Depends(verificar_token),
    db: Session = Depends(get_db)
):

    service = ReservaService(db)
    resultado = service.consultar_reservas(
        id_cliente=cliente_id,
        estado=estado,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin
    )

    return resultado