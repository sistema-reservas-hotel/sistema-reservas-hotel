from api import Registro_api
from api import Inicio_api
from api import Perfil_api
from api import Reserva_api
from api import Habitacion_api
from api import fechas_api
from api import pago_api
from api import Plan_api
from api import preferencias_api

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