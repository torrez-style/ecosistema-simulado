"""
Fase 4 — Búsqueda u ordenamiento integrada a la simulación.

Ideas válidas (FAQ P11): formalizar la búsqueda de presa en las vecinas,
extender el radio de búsqueda, o un ranking por energía/edad mostrado
al final de cada turno.
"""


def distancia(pos_a, pos_b):
    """Distancia de Chebyshev: cuántos pasos (con diagonales) separan dos celdas."""
    return max(abs(pos_a[0] - pos_b[0]), abs(pos_a[1] - pos_b[1]))


def presa_mas_cercana(mundo, organismo, clase_presa):
    # TODO: entre las vecinas de organismo, devolver la presa viva de tipo
    # clase_presa más cercana (o None). Úsenla dentro de actuar().
    raise NotImplementedError("Fase 4: presa_mas_cercana()")


def ranking_por_energia(organismos):
    # TODO: devolver la lista ordenada de mayor a menor energía.
    raise NotImplementedError("Fase 4: ranking_por_energia()")
