from sqlalchemy.orm import Session
from app.repository.TipoHabitacion_repository import TipoHabitacionRepository
from app.domain.TipoHabitacion_model import TipoHabitacionCreate, TipoHabitacionResponse
from fastapi import HTTPException, status

class TipoHabitacionService:
    def __init__(self, db: Session):
        self.repository = TipoHabitacionRepository(db)

    def create_tipo(self, tipo_data: TipoHabitacionCreate) -> TipoHabitacionResponse:
        # Validar nombre duplicado
        existing_tipo = self.repository.get_by_nombre(tipo_data.nombre)
        if existing_tipo:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nombre de tipo de habitación ya registrado")
        tipo = self.repository.create_tipo(tipo_data)
        return TipoHabitacionResponse.from_orm(tipo)

    def update_tipo(self, id_tipo: int, tipo_data: TipoHabitacionCreate) -> TipoHabitacionResponse:
        tipo = self.repository.get_by_id(id_tipo)
        if not tipo:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tipo de habitación no encontrado")
        updated_tipo = self.repository.update_tipo(id_tipo, tipo_data.dict())
        return TipoHabitacionResponse.from_orm(updated_tipo)

    def delete_tipo(self, id_tipo: int):
        tipo = self.repository.get_by_id(id_tipo)
        if not tipo:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tipo de habitación no encontrado")
        result = self.repository.delete_tipo(id_tipo)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="No es posible eliminar el tipo de habitación, existen reservas asociadas.",
            )
        return {"mensaje": "Tipo de habitación eliminado correctamente.", "success": True}
