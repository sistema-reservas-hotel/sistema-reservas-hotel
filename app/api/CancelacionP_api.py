from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal # Asumiendo que 'database.py' existe
from app.services.CancelacionP_services import PagoService
from app.domain.CancelacionP_model import PagoCancelacionSalida

router = APIRouter(prefix="/pagos", tags=["Pagos"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.delete(
    "/{id_pago}",
    status_code=status.HTTP_200_OK,
    response_model=PagoCancelacionSalida,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": dict},
        status.HTTP_403_FORBIDDEN: {"model": dict},
    }
)
def cancelar_pago(id_pago: int, db: Session = Depends(get_db)):
    """
    🚨 **[DELETE /pagos/{id_pago}]**
    Cancela un pago asociado a una reserva por solicitud del personal administrativo.
    """
    try:
        service = PagoService(db)
        # Se llama al método con el ID
        return service.cancelar_pago_por_id(id_pago)
    except HTTPException as e:
        raise e