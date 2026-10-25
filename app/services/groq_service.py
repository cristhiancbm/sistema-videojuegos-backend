import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Inicializar el cliente de Groq
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


def consultar_modelo_groq(pregunta: str) -> str:
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": pregunta}],
        model="qwen/qwen3.8-27b",
    )
    return chat_completion.choices[0].message.content


def obtener_datos_videojuego_ia(nombre_juego: str) -> dict:
    prompt = f"""
    Actúa como una base de datos experta en videojuegos. 
    Analiza el siguiente juego: "{nombre_juego}".
    Devuelve ÚNICAMENTE un objeto JSON válido con las siguientes llaves exactas:
    - "titulo": El nombre oficial del juego (string)
    - "genero": El género principal del juego (string)
    - "anio": El año de lanzamiento (número entero)
    - "desarrollador": El estudio o empresa desarrolladora (string)
    """

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "Eres un asistente que solo responde en JSON válido.",
            },
            {"role": "user", "content": prompt},
        ],
        model="qwen/qwen3.8-27b",  # O el modelo que estés utilizando en tu entorno
        response_format={"type": "json_object"},
    )

    # Convertimos el texto plano de la respuesta en un diccionario de Python
    contenido = chat_completion.choices[0].message.content
    return json.loads(contenido)