from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repository.preferencias_repository import PreferenciasRepository
from app.utils.jwt_manager import validate_token
from app.domain.preferencias_model import PreferenciasBase, PreferenciasResponse

class PreferenciasService:

    def __init__(self):
        self.repository = PreferenciasRepository()

    def get_preferencias(self, db: Session, token: str):
        payload = validate_token(token)
        id_cliente = payload.get("id")

        prefs = self.repository.get_by_cliente(db, id_cliente)

        if not prefs:
            return PreferenciasResponse(
                mensaje="No existen preferencias registradas para este usuario.",
                data=None,
                success=False,
            )

        return PreferenciasResponse(
            mensaje="Preferencias obtenidas correctamente.",
            data=prefs,
            success=True
        )

    def update_preferencias(self, db: Session, token: str, preferencias: PreferenciasBase):
        try:
            payload = validate_token(token)
            id_cliente = payload.get("id")

            data = preferencias.dict(exclude_unset=True)

            prefs = self.repository.save_or_update(db, id_cliente, data)

            return {
                "mensaje": "Preferencias guardadas correctamente.",
                "data": {
                    "id_cliente": id_cliente,
                    "documento": prefs.documento,
                    "tipo_habitacion_preferida": prefs.tipo_habitacion_preferida,
                    "metodo_pago_preferido": prefs.metodo_pago_preferido,
                    "hora_llegada": prefs.hora_llegada
                },
                "success": True
            }

        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail={
                    "success": False,
                    "error_code": "PRF_400",
                    "mensaje": "Error al guardar las preferencias. Verifique los datos enviados."
                }
            )
