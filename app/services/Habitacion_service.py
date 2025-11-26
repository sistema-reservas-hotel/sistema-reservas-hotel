from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repository.Habitacion_repository import HabitacionesRepository


class HabitacionesService:
    def __init__(self, db: Session):
        self.repository = HabitacionesRepository(db)

    def listar_habitaciones(self, tipo: str | None = None):

        # Si el usuario envía un tipoHabitacion específico
        if tipo:
            hab = self.repository.get_habitacion_by_tipo(tipo)
            if not hab:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No existe habitación con tipo '{tipo}'."
                )
            return hab

        # Si NO envía tipoHabitacion → devolver todas
        habitaciones = self.repository.get_all_habitaciones()
        if not habitaciones:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No hay habitaciones disponibles."
            )

        return habitaciones

    def obtener_planes(self, tipo: str):
        habitacion = self.repository.get_habitacion_by_tipo(tipo)

        if not habitacion:
            raise HTTPException(
                status_code=404,
                detail=f"No existe habitación con tipo '{tipo}'."
            )

        planes = self.repository.get_planes_por_habitacion(habitacion.id_tipoHabitacion)

        return {
            "habitacion": habitacion,
            "planes": planes
        }
