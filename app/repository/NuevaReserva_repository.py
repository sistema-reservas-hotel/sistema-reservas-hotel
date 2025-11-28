from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from app.models.ReservaBD import ReservasDB, HabitacionesDB, TipoHabitacionDB # Asumiendo acceso a HabitacionesDB y TipoHabitacionDB
from app.domain.NuevaReserva_model import ReservaCreacion
from datetime import date, datetime
from typing import Optional, Tuple

class ReservaRepository:
    def __init__(self, db: Session):
        self.db = db

    def _generar_id_unico(self) -> str:
        """Genera un ID único para la reserva (RSV-YYYYMMDD-SECUENCIA)."""
        fecha_str = datetime.now().strftime("%Y%m%d")
        # Contamos cuántas reservas se han creado hoy (o similar, para la secuencia)
        conteo = self.db.query(ReservasDB).filter(
             func.date(ReservasDB.fecha_reserva) == date.today()
        ).count()
        secuencia = str(conteo + 1).zfill(4)
        return f"RSV-{fecha_str}-{secuencia}"
    
    def get_capacidad_y_nombre_tipo(self, id_tipo: int) -> Optional[Tuple[int, str]]:
        """Obtiene la capacidad máxima y el nombre del tipo de habitación."""
        tipo = self.db.query(TipoHabitacionDB).filter(
            TipoHabitacionDB.id_tipoHabitacion == id_tipo
        ).first()
        if tipo:
            # Asumiendo que TipoHabitacionDB tiene 'capacidad_maxima' y 'nombre'
            return tipo.capacidad_maxima, tipo.nombre 
        return None
        
    def find_disponible_habitacion(
        self, id_tipo: int, fecha_entrada: date, fecha_salida: date
    ) -> Optional[HabitacionesDB]:
        """
        Encuentra la primera instancia de HabitacionesDB disponible del tipo solicitado.
        """
        
        # 1. Habitaciones de ese Tipo
        id_habitaciones_del_tipo = self.db.query(HabitacionesDB.id_habitacion).filter(
            HabitacionesDB.id_tipoHabitacion == id_tipo
        ).all()
        id_habitaciones = [h[0] for h in id_habitaciones_del_tipo]

        # 2. Habitaciones ocupadas en el rango (solapamiento)
        reservas_solapadas = self.db.query(ReservasDB.id_habitacion_fk).filter( # Usamos el FK a instancia
            ReservasDB.id_habitacion_fk.in_(id_habitaciones),
            ReservasDB.estado_reserva != "Cancelada",
            and_(
                ReservasDB.check_in < fecha_salida,
                ReservasDB.check_out > fecha_entrada
            )
        ).distinct().all()
        
        id_habitaciones_ocupadas = [r[0] for r in reservas_solapadas]

        # 3. Identifica la primera instancia disponible (por ID)
        id_disponible = next(
            (id_h for id_h in id_habitaciones if id_h not in id_habitaciones_ocupadas), 
            None
        )

        if id_disponible is None:
            return None

        # Retorna el objeto HabitacionesDB completo (necesitamos el número/código)
        return self.db.query(HabitacionesDB).filter(
            HabitacionesDB.id_habitacion == id_disponible
        ).first()


    def crear_reserva(self, data: ReservaCreacion, habitacion_asignada: HabitacionesDB, nombre_tipo: str) -> dict:
        """Crea la reserva usando los campos de tu tabla ReservasDB."""
        
        id_reserva_unico = self._generar_id_unico()
        
        nueva_reserva = ReservasDB(
            # Campos requeridos por la HU (necesarios en tu modelo)
            id_reserva_unico=id_reserva_unico,
            id_habitacion_fk=habitacion_asignada.id_habitacion, # Asignamos el FK a la instancia
            
            # Campos de tu modelo ReservasDB
            id_cliente=data.id_cliente,
            id_tipoHabitacion=data.id_tipoHabitacion,
            fecha_reserva=datetime.now(),
            check_in=data.fecha_entrada,
            check_out=data.fecha_salida,
            habitacion=habitacion_asignada.numero, # Usamos el número de habitación (String)
            plan=data.plan,
            valor_total=0, # Pendiente de cálculo real
            estado_reserva="Confirmada"
        )
        
        self.db.add(nueva_reserva)
        self.db.commit() # Bloqueo atómico de la habitación
        self.db.refresh(nueva_reserva)
        
        return {
            "id_reserva_unico": nueva_reserva.id_reserva_unico,
            "id_cliente": nueva_reserva.id_cliente,
            "id_habitacion_fk": nueva_reserva.id_habitacion_fk, # ID de la instancia
            "tipoHabitacion": nombre_tipo,
            "fecha_entrada": nueva_reserva.check_in,
            "fecha_salida": nueva_reserva.check_out,
            "num_personas": data.num_personas, # Este campo no está en ReservasDB, pero es necesario para la respuesta.
            "estado_reserva": nueva_reserva.estado_reserva
        }