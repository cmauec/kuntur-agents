from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from datetime import datetime

from models import Task, TaskCreate, TaskUpdate, TaskStatus

app = FastAPI(
    title="API de Lista de Tareas",
    description="API REST para gestión de tareas con FastAPI",
    version="1.0.0"
)

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Base de datos en memoria
tasks_db: List[Task] = []
task_id_counter = 1


@app.get("/")
def read_root():
    """Endpoint de bienvenida"""
    return {
        "message": "Bienvenido a la API de Lista de Tareas",
        "docs": "/docs",
        "version": "1.0.0"
    }


@app.get("/health")
def health_check():
    """Endpoint de health check"""
    return {"status": "healthy"}


@app.get("/tasks", response_model=List[Task])
def get_tasks(status: TaskStatus = None):
    """
    Obtener todas las tareas.
    Opcionalmente filtrar por estado.
    """
    if status:
        return [task for task in tasks_db if task.status == status]
    return tasks_db


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    """Obtener una tarea específica por ID"""
    for task in tasks_db:
        if task.id == task_id:
            return task
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Tarea con ID {task_id} no encontrada"
    )


@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate):
    """Crear una nueva tarea"""
    global task_id_counter

    new_task = Task(
        id=task_id_counter,
        title=task.title,
        description=task.description,
        status=task.status,
        created_at=datetime.now(),
        updated_at=None
    )

    tasks_db.append(new_task)
    task_id_counter += 1

    return new_task


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task_update: TaskUpdate):
    """Actualizar una tarea existente"""
    for index, task in enumerate(tasks_db):
        if task.id == task_id:
            updated_data = task.model_dump()

            if task_update.title is not None:
                updated_data["title"] = task_update.title
            if task_update.description is not None:
                updated_data["description"] = task_update.description
            if task_update.status is not None:
                updated_data["status"] = task_update.status

            updated_data["updated_at"] = datetime.now()

            updated_task = Task(**updated_data)
            tasks_db[index] = updated_task

            return updated_task

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Tarea con ID {task_id} no encontrada"
    )


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    """Eliminar una tarea"""
    for index, task in enumerate(tasks_db):
        if task.id == task_id:
            tasks_db.pop(index)
            return None

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Tarea con ID {task_id} no encontrada"
    )


@app.patch("/tasks/{task_id}/complete", response_model=Task)
def complete_task(task_id: int):
    """Marcar una tarea como completada"""
    for index, task in enumerate(tasks_db):
        if task.id == task_id:
            updated_data = task.model_dump()
            updated_data["status"] = TaskStatus.COMPLETED
            updated_data["updated_at"] = datetime.now()

            updated_task = Task(**updated_data)
            tasks_db[index] = updated_task

            return updated_task

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Tarea con ID {task_id} no encontrada"
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
