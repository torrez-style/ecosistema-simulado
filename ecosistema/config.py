"""
Parámetros del ecosistema.

Valores de referencia de la tabla de la sección 4 de la guía del proyecto.
Si los cambian, documenten el cambio en docs/decisiones_diseno.md (Fase 8).
"""

# --- Mundo (sección 4.1) ---------------------------------------------------
FILAS = 10
COLUMNAS = 10

# Cantidad inicial de organismos por especie (no ocupar más del 30-40 % del grid)
POBLACION_INICIAL = {
    "Planta": 15,
    "Herbivoro": 8,
    "Carnivoro": 3,
}

# Semilla para random: None = corrida distinta cada vez; un número (ej. 42)
# hace que la corrida sea reproducible.
SEMILLA = None

# --- Reproducción (sección 4.4) --------------------------------------------
PORCENTAJE_UMBRAL_REPRODUCCION = 70   # % de la energía máxima
PORCENTAJE_ENERGIA_AL_NACER = 50      # % de la energía máxima

# --- Parámetros por especie (tabla de la sección 4) -------------------------
PARAMETROS = {
    "Planta": {
        "energia_inicial": 10,
        "energia_max": 20,
        "metabolismo": 0,     # lo compensa la fotosíntesis
        "ganancia": 2,        # por fotosíntesis, cada turno
        "edad_max": 15,
    },
    "Herbivoro": {
        "energia_inicial": 12,
        "energia_max": 24,
        "metabolismo": 1,
        "ganancia": 6,        # al comer una planta
        "edad_max": 30,
    },
    "Carnivoro": {
        "energia_inicial": 15,
        "energia_max": 30,
        "metabolismo": 2,
        "ganancia": 10,       # al comer un herbívoro
        "edad_max": 45,
    },
}
