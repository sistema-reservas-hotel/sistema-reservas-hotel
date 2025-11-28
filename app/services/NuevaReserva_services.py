from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repository.NuevaReserva_repository import ReservaRepository
from app.domain.NuevaReserva_model import ReservaCreacion, ReservaCreacionSalida, ReservaDetalle
from pydantic import ValidationError # Importar para manejar errores de validación de Pydantic

class ReservaService:
    def __init__(self, db: Session):
        self.repository = ReservaRepository(db)

    def crear_nueva_reserva(self, reserva_data: ReservaCreacion) -> ReservaCreacionSalida:
        
        # 1. Validación de Fechas (Manejada por Pydantic/Validator)
        # Se asume que el router ya maneja la validación inicial de Pydantic.
        # Capturaremos el error aquí para formatearlo como RES_400 si la validación falla
        # (Aunque en FastAPI, el ValidationError es capturado por el framework automáticamente con status 422,
        # lo haremos explícito si la validación se ejecuta después de la inicialización).
        
        # 2. Validación de Capacidad (Caso 4: Capacidad excedida)
        capacidad_data = self.repository.get_capacidad_y_nombre_tipo(reserva_data.id_tipoHabitacion)
        
        if not capacidad_data:
             raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"mensaje": "Tipo de habitación no encontrado.", "success": False}
            )
            
        capacidad_maxima, nombre_tipo = capacidad_data
        
        if reserva_data.num_personas > capacidad_maxima:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "mensaje": f"El número de personas ({reserva_data.num_personas}) excede la capacidad máxima ({capacidad_maxima}) de la habitación '{nombre_tipo}'.",
                    "success": False, 
                    "error_code": "RES_409"
                }
            )

        # 3. Validación de Disponibilidad (Caso 3: Sin disponibilidad)
        habitacion_disponible = self.repository.find_disponible_habitacion(
            reserva_data.id_tipoHabitacion, 
            reserva_data.fecha_entrada, 
            reserva_data.fecha_salida
        )

        if not habitacion_disponible:
            raise HTTPException(
                status_code=status.HTTP_204_NO_CONTENT, 
                detail={
                    "mensaje": "No hay habitaciones disponibles para el rango de fechas solicitado.", 
                    "success": False, 
                    "error_code": "RES_204"
                }
            )
            
        # 4. Creación y Bloqueo Atómico (Caso 1: Creación exitosa)
        try:
            datos_reserva = self.repository.crear_reserva(reserva_data, habitacion_disponible, nombre_tipo)
            
            return ReservaCreacionSalida(
                mensaje="Reserva creada exitosamente.",
                data=ReservaDetalle(**datos_reserva),
                success=True
            )
        except Exception as e:
            # Fallo en la transacción de BD (RES_500)
            print(f"Error al crear reserva: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"mensaje": "Error interno al procesar la reserva.", "success": False, "error_code": "RES_500"}
            )