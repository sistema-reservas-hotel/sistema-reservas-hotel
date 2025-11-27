from pydantic import BaseModel, Field
from typing import Annotated

class TipoHabitacionPrecioUpdate(BaseModel):
    nuevo_precio: Annotated[int, Field(gt=0)]
