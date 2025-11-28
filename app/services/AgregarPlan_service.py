from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repository.AgregarPlan_repository import PlanesRepository
from app.domain.AgregarPlan_models import PlanCreate, PlanUpdate
from app.models.PlanesBD import PlanesDB

class PlanesService:
    def __init__(self, db: Session):
        self.repo = PlanesRepository(db)

    def agregar_plan(self, plan_data: PlanCreate):
        # Validación: nombre duplicado
        existing = self.repo.db.query(self.repo.db.query(PlanesDB).filter(
            PlanesDB.nombre == plan_data.nombre,
            PlanesDB.id_tipoHabitacion == plan_data.id_tipoHabitacion
        ).exists()).scalar()
        if existing:
            raise HTTPException(status_code=409, detail="Nombre de plan duplicado")
        
        plan_dict = plan_data.dict()
        plan_dict["serviciosIncluidos"] = ",".join(plan_data.serviciosIncluidos)
        plan = self.repo.create_plan(plan_dict)
        plan.serviciosIncluidos = plan.serviciosIncluidos.split(",")
        return {"mensaje": "Plan agregado correctamente.", "data": plan, "success": True}

    def editar_plan(self, id_Plan: int, plan_data: PlanUpdate):
        data = plan_data.dict(exclude_unset=True)
        if "serviciosIncluidos" in data:
            data["serviciosIncluidos"] = ",".join(data["serviciosIncluidos"])
        plan = self.repo.update_plan(id_Plan, data)
        if not plan:
            raise HTTPException(status_code=404, detail="Plan no encontrado")
        plan.serviciosIncluidos = plan.serviciosIncluidos.split(",")
        return {"mensaje": "Plan actualizado correctamente.", "data": plan, "success": True}

    def eliminar_plan(self, id_Plan: int):
        plan = self.repo.delete_plan(id_Plan)
        if not plan:
            raise HTTPException(status_code=404, detail="Plan no encontrado")
        return {"mensaje": "Plan eliminado correctamente.", "data": {"idPlan": plan.id_Plan, "nombre": plan.nombre}, "success": True}
