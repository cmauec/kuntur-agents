"""
API FastAPI para guardar y gestionar notas.
"""

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from uuid import uuid4, UUID

app = FastAPI(
    title="Notas API",
    description="API para guardar y gestionar notas",
    version="1.0.0"
)


class NotaBase(BaseModel):
    """Modelo base para una nota."""
    titulo: str = Field(..., min_length=1, max_length=200, description="Título de la nota")
    contenido: str = Field(..., min_length=1, description="Contenido de la nota")
    etiquetas: Optional[List[str]] = Field(default=[], description="Etiquetas de la nota")


class NotaCreate(NotaBase):
    """Modelo para crear una nueva nota."""
    pass


class NotaUpdate(BaseModel):
    """Modelo para actualizar una nota existente."""
    titulo: Optional[str] = Field(None, min_length=1, max_length=200)
    contenido: Optional[str] = Field(None, min_length=1)
    etiquetas: Optional[List[str]] = None


class Nota(NotaBase):
    """Modelo completo de una nota incluyendo metadatos."""
    id: UUID
    creada_en: datetime
    actualizada_en: datetime

    class Config:
        from_attributes = True


# Almacenamiento en memoria para las notas
notas_db: dict[UUID, Nota] = {}


@app.get("/")
def root():
    """Endpoint de bienvenida."""
    return {
        "mensaje": "Bienvenido a la API de Notas",
        "documentacion": "/docs"
    }


@app.get("/health")
def health_check():
    """Endpoint de verificación de salud."""
    return {"estado": "saludable"}


@app.post("/notas", response_model=Nota, status_code=status.HTTP_201_CREATED)
def crear_nota(nota: NotaCreate):
    """
    Crea una nueva nota.

    Args:
        nota: Datos de la nota a crear

    Returns:
        La nota creada con su ID y metadatos
    """
    ahora = datetime.utcnow()
    nueva_nota = Nota(
        id=uuid4(),
        titulo=nota.titulo,
        contenido=nota.contenido,
        etiquetas=nota.etiquetas or [],
        creada_en=ahora,
        actualizada_en=ahora
    )
    notas_db[nueva_nota.id] = nueva_nota
    return nueva_nota


@app.get("/notas", response_model=List[Nota])
def listar_notas(etiqueta: Optional[str] = None):
    """
    Lista todas las notas, opcionalmente filtradas por etiqueta.

    Args:
        etiqueta: Filtrar notas por esta etiqueta

    Returns:
        Lista de notas
    """
    notas = list(notas_db.values())

    if etiqueta:
        notas = [n for n in notas if etiqueta in (n.etiquetas or [])]

    return sorted(notas, key=lambda x: x.creada_en, reverse=True)


@app.get("/notas/{nota_id}", response_model=Nota)
def obtener_nota(nota_id: UUID):
    """
    Obtiene una nota específica por su ID.

    Args:
        nota_id: UUID de la nota

    Returns:
        La nota encontrada

    Raises:
        HTTPException: Si la nota no existe
    """
    if nota_id not in notas_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nota con ID {nota_id} no encontrada"
        )
    return notas_db[nota_id]


@app.put("/notas/{nota_id}", response_model=Nota)
def actualizar_nota(nota_id: UUID, nota_actualizada: NotaUpdate):
    """
    Actualiza una nota existente.

    Args:
        nota_id: UUID de la nota a actualizar
        nota_actualizada: Datos a actualizar

    Returns:
        La nota actualizada

    Raises:
        HTTPException: Si la nota no existe
    """
    if nota_id not in notas_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nota con ID {nota_id} no encontrada"
        )

    nota_existente = notas_db[nota_id]

    # Actualizar solo los campos proporcionados
    if nota_actualizada.titulo is not None:
        nota_existente.titulo = nota_actualizada.titulo
    if nota_actualizada.contenido is not None:
        nota_existente.contenido = nota_actualizada.contenido
    if nota_actualizada.etiquetas is not None:
        nota_existente.etiquetas = nota_actualizada.etiquetas

    nota_existente.actualizada_en = datetime.utcnow()
    notas_db[nota_id] = nota_existente

    return nota_existente


@app.delete("/notas/{nota_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_nota(nota_id: UUID):
    """
    Elimina una nota por su ID.

    Args:
        nota_id: UUID de la nota a eliminar

    Raises:
        HTTPException: Si la nota no existe
    """
    if nota_id not in notas_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nota con ID {nota_id} no encontrada"
        )

    del notas_db[nota_id]
    return None


@app.get("/notas/{nota_id}/resumen")
def resumen_nota(nota_id: UUID, longitud: int = 100):
    """
    Obtiene un resumen del contenido de una nota.

    Args:
        nota_id: UUID de la nota
        longitud: Longitud máxima del resumen (default: 100 caracteres)

    Returns:
        Resumen de la nota
    """
    nota = obtener_nota(nota_id)
    contenido = nota.contenido

    if len(contenido) <= longitud:
        resumen = contenido
    else:
        resumen = contenido[:longitud].rsplit(' ', 1)[0] + "..."

    return {
        "id": nota_id,
        "titulo": nota.titulo,
        "resumen": resumen,
        "longitud_total": len(contenido)
    }
