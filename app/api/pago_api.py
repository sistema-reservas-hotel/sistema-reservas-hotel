from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from services.pago_service import PagoService
from domain.pago_model import ResponsePagos
from typing import Optional
from datetime import datetime

router = APIRouter(prefix="/clientes", tags=["Pagos"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/pagos", response_model=ResponsePagos)
def historial_pagos(id_cliente: int,
                    estado: Optional[str] = None,
                    desde: Optional[datetime] = None,
                    hasta: Optional[datetime] = None,
                    db: Session = Depends(get_db)):
    """Consulta el historial de pagos del cliente autenticado"""
    service = PagoService(db)
    return service.historial_pagos(id_cliente=id_cliente, estado=estado, desde=desde, hasta=hasta)
