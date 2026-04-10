from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import or_, func

from app.models import Note
from app.schemas import NoteCreate, NoteUpdate


def create_note(db: Session, note_data: NoteCreate) -> Note:
    """Crear una nueva nota"""
    db_note = Note(
        title=note_data.title,
        content=note_data.content,
        tags=note_data.tags,
        is_pinned=note_data.is_pinned,
        is_archived=note_data.is_archived,
        color=note_data.color
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


def get_note_by_id(db: Session, note_id: int) -> Optional[Note]:
    """Obtener una nota por su ID"""
    return db.query(Note).filter(Note.id == note_id).first()


def get_all_notes(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    is_archived: Optional[bool] = None,
    is_pinned: Optional[bool] = None,
    tag: Optional[str] = None
) -> Tuple[List[Note], int]:
    """Obtener todas las notas con filtros opcionales"""
    query = db.query(Note)

    if is_archived is not None:
        query = query.filter(Note.is_archived == is_archived)

    if is_pinned is not None:
        query = query.filter(Note.is_pinned == is_pinned)

    if tag:
        query = query.filter(Note.tags.contains(tag))

    # Ordenar: primero fijadas, luego por fecha de creación descendente
    query = query.order_by(Note.is_pinned.desc(), Note.created_at.desc())

    total = query.count()
    notes = query.offset(skip).limit(limit).all()

    return notes, total


def update_note(db: Session, note_id: int, note_update: NoteUpdate) -> Optional[Note]:
    """Actualizar una nota existente"""
    db_note = get_note_by_id(db, note_id)
    if not db_note:
        return None

    update_data = note_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_note, field, value)

    db.commit()
    db.refresh(db_note)
    return db_note


def delete_note(db: Session, note_id: int) -> bool:
    """Eliminar una nota"""
    db_note = get_note_by_id(db, note_id)
    if not db_note:
        return False

    db.delete(db_note)
    db.commit()
    return True


def search_notes(
    db: Session,
    query: str,
    skip: int = 0,
    limit: int = 100
) -> Tuple[List[Note], int]:
    """Buscar notas por título o contenido"""
    search_filter = or_(
        Note.title.ilike(f"%{query}%"),
        Note.content.ilike(f"%{query}%")
    )

    db_query = db.query(Note).filter(search_filter)
    total = db_query.count()

    notes = db_query.order_by(
        Note.is_pinned.desc(),
        Note.created_at.desc()
    ).offset(skip).limit(limit).all()

    return notes, total


def get_all_tags(db: Session) -> List[str]:
    """Obtener todos los tags únicos"""
    tags_result = db.query(Note.tags).filter(Note.tags.isnot(None)).all()

    unique_tags = set()
    for (tags_str,) in tags_result:
        if tags_str:
            # Separar por comas y limpiar espacios
            tags = [tag.strip() for tag in tags_str.split(",")]
            unique_tags.update(tag for tag in tags if tag)

    return sorted(list(unique_tags))


def toggle_pin(db: Session, note_id: int) -> Optional[Note]:
    """Alternar el estado de fijado de una nota"""
    db_note = get_note_by_id(db, note_id)
    if not db_note:
        return None

    db_note.is_pinned = not db_note.is_pinned
    db.commit()
    db.refresh(db_note)
    return db_note


def toggle_archive(db: Session, note_id: int) -> Optional[Note]:
    """Alternar el estado de archivado de una nota"""
    db_note = get_note_by_id(db, note_id)
    if not db_note:
        return None

    db_note.is_archived = not db_note.is_archived
    db.commit()
    db.refresh(db_note)
    return db_note
