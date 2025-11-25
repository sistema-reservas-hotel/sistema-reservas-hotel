from fastapi import FastAPI
from app.config.routers import ROUTERS
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Sistema de Reservas de Hotel",
    description="API con arquitectura en capas",
    version="1.0.0"
)

# --- CORS CONFIG ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite cualquier origen (Swagger lo necesita)
    allow_credentials=True,
    allow_methods=["*"],   # Permite todos los métodos
    allow_headers=["*"],   # Permite todos los headers
)

# Registrar automáticamente todos los routers del sistema
for router in ROUTERS:
    app.include_router(router)

# Endpoint raíz
@app.get("/")
def root():
    return {"message": "API funcionando correctamente"}
