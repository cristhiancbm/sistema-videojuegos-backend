from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.config import get_db
from app.schemas.videojuego import JuegoCreateRequest, JuegoResponse
from app.services.videojuego import (
    registrar_videojuego_service,
    listar_videojuegos_service,
)

router = APIRouter(prefix="/videojuegos", tags=["Videojuegos"])


@router.post("/", status_code=201)
def registrar_videojuego(request: JuegoCreateRequest, db: Session = Depends(get_db)):
    try:
        # Delegamos la lógica al servicio
        datos_registrados = registrar_videojuego_service(request.nombre, db)

        # Retornamos la respuesta exitosa
        return {
            "mensaje": "Videojuego registrado exitosamente en la base de datos",
            "datos_registrados": datos_registrados,
        }

    except Exception as e:
        db.rollback()  # Revierte si ocurre algún error
        raise HTTPException(
            status_code=500, detail=f"Error al procesar el videojuego: {str(e)}"
        )


@router.get("/", response_model=List[JuegoResponse])
def listar_videojuegos(db: Session = Depends(get_db)):
    try:
        # El router solo llama al servicio
        return listar_videojuegos_service(db)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al obtener los videojuegos: {str(e)}"
        )