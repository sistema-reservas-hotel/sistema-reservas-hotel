from fastapi import HTTPException
from app.repository.NuevaReserva_repository import ReservaRepository
from app.models.ReservasBD import ReservasDB
from datetime import datetime

class ReservaService:

    def __init__(self, db):
        self.db = db
        self.repo = ReservaRepository(db)

    def crear_reserva(self, data):

        # Validación de fechas
        if data.check_out <= data.check_in:
            raise HTTPException(status_code=400, detail={
                "mensaje": "La fecha de salida debe ser posterior a la fecha de entrada.",
                "success": False
            })

        # Buscar habitación disponible
        habitacion_libre = self.repo.buscar_disponibilidad(data.id_tipoHabitacion)
        if not habitacion_libre:
            raise HTTPException(status_code=204, detail={
                "mensaje": "No hay habitaciones disponibles para el tipo solicitado.",
                "success": False
            })

        # Validar capacidad
        if data.capacidad > habitacion_libre.capacidad:
            raise HTTPException(status_code=409, detail={
                "mensaje": "El número de personas excede la capacidad de la habitación.",
                "success": False
            })

        # Crear reserva
        nueva_reserva = ReservasDB(
            id_cliente=data.id_cliente,
            id_tipoHabitacion=data.id_tipoHabitacion,
            fecha_reserva=datetime.now(),
            check_in=data.check_in,
            check_out=data.check_out,
            nombre=habitacion_libre.nombre,
            plan_incluido=data.plan_incluido,
            valor_total=habitacion_libre.precio_base,
            estado_reserva="Confirmada"
        )

        reserva = self.repo.crear_reserva(nueva_reserva)

        return {
            "mensaje": "Reserva creada exitosamente.",
            "success": True,
            "data": {
                "id_reserva": reserva.id_reserva,
                "id_cliente": reserva.id_cliente,
                "habitacion": reserva.habitacion,
                "nombre": reserva.nombre,
                "plan_incluido": reserva.plan_incluido,
                "check_in": str(reserva.check_in),
                "check_out": str(reserva.check_out),
                "valor_total": reserva.valor_total,
                "estado": reserva.estado_reserva
            }
        }

    def obtener_reserva(self, id_reserva: int):
        reserva = self.repo.obtener_reserva(id_reserva)
        if not reserva:
            raise HTTPException(status_code=404, detail={
                "mensaje": "Reserva no encontrada",
                "success": False
            })
        return reserva
