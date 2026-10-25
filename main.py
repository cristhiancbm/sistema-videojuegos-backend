from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
import os

from groq import Groq
from dotenv import load_dotenv

from app.database.config import verificar_conexion_db
from app.database.runner import ejecutar_migraciones


@asynccontextmanager
async def lifespan(app: FastAPI):
    verificar_conexion_db()
    ejecutar_migraciones()
    yield

load_dotenv()



# Instancia principal de la aplicación
app = FastAPI(
    title="API REST VIDEOJUEGOS",
    description="API para la gestión de videojuegos",
    version="1.0.0",
    lifespan=lifespan,
)

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.get("/preguntar")
def consultar_groq(pregunta: str):
    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": pregunta}],
            model="qwen/qwen3.8-27b",
        )
        return {"respuesta": chat_completion.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint GET raíz
@app.get("/")
def ruta_raiz():
    return {
        "estado": "exitoso",
        "mensaje": "Servidor activo y respondiendo correctamente."
    }
