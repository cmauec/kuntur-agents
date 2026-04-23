"""
Esquemas Pydantic para validación de datos.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class NoteBase(BaseModel):
    """Esquema base para notas."""
    title: str = Field(..., min_length=1, max_length=255, description="Título de la nota")
    content: str = Field(..., min_length=1, description="Contenido de la nota")


class NoteCreate(NoteBase):
    """Esquema para crear una nueva nota."""
    pass


class NoteUpdate(BaseModel):
    """Esquema para actualizar una nota existente."""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    content: Optional[str] = Field(None, min_length=1)


class NoteResponse(NoteBase):
    """Esquema de respuesta con los datos de la nota."""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
