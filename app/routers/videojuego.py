from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.config import get_db
from app.schemas.videojuego import JuegoCreateRequest, JuegoResponse, JuegoUpdateRequest
from app.services.videojuego import (
    registrar_videojuego_service,
    listar_videojuegos_service,
    actualizar_videojuego_service,
    eliminar_videojuego_service,
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


@router.patch("/{id}")
def actualizar_videojuego(
    id: int, request: JuegoUpdateRequest, db: Session = Depends(get_db)
):
    try:
        videojuego_actualizado = actualizar_videojuego_service(id, request, db)

        if not videojuego_actualizado:
            raise HTTPException(status_code=404, detail="Videojuego no encontrado")

        return {
            "mensaje": "Videojuego actualizado exitosamente en la base de datos",
            "datos_registrados": videojuego_actualizado,
        }

    except HTTPException as he:
        raise he
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail=f"Error al actualizar el videojuego: {str(e)}"
        )

@router.delete("/{id}")
def eliminar_videojuego(id: int, db: Session = Depends(get_db)):
    try:
        # Delegamos la eliminación al servicio
        fue_eliminado = eliminar_videojuego_service(id, db)

        if not fue_eliminado:
            raise HTTPException(status_code=404, detail="Videojuego no encontrado")

        return {
            "mensaje": f"Videojuego con ID {id} eliminado exitosamente de la base de datos"
        }

    except HTTPException as he:
        raise he
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail=f"Error al eliminar el videojuego: {str(e)}"
        )