from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database import SessionLocal
from services.Registro_service import ClienteService
from domain.Registro_model import ClienteCreate

router = APIRouter(
    prefix= "/api/v1/cliente",
    tags=["Cliente"]
)

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()

@router.post("/registro", status_code=status.HTTP_201_CREATED)
def resgistrar_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    service = ClienteService(db)
    return service.registrar_cliente(cliente)