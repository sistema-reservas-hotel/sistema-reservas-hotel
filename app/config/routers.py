from api import Registro_api
from api import Inicio_api
from api import Perfil_api
from api import Reserva_api
from api import 

ROUTERS = [
    Registro_api.router, 
    Inicio_api.router,
    Perfil_api.router,
    Reserva_api.router,
]