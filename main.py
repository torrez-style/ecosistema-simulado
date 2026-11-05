"""
Punto de entrada del proyecto: Panta Rhei — Ecosistema simulado.

Uso:
    python main.py                          abre la ventana (partida nueva)
    python main.py --semilla 42             ventana con una semilla fija
    python main.py --cargar                 ventana con la partida guardada

    python main.py --consola                10 turnos por consola
    python main.py --consola 30 --semilla 7
    python main.py --consola 10 --guardar   ... y guarda la partida al final
    python main.py --consola 10 --cargar    sigue 10 turnos desde la partida guardada
"""

import argparse
import sys

from ecosistema import persistencia
from ecosistema.organismos import ESPECIES
from ecosistema.partida import crear_mundo, especies_extintas, semilla_aleatoria
from ecosistema.recursividad import colonias


def mostrar_poblacion(mundo):
    poblacion = mundo.poblacion()
    partes = [f"{nombre}: {poblacion.get(nombre, 0)}" for nombre in ESPECIES]
    print("Población -> " + " | ".join(partes))

    # Fase 5: colonias de plantas contadas con recursión
    tamanos = colonias(mundo)
    if tamanos:
        print(f"Colonias de plantas: {len(tamanos)} | la más grande: {tamanos[0]} plantas")


def simular_en_consola(mundo, turnos):
    """Corre la simulación por consola mostrando cada turno."""
    print(f"Turno {mundo.turno}")
    print(mundo)
    mostrar_poblacion(mundo)

    for _ in range(turnos):
        mundo.ejecutar_turno()
        print(f"\n--- Turno {mundo.turno} ---")
        for suceso in mundo.bitacora:
            print(f"  • {suceso}")
        print()
        print(mundo)
        mostrar_poblacion(mundo)

        extintas = especies_extintas(mundo)
        if extintas:
            print(f"\nExtinción de: {', '.join(extintas)}. "
                  f"El ecosistema sobrevivió {mundo.turno} turnos.")
            break


def leer_argumentos():
    lector = argparse.ArgumentParser(description="Panta Rhei — Ecosistema simulado")
    lector.add_argument("--consola", action="store_true",
                        help="correr por consola en vez de abrir la ventana")
    lector.add_argument("turnos", type=int, nargs="?", default=10,
                        help="turnos a simular en modo consola (por defecto 10)")
    lector.add_argument("--semilla", type=int, default=None,
                        help="semilla del azar para una partida nueva (por defecto, al azar)")
    lector.add_argument("--guardar", nargs="?", const=persistencia.RUTA_POR_DEFECTO,
                        metavar="RUTA", help="consola: guardar la partida al terminar")
    lector.add_argument("--cargar", nargs="?", const=persistencia.RUTA_POR_DEFECTO,
                        metavar="RUTA", help="continuar una partida guardada")
    return lector.parse_args()


def preparar_mundo(argumentos):
    if argumentos.cargar:
        try:
            mundo = persistencia.cargar(argumentos.cargar)
        except (FileNotFoundError, ValueError) as error:
            print(f"No se pudo cargar la partida: {error}")
            sys.exit(1)
        print(f"Partida cargada de {argumentos.cargar} (turno {mundo.turno})")
        return mundo
    semilla = argumentos.semilla if argumentos.semilla is not None else semilla_aleatoria()
    print(f"Partida nueva (semilla {semilla})")
    return crear_mundo(semilla)


def main():
    argumentos = leer_argumentos()
    mundo = preparar_mundo(argumentos)

    if argumentos.consola:
        print()
        simular_en_consola(mundo, argumentos.turnos)
        if argumentos.guardar:
            persistencia.guardar(mundo, argumentos.guardar)
            print(f"\nPartida guardada en {argumentos.guardar} (turno {mundo.turno})")
    else:
        from interfaz.ventana import Ventana   # pygame solo se carga si hay ventana
        Ventana(mundo).ejecutar()


if __name__ == "__main__":
    main()
