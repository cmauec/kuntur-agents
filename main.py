"""
API FastAPI para gestión de notas.

Endpoints disponibles:
- POST /notes - Crear una nueva nota
- GET /notes - Listar todas las notas
- GET /notes/{id} - Obtener una nota específica
- PUT /notes/{id} - Actualizar una nota
- DELETE /notes/{id} - Eliminar una nota
"""
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import engine, Base, get_db
from schemas import NoteCreate, NoteUpdate, NoteResponse
from crud import create_note, get_note, get_notes, update_note, delete_note

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Inicializar la aplicación FastAPI
app = FastAPI(
    title="Notes API",
    description="API para crear y gestionar notas",
    version="1.0.0",
)


@app.get("/")
def root():
    """Endpoint de bienvenida."""
    return {
        "message": "Bienvenido a la API de Notas",
        "docs": "/docs",
        "endpoints": {
            "create_note": "POST /notes",
            "list_notes": "GET /notes",
            "get_note": "GET /notes/{id}",
            "update_note": "PUT /notes/{id}",
            "delete_note": "DELETE /notes/{id}"
        }
    }


@app.post("/notes", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
def create_new_note(note: NoteCreate, db: Session = Depends(get_db)):
    """
    Crea una nueva nota.

    - **title**: Título de la nota (requerido)
    - **content**: Contenido de la nota (requerido)
    """
    return create_note(db, note)


@app.get("/notes", response_model=List[NoteResponse])
def list_notes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Obtiene la lista de todas las notas.

    - **skip**: Número de notas a saltar (paginación)
    - **limit**: Número máximo de notas a retornar
    """
    notes = get_notes(db, skip=skip, limit=limit)
    return notes


@app.get("/notes/{note_id}", response_model=NoteResponse)
def read_note(note_id: int, db: Session = Depends(get_db)):
    """
    Obtiene una nota específica por su ID.
    """
    db_note = get_note(db, note_id)
    if db_note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nota con id {note_id} no encontrada"
        )
    return db_note


@app.put("/notes/{note_id}", response_model=NoteResponse)
def update_existing_note(
    note_id: int,
    note: NoteUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualiza una nota existente.

    - **title**: Nuevo título (opcional)
    - **content**: Nuevo contenido (opcional)
    """
    db_note = update_note(db, note_id, note)
    if db_note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nota con id {note_id} no encontrada"
        )
    return db_note


@app.delete("/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_note(note_id: int, db: Session = Depends(get_db)):
    """
    Elimina una nota por su ID.
    """
    deleted = delete_note(db, note_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nota con id {note_id} no encontrada"
        )
    return None
