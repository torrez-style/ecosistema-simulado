"""
¿Cuánto dura el ecosistema con los parámetros actuales de config.py?

Corre muchas simulaciones con semillas distintas y cuenta cuántos turnos
pasan hasta que alguna especie se extingue. Sirve para justificar los
ajustes a la tabla de referencia (sección 4 de la guía).

Uso, desde la carpeta del proyecto:
    python -m herramientas.probar_balance            # 100 semillas
    python -m herramientas.probar_balance 30         # 30 semillas
"""

import sys

from ecosistema import config
from ecosistema.partida import crear_mundo, especies_extintas

TOPE_TURNOS = 150


def duracion(semilla):
    """Turnos hasta la primera extinción (o TOPE_TURNOS) y qué especie cayó."""
    mundo = crear_mundo(semilla)
    for _ in range(TOPE_TURNOS):
        mundo.ejecutar_turno()
        extintas = especies_extintas(mundo)
        if extintas:
            return mundo.turno, "+".join(extintas)
    return TOPE_TURNOS, None


def main(semillas):
    duraciones = []
    extinciones = {}
    for semilla in range(semillas):
        turnos, especie = duracion(semilla)
        duraciones.append(turnos)
        if especie is not None:
            extinciones[especie] = extinciones.get(especie, 0) + 1

    duraciones.sort()
    n = len(duraciones)
    print(f"Grid {config.FILAS}x{config.COLUMNAS}, población inicial {config.POBLACION_INICIAL}")
    print(f"Semillas probadas: {n}")
    print(f"Mediana de duración: {duraciones[n // 2]} turnos")
    print(f"25 % de las corridas dura menos de: {duraciones[n // 4]} turnos")
    for limite in (30, 50, 100):
        porcentaje = sum(d >= limite for d in duraciones) / n
        print(f"Llegan a {limite} turnos: {porcentaje:.0%}")
    print(f"Primera especie en extinguirse: {extinciones}")


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 100)
