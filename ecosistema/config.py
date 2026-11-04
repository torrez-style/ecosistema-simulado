"""
Parámetros del ecosistema.

Valores de referencia de la tabla de la sección 4 de la guía del proyecto,
con DOS ajustes para que el ecosistema dure varias decenas de turnos
(ver docs/decisiones_diseno.md y herramientas/probar_balance.py):
    - Grid de 20 x 20 (la guía sugiere 10 x 10, "ajustable").
    - Metabolismo del carnívoro: 1 por turno (referencia: 2).
"""

# --- Mundo (sección 4.1) ---------------------------------------------------
FILAS = 20       # referencia: 10
COLUMNAS = 20    # referencia: 10

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
        "metabolismo": 1,     # referencia: 2
        "ganancia": 10,       # al comer un herbívoro
        "edad_max": 45,
    },
}
