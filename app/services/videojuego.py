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

def listar_videojuegos_service(db: Session):
    query = text("SELECT * FROM videojuegos")
    resultados = db.execute(query).mappings().all()
    return list(resultados)

def actualizar_videojuego_service(id: int, request, db: Session):
    # 1. Verificar si el videojuego existe
    buscar_videojuego = text(
        "SELECT id, titulo, genero, anio, desarrollador FROM videojuegos WHERE id = :id"
    )
    existe_videojuego = db.execute(buscar_videojuego, {"id": id}).mappings().first()

    if not existe_videojuego:
        return None  # Retornamos None para que el router maneje el 404

    # 2. Filtrar solo los campos que el usuario mandó a actualizar (excluyendo los que están en None)
    datos_actualizar = request.dict(exclude_unset=True)
    if not datos_actualizar:
        return dict(
            existe_videojuego
        )  # Si no mandó nada, devolvemos el actual sin cambios

    # 3. Construir la consulta SQL dinámica de actualización
    partes_sql = [f"{key} = :{key}" for key in datos_actualizar.keys()]
    sql_unido = ", ".join(partes_sql)

    datos_actualizar["id"] = id
    query = text(f"UPDATE videojuegos SET {sql_unido} WHERE id = :id")

    db.execute(query, datos_actualizar)
    db.commit()

    # 4. Retornar el registro ya actualizado
    updated = db.execute(buscar_videojuego, {"id": id}).mappings().first()
    return dict(updated)
