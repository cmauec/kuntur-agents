from fastapi import FastAPI
from app.routers import tasks

app = FastAPI(
    title="API de Lista de Tareas",
    description="Una API RESTful para gestionar tareas usando FastAPI",
    version="1.0.0"
)

app.include_router(tasks.router, prefix="/api/v1", tags=["tareas"])

@app.get("/")
async def root():
    return {
        "message": "Bienvenido a la API de Lista de Tareas",
        "docs": "/docs",
        "api": "/api/v1/tasks"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
