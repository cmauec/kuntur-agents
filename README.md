# Notes API

API REST construida con FastAPI para crear y gestionar notas.

## Características

- Crear notas con título y contenido
- Listar todas las notas (con paginación)
- Obtener una nota específica por ID
- Actualizar notas existentes
- Eliminar notas
- Validación automática de datos con Pydantic
- Base de datos SQLite

## Requisitos

- Python 3.8+
- FastAPI
- SQLAlchemy

## Instalación

1. Clonar el repositorio:
```bash
git clone <repositorio>
cd repo
```

2. Crear entorno virtual (opcional pero recomendado):
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate  # Windows
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Uso

### Iniciar el servidor

```bash
uvicorn main:app --reload
```

El servidor se iniciará en `http://localhost:8000`

### Documentación interactiva

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/notes` | Crear una nueva nota |
| GET | `/notes` | Listar todas las notas |
| GET | `/notes/{id}` | Obtener una nota específica |
| PUT | `/notes/{id}` | Actualizar una nota |
| DELETE | `/notes/{id}` | Eliminar una nota |

### Ejemplos de uso

#### Crear una nota
```bash
curl -X POST "http://localhost:8000/notes" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Mi primera nota",
    "content": "Este es el contenido de mi nota"
  }'
```

#### Listar notas
```bash
curl -X GET "http://localhost:8000/notes"
```

#### Obtener una nota específica
```bash
curl -X GET "http://localhost:8000/notes/1"
```

#### Actualizar una nota
```bash
curl -X PUT "http://localhost:8000/notes/1" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Título actualizado",
    "content": "Contenido actualizado"
  }'
```

#### Eliminar una nota
```bash
curl -X DELETE "http://localhost:8000/notes/1"
```

## Estructura del proyecto

```
.
├── main.py           # Punto de entrada de la aplicación
├── models.py         # Modelos SQLAlchemy
├── schemas.py        # Esquemas Pydantic
├── crud.py           # Operaciones CRUD
├── database.py       # Configuración de la base de datos
├── requirements.txt  # Dependencias
└── README.md         # Documentación
```

## Tecnologías utilizadas

- **FastAPI**: Framework web moderno y rápido
- **SQLAlchemy**: ORM para la base de datos
- **Pydantic**: Validación de datos
- **SQLite**: Base de datos ligera
- **Uvicorn**: Servidor ASGI
