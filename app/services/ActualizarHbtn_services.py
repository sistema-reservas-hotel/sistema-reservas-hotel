from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repository.ActualizarHbtn_repository import ActualizarRepository
from app.domain.ActualizarHbtn_model import ActualizarEstado

class HabitacionService:
    def _init_(self, db: Session):
        self.repository = ActualizarRepository(db)

    def cambiar_estado(self, id_habitacion: int, estado_data: ActualizarEstado):
        resultado = self.repository.update_estado(id_habitacion, estado_data.nuevo_estado)
        if resultado is None:
            raise HTTPException(status_code=404, detail="Habitación no encontrada")
        if resultado is False:
            raise HTTPException(
                status_code=409,
                detail="No se puede cambiar a 'Disponible', existen reservas activas"
            )
        return {
            "mensaje": "Estado de la habitación actualizado correctamente.",
            "data": resultado,
            "success": True
        }