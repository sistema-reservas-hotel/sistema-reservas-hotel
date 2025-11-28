from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.ProcesoPago_services import PagosService
from app.domain.ProcesoPago_model import PagoCreacion

router = APIRouter(prefix="/api/pagos", tags=["Pagos"])

@router.post("/procesar")
def procesar_pago(data: PagoCreacion, db: Session = Depends(get_db)):
    service = PagosService(db)
    return service.procesar_pago(data)

@router.post("/webhook")
async def webhook(request: Request, db: Session = Depends(get_db)):
    payload = await request.json()
    service = PagosService(db)
    return service.recibir_webhook(payload)

@router.put("/{id_pago}/reembolsar")
def reembolsar(id_pago: int, db: Session = Depends(get_db)):
    service = PagosService(db)
    return service.procesar_reembolso(id_pago)
