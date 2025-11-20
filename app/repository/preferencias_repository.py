from sqlalchemy.orm import Session
from database import PreferenciasClienteDB

class PreferenciasRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_cliente(self, id_cliente: int):
        return self.db.query(PreferenciasClienteDB).filter(
            PreferenciasClienteDB.id_cliente == id_cliente
        ).first()

    def save(self, id_cliente: int, data):
        preferencias = self.get_by_cliente(id_cliente)

        if preferencias:
            preferencias.documento = data.documento
            preferencias.tipo_habitacion_preferida = data.tipo_habitacion_preferida
            preferencias.metodo_pago_preferido = data.metodo_pago_preferido
            preferencias.hora_llegada = data.hora_llegada
        else:
            preferencias = PreferenciasClienteDB(
                id_cliente=id_cliente,
                documento=data.documento,
                tipo_habitacion_preferida=data.tipo_habitacion_preferida,
                metodo_pago_preferido=data.metodo_pago_preferido,
                hora_llegada=data.hora_llegada,
            )
            self.db.add(preferencias)

        self.db.commit()
        self.db.refresh(preferencias)
        return preferencias
