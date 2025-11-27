from sqlalchemy import inspect
from app.database import engine

inspector = inspect(engine)
columns = inspector.get_columns('habitaciones')
print("Columnas actuales en 'habitaciones':")
for col in columns:
    print(col['name'])
