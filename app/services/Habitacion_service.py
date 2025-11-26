from sqlalchemy.orm import Session
from app.repository.Habitacion_repository import HabitacionesRepository
from app.domain.Habitacion_model import HabitacionesResponse, HabitacionResponse, ErrorResponse, PlanIncluido, HabitacionBase

class HabitacionesService:
    def __init__(self, db: Session):
        self.repository = HabitacionesRepository(db)

    def listar_habitaciones(self, tipoHabitacion: str = None):
        if tipoHabitacion:
            habitacion = self.repository.get_habitacion_by_tipo(tipoHabitacion)
            
            if not habitacion:
                return ErrorResponse(
                    message="El tipo de habitación ingresado no existe en nuestro sistema. Verifique el nombre y vuelva a intentarlo",
                    error_code="RES_404",
                    details={"tipoHabitacion": tipoHabitacion}
                )
            
            if not habitacion.disponible or habitacion.habitacionesDisponibles == 0:
                return ErrorResponse(
                    message="Lo sentimos. En este momento la habitación seleccionada no cuenta con disponibilidad",
                    error_code="RES_204",
                    details={"tipoHabitacion": tipoHabitacion}
                )

            planes = [
                PlanIncluido(
                    plan=p.nombre,
                    precio=p.precio,
                    serviciosIncluidos=p.serviciosIncluidos.split(",")
                ) for p in self.repository.get_planes_por_habitacion(habitacion.idTipoHabitacion)
            ]

            habitacion_data = HabitacionBase(
                idTipoHabitacion=habitacion.idTipoHabitacion,
                nombre=habitacion.nombre,
                descripcion=habitacion.descripcion,
                capacidad=habitacion.capacidad,
                precioPorNoche=habitacion.precioPorNoche,
                imagen=habitacion.imagen,
                disponible=habitacion.disponible,
                habitacionesDisponibles=habitacion.habitacionesDisponibles,
                planes=planes
            )

            return HabitacionResponse(
                success=True,
                message="La habitación seleccionada cuenta con disponibilidad",
                data=habitacion_data
            )

        else:
            habitaciones = self.reposi
