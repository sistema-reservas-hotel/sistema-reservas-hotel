from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repository.Preferencias_repository import PreferenciasRepository
from app.domain.Preferencias_model import PreferenciasBase, PreferenciasResponse

class PreferenciasService:
    def __init__(self, db: Session):
        self.repository = PreferenciasRepository(db)

    def get_preferencias(self, id_cliente: int):
        prefs = self.repository.get_by_cliente(id_cliente)
        if not prefs:
            raise HTTPException(
                status_code=200,
                detail="No existen preferencias registradas para este usuario."
            )
        return PreferenciasResponse(
            mensaje="Preferencias encontradas",
            data=PreferenciasBase.from_orm(prefs),
            success=True
        )

    def save_preferencias(self, id_cliente: int, datos: PreferenciasBase):
        prefs = self.repository.save_or_update(id_cliente, datos.dict())
        return PreferenciasResponse(
            mensaje="Preferencias guardadas correctamente",
            data=PreferenciasBase.from_orm(prefs),
            success=True
        )
