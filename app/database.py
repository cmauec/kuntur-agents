from typing import Dict, Optional
from datetime import datetime
from app.models import Task, TaskStatus, TaskPriority


class TaskDatabase:
    def __init__(self):
        self._tasks: Dict[int, Task] = {}
        self._counter: int = 0

    def get_all(self, status: Optional[TaskStatus] = None, priority: Optional[TaskPriority] = None) -> list[Task]:
        tasks = list(self._tasks.values())
        if status:
            tasks = [t for t in tasks if t.status == status]
        if priority:
            tasks = [t for t in tasks if t.priority == priority]
        return sorted(tasks, key=lambda x: x.created_at, reverse=True)

    def get_by_id(self, task_id: int) -> Optional[Task]:
        return self._tasks.get(task_id)

    def create(self, task_data: dict) -> Task:
        self._counter += 1
        task = Task(
            id=self._counter,
            **task_data,
            created_at=datetime.now()
        )
        self._tasks[task.id] = task
        return task

    def update(self, task_id: int, task_data: dict) -> Optional[Task]:
        if task_id not in self._tasks:
            return None
        existing = self._tasks[task_id]
        update_data = {k: v for k, v in task_data.items() if v is not None}
        update_data["updated_at"] = datetime.now()
        updated_task = existing.model_copy(update=update_data)
        self._tasks[task_id] = updated_task
        return updated_task

    def delete(self, task_id: int) -> bool:
        if task_id not in self._tasks:
            return False
        del self._tasks[task_id]
        return True

    def clear(self):
        self._tasks.clear()
        self._counter = 0


db = TaskDatabase()
