from sqlalchemy.orm import Session
from datetime import datetime
from app.repository.ProcesoPago_repository import PagosRepository
from app.repository.ProcesoPago_repository import ReservaRepository
from app.services.ProcesoPago_services import FacturacionService
from app.domain.ProcesoPago_model import PagoCreacion

class PagosService:

    def __init__(self, db: Session):
        self.db = db
        self.pagos_repo = PagosRepository(db)
        self.reservas_repo = ReservaRepository(db)
        self.facturacion_service = FacturacionService(db)

    def procesar_pago(self, pago_data: PagoCreacion):
        # 1. Verificar reserva
        reserva = self.reservas_repo.obtener_reserva(pago_data.id_reserva)
        if not reserva:
            return {"success": False, "mensaje": "Reserva no existe."}, 404

        if reserva.estado != "Pendiente de pago":
            return {"success": False, "mensaje": "La reserva no está pendiente de pago."}, 409

        # 2. Registrar pago en estado Pendiente
        pago = self.pagos_repo.crear_pago(pago_data)

        # 3. Normalmente aquí rediriges a la pasarela
        return {"success": True, "mensaje": "Pago iniciado.", "id_pago": pago.id_pago}, 200

    def recibir_webhook(self, payload: dict):
        id_pago = payload.get("id_pago")
        estado = payload.get("estado")
        comprobante = payload.get("comprobante")

        pago = self.pagos_repo.obtener_pago(id_pago)
        if not pago:
            return {"success": False, "mensaje": "Pago no encontrado."}, 404

        # Actualizar pago
        pago = self.pagos_repo.actualizar_estado_pago(id_pago, estado, comprobante)

        # Si es exitoso: confirmar reserva, generar factura
        if estado == "Exitoso":

            self.reservas_repo.actualizar_estado(pago.id_reserva, "Confirmada")

            factura = self.facturacion_service.generar_factura(
                id_pago=pago.id_pago,
                total=pago.monto
            )

            return {
                "success": True,
                "mensaje": "Pago procesado exitosamente. Reserva confirmada.",
                "data": {
                    "id_pago": pago.id_pago,
                    "id_reserva": pago.id_reserva,
                    "monto": pago.monto,
                    "estado_pago": pago.estado_pago,
                    "factura": factura
                }
            }, 200

        return {"success": False, "mensaje": "Pago fallido."}, 402

    def procesar_reembolso(self, id_pago: int):
        pago = self.pagos_repo.obtener_pago(id_pago)
        if not pago:
            return {"success": False, "mensaje": "Pago no encontrado."}, 404

        if pago.estado_pago != "Exitoso":
            return {"success": False, "mensaje": "No se puede reembolsar un pago no confirmado."}, 409

        reserva = self.reservas_repo.obtener_reserva(pago.id_reserva)

        # Política de reembolso
        horas = reserva.horas_antes_checkin()

        if horas >= 48:
            monto = pago.monto  # 100%
        elif 24 <= horas < 48:
            monto = pago.monto * 0.5
        else:
            return {"success": False, "mensaje": "No aplica reembolso."}, 409

        pago = self.pagos_repo.registrar_reembolso(pago.id_pago, monto)

        return {
            "success": True,
            "mensaje": "Reembolso procesado exitosamente.",
            "data": {
                "id_pago": pago.id_pago,
                "id_reserva": pago.id_reserva,
                "monto_reembolsado": monto,
                "fecha_reembolso": datetime.utcnow()
            }
        }, 200
