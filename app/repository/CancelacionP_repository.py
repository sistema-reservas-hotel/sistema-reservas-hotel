from sqlalchemy.orm import Session
from app.models.PagosBD import PagosDB
from datetime import datetime
from typing import Optional

class PagoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, id_pago: int) -> Optional[PagosDB]:
        """Busca un pago por su ID."""
        return self.db.query(PagosDB).filter(PagosDB.id_pago == id_pago).first()

    def cancelar_pago(self, id_pago: int, motivo: str) -> Optional[dict]:
        """
        Actualiza el estado de un pago a 'Cancelado' y registra fecha/motivo.
        Retorna los datos del pago cancelado o None si no existe/no se pudo actualizar.
        """
        pago = self.get_by_id(id_pago)
        
        if not pago:
            return None 
        
        
        if pago.estado_pago == "Cancelado":
             return None 

        
        
        pago.estado_pago = "Cancelado"
        self.db.commit()
        self.db.refresh(pago)
        
    
        fecha_cancelacion_mock = datetime.now() 
        return {
            "id_pago": pago.id_pago,
            "id_reserva": pago.id_reserva,
            "monto": pago.monto,
            "estado_pago": pago.estado_pago,
            "fechaCancelacion": fecha_cancelacion_mock, 
            "motivo": motivo
        }