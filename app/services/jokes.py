import random
from typing import Optional, Tuple, List
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models import Joke
from app.schemas import JokeCreate, JokeUpdate


def create_joke(db: Session, joke: JokeCreate) -> Joke:
    """Crear un nuevo chiste"""
    db_joke = Joke(
        content=joke.content,
        category=joke.category,
        author=joke.author
    )
    db.add(db_joke)
    db.commit()
    db.refresh(db_joke)
    return db_joke


def get_joke_by_id(db: Session, joke_id: int) -> Optional[Joke]:
    """Obtener un chiste por ID"""
    return db.query(Joke).filter(Joke.id == joke_id).first()


def get_all_jokes(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None
) -> Tuple[List[Joke], int]:
    """Obtener lista de chistes con filtros opcionales"""
    query = db.query(Joke)

    if category:
        query = query.filter(Joke.category == category)

    total = query.count()
    jokes = query.offset(skip).limit(limit).all()
    return jokes, total


def get_random_joke(db: Session, category: Optional[str] = None) -> Optional[Joke]:
    """Obtener un chiste aleatorio, opcionalmente filtrado por categoría"""
    query = db.query(Joke)

    if category:
        query = query.filter(Joke.category == category)

    jokes = query.all()
    if not jokes:
        return None

    return random.choice(jokes)


def get_random_jokes(db: Session, count: int = 5) -> List[Joke]:
    """Obtener múltiples chistes aleatorios"""
    all_jokes = db.query(Joke).all()
    if len(all_jokes) <= count:
        return all_jokes

    return random.sample(all_jokes, count)


def update_joke(
    db: Session,
    joke_id: int,
    joke_update: JokeUpdate
) -> Optional[Joke]:
    """Actualizar un chiste existente"""
    db_joke = db.query(Joke).filter(Joke.id == joke_id).first()
    if not db_joke:
        return None

    update_data = joke_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_joke, key, value)

    db.commit()
    db.refresh(db_joke)
    return db_joke


def delete_joke(db: Session, joke_id: int) -> bool:
    """Eliminar un chiste"""
    db_joke = db.query(Joke).filter(Joke.id == joke_id).first()
    if not db_joke:
        return False

    db.delete(db_joke)
    db.commit()
    return True


def get_all_categories(db: Session) -> List[str]:
    """Obtener todas las categorías únicas"""
    categories = db.query(Joke.category).distinct().all()
    return [c[0] for c in categories if c[0] is not None]


def search_jokes(
    db: Session,
    query: str,
    skip: int = 0,
    limit: int = 100
) -> Tuple[List[Joke], int]:
    """Buscar chistes por contenido"""
    search = f"%{query}%"
    db_query = db.query(Joke).filter(
        Joke.content.ilike(search)
    )

    total = db_query.count()
    jokes = db_query.offset(skip).limit(limit).all()
    return jokes, total


def get_jokes_count(db: Session) -> int:
    """Obtener el número total de chistes"""
    return db.query(Joke).count()
