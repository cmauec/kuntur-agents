from fastapi import FastAPI
from fastapi.responses import JSONResponse
import random

app = FastAPI(
    title="Frases API",
    description="API para generar frases aleatorias",
    version="1.0.0"
)

# Banco de palabras para generar frases
SUJETOS = [
    "El gato", "La abuela", "Un astronauta", "Mi vecino", "El programador",
    "La profesora", "Un dragón", "El panadero", "La cantante", "Un robot",
    "El mago", "La detective", "Un pingüino", "El chef", "La astronauta"
]

VERBOS = [
    "salta sobre", "programa", "cocina", "descubre", "pinta",
    "explora", "construye", "salva", "transforma", "investiga",
    "vuela hacia", "escribe", "repara", "diseña", "encuentra"
]

OBJETOS = [
    "un teclado", "la luna", "un pastel", "un misterio", "un cuadro",
    "galaxias", "castillos", "ciudades", "recetas secretas", "algoritmos",
    "tésomas voladores", "historias", "robots", "sueños", "aventuras"
]

ADVERBios = [
    "rápidamente", "con entusiasmo", "en silencio", "magistralmente",
    "sin miedo", "creativamente", "precisamente", "alegremente",
    "misteriosamente", "perfectamente", "divertidamente", "sabiamente"
]

COMPLEMENTOS = [
    "en la noche", "durante el día", "en el espacio", "en la cocina",
    "con amigos", "en el jardín", "bajo la lluvia", "en la biblioteca",
    "con mucho cuidado", "para salvar el mundo", "mientras canta",
    "con una sonrisa", "en invierno", "con determinación"
]


def generar_frase_simple() -> str:
    """Genera una frase simple: Sujeto + Verbo + Objeto"""
    return f"{random.choice(SUJETOS)} {random.choice(VERBOS)} {random.choice(OBJETOS)}"


def generar_frase_compleja() -> str:
    """Genera una frase compleja con adverbio y complemento"""
    return f"{random.choice(SUJETOS)} {random.choice(VERBOS)} {random.choice(OBJETOS)} {random.choice(ADVERBios)} {random.choice(COMPLEMENTOS)}"


@app.get("/")
async def root():
    """Endpoint de bienvenida"""
    return {
        "mensaje": "Bienvenido a la API de Frases Aleatorias",
        "documentacion": "/docs",
        "endpoints": [
            "/frase-simple",
            "/frase-compleja",
            "/frases/{cantidad}"
        ]
    }


@app.get("/frase-simple")
async def frase_simple():
    """Genera una frase simple aleatoria"""
    return {
        "frase": generar_frase_simple(),
        "tipo": "simple"
    }


@app.get("/frase-compleja")
async def frase_compleja():
    """Genera una frase compleja aleatoria"""
    return {
        "frase": generar_frase_compleja(),
        "tipo": "compleja"
    }


@app.get("/frases/{cantidad}")
async def frases_multiple(cantidad: int):
    """
    Genera múltiples frases aleatorias

    - **cantidad**: Número de frases a generar (1-10)
    """
    if cantidad < 1 or cantidad > 10:
        return JSONResponse(
            status_code=400,
            content={"error": "La cantidad debe estar entre 1 y 10"}
        )

    frases = []
    for _ in range(cantidad):
        if random.choice([True, False]):
            frases.append({
                "frase": generar_frase_simple(),
                "tipo": "simple"
            })
        else:
            frases.append({
                "frase": generar_frase_compleja(),
                "tipo": "compleja"
            })

    return {
        "cantidad": cantidad,
        "frases": frases
    }


@app.get("/categorias")
async def categorias():
    """Retorna las categorías de palabras disponibles"""
    return {
        "sujetos": len(SUJETOS),
        "verbos": len(VERBOS),
        "objetos": len(OBJETOS),
        "adverbios": len(ADVERBios),
        "complementos": len(COMPLEMENTOS),
        "combinaciones_posibles": len(SUJETOS) * len(VERBOS) * len(OBJETOS) * len(ADVERBios) * len(COMPLEMENTOS)
    }
