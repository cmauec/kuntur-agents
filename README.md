# Notes API

API RESTful para gestión de notas construida con FastAPI.

## Características

- ✅ CRUD completo de notas
- ✅ Búsqueda de notas por título o contenido
- ✅ Fijar/archivar notas
- ✅ Sistema de tags
- ✅ Colores personalizados para notas
- ✅ Documentación automática con Swagger UI
- ✅ Base de datos SQLite con SQLAlchemy

## Endpoints

### Notas

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/v1/notes/` | Crear nota |
| GET | `/api/v1/notes/` | Listar notas |
| GET | `/api/v1/notes/{id}` | Obtener nota |
| PUT | `/api/v1/notes/{id}` | Actualizar nota |
| DELETE | `/api/v1/notes/{id}` | Eliminar nota |
| PATCH | `/api/v1/notes/{id}/pin` | Fijar/desfijar nota |
| PATCH | `/api/v1/notes/{id}/archive` | Archivar/desarchivar nota |
| GET | `/api/v1/notes/search?q={query}` | Buscar notas |
| GET | `/api/v1/notes/tags` | Listar tags |

### Sistema

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Información de la API |
| GET | `/health` | Health check |
| GET | `/docs` | Documentación Swagger UI |
| GET | `/redoc` | Documentación ReDoc |

## Instalación

```bash
pip install -r requirements.txt
```

## Ejecución

```bash
uvicorn main:app --reload
```

La API estará disponible en `http://localhost:8000`

## Ejemplos de uso

### Crear una nota
```bash
curl -X POST "http://localhost:8000/api/v1/notes/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Mi primera nota",
    "content": "Contenido de la nota",
    "tags": "personal,ideas",
    "color": "yellow"
  }'
```

### Listar notas
```bash
curl "http://localhost:8000/api/v1/notes/"
```

### Buscar notas
```bash
curl "http://localhost:8000/api/v1/notes/search?q=importante"
```

### Fijar una nota
```bash
curl -X PATCH "http://localhost:8000/api/v1/notes/1/pin"
```
