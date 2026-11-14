"""
Fase 4 — Búsqueda y ordenamiento integrados a la simulación.

- presa_mas_cercana(): búsqueda lineal del mínimo. La usan Herbivoro.actuar()
  y Carnivoro.actuar() para decidir a quién comer (FAQ P11).
- ranking_por_energia(): algoritmo de la burbuja. El top 3 se muestra al
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
    Algoritmo de la burbuja (versión 2, con la bandera hubo_intercambio),
    de mayor a menor energía, igual al visto en clase (Semana 11).

    - Ordena una COPIA (organismos.copy()): como sorted(), no cambia la lista
      original. Ojo: copia = organismos NO sería una copia, solo otra etiqueta.
    - Compara el atributo energia de dos vecinos; si el de la izquierda tiene
      MENOS, los intercambia. El intercambio mueve el organismo completo.
    - Si en una pasada no hubo intercambios, la lista ya está ordenada y se detiene.
    - Es estable: con la misma energía se conserva el orden original.

    cantidad: si se indica, devuelve solo los primeros (ej. el top 3).
    Se muestra al final de cada turno en la ventana y en la consola.
    """
    ordenados = organismos.copy()
    n = len(ordenados)
    for i in range(n - 1):                      # cada vuelta es una pasada
        hubo_intercambio = False
        for j in range(n - 1 - i):              # los últimos i ya están en su lugar
            if ordenados[j].energia < ordenados[j + 1].energia:
                ordenados[j], ordenados[j + 1] = ordenados[j + 1], ordenados[j]
                hubo_intercambio = True
        if not hubo_intercambio:
            break
    if cantidad is not None:
        return ordenados[:cantidad]
    return ordenados
