from sqlalchemy.orm import Session
from app.models.PagosBD import PagosDB

class PagoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_pagos_cliente(self, id_cliente: int, estado=None, desde=None, hasta=None):
        query = self.db.query(PagosDB).filter(PagosDB.id_cliente == id_cliente)

        if estado:
            query = query.filter(PagosDB.estado == estado)
        if desde:
            query = query.filter(PagosDB.fecha_pago >= desde)
        if hasta:
            query = query.filter(PagosDB.fecha_pago <= hasta)

        return query.all()
