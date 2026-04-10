from fastapi import APIRouter, HTTPException, Query, status
from typing import Optional
from app.models import Task, TaskCreate, TaskUpdate, TaskStatus, TaskPriority
from app.database import db

router = APIRouter(prefix="/tasks")


@router.get("/", response_model=list[Task])
async def get_tasks(
    status: Optional[TaskStatus] = Query(None, description="Filtrar por estado"),
    priority: Optional[TaskPriority] = Query(None, description="Filtrar por prioridad")
):
    """Obtener todas las tareas, con filtros opcionales por estado y prioridad."""
    return db.get_all(status=status, priority=priority)


@router.get("/{task_id}", response_model=Task)
async def get_task(task_id: int):
    """Obtener una tarea específica por su ID."""
    task = db.get_by_id(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarea con id {task_id} no encontrada"
        )
    return task


@router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate):
    """Crear una nueva tarea."""
    task_data = task.model_dump()
    return db.create(task_data)


@router.put("/{task_id}", response_model=Task)
async def update_task(task_id: int, task_update: TaskUpdate):
    """Actualizar una tarea existente."""
    update_data = task_update.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se proporcionaron campos para actualizar"
        )
    updated_task = db.update(task_id, update_data)
    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarea con id {task_id} no encontrada"
        )
    return updated_task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int):
    """Eliminar una tarea por su ID."""
    if not db.delete(task_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarea con id {task_id} no encontrada"
        )
    return None


@router.patch("/{task_id}/complete", response_model=Task)
async def complete_task(task_id: int):
    """Marcar una tarea como completada."""
    task = db.update(task_id, {"status": TaskStatus.COMPLETED})
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarea con id {task_id} no encontrada"
        )
    return task
