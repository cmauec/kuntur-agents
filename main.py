from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.database import engine, Base
from app.routers import jokes


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Crear tablas al iniciar
    Base.metadata.create_all(bind=engine)
    # Poblar con datos iniciales si es necesario
    from app.database import SessionLocal
    from app.seed_data import seed_database
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()
    yield
    # Cleanup al cerrar (si es necesario)


app = FastAPI(
    title="Jokes API",
    description="API para crear y obtener chistes aleatorios con FastAPI",
    version="1.0.0",
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(jokes.router, prefix="/api/v1/jokes", tags=["jokes"])


@app.get("/")
def root():
    return {"message": "Jokes API - Visita /docs para la documentación"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
