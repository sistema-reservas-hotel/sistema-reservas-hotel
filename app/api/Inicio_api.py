from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.domain.Inicio_model import InicioRequest
from app.services.Inicio_service import InicioService


router = APIRouter(
    prefix="/api/v1/cliente",
    tags=["Login"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/login", status_code=status.HTTP_200_OK)
def login(credentials: InicioRequest, db: Session = Depends(get_db)):
    service = InicioService(db)
    return service.inicio(credentials)