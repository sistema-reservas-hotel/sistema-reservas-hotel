from sqlalchemy.orm import Session
from app.repository.pago_repository import PagoRepository
from app.domain.pago_model import ResponsePagos, PagoDetalle
from fastapi import HTTPException
from typing import Optional
from datetime import datetime

class PagoService:
    def __init__(self, db: Session):
        self.repository = PagoRepository(db)

    def historial_pagos(self, id_cliente: int,
                        estado: Optional[str] = None,
                        desde: Optional[datetime] = None,
                        hasta: Optional[datetime] = None) -> ResponsePagos:
        try:
            pagos = self.repository.get_pagos_cliente(id_cliente, estado, desde, hasta)
            if not pagos:
                return ResponsePagos(success=False, mensaje="No existen pagos registrados para este usuario.", data={"pagos": []})

            pagos_list = [PagoDetalle(
                id_pago=p.id_pago,
                fecha_pago=p.fecha_pago,
                monto=p.monto,
                metodo=p.metodo,
                estado=p.estado,
                comprobante=p.comprobante if p.estado.lower() == "completado" else None
            ) for p in pagos]

            return ResponsePagos(success=True, mensaje="Historial de pagos consultado correctamente.", data={"pagos": pagos_list})
        except Exception as e:
            raise HTTPException(status_code=503, detail={"success": False, "error_code": "PAY_503", "mensaje": "No se pudo obtener el historial de pagos. Intente más tarde."})
