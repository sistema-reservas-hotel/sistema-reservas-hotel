from sqlalchemy.orm import Session
from repository.fechas_repository import FechasRepository
from domain.fechas_model import FechaItem, DisponibilidadData, DisponibilidadResponse
from datetime import datetime, timedelta, date
from typing import Optional, List

class FechasService:
    """
    Lógica de negocio para calcular disponibilidad por rango de fechas.
    """

    def __init__(self, db: Session):
        self.repo = FechasRepository(db)

    def _parse_iso(self, s: str) -> Optional[datetime]:
        """
        Parsea una fecha ISO 8601 (acepta 'Z' final). Retorna datetime en UTC.
        Si formato inválido, retorna None.
        """
        if not s:
            return None
        try:
           
            if s.endswith("Z"):
                s2 = s.replace("Z", "+00:00")
            else:
                s2 = s
            return datetime.fromisoformat(s2)
        except Exception:
            return None

    def buscar_disponibilidad(
        self,
        fechaEntrada_iso: Optional[str],
        fechaSalida_iso: Optional[str]
    ) -> dict:
        """
        - Si no vienen fechas: devuelve calendario general (próximas fechas con disponibilidad)
        - Si vienen fechas: valida formato y rango, revisa disponibilidad y sugiere alternativas si no hay.
        """

       
        if fechaEntrada_iso and fechaSalida_iso:
            dt_inicio = self._parse_iso(fechaEntrada_iso)
            dt_fin = self._parse_iso(fechaSalida_iso)

            if not dt_inicio or not dt_fin:
                return {
                    "success": False,
                    "error_code": "RES_400",
                    "message": "Formato no válido. Debe ser YYYY-MM-DDTHH:MM:SSZ",
                    "details": {
                        "fechaEntrada": fechaEntrada_iso,
                        "fechaSalida": fechaSalida_iso,
                        "error": "Formato ISO inválido"
                    }
                }

           
            if dt_fin <= dt_inicio:
                return {
                    "success": False,
                    "error_code": "RES_400",
                    "message": "Rango de fechas inválido.",
                    "details": {
                        "fechaEntrada": fechaEntrada_iso,
                        "fechaSalida": fechaSalida_iso,
                        "error": "La fecha de salida no puede ser igual ni anterior a la fecha de entrada."
                    }
                }

            
            check_in_date = dt_inicio.date()
            check_out_date = dt_fin.date()

            try:
                tipos = self.repo.obtener_tipos_habitacion()
            except Exception:
                return {
                    "success": False,
                    "error_code": "RES_503",
                    "message": "Error al consultar la disponibilidad. Intente más tarde.",
                    "data": None
                }

            fechas_disponibles = [] 
            sugerencias = []

            for t in tipos:
             
                total_stock = getattr(t, "habitacionesDisponibles", None)
                if total_stock is None:
                  
                    continue

               
                reservas_solapadas = self.repo.reservas_entre_rango_para_tipo(t.id_tipoHabitacion, check_in_date, check_out_date)
                ocupadas = len(reservas_solapadas)

                disponibles_para_rango = max(0, total_stock - ocupadas)

                if disponibles_para_rango > 0:
                    
                    fechas_disponibles.append({"fecha": dt_inicio.isoformat().replace("+00:00","Z")})
                   
                else:
                    
                    ventana_dias = 30
                    found = False
                    for offset in range(1, ventana_dias+1):
                        cand_start = check_in_date + timedelta(days=offset)
                        cand_end = check_out_date + timedelta(days=offset)
                        reservas_cand = self.repo.reservas_entre_rango_para_tipo(t.id_tipoHabitacion, cand_start, cand_end)
                        if len(reservas_cand) < total_stock:
                            sugerencias.append({"fecha": datetime.combine(cand_start, datetime.min.time()).isoformat()+"Z"})
                            found = True
                            break
                    if not found:
                     
                        pass

          
            if fechas_disponibles:
                return {
                    "success": True,
                    "message": "Fechas disponibles. Las fechas solicitadas se encuentran disponibles",
                    "data": {
                        "fechaEntrada": dt_inicio.isoformat().replace("+00:00","Z"),
                        "fechaSalida": dt_fin.isoformat().replace("+00:00","Z"),
                        "fechasDisponibles": fechas_disponibles
                    }
                }
            else:
               
                return {
                    "success": True,
                    "message": "No hay disponibilidad para el rango solicitado, pero contamos con otras fechas que quizá podrían interesarte",
                    "data": {
                        "fechaEntrada": dt_inicio.isoformat().replace("+00:00","Z"),
                        "fechaSalida": dt_fin.isoformat().replace("+00:00","Z"),
                        "fechasDisponibles": [],
                        "sugerencias": sugerencias
                    }
                }

        else:
          
            try:
                tipos = self.repo.obtener_tipos_habitacion()
            except Exception:
                return {
                    "success": False,
                    "error_code": "RES_503",
                    "message": "Error al consultar la disponibilidad. Intente más tarde.",
                    "data": None
                }

            
            hoy = datetime.utcnow().date()
            fin = hoy + timedelta(days=90)
            disponibilidad = []

           
            for delta in range(0, (fin - hoy).days + 1):
                dia = hoy + timedelta(days=delta)
                any_available = False
                for t in tipos:
                    total_stock = getattr(t, "habitacionesDisponibles", 0)
                    if total_stock <= 0:
                        continue
                  
                    reservas_dia = self.repo.reservas_entre_rango_para_tipo(t.id_tipoHabitacion, dia, dia + timedelta(days=1))
                    if len(reservas_dia) < total_stock:
                        any_available = True
                        break
                if any_available:
                    disponibilidad.append({"fecha": datetime.combine(dia, datetime.min.time()).isoformat() + "Z"})
            return {
                "success": True,
                "message": "Disponibilidad general de habitaciones para las próximas fechas.",
                "data": {
                    "rangoConsultado": {
                        "inicio": datetime.combine(hoy, datetime.min.time()).isoformat() + "Z",
                        "fin": datetime.combine(fin, datetime.min.time()).isoformat() + "Z"
                    },
                    "disponibilidad": disponibilidad
                }
            }
