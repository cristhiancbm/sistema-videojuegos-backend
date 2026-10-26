from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.videojuego import router as videojuego_router

from app.database.config import verificar_conexion_db
from app.database.runner import ejecutar_migraciones


@asynccontextmanager
async def lifespan(app: FastAPI):
    verificar_conexion_db()
    ejecutar_migraciones()
    yield


# Instancia principal de la aplicación
app = FastAPI(
    title="API REST VIDEOJUEGOS",
    description="API para la gestión de videojuegos",
    version="1.0.0",
    lifespan=lifespan,
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción puedes especificar los dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(videojuego_router)


# Endpoint GET raíz
@app.get("/")
def ruta_raiz():
    return {
        "estado": "exitoso",
        "mensaje": "Servidor activo y respondiendo correctamente.",
    }