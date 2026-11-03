"""
Fase 5 — Recursividad genuina.

Idea sugerida: contar el tamaño de una colonia de plantas conectadas
(flood-fill). Documenten: qué resuelve, por qué recursión y no un ciclo,
y cuál es el caso base.
"""


def tamano_colonia(mundo, fila, columna, visitadas=None):
    # TODO:
    #   Casos base (devuelven 0):
    #     - la celda ya está en visitadas
    #     - en la celda no hay una Planta viva
    #   Caso recursivo:
    #     - marcar la celda como visitada
    #     - 1 + suma de tamano_colonia() en cada vecina
    raise NotImplementedError("Fase 5: tamano_colonia()")
