from sqlalchemy.orm import Session
from app.repository.SeleccionPlanes_repository import PlanesRepository
from app.domain.SeleccionPlanes_models import PlanesResponse, PlanResponse, ErrorResponse
from app.models.PlanesBD import PlanesDB

class PlanesService:
    def __init__(self, db: Session):
        self.repository = PlanesRepository(db)

    def obtener_planes(self):
        try:
            planes = self.repository.listar_planes()
            if not planes:
                return ErrorResponse(
                    success=False,
                    error_code="RES_404",
                    message="Lo sentimos, no se encontraron planes disponibles",
                    details={}
                )
            
            planes_data = [
                PlanResponse(
                    idPlan=p.id_Plan,
                    nombre=p.nombre,
                    precio=p.precio,
                    serviciosIncluidos=p.serviciosIncluidos.split(",")
                ) for p in planes
            ]

            return PlanesResponse(
                success=True,
                message="Consulta de planes realizada correctamente.",
                data=planes_data
            )
        except Exception as e:
            return ErrorResponse(
                success=False,
                error_code="RES_503",
                message="Fallo la conexión a la base de datos",
                details={"error": str(e)}
            )

    def agregar_plan(self, id_tipoHabitacion: int, nombre: str, precio: int, servicios: str):
        plan = PlanesDB(
            id_tipoHabitacion=id_tipoHabitacion,
            nombre=nombre,
            precio=precio,
            serviciosIncluidos=servicios
        )
        try:
            return self.repository.agregar_plan(plan)
        except Exception as e:
            raise Exception(f"Error al agregar plan: {str(e)}")

    def editar_plan(self, id_plan: int, nombre: str, precio: int, str, servicios: str):
        plan = self.repository.obtener_plan_por_id(id_plan)
        if not plan:
            return None
        plan.nombre = nombre
        plan.precio = precio
        plan.serviciosIncluidos = servicios
        try:
            return self.repository.editar_plan(plan)
        except Exception as e:
            raise Exception(f"Error al editar plan: {str(e)}")

    def eliminar_plan(self, id_plan: int):
        plan = self.repository.obtener_plan_por_id(id_plan)
        if not plan:
            return None
        try:
            return self.repository.eliminar_plan(plan)
        except Exception as e:
            raise Exception(f"Error al eliminar plan: {str(e)}")
