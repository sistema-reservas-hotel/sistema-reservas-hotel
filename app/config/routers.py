from app.api import Registrar_api
from app.api import Inicio_api
from app.api import Perfil_api
from app.api import Reservas_api
from app.api import Pagos_api
from app.api import Preferencias_api


ROUTERS = [
   Registrar_api.router,
   Inicio_api.router,
   Perfil_api.router,
   Reservas_api.router,
   Pagos_api.router,
   Preferencias_api.router,
]