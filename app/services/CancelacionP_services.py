from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repository.CancelacionP_repository import PagoRepository
from app.domain.CancelacionP_model import PagoCancelacionSalida, PagoCanceladoResponse

class PagoService:
    def __init__(self, db: Session):
        self.repository = PagoRepository(db)
        self.MOTIVO_CANCELACION_CLIENTE = "Cancelación solicitada por el cliente antes del check-in."

    def cancelar_pago_por_id(self, id_pago: int) -> PagoCancelacionSalida:
        """
        Cancela un pago verificando su existencia y su estado actual.
        """
        pago_existente = self.repository.get_by_id(id_pago)

        # 1. Pago Inexistente o ya Cancelado (PAY_404)
        if not pago_existente or pago_existente.estado_pago == "Cancelado":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "success": False,
                    "error_code": "PAY_404",
                    "message": "El pago indicado no existe o ya fue cancelado previamente.",
                    "details": {"idPago": id_pago}
                }
            )

        # 2. Pago no Cancelable (PAY_403)
        # Asumimos que 'Completado' o 'Liquidado' es el estado final no cancelable
        if pago_existente.estado_pago in ["Completado", "Liquidado"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "success": False,
                    "error_code": "PAY_403",
                    "message": "El pago no puede ser cancelado porque ya fue liquidado o verificado por la pasarela bancaria.",
                    "details": {"idPago": id_pago, "estadoActual": pago_existente.estado_pago}
                }
            )

        # 3. Cancelación Exitosa
        datos_cancelados = self.repository.cancelar_pago(id_pago, self.MOTIVO_CANCELACION_CLIENTE)
        
        # El repositorio debe retornar datos si fue exitoso
        if datos_cancelados:
            return PagoCancelacionSalida(
                success=True,
                message="El pago ha sido cancelado exitosamente por solicitud del cliente.",
                data=PagoCanceladoResponse(**datos_cancelados)
            )
        
        # Fallo inesperado
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"success": False, "message": "Fallo interno al procesar la cancelación."}
        )