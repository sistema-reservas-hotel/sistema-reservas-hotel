from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repository.Habitacion_repository import HabitacionesRepository


class HabitacionesService:

    def __init__(self, db: Session):
        self.repository = HabitacionesRepository(db)

    def listar_habitaciones(self, tipoHabitacion: str = None):

        if tipoHabitacion:
            habitacion = self.repository.get_habitacion_by_tipo(tipoHabitacion)

            # ❌ Tipo inexistente
            if not habitacion:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail={
                        "success": False,
                        "error_code": "RES_404",
                        "message": "El tipo de habitación ingresado no existe en nuestro sistema. Verifique el nombre y vuelva a intentarlo.",
                        "details": {"tipoHabitacion": tipoHabitacion}
                    }
                )

            # ❌ Existe pero no hay disponibilidad
            if not habitacion.disponible or habitacion.habitacionesDisponibles == 0:
                raise HTTPException(
                    status_code=status.HTTP_204_NO_CONTENT,
                    detail={
                        "success": False,
                        "error_code": "RES_204",
                        "message": "Lo sentimos. En este momento la habitación seleccionada no cuenta con disponibilidad.",
                        "details": {"tipoHabitacion": tipoHabitacion}
                    }
                )

            # ✔️ Disponibilidad específica encontrada
            planes_bd = self.repository.get_planes_por_habitacion(habitacion.id_tipoHabitacion)
            planes = [{
                "plan": p.nombre,
                "precio": p.precio,
                "serviciosIncluidos": p.serviciosIncluidos.split(",")
            } for p in planes_bd]

            return {
                "success": True,
                "message": "Disponibilidad encontrada para el tipo de habitación solicitado.",
                "data": {
                    "tipoHabitacion": habitacion.nombre,
                    "capacidad": habitacion.capacidad,
                    "precioNoche": habitacion.precioPorNoche,
                    "moneda": "COP",
                    "planes": planes,
                    "disponible": habitacion.disponible,
                    "habitacionesDisponibles": habitacion.habitacionesDisponibles
                }
            }

        # ------------------------------
        # 2️⃣ CONSULTA GENERAL
        # ------------------------------
        habitaciones = self.repository.get_all_habitaciones()
        lista = []

        for h in habitaciones:
            planes_bd = self.repository.get_planes_por_habitacion(h.id_tipoHabitacion)
            planes = [{
                "plan": p.nombre,
                "precio": p.precio,
                "serviciosIncluidos": p.serviciosIncluidos.split(",")
            } for p in planes_bd]

            lista.append({
                "tipoHabitacion": h.nombre,
                "capacidad": h.capacidad,
                "precioNoche": h.precioPorNoche,
                "disponible": h.disponible,
                "habitacionesDisponibles": h.habitacionesDisponibles,
                "planes": planes,
                "imagen": h.imagen
            })

        return {
            "success": True,
            "message": "Disponibilidad general de habitaciones.",
            "data": lista
        }
