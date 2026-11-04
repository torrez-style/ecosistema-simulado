"""
Fase 5 — Recursividad genuina: colonias de plantas (flood-fill).

QUÉ RESUELVE
    Cuántas plantas forman una colonia: un grupo de plantas conectadas entre
    sí, donde dos plantas están conectadas si son vecinas (8 direcciones) o si
    se puede llegar de una a otra saltando de planta en planta.

POR QUÉ RECURSIÓN Y NO UN CICLO
    La definición del problema ya es recursiva:
        tamaño(colonia desde una planta) = 1 + suma de tamaño(colonia desde cada vecina)
    Una colonia puede tener cualquier forma (una línea, una L, un anillo), así
    que no se sabe de antemano cuántos pasos dar ni en qué dirección. Con un
    ciclo habría que manejar a mano una pila de celdas pendientes; la
    recursión usa la pila de llamadas de Python para eso y el código queda
    escrito igual que la definición.

CASOS BASE (devuelven 0 y no siguen)
    1. La celda ya fue visitada: evita contar dos veces la misma planta y
       quedarse rebotando entre dos vecinas para siempre.
    2. En la celda no hay una planta viva: ahí termina la colonia.

PROFUNDIDAD
    Cada llamada recursiva visita una planta distinta, así que la profundidad
    máxima es el número de celdas del grid (20 x 20 = 400), por debajo del
    límite de recursión de Python (1000).
"""

from ecosistema.organismos.planta import Planta


def tamano_colonia(mundo, fila, columna, visitadas=None):
    """Cantidad de plantas vivas conectadas con la celda (fila, columna)."""
    if visitadas is None:
        visitadas = set()

    # Caso base 1: esta celda ya se contó
    if (fila, columna) in visitadas:
        return 0

    # Caso base 2: aquí no hay una planta viva
    organismo = mundo.celda(fila, columna)
    if not (isinstance(organismo, Planta) and organismo.vivo):
        return 0

    # Caso recursivo: esta planta + las colonias que salen de sus vecinas
    visitadas.add((fila, columna))
    tamano = 1
    for vecina_fila, vecina_columna in mundo.vecinas(fila, columna):
        tamano += tamano_colonia(mundo, vecina_fila, vecina_columna, visitadas)
    return tamano


def colonias(mundo):
    """
    Tamaños de todas las colonias de plantas del mundo, de mayor a menor.
    Comparte el conjunto de visitadas entre llamadas para no contar dos veces
    la misma colonia.
    """
    visitadas = set()
    tamanos = []
    for fila in range(mundo.filas):
        for columna in range(mundo.columnas):
            tamano = tamano_colonia(mundo, fila, columna, visitadas)
            if tamano > 0:
                tamanos.append(tamano)
    return sorted(tamanos, reverse=True)
