from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repository.Perfil_repository import PerfilRepository
from app.domain.Perfil_model import PerfilResponse, PerfilUpdateRequest
from app.utils.jwt_manager import decode_token

class PerfilService:

    def _init_(self, db: Session):
        self.repository = PerfilRepository(db)

    def obtener_perfil(self, token: str):
        payload = decode_token(token)
        if payload is None:
            raise HTTPException(
                 status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido o sesión expirada."
            )   
        id_cliente = payload.get("id_cliente")
        cliente = self.repository.get_cliente_by_id(id_cliente)

        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente no encontrado."
            )
        
        return {
            "mensaje":"Perfil obtenido correctamente.",
            "data":PerfilResponse.from_orm(cliente),
            "success": True
        }
    
    def actualizar_perfil(self, token: str, data: PerfilUpdateRequest):
        payload = decode_token(token)
        if payload is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido o sesión expirada."
            )
        
        id_cliente = payload.get("id_cliente")
        cliente = self.repository.get_cliente_by_id(id_cliente)

        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente no encontrado."
            )
        
        
        if data.telefono and (not data.telefono.isdigit()) or len(data.telefono) not in [10]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Formato de teléfono inválido."
            )
        
        update_dict = {K: v for K, v in data.model_dump().items() if v is not None}

        cliente = self.repository.update_cliente(cliente, update_dict)

        return {
            "mensaje": "Perfil actualizado correctamente.",
            "data": update_dict,
            "success": True
        }
