"""
Operaciones CRUD (Create, Read, Update, Delete) para notas.
"""
from sqlalchemy.orm import Session
from models import Note
from schemas import NoteCreate, NoteUpdate


def create_note(db: Session, note: NoteCreate) -> Note:
    """Crea una nueva nota en la base de datos."""
    db_note = Note(title=note.title, content=note.content)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


def get_note(db: Session, note_id: int) -> Note | None:
    """Obtiene una nota por su ID."""
    return db.query(Note).filter(Note.id == note_id).first()


def get_notes(db: Session, skip: int = 0, limit: int = 100) -> list[Note]:
    """Obtiene una lista de notas con paginación."""
    return db.query(Note).offset(skip).limit(limit).all()


def update_note(db: Session, note_id: int, note_update: NoteUpdate) -> Note | None:
    """Actualiza una nota existente."""
    db_note = db.query(Note).filter(Note.id == note_id).first()
    if db_note is None:
        return None

    update_data = note_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_note, field, value)

    db.commit()
    db.refresh(db_note)
    return db_note


def delete_note(db: Session, note_id: int) -> bool:
    """Elimina una nota por su ID."""
    db_note = db.query(Note).filter(Note.id == note_id).first()
    if db_note is None:
        return False

    db.delete(db_note)
    db.commit()
    return True
