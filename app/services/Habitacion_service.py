from sqlalchemy.orm import Session
from app.repository.Habitacion_repository import HabitacionesRepository
from app.domain.Habitacion_model import HabitacionesResponse, HabitacionResponse, ErrorResponse, PlanIncluido, HabitacionBase

class HabitacionesService:
    def __init__(self, db: Session):
        self.repository = HabitacionesRepository(db)

    def listar_habitaciones(self, id_tipoHabitacion: str = None):
        if id_tipoHabitacion:
            habitacion = self.repository.get_habitacion_by_tipo(id_tipoHabitacion)
            
            if not habitacion:
                return ErrorResponse(
                    message="El tipo de habitación ingresado no existe en nuestro sistema. Verifique el nombre y vuelva a intentarlo",
                    error_code="RES_404",
                    details={"tipoHabitacion": id_tipoHabitacion}
                )
            
            if habitacion.estado_habitacion != "Disponible" or habitacion.habitacionesDisponibles == 0:
                return ErrorResponse(
                    message="Lo sentimos. En este momento la habitación seleccionada no cuenta con disponibilidad",
                    error_code="RES_204",
                    details={"tipoHabitacion": id_tipoHabitacion}
                )

            planes = [
                PlanIncluido(
                    plan=p.nombre,
                    precio=p.precio,
                    serviciosIncluidos=p.serviciosIncluidos.split(",")
                ) for p in self.repository.get_planes_por_habitacion(habitacion.id_tipoHabitacion)
            ]

            habitacion_data = HabitacionBase(
                idTipoHabitacion=habitacion.id_tipoHabitacion,
                nombre=habitacion.nombre,
                descripcion=habitacion.descripcion,
                capacidad=habitacion.capacidad,
                precioPorNoche=habitacion.precio_base,
                estado_habitacion=habitacion.estado_habitacion,
                plan_incluido=planes 
            )

            return HabitacionResponse(
                success=True,
                message="La habitación seleccionada cuenta con disponibilidad",
                data=habitacion_data
            )

        else:
            habitaciones = self.repository.listar_todas_habitaciones()
            
            habitaciones_data = []
            for habitacion in habitaciones:
                if habitacion.estado_habitacion == "Disponible" and habitacion.habitacionesDisponibles > 0:
                    planes = [
                        PlanIncluido(
                            plan=p.nombre,
                            precio=p.precio,
                            serviciosIncluidos=p.serviciosIncluidos.split(",")
                        ) for p in self.repository.get_planes_por_habitacion(habitacion.id_tipoHabitacion)
                    ]

                    habitaciones_data.append(
                        HabitacionBase(
                            idTipoHabitacion=habitacion.id_tipoHabitacion,
                            nombre=habitacion.nombre,
                            descripcion=habitacion.descripcion,
                            capacidad=habitacion.capacidad,
                            precioPorNoche=habitacion.precio_base,
                            estado_habitacion=habitacion.estado_habitacion,
                            plan_incluido=planes
                        )
                    )

            return HabitacionesResponse(
                success=True,
                message="Listado de habitaciones disponibles",
                data=habitaciones_data
            )
