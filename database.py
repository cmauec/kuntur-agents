"""
Configuración de la base de datos.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Usar SQLite como base de datos
SQLALCHEMY_DATABASE_URL = "sqlite:///./notes.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Generador de sesiones de base de datos para dependency injection."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
