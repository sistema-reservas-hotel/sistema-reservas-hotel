from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repository.preferencias_repository import PreferenciasRepository
from app.domain.preferencias_model import PreferenciasBase, PreferenciasResponse

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
        return PreferenciasResponse.from_orm(prefs)

    def save_preferencias(self, id_cliente: int, datos: PreferenciasBase):
        prefs = self.repository.save(id_cliente, datos)
        return PreferenciasResponse.from_orm(prefs)
