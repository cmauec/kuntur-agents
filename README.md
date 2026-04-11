# Frases Aleatorias API

API REST construida con FastAPI para generar frases aleatorias inspiradoras, motivacionales y divertidas.

## Requisitos

- Python 3.8+

## Instalación

```bash
pip install -r requirements.txt
```

## Uso

### Iniciar el servidor

```bash
uvicorn main:app --reload
```

### Endpoints

- `GET /` - Información de la API
- `GET /frase` - Obtener una frase aleatoria
- `GET /frases/{cantidad}` - Obtener múltiples frases aleatorias (1-10)
- `GET /health` - Health check
- `GET /docs` - Documentación interactiva (Swagger UI)

### Ejemplos

```bash
# Obtener una frase aleatoria
curl http://localhost:8000/frase

# Obtener 5 frases aleatorias
curl http://localhost:8000/frases/5

# Verificar estado de la API
curl http://localhost:8000/health
```

## Características

- Más de 50 frases aleatorias de personajes históricos y filósofos
- Documentación automática con Swagger UI
- Soporte CORS habilitado
- Límite de 10 frases por petición
- Health check endpoint
