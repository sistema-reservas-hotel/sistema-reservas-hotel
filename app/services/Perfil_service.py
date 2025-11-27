from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repository.Perfil_repository import PerfilRepository
from app.domain.Perfil_model import PerfilUpdateRequest, PerfilResponse

class PerfilService:
    def __init__(self, db: Session):
        self.repository = PerfilRepository(db)

    def obtener_perfil(self, id_cliente: int):
        perfil = self.repository.get_by_cliente(id_cliente)
        if not perfil:
            raise HTTPException(status_code=404, detail="Perfil no encontrado")
        return PerfilResponse(
            mensaje="Perfil obtenido correctamente",
            data=PerfilUpdateRequest.from_orm(perfil),
            success=True
        )

    def actualizar_perfil(self, id_cliente: int, data: PerfilUpdateRequest):
        perfil = self.repository.update_cliente(id_cliente, data.dict())
        return PerfilResponse(
            mensaje="Perfil actualizado correctamente",
            data=PerfilUpdateRequest.from_orm(perfil),
            success=True
        )
