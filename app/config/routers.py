from app.api import Registrar_api
from app.api import Inicio_api
from app.api import Perfil_api


ROUTERS = [
   Registrar_api.router,
   Inicio_api.router,
   Perfil_api.router,
]