from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class JokeBase(BaseModel):
    content: str = Field(..., min_length=1, description="El contenido del chiste")
    category: Optional[str] = Field(None, max_length=100, description="Categoría del chiste")
    author: Optional[str] = Field(None, max_length=200, description="Autor del chiste")


class JokeCreate(JokeBase):
    pass


class JokeUpdate(BaseModel):
    content: Optional[str] = Field(None, min_length=1, description="El contenido del chiste")
    category: Optional[str] = Field(None, max_length=100)
    author: Optional[str] = Field(None, max_length=200)


class JokeResponse(JokeBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class JokeListResponse(BaseModel):
    total: int
    items: List[JokeResponse]


class CategoryListResponse(BaseModel):
    categories: List[str]
