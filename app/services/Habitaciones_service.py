from sqlalchemy import Session 
from repository.Habitacion_repository import HabitacionesRepository
from domain.Habitacion_model import HabitacionResponse, HabitacionesResponse, PlanIncluido, ErrorResponse

class HabitacionesService:
    def __init__(self, db: Session):
        self.repository = HabitacionesRepository(db)

    def listar_habitaciones(self, tipoHabitacion: str = None):
        if tipoHabitacion:
            habitacion = self.repository.get_habitacion_by_tipo(tipoHabitacion)
            if not habitacion:
                return ErrorResponse(
                    message="El tipo de habitacion ingresado no existe en nuestro sistema.",
                    error_code="RES_404",
                    details={"tipohabitacion": tipoHabitacion}
                )
            
            if not habitacion.disponible or habitacion.habitacionesDisponibles == 0:
                return ErrorResponse(
                    message="No hay disponibilidad para el tipo de habitacion seleccionada.",
                    error_code="RES_2040",
                    details={"tipoHabitacion": tipoHabitacion}
                )
            
            planes = [
                PlanIncluido(
                    nombre=p.nombre,
                    precio=p.precio,
                    serviciosIncluidos=p.serviciosIncluidos.split(",")
                ) for p in self.repository.get_planes_por_habitacion(habitacion.id_tipoHabitacion)
            ] 

            return HabitacionResponse(
                idTipoHabitacion=habitacion.idTipoHabitacion,
                nombre=habitacion.nombre,
                descripcion=habitacion.descripcion,
                capacidad=habitacion.capacidad,
                precioPorNoche=habitacion.precioPorNoche,
                imagen=habitacion.imagen,
                disponible=habitacion.disponible,
                habitacionesDisponibles=habitacion.habitacionesDisponibles,
                planes=planes,
                success=True,
                message="La habitación seleccionada cuenta con disponibilidad"
            )
        
        else:
            habitacion = self.repository.get_all_habitaciones()
            lista = []
            for h in habitacion:
                planes = [
                    PlanIncluido(
                    nombre=p.nombre,
                    precio=p.precio,
                    serviciosInlcuidos=p.serviciosIncluidos.split(",")
                    ) for p in self.repository.get_planes_por_habitacion(h.id_tipoHabitacion)
                ]

                lista.append({
                    "idTipoHabitacion": h.idTipoHabitacion,
                    "nombre": h.nombre,
                    "descripcion": h.descripcion,
                    "capacidad": h.capacidad,
                    "precioPorNoche": h.precioPorNoche,
                    "imagen": h.imagen,
                    "disponible": h.disponible,
                    "habitacionesDisponibles": h.habitacionesDisponibles,
                    "planes": planes
                })

                return HabitacionesResponse(
                    success=True,
                    message="Disponibilidad general de habitaciones.",
                    data=lista
                )
            

