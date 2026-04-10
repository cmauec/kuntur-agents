from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class NoteBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Título de la nota")
    content: Optional[str] = Field(None, description="Contenido de la nota")
    tags: Optional[str] = Field(None, max_length=500, description="Tags separados por comas")
    is_pinned: bool = Field(False, description="Si la nota está fijada")
    is_archived: bool = Field(False, description="Si la nota está archivada")
    color: Optional[str] = Field(None, max_length=50, description="Color de la nota")


class NoteCreate(NoteBase):
    pass


class NoteUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = None
    tags: Optional[str] = Field(None, max_length=500)
    is_pinned: Optional[bool] = None
    is_archived: Optional[bool] = None
    color: Optional[str] = Field(None, max_length=50)


class NoteResponse(NoteBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class NoteListResponse(BaseModel):
    total: int
    items: List[NoteResponse]


class TagListResponse(BaseModel):
    tags: List[str]
