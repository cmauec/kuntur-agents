# Frases API

API en FastAPI para generar frases aleatorias.

## Instalación

```bash
pip install -r requirements.txt
```

## Ejecución

```bash
uvicorn main:app --reload
```

## Endpoints

| Endpoint | Descripción |
|----------|-------------|
| `GET /` | Información de la API |
| `GET /frase-simple` | Genera una frase simple |
| `GET /frase-compleja` | Genera una frase compleja |
| `GET /frases/{cantidad}` | Genera múltiples frases (1-10) |
| `GET /categorias` | Información de categorías disponibles |

## Documentación

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
