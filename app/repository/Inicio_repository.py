from sqlalchemy.orm import Session
from app.database import ClienteDB


class InicioRepository:

    def _init_(self, db: Session):
        self.db = db

    def get_user_by_email(self, email: str) -> ClienteDB:
        return (
            self.db.query(ClienteDB)
            .filter(ClienteDB.email == email)
            .first()
        )