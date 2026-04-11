"""
FastAPI API para generar frases aleatorias.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import random
import uvicorn

app = FastAPI(
    title="Frases Aleatorias API",
    description="API para generar frases aleatorias inspiradoras, motivacionales y divertidas.",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Lista de frases aleatorias
FRASES = [
    "El único modo de hacer un gran trabajo es amar lo que haces. - Steve Jobs",
    "La vida es lo que pasa mientras estás ocupado haciendo otros planes. - John Lennon",
    "El conocimiento es poder. - Francis Bacon",
    "La imaginación es más importante que el conocimiento. - Albert Einstein",
    "El éxito es la suma de pequeños esfuerzos repetidos cada día. - Robert Collier",
    "No cuentes los días, haz que los días cuenten. - Muhammad Ali",
    "La mejor manera de predecir el futuro es crearlo. - Peter Drucker",
    "El fracaso es la oportunidad de comenzar de nuevo con más inteligencia. - Henry Ford",
    "La felicidad no es algo hecho. Viene de tus propias acciones. - Dalai Lama",
    "Cree que puedes y ya estás a medio camino. - Theodore Roosevelt",
    "No importa lo lento que vayas, siempre y cuando no te detengas. - Confucio",
    "Todo lo que siempre has querido está al otro lado del miedo. - George Addair",
    "El propósito de nuestra vida es ser felices. - Dalai Lama",
    "La vida es 10% lo que me ocurre y 90% cómo reacciono a ello. - Charles Swindoll",
    "El momento que das por sentado es el momento que empiezas a perder. - Tiger Woods",
    "El éxito no es definitivo, el fracaso no es fatal: es el coraje para continuar lo que cuenta. - Winston Churchill",
    "La vida es como andar en bicicleta. Para mantener el equilibrio, debes seguir adelante. - Albert Einstein",
    "El futuro pertenece a quienes creen en la belleza de sus sueños. - Eleanor Roosevelt",
    "No puedes cruzar el mar simplemente mirando el agua. - Rabindranath Tagore",
    "El único límite para nuestra realización de mañana serán nuestras dudas de hoy. - Franklin D. Roosevelt",
    "Haz de cada día tu obra maestra. - John Wooden",
    "El secreto del éxito es la constancia del propósito. - Benjamin Disraeli",
    "La mejor venganza es un éxito masivo. - Frank Sinatra",
    "Arriesgate más de lo que otros creen seguro. Sueña más de lo que otros creen práctico. - Howard Schultz",
    "No dejes que lo que no puedes hacer interfiera con lo que puedes hacer. - John Wooden",
    "La excelencia no es un acto, es un hábito. - Aristóteles",
    "Si puedes soñarlo, puedes lograrlo. - Walt Disney",
    "El éxito es ir de fracaso en fracaso sin perder entusiasmo. - Winston Churchill",
    "La vida comienza al final de tu zona de confort. - Neale Donald Walsch",
    "El único lugar donde el éxito viene antes que el trabajo es en el diccionario. - Vidal Sassoon",
    "Nunca es tarde para ser lo que podrías haber sido. - George Eliot",
    "El cambio es el resultado final del verdadero aprendizaje. - Leo Buscaglia",
    "La felicidad es un viaje, no un destino. - Roy Goodman",
    "Todo parece imposible hasta que se hace. - Nelson Mandela",
    "La perseverancia no es una carrera larga; son muchas carreras cortas una tras otra. - Walter Elliot",
    "El talento gana partidos, pero el trabajo en equipo y la inteligencia ganan campeonatos. - Michael Jordan",
    "El éxito es conseguir lo que quieres. La felicidad es querer lo que consigues. - Dale Carnegie",
    "La mente es todo. Lo que piensas, te conviertes. - Buda",
    "Los grandes logros requieren tiempo y paciencia. - Confucio",
    "La creatividad es la inteligencia divirtiéndose. - Albert Einstein",
    "La acción es la clave fundamental para todo éxito. - Pablo Picasso",
    "Nunca sabes lo fuerte que eres hasta que ser fuerte es la única opción que tienes. - Bob Marley",
    "El éxito no es cuánto dinero ganas, es la diferencia que haces en la vida de otros. - Michelle Obama",
    "Sé el cambio que quieres ver en el mundo. - Mahatma Gandhi",
    "El amor es la fuerza más poderosa del universo. - Martin Luther King Jr.",
    "La vida es un riesgo, pero te aseguro que vale la pena. - Anónimo",
    "Nunca es demasiado tarde para aprender algo nuevo. - Anónimo",
    "El optimismo es la fe que conduce al logro. - Helen Keller",
    "El verdadero fracaso es no intentarlo. - Anónimo",
]


@app.get("/")
async def root():
    """Endpoint raíz con información de la API."""
    return {
        "message": "Bienvenido a la API de Frases Aleatorias",
        "documentation": "/docs",
        "endpoints": {
            "/frase": "Obtener una frase aleatoria",
            "/frases/{cantidad}": "Obtener múltiples frases aleatorias"
        }
    }


@app.get("/frase")
async def get_frase():
    """Obtener una frase aleatoria."""
    return {
        "frase": random.choice(FRASES)
    }


@app.get("/frases/{cantidad}")
async def get_frases(cantidad: int):
    """
    Obtener múltiples frases aleatorias.

    - **cantidad**: Número de frases a retornar (1-10)
    """
    if cantidad < 1:
        cantidad = 1
    elif cantidad > 10:
        cantidad = 10

    frases_seleccionadas = random.sample(FRASES, min(cantidad, len(FRASES)))

    return {
        "cantidad": len(frases_seleccionadas),
        "frases": frases_seleccionadas
    }


@app.get("/health")
async def health():
    """Endpoint de health check."""
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
