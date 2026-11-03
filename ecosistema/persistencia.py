"""
Fase 6 — Guardar y cargar el estado completo del ecosistema (JSON).

El archivo debe incluir el turno, el tamaño del grid y, por cada organismo:
especie, fila, columna, energía y edad.
"""

import json  # noqa: F401  (se usará al implementar)

RUTA_POR_DEFECTO = "guardados/partida.json"


def guardar(mundo, ruta=RUTA_POR_DEFECTO):
    # TODO: convertir el mundo a un diccionario y escribirlo con json.dump()
    raise NotImplementedError("Fase 6: guardar()")


def cargar(ruta=RUTA_POR_DEFECTO):
    # TODO: leer con json.load() y reconstruir un Mundo idéntico.
    # Pista: un diccionario {"Planta": Planta, ...} evita un if/elif por especie.
    raise NotImplementedError("Fase 6: cargar()")
