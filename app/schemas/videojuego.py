from pydantic import BaseModel


# 1. Esquema para VALIDAR lo que envía el usuario (Entrada)
class JuegoCreateRequest(BaseModel):
    nombre: str


# 2. Esquema para VALIDAR y dar forma a lo que RESPONDE tu API (Salida)
class JuegoResponse(BaseModel):
    id: int
    titulo: str
    genero: str
    anio: int
    desarrollador: str

    class Config:
        from_attributes = True