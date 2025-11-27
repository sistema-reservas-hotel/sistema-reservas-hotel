from app.models.Base import Base
from app.models.HabitacionesBD import HabitacionesDB
from app.database import engine

# Borra todas las tablas (cuidado, se pierden datos existentes)
Base.metadata.drop_all(bind=engine)
# Crea todas las tablas según los modelos actuales
Base.metadata.create_all(bind=engine)

print("Tabla 'habitaciones' recreada correctamente con todas las columnas del modelo.")
