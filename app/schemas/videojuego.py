from typing import Optional
from pydantic import BaseModel


# 1. Esquema para VALIDAR lo que envía el usuario (Entrada)
class JuegoCreateRequest(BaseModel):
    nombre: str


class JuegoUpdateRequest(BaseModel):
    titulo: Optional[str] = None
    genero: Optional[str] = None
    anio: Optional[int] = None
    desarrollador: Optional[str] = None



# 2. Esquema para VALIDAR y dar forma a lo que RESPONDE tu API (Salida)
class JuegoResponse(BaseModel):
    id: int
    titulo: str
    genero: str
    anio: int
    desarrollador: str

    class Config:
        from_attributes = True