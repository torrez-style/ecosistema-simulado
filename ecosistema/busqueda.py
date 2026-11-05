"""
Fase 4 — Búsqueda y ordenamiento integrados a la simulación.

- presa_mas_cercana(): búsqueda lineal del mínimo. La usan Herbivoro.actuar()
  y Carnivoro.actuar() para decidir a quién comer (FAQ P11).
- ranking_por_energia(): ordenamiento por inserción. El top 3 se muestra al
  final de cada turno en la ventana y en la consola.
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


def ranking_por_energia(organismos, cantidad=None):
    """
    Ordenamiento por inserción, de mayor a menor energía.

    Se recorre la lista y cada organismo se inserta en su lugar dentro de la
    parte que ya está ordenada: se corre hacia la izquierda mientras el de al
    lado tenga MENOS energía. Es estable: con la misma energía se conserva el
    orden original. No modifica la lista que recibe.

    cantidad: si se indica, devuelve solo los primeros (ej. el top 3).
    Se muestra al final de cada turno en la ventana y en la consola.
    """
    ordenados = list(organismos)
    for i in range(1, len(ordenados)):
        actual = ordenados[i]
        j = i - 1
        while j >= 0 and ordenados[j].energia < actual.energia:
            ordenados[j + 1] = ordenados[j]   # correr el de menos energía a la derecha
            j -= 1
        ordenados[j + 1] = actual
    if cantidad is not None:
        return ordenados[:cantidad]
    return ordenados
