from app.api import Registro_api
from app.api import Inicio_api
from app.api import Perfil_api
from app.api import Reserva_api
from app.api import Habitacion_api
from app.api import fechas_api
from app.api import pago_api
from app.api import Plan_api
from app.api import preferencias_api

ROUTERS = [
    Registro_api.router, 
    Inicio_api.router,
    Perfil_api.router,
    Reserva_api.router,
    Habitacion_api.router,
    fechas_api.router,
    pago_api.router,
    Plan_api.router,
    preferencias_api.router,




]