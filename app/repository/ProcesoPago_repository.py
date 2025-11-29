from sqlalchemy.orm import Session
from app.models.PagosBD import PagosDB
from app.domain.ProcesoPago_model import PagoBase
from datetime import datetime

class PagosRepository:

    def __init__(self, db: Session):
        self.db = db

    def crear_pago(self, data: PagoBase):
        nuevo_pago = PagosDB(
            id_cliente=data.id_cliente,
            id_reserva=data.id_reserva,
            monto=data.monto,
            metodo=data.metodo,
            estado_pago="Pendiente",
            fecha_pago=datetime.utcnow()
        )
        self.db.add(nuevo_pago)
        self.db.commit()
        self.db.refresh(nuevo_pago)
        return nuevo_pago

    def obtener_pago(self, id_pago: int):
        return self.db.query(PagosDB).filter(PagosDB.id_pago == id_pago).first()

    def actualizar_estado_pago(self, id_pago: int, estado: str, comprobante: str = None):
        pago = self.obtener_pago(id_pago)
        if not pago:
            return None

        pago.estado_pago = estado
        if comprobante:
            pago.comprobante = comprobante

        self.db.commit()
        self.db.refresh(pago)
        return pago

    def registrar_reembolso(self, id_pago: int, monto):
        pago = self.obtener_pago(id_pago)
        if not pago:
            return None

        pago.estado_pago = "Reembolsado"
        pago.monto = pago.monto - monto

        self.db.commit()
        self.db.refresh(pago)
        return pago
