from sqlalchemy.orm import Session
from typing import Optional
from repository.Reserva_repository import ReservaRepository
from domain.Reserva_model import ReservaItem, ReservasData, ReservasResponse
from datetime import datetime, date

class ReservaService:

    def __init__(self, db: Session):
        self.repo = ReservaRepository(db)

    def consultar_reservas(
        self,
        id_cliente: int,
        estado: Optional[str] = None,
        fecha_inicio: Optional[str] = None,
        fecha_fin: Optional[str] = None
    ) -> dict:

        fecha_inicio_dt = None
        fecha_fin_dt = None

        try:
            if fecha_inicio:
                fecha_inicio_dt = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
            if fecha_fin:
                fecha_fin_dt = datetime.strptime(fecha_fin, "%Y-%m-%d").date()
        except ValueError:

            return {
                "mensaje": "Formato de fecha inválido. Use YYYY-MM-DD.",
                "data": {"reservas": []},
                "success": False
            }

        reservas_orm = self.repo.obtener_reservas_por_cliente(
            id_cliente=id_cliente,
            estado=estado,
            fecha_inicio=fecha_inicio_dt,
            fecha_fin=fecha_fin_dt
        )

        if not reservas_orm:
            return {
                "mensaje": "No existen reservas registradas para este usuario.",
                "data": {"reservas": []},
                "success": False
            }

        reservas_list = [ReservaItem.from_orm(r) for r in reservas_orm]
        reservas_data = ReservasData(reservas=reservas_list)

        response: ReservasResponse = ReservasResponse(
            mensaje="Consulta de reservas exitosa.",
            data=reservas_data,
            success=True
        )

        return response.dict()
