"""Datos iniciales de chistes para poblar la base de datos"""

SAMPLE_JOKES = [
    {
        "content": "¿Por qué los pájaros no usan Facebook? Porque ya tienen Twitter.",
        "category": "tecnología",
        "author": "Chistes Clásicos"
    },
    {
        "content": "¿Qué hace una abeja en el gimnasio? ¡Zum-ba!",
        "category": "animales",
        "author": "Chistes Cortos"
    },
    {
        "content": "¿Cómo se llama un boomerang que no vuelve? Palo.",
        "category": "general",
        "author": "Humor Universal"
    },
    {
        "content": "¿Por qué los programadores prefieren el otoño? Porque caen las hojas y no los servidores.",
        "category": "tecnología",
        "author": "Dev Humor"
    },
    {
        "content": "¿Qué le dice un jardinero a otro? Nos plantamos aquí.",
        "category": "general",
        "author": "Chistes Clásicos"
    },
    {
        "content": "¿Por qué el libro de matemáticas se deprimió? Porque tenía demasiados problemas.",
        "category": "educación",
        "author": "Chistes Escolares"
    },
    {
        "content": "¿Cómo se dice 'pañuelo' en japonés? Saka-moko.",
        "category": "lenguaje",
        "author": "Humor Internacional"
    },
    {
        "content": "¿Qué hace un pez en la biblioteca? Nada, porque no puede leer.",
        "category": "animales",
        "author": "Chistes Infantiles"
    },
    {
        "content": "¿Por qué los fantasmas no mienten? Porque se ven a través de ellos.",
        "category": "fantasía",
        "author": "Humor Sobrenatural"
    },
    {
        "content": "¿Qué le dice un gusano a otro? Voy a dar una vuelta a la manzana.",
        "category": "animales",
        "author": "Chistes Cortos"
    }
]


def seed_database(db):
    """Poblar la base de datos con chistes de ejemplo"""
    from app.models import Joke

    existing_count = db.query(Joke).count()
    if existing_count > 0:
        return  # Ya hay datos, no duplicar

    for joke_data in SAMPLE_JOKES:
        joke = Joke(**joke_data)
        db.add(joke)

    db.commit()
