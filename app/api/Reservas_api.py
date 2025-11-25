from fastapi import APIRouter, Depends, Header, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.Reserva_service import ReservaService
from app.utils.jwt_manager import decode_token 

router = APIRouter(prefix="/api/cliente", tags=["Reservas"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def verificar_token(authorization: str = Header(None)):

    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "mensaje": "No tiene permisos para acceder a esta información.",
                "success": False,
                "error_code": "AUTH_401"
            }
        )

    token = authorization.replace("Bearer ", "").strip()
    payload = decode_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "mensaje": "No tiene permisos para acceder a esta información.",
                "success": False,
                "error_code": "AUTH_401"
            }
        )

    id_cliente = payload.get("id_cliente") or payload.get("sub") or payload.get("email")
    return {"payload": payload, "id_cliente": id_cliente}


@router.get("/reservas")
def obtener_reservas_cliente(
    estado: str | None = Query(None),
    fecha_inicio: str | None = Query(None, description="Formato YYYY-MM-DD"),
    fecha_fin: str | None = Query(None, description="Formato YYYY-MM-DD"),
    token_data: dict = Depends(verificar_token),
    db: Session = Depends(get_db)
):

    id_cliente = token_data.get("id_cliente")

    try:
        if isinstance(id_cliente, int):
            cliente_id = id_cliente
        else:
            cliente_id = int(id_cliente)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "mensaje": "Token inválido o sesión expirada.",
                "data": None,
                "success": False,
                "error_code": "AUTH_401"
            }
        )

    service = ReservaService(db)
    resultado = service.consultar_reservas(
        id_cliente=cliente_id,
        estado=estado,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin
    )

    return resultado