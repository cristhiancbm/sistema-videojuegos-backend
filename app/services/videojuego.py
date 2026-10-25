from sqlalchemy.orm import Session
from sqlalchemy import text
from app.services.groq_service import obtener_datos_videojuego_ia


def registrar_videojuego_service(nombre: str, db: Session) -> dict:
    # 1. Llamamos a Groq para que obtenga los datos automáticamente
    datos_ia = obtener_datos_videojuego_ia(nombre)

    titulo = datos_ia.get("titulo")
    genero = datos_ia.get("genero")
    anio = datos_ia.get("anio")
    desarrollador = datos_ia.get("desarrollador")

    # 2. Preparamos el diccionario con los datos
    nuevo_videojuego = {
        "titulo": titulo,
        "genero": genero,
        "anio": anio,
        "desarrollador": desarrollador,
    }

    # 3. Ejecutamos la consulta SQL directamente
    query = text("""
        INSERT INTO videojuegos (titulo, genero, anio, desarrollador) 
        VALUES (:titulo, :genero, :anio, :desarrollador)
    """)

    db.execute(query, nuevo_videojuego)
    db.commit()  # Guardamos los cambios en la BD MySQL

    return nuevo_videojuego