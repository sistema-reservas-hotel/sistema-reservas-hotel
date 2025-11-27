from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repository.HabitacionPrecio_repository import TipoHabitacionRepository
from app.domain.HabitacionPrecio_model import TipoHabitacionPrecioUpdate

class TipoHabitacionService:
    def __init__(self, db: Session):
        self.repository = TipoHabitacionRepository(db)

    def cambiar_precio(self, id_tipoHabitacion: int, precio_data: TipoHabitacionPrecioUpdate):
        # Ya no hace falta validar <= 0 porque Pydantic lo maneja
        resultado = self.repository.update_precio(id_tipoHabitacion, precio_data.nuevo_precio)
        if resultado is None:
            raise HTTPException(status_code=404, detail="Tipo de habitación no encontrado")
        
        return {
            "mensaje": "Precio actualizado correctamente.",
            "data": resultado,
            "success": True
        }
