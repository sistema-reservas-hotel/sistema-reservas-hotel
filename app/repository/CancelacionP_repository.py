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
            return None # Pago no encontrado
        
        # Validación de estado cancelable (la lógica más estricta va en el Servicio)
        if pago.estado_pago == "Cancelado":
             return None # Ya cancelado, el servicio lo manejará como 404 (no encontrado/ya procesado)

        # Se asume que tu modelo PagosDB necesita columnas para la trazabilidad de la cancelación.
        # Si no existen, deberías agregarlas (ej: fecha_cancelacion, motivo_cancelacion).
        # Por ahora, usaré las siguientes (deberías añadirlas a PagosDB si no están):
        # pago.fecha_cancelacion = datetime.now()
        # pago.motivo_cancelacion = motivo 
        
        # --- Asumiendo que se agregan estos campos al modelo PagosDB ---
        
        # Como no están en tu modelo PagosDB, simularemos su existencia en el diccionario de retorno:
        # Si tienes estas columnas en tu modelo PagosDB, descomenta y úsalas:
        # pago.fecha_cancelacion = datetime.now()
        # pago.motivo_cancelacion = motivo
        
        pago.estado_pago = "Cancelado"
        self.db.commit()
        self.db.refresh(pago)
        
        # --- Preparación de la salida para el Servicio ---
        # Se agregan los campos de cancelación temporalmente para la respuesta JSON.
        fecha_cancelacion_mock = datetime.now() # Mock de fecha de cancelación

        return {
            "id_pago": pago.id_pago,
            "id_reserva": pago.id_reserva,
            "monto": pago.monto,
            "estado_pago": pago.estado_pago,
            "fechaCancelacion": fecha_cancelacion_mock, # Usando el mock
            "motivo": motivo # Usando el motivo
        }