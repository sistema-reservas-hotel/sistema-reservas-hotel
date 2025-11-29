from sqlalchemy.orm import Session
from app.repository.SeleccionPlanes_repository import PlanesRepository
from app.models.PlanesBD import PlanesDB

class PlanesService:

    def __init__(self, db: Session):
        self.db = db
        self.repo = PlanesRepository()

    def obtener_planes(self):
        return self.repo.obtener_planes(self.db)

    def agregar_plan(self, id_tipoHabitacion, nombre, precio, serviciosIncluidos):
        nuevo_plan = PlanesDB(
            id_tipoHabitacion=id_tipoHabitacion,
            nombre=nombre,
            precio=precio,
            serviciosIncluidos=serviciosIncluidos
        )
        return self.repo.agregar_plan(self.db, nuevo_plan)

    def editar_plan(self, id_plan, nombre, precio, serviciosIncluidos):
        plan = self.repo.obtener_por_id(self.db, id_plan)
        if not plan:
            return None

        plan.nombre = nombre
        plan.precio = precio
        plan.serviciosIncluidos = serviciosIncluidos

        return self.repo.actualizar_plan(self.db, plan)

    def eliminar_plan(self, id_plan):
        plan = self.repo.obtener_por_id(self.db, id_plan)
        if not plan:
            return None

        return self.repo.eliminar_plan(self.db, plan)
