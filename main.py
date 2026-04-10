from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.database import engine, Base
from app.routers import notes


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Crear tablas al iniciar
    Base.metadata.create_all(bind=engine)
    yield
    # Cleanup al cerrar (si es necesario)


app = FastAPI(
    title="Notes API",
    description="API para gestión de notas con FastAPI",
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
app.include_router(notes.router, prefix="/api/v1/notes", tags=["notes"])


@app.get("/")
def root():
    return {"message": "Notes API - Visita /docs para la documentación"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
