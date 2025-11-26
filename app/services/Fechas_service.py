from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from dateutil.parser import isoparse
from datetime import datetime, timedelta
from app.repository.Fechas_repository import FechasRepository
from app.domain.Fechas_model import FechasDisponibilidadResponse

class FechasService:
    def __init__(self):
        self.repo = FechasRepository()

    def validar_iso(self, fecha_str: str) -> datetime:
        try:
            dt = isoparse(fecha_str)
            return dt
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "success": False,
                    "error_code": "RES_400",
                    "message": "Formato no válido. Debe ser YYYY-MM-DDTHH:MM:SSZ",
                    "details": {"fecha": fecha_str}
                }
            )

    def disponibilidad(self, db: Session, fechaEntrada: str = None, fechaSalida: str = None):
        # consulta general sin parámetros
        if not fechaEntrada and not fechaSalida:
            return {
                "success": True,
                "message": "Disponibilidad general para las próximas fechas.",
                "data": {
                    "rangoConsultado": {
                        "inicio": "2025-10-01T00:00:00Z",
                        "fin": "2025-12-31T00:00:00Z"
                    },
                    "disponibilidad": [
                        {"fecha": "2025-10-20T00:00:00Z"},
                        {"fecha": "2025-10-21T00:00:00Z"},
                        {"fecha": "2025-10-22T00:00:00Z"}
                    ]
                }
            }

        inicio = self.validar_iso(fechaEntrada) if fechaEntrada else None
        fin = self.validar_iso(fechaSalida) if fechaSalida else None

        if inicio is None or fin is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "success": False,
                    "error_code": "RES_400",
                    "message": "Debe proporcionar fechaEntrada y fechaSalida en formato ISO 8601.",
                    "details": {}
                }
            )

        if fin <= inicio:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "success": False,
                    "error_code": "RES_400",
                    "message": "Rango de fechas inválido.",
                    "details": {
                        "fechaEntrada": fechaEntrada,
                        "fechaSalida": fechaSalida,
                        "error": "La fecha de salida no puede ser anterior o igual a la fecha de entrada."
                    }
                }
            )

        try:
            fechas_libres = self.repo.encontrar_fechas_libres_por_dia(db, inicio, fin)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail={
                    "success": False,
                    "error_code": "RES_503",
                    "message": "Error al consultar la disponibilidad. Intente nuevamente.",
                    "details": {"error": str(e)}
                }
            )

        if fechas_libres:
            return {
                "success": True,
                "message": "Fechas disponibles. Las fechas solicitadas se encuentran disponibles.",
                "data": {
                    "fechaEntrada": fechaEntrada,
                    "fechaSalida": fechaSalida,
                    "fechasDisponibles": fechas_libres
                }
            }

        try:
            sugerencias = self.repo.sugerencias_proximas(db, inicio, fin, dias_adelante=30, max_sugerencias=5)
        except Exception as e:
            sugerencias = []

        return {
            "success": True,
            "message": "No hay disponibilidad para el rango seleccionado, pero contamos con otras fechas que podrían interesarte.",
            "data": {
                "fechasDisponibles": [],
                "sugerencias": sugerencias
            }
        }
