from fastapi import FastAPI
from config.routers import ROUTERS

app = FastAPI(
    title="Sistema de Reservas de Hotel",
    description="API con arquitectura en capas",
    version="1.0.0"
)

# Registrar automáticamente todos los routers del sistema
for router in ROUTERS:
    app.include_router(router)

# Endpoint raíz
@app.get("/")
def root():
    return {"message": "API funcionando correctamente"}
