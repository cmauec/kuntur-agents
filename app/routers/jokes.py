from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import (
    JokeCreate,
    JokeUpdate,
    JokeResponse,
    JokeListResponse,
    CategoryListResponse
)
from app.services.jokes import (
    create_joke,
    get_joke_by_id,
    get_all_jokes,
    get_random_joke,
    get_random_jokes,
    update_joke,
    delete_joke,
    get_all_categories,
    search_jokes,
    get_jokes_count
)

router = APIRouter()


@router.post("/", response_model=JokeResponse, status_code=status.HTTP_201_CREATED)
def create_new_joke(joke: JokeCreate, db: Session = Depends(get_db)):
    """Crear un nuevo chiste"""
    return create_joke(db, joke)


@router.get("/", response_model=JokeListResponse)
def list_jokes(
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros"),
    category: Optional[str] = Query(None, description="Filtrar por categoría"),
    db: Session = Depends(get_db)
):
    """Obtener lista de chistes con filtros opcionales"""
    jokes, total = get_all_jokes(db, skip=skip, limit=limit, category=category)
    return {"items": jokes, "total": total}


@router.get("/random", response_model=JokeResponse)
def get_random(
    category: Optional[str] = Query(None, description="Filtrar por categoría"),
    db: Session = Depends(get_db)
):
    """Obtener un chiste aleatorio"""
    joke = get_random_joke(db, category=category)
    if not joke:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontraron chistes"
        )
    return joke


@router.get("/random/multiple", response_model=JokeListResponse)
def get_multiple_random(
    count: int = Query(5, ge=1, le=50, description="Cantidad de chistes aleatorios a obtener"),
    db: Session = Depends(get_db)
):
    """Obtener múltiples chistes aleatorios"""
    jokes = get_random_jokes(db, count=count)
    return {"items": jokes, "total": len(jokes)}


@router.get("/categories", response_model=CategoryListResponse)
def list_categories(db: Session = Depends(get_db)):
    """Obtener todas las categorías únicas"""
    categories = get_all_categories(db)
    return {"categories": categories}


@router.get("/search", response_model=JokeListResponse)
def search_jokes_endpoint(
    q: str = Query(..., min_length=1, description="Término de búsqueda"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Buscar chistes por contenido"""
    jokes, total = search_jokes(db, query=q, skip=skip, limit=limit)
    return {"items": jokes, "total": total}


@router.get("/stats/count")
def get_stats(db: Session = Depends(get_db)):
    """Obtener estadísticas de chistes"""
    return {"total_jokes": get_jokes_count(db)}


@router.get("/{joke_id}", response_model=JokeResponse)
def get_joke(joke_id: int, db: Session = Depends(get_db)):
    """Obtener un chiste específico por ID"""
    joke = get_joke_by_id(db, joke_id)
    if not joke:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Chiste con ID {joke_id} no encontrado"
        )
    return joke


@router.put("/{joke_id}", response_model=JokeResponse)
def update_existing_joke(
    joke_id: int,
    joke_update: JokeUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar un chiste existente"""
    joke = update_joke(db, joke_id, joke_update)
    if not joke:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Chiste con ID {joke_id} no encontrado"
        )
    return joke


@router.delete("/{joke_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_joke(joke_id: int, db: Session = Depends(get_db)):
    """Eliminar un chiste"""
    success = delete_joke(db, joke_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Chiste con ID {joke_id} no encontrado"
        )
    return None
