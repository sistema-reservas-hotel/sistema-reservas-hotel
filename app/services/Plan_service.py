from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repository.Plan_repository import PlanRepository
from app.domain.Plan_model import ResponsePlanList, ResponsePlanDetalle, PlanResponse


class PlanService:
    def __init__(self, db: Session):
        self.repository = PlanRepository(db)

    def listar_planes(self) -> ResponsePlanList:
        try:
            planes = self.repository.obtener_planes_activos()
        except Exception:
            raise HTTPException(
                status_code=503,
                detail={
                    "success": False,
                    "error_code": "RES_503",
                    "message": "Falló la conexión a la base de datos",
                    "details": {"conexion": "No se pudo obtener la información de los planes"}
                }
            )

        if not planes:
            raise HTTPException(
                status_code=404,
                detail={
                    "success": False,
                    "error_code": "RES_404",
                    "message": "Lo sentimos, no se encontraron planes disponibles.",
                    "details": {}
                }
            )

        data = [
            PlanResponse(
                idPlan=p.idPlan,
                nombre=p.nombre,
                descripcion=p.descripcion,
                precio=p.precio,
                moneda="COP",
                serviciosIncluidos=p.serviciosIncluidos
            )
            for p in planes
        ]

        return ResponsePlanList(
            success=True,
            message="Planes disponibles obtenidos correctamente.",
            data=data
        )

    def obtener_plan_por_id(self, idPlan: int) -> ResponsePlanDetalle:
        plan = self.repository.obtener_plan_por_id(idPlan)

        if not plan:
            return ResponsePlanDetalle(
                success=False,
                error_code="RES_404",
                message="El plan solicitado no existe o no está disponible.",
                details={"field": "idPlan", "value": idPlan}
            )

        data = PlanResponse(
            idPlan=plan.idPlan,
            nombre=plan.nombre,
            descripcion=plan.descripcion,
            precio=plan.precio,
            moneda="COP",
            serviciosIncluidos=plan.serviciosIncluidos
        )

        return ResponsePlanDetalle(
            success=True,
            message="Consulta de plan realizada correctamente.",
            data=data
        )
