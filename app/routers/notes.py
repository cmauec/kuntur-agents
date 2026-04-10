from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import NoteCreate, NoteUpdate, NoteResponse, NoteListResponse, TagListResponse
from app.services.notes import (
    create_note,
    get_note_by_id,
    get_all_notes,
    update_note,
    delete_note,
    search_notes,
    get_all_tags,
    toggle_pin,
    toggle_archive
)

router = APIRouter()


@router.post("/", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
def create_new_note(note: NoteCreate, db: Session = Depends(get_db)):
    """Crear una nueva nota"""
    return create_note(db, note)


@router.get("/", response_model=NoteListResponse)
def list_notes(
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros"),
    is_archived: Optional[bool] = Query(None, description="Filtrar por estado de archivado"),
    is_pinned: Optional[bool] = Query(None, description="Filtrar por estado de fijado"),
    tag: Optional[str] = Query(None, description="Filtrar por tag específico"),
    db: Session = Depends(get_db)
):
    """Obtener lista de notas con filtros opcionales"""
    notes, total = get_all_notes(
        db,
        skip=skip,
        limit=limit,
        is_archived=is_archived,
        is_pinned=is_pinned,
        tag=tag
    )
    return {"items": notes, "total": total}


@router.get("/search", response_model=NoteListResponse)
def search_notes_endpoint(
    q: str = Query(..., min_length=1, description="Término de búsqueda"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Buscar notas por título o contenido"""
    notes, total = search_notes(db, query=q, skip=skip, limit=limit)
    return {"items": notes, "total": total}


@router.get("/tags", response_model=TagListResponse)
def list_all_tags(db: Session = Depends(get_db)):
    """Obtener todos los tags únicos usados en las notas"""
    tags = get_all_tags(db)
    return {"tags": tags}


@router.get("/{note_id}", response_model=NoteResponse)
def get_note(note_id: int, db: Session = Depends(get_db)):
    """Obtener una nota específica por ID"""
    note = get_note_by_id(db, note_id)
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nota con ID {note_id} no encontrada"
        )
    return note


@router.put("/{note_id}", response_model=NoteResponse)
def update_existing_note(
    note_id: int,
    note_update: NoteUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar una nota existente"""
    note = update_note(db, note_id, note_update)
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nota con ID {note_id} no encontrada"
        )
    return note


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_note(note_id: int, db: Session = Depends(get_db)):
    """Eliminar una nota"""
    success = delete_note(db, note_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nota con ID {note_id} no encontrada"
        )
    return None


@router.patch("/{note_id}/pin", response_model=NoteResponse)
def pin_note(note_id: int, db: Session = Depends(get_db)):
    """Alternar estado de fijado de una nota"""
    note = toggle_pin(db, note_id)
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nota con ID {note_id} no encontrada"
        )
    return note


@router.patch("/{note_id}/archive", response_model=NoteResponse)
def archive_note(note_id: int, db: Session = Depends(get_db)):
    """Alternar estado de archivado de una nota"""
    note = toggle_archive(db, note_id)
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nota con ID {note_id} no encontrada"
        )
    return note
