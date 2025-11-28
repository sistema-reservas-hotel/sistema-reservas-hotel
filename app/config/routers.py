from app.api import Registrar_api
from app.api import Inicio_api
from app.api import Perfil_api
from app.api import Reservas_api
from app.api import Pagos_api
from app.api import Preferencias_api
from app.api import Habitacion_api
from app.api import Fechas_api
from app.api import TipoHabitacion_api
from app.api import ActualizarHbtn_api
from app.api import HabitacionPrecio_api
from app.api import SeleccionPlanes_api
from app.api import CancelacionP_api


ROUTERS = [
   Registrar_api.router,
   Inicio_api.router,
   Perfil_api.router,
   Reservas_api.router,
   Pagos_api.router,
   Preferencias_api.router,
   Habitacion_api.router,
   Fechas_api.router,
   TipoHabitacion_api.router,
   ActualizarHbtn_api.router,
   HabitacionPrecio_api.router,
   SeleccionPlanes_api.router,
   CancelacionP_api.router,
]