# API de Lista de Tareas - FastAPI

Una API RESTful completa para gestionar tareas, construida con FastAPI.

## Características

- ✅ CRUD completo para tareas
- ✅ Filtrado por estado y prioridad
- ✅ Documentación automática (Swagger/OpenAPI)
- ✅ Validación de datos con Pydantic
- ✅ Base de datos en memoria (para desarrollo)

## Instalación

```bash
# Clonar el repositorio
git clone <repo-url>
cd repo

# Crear entorno virtual (opcional)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt
```

## Uso

```bash
# Iniciar el servidor
uvicorn main:app --reload
```

La API estará disponible en: http://localhost:8000

## Documentación

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Información de la API |
| GET | `/health` | Health check |
| GET | `/api/v1/tasks/` | Listar todas las tareas |
| GET | `/api/v1/tasks/{id}` | Obtener una tarea |
| POST | `/api/v1/tasks/` | Crear tarea |
| PUT | `/api/v1/tasks/{id}` | Actualizar tarea |
| DELETE | `/api/v1/tasks/{id}` | Eliminar tarea |
| PATCH | `/api/v1/tasks/{id}/complete` | Completar tarea |

## Modelos

### Task
- `id`: int (autogenerado)
- `title`: str (requerido)
- `description`: str (opcional)
- `status`: pending | in_progress | completed
- `priority`: low | medium | high
- `created_at`: datetime
- `updated_at`: datetime (opcional)

## Ejemplos

### Crear una tarea
```bash
curl -X POST "http://localhost:8000/api/v1/tasks/" \
  -H "Content-Type: application/json" \
  -d '{"title": "Aprender FastAPI", "priority": "high"}'
```

### Listar tareas
```bash
curl "http://localhost:8000/api/v1/tasks/"
```

### Filtrar por estado
```bash
curl "http://localhost:8000/api/v1/tasks/?status=pending"
```
