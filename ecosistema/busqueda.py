"""
Fase 4 — Búsqueda integrada a la simulación.

presa_mas_cercana() es la que usan Herbivoro.actuar() y Carnivoro.actuar()
para decidir a quién comer (FAQ P11).
"""


def distancia(pos_a, pos_b):
    """
    Distancia euclidiana al cuadrado entre dos celdas.
    Una vecina de lado está a 1 y una diagonal a 2, así que se prefieren
    las presas de lado. (Al cuadrado para no usar raíces: el orden es el mismo.)
    """
    return (pos_a[0] - pos_b[0]) ** 2 + (pos_a[1] - pos_b[1]) ** 2


def presa_mas_cercana(mundo, organismo, clase_presa):
    """
    Búsqueda lineal del mínimo entre las 8 vecinas.
    Devuelve la presa VIVA de tipo clase_presa más cercana, o None.
    Si hay empate, gana la primera encontrada (orden de Mundo.DIRECCIONES).
    """
    mejor = None
    mejor_distancia = None
    for fila, columna in mundo.vecinas(*organismo.posicion):
        candidata = mundo.celda(fila, columna)
        if isinstance(candidata, clase_presa) and candidata.vivo:
            d = distancia(organismo.posicion, candidata.posicion)
            if mejor is None or d < mejor_distancia:
                mejor = candidata
                mejor_distancia = d
    return mejor


def ranking_por_energia(organismos):
    # TODO (Fase 4, opcional): devolver la lista ordenada de mayor a menor
    # energía y mostrarla al final de cada turno.
    raise NotImplementedError("Fase 4: ranking_por_energia()")
