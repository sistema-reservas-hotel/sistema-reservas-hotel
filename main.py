from fastapi import FastAPI
from app.config.routers import ROUTERS
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer

# Crear una sola instancia
app = FastAPI(
    title="Sistema de Reservas de Hotel",
    description="API con arquitectura en capas",
    version="1.0.0"
)

# Seguridad global para Swagger
security = HTTPBearer()

# --- CORS CONFIG ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

# Registrar routers
for router in ROUTERS:
    app.include_router(router)

@app.get("/")
def root():
    return {"message": "API funcionando correctamente"}
