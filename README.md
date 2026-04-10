# Jokes API - API de Chistes Aleatorios

API REST desarrollada con FastAPI para crear, gestionar y obtener chistes aleatorios.

## Características

- **Crear chistes**: Agrega nuevos chistes con categoría y autor
- **Obtener chistes aleatorios**: Endpoint especial para obtener chistes al azar
- **Filtrar por categoría**: Organiza los chistes por categorías
- **Búsqueda**: Busca chistes por contenido
- **CRUD completo**: Crear, leer, actualizar y eliminar chistes
- **Documentación automática**: Swagger UI y ReDoc incluidos

## Tecnologías

- FastAPI 0.109.0
- SQLAlchemy 2.0.25
- SQLite (base de datos)
- Pydantic 2.5.3

## Instalación

```bash
# Clonar el repositorio
git clone <repo-url>
cd repo

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt
```

## Uso

### Iniciar el servidor

```bash
uvicorn main:app --reload
```

El servidor estará disponible en: http://localhost:8000

### Documentación

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Endpoints principales

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/v1/jokes/` | Crear un nuevo chiste |
| GET | `/api/v1/jokes/` | Listar todos los chistes |
| GET | `/api/v1/jokes/random` | Obtener un chiste aleatorio |
| GET | `/api/v1/jokes/random/multiple` | Obtener múltiples chistes aleatorios |
| GET | `/api/v1/jokes/{id}` | Obtener un chiste por ID |
| PUT | `/api/v1/jokes/{id}` | Actualizar un chiste |
| DELETE | `/api/v1/jokes/{id}` | Eliminar un chiste |
| GET | `/api/v1/jokes/categories` | Listar categorías disponibles |
| GET | `/api/v1/jokes/search` | Buscar chistes |
| GET | `/api/v1/jokes/stats/count` | Obtener estadísticas |

### Ejemplos de uso

#### Crear un chiste

```bash
curl -X POST "http://localhost:8000/api/v1/jokes/" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "¿Por qué los pájaros no usan Facebook? Porque ya tienen Twitter.",
    "category": "tecnología",
    "author": "Chistes Clásicos"
  }'
```

#### Obtener un chiste aleatorio

```bash
curl "http://localhost:8000/api/v1/jokes/random"
```

#### Obtener chistes aleatorios por categoría

```bash
curl "http://localhost:8000/api/v1/jokes/random?category=animales"
```

#### Buscar chistes

```bash
curl "http://localhost:8000/api/v1/jokes/search?q=programador"
```

## Estructura del proyecto

```
.
├── app/
│   ├── __init__.py
│   ├── database.py      # Configuración de SQLAlchemy
│   ├── models.py        # Modelos de la base de datos
│   ├── schemas.py       # Esquemas Pydantic
│   ├── seed_data.py     # Datos iniciales
│   ├── routers/
│   │   ├── __init__.py
│   │   └── jokes.py     # Rutas de la API
│   └── services/
│       ├── __init__.py
│       └── jokes.py     # Lógica de negocio
├── main.py              # Punto de entrada
├── requirements.txt     # Dependencias
└── README.md
```

## Modelo de datos

### Joke (Chiste)

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | Integer | Identificador único |
| content | Text | El contenido del chiste |
| category | String | Categoría del chiste |
| author | String | Autor del chiste |
| created_at | DateTime | Fecha de creación |

## Licencia

MIT
