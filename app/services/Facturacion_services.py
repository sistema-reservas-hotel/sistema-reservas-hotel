from sqlalchemy.orm import Session
from datetime import datetime
from app.models.FacturaBD import FacturaBD
from uuid import uuid4

class FacturacionService:

    def __init__(self, db: Session):
        self.db = db

    def generar_factura(self, id_pago: int, id_reserva: int, id_cliente: int, monto_total: float):
        numero_factura = f"FAC-{uuid4().hex[:8].upper()}"
        factura = FacturaBD(
            id_pago=id_pago,
            id_reserva=id_reserva,
            id_cliente=id_cliente,
            numero_factura=numero_factura,
            monto_total=monto_total,
            fecha_emision=datetime.utcnow(),
            estado="Emitida"
        )
        self.db.add(factura)
        self.db.commit()
        self.db.refresh(factura)
        return factura
