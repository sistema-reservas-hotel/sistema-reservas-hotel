# app/services/Plan_service.py
from sqlalchemy.orm import Session
from app.repository.SeleccionPlanes_repository import PlanesRepository
from app.domain.SeleccionPlanes_models import PlanesResponse, PlanResponse, ErrorResponse

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
                    idPlan=p.id_plan,
                    nombre=p.nombre,
                    descripcion=p.descripcion,
                    precio=p.precio,
                    moneda=p.moneda,
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
