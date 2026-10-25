from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.services.groq_service import obtener_datos_videojuego_ia
from app.database.config import get_db

from app.schemas.videojuego import JuegoCreateRequest, JuegoResponse

router = APIRouter(prefix="/juegos", tags=["Videojuegos"])


@router.post("/", status_code=201)
def registrar_videojuego(request: JuegoCreateRequest, db: Session = Depends(get_db)):
    try:
        # 1. Llamamos a Groq para que obtenga los datos automáticamente
        datos_ia = obtener_datos_videojuego_ia(request.nombre)

        titulo = datos_ia.get("titulo")
        genero = datos_ia.get("genero")
        anio = datos_ia.get("anio")
        desarrollador = datos_ia.get("desarrollador")

        # 2. Ejecutamos la consulta SQL directamente usando la sesión de config.py
        query = text("""
            INSERT INTO videojuegos (titulo, genero, anio, desarrollador) 
            VALUES (:titulo, :genero, :anio, :desarrollador)
        """)

        nuevo_videojuego = {
            "titulo": titulo,
            "genero": genero,
            "anio": anio,
            "desarrollador": desarrollador,
        }

        db.execute(
            query,
            nuevo_videojuego,
        )
        db.commit()  # Guardamos los cambios en la BD MySQL

        # 3. Retornamos la respuesta exitosa
        return {
            "mensaje": "Videojuego registrado exitosamente en la base de datos",
            "datos_registrados": nuevo_videojuego,
        }

    except Exception as e:
        db.rollback()  # Revierte si ocurre algún error
        raise HTTPException(
            status_code=500, detail=f"Error al procesar el videojuego: {str(e)}"
        )