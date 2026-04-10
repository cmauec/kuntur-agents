# API de Lista de Tareas

API REST para gestión de tareas construida con FastAPI.

## Características

- ✅ CRUD completo de tareas
- ✅ Filtrado por estado
- ✅ Validación de datos con Pydantic
- ✅ Documentación automática con Swagger UI
- ✅ CORS habilitado

## Instalación

```bash
pip install -r requirements.txt
```

## Uso

### Iniciar el servidor

```bash
uvicorn main:app --reload
```

O directamente:

```bash
python main.py
```

### Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Mensaje de bienvenida |
| GET | `/health` | Health check |
| GET | `/tasks` | Listar todas las tareas |
| GET | `/tasks?status=pending` | Filtrar por estado |
| GET | `/tasks/{id}` | Obtener tarea específica |
| POST | `/tasks` | Crear nueva tarea |
| PUT | `/tasks/{id}` | Actualizar tarea completa |
| PATCH | `/tasks/{id}/complete` | Marcar como completada |
| DELETE | `/tasks/{id}` | Eliminar tarea |

### Documentación

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Ejemplo de uso

**Crear una tarea:**
```bash
curl -X POST "http://localhost:8000/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Aprender FastAPI",
    "description": "Completar el tutorial de FastAPI",
    "status": "pending"
  }'
```

**Listar tareas:**
```bash
curl "http://localhost:8000/tasks"
```

**Actualizar una tarea:**
```bash
curl -X PUT "http://localhost:8000/tasks/1" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Aprender FastAPI - Actualizado",
    "status": "in_progress"
  }'
```

**Marcar como completada:**
```bash
curl -X PATCH "http://localhost:8000/tasks/1/complete"
```

**Eliminar una tarea:**
```bash
curl -X DELETE "http://localhost:8000/tasks/1"
```

## Estados de tareas

- `pending` - Pendiente
- `in_progress` - En progreso
- `completed` - Completada
