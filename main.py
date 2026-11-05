"""
Punto de entrada del proyecto.

Por ahora corre la simulación por consola. Las pruebas de las Fases 1 y 2
siguen aquí como funciones (prueba_fase1, prueba_fase2).

Uso:
    python main.py                        10 turnos, semilla 42
    python main.py 30 7                   30 turnos, semilla 7
    python main.py 10 --guardar           ... y guarda la partida al final
    python main.py 10 --cargar            sigue 10 turnos desde la partida guardada
"""

import argparse
import sys

from ecosistema import config, persistencia
from ecosistema.mundo import Mundo
from ecosistema.recursividad import colonias
from ecosistema.organismos import Organismo, Planta, Herbivoro, Carnivoro, ESPECIES


def prueba_fase1():
    print("=== Fase 1: núcleo de clases ===\n")

    # Organismo es abstracta: no se puede instanciar
    try:
        Organismo(0, 0, 10)
    except TypeError as error:
        print(f"Organismo(...) no se puede crear: {error}\n")

    planta = Planta(2, 3)
    herbivoro = Herbivoro(4, 5)
    carnivoro = Carnivoro(7, 1)
    for organismo in (planta, herbivoro, carnivoro):
        print(organismo)

    print("\nLa planta hace fotosíntesis 3 turnos:")
    for _ in range(3):
        planta.actuar(None)
        print(f"  energía = {planta.energia}")

    print("\nEl herbívoro paga su metabolismo hasta morir:")
    while herbivoro.vivo:
        herbivoro.pagar_metabolismo()
    print(f"  {herbivoro}")

    print(f"\nUmbral de reproducción del carnívoro: {carnivoro.umbral_reproduccion}")


def prueba_fase2():
    print("\n=== Fase 2: el mundo (matriz) ===\n")
    mundo = Mundo(config.FILAS, config.COLUMNAS, semilla=42)

    # Población inicial: nombre de especie (config) -> clase (ESPECIES)
    poblacion = {ESPECIES[nombre]: cantidad
                 for nombre, cantidad in config.POBLACION_INICIAL.items()}
    mundo.poblar_aleatorio(poblacion)
    print(mundo)
    print(f"\nOrganismos colocados: {len(mundo.organismos)}")

    # Colisiones y bordes controlados
    ocupada = mundo.organismos[0].posicion
    for fila, columna in (ocupada, (10, 3), (-1, 0)):
        try:
            mundo.colocar(Planta(fila, columna))
            print(f"Se colocó una planta en ({fila}, {columna})")
        except ValueError as error:
            print(f"No se pudo colocar en ({fila}, {columna}): {error}")

    # Mover un herbívoro a una vecina libre
    herbivoro = next(o for o in mundo.organismos if isinstance(o, Herbivoro))
    destino = mundo.elegir(mundo.vecinas_libres(*herbivoro.posicion))
    origen = herbivoro.posicion
    mundo.mover(herbivoro, *destino)
    print(f"\nHerbívoro movido de {origen} a {herbivoro.posicion}")

    # Retirar a un carnívoro: su celda queda libre de inmediato
    carnivoro = next(o for o in mundo.organismos if isinstance(o, Carnivoro))
    mundo.retirar(carnivoro)
    print(f"Carnívoro retirado de {carnivoro.posicion}; "
          f"celda libre: {mundo.celda(*carnivoro.posicion) is None}")
    print(f"\n{mundo}")


def crear_mundo(semilla):
    mundo = Mundo(config.FILAS, config.COLUMNAS, semilla)
    poblacion = {ESPECIES[nombre]: cantidad
                 for nombre, cantidad in config.POBLACION_INICIAL.items()}
    mundo.poblar_aleatorio(poblacion)
    return mundo


def mostrar_poblacion(mundo):
    poblacion = mundo.poblacion()
    partes = [f"{nombre}: {poblacion.get(nombre, 0)}" for nombre in ESPECIES]
    print("Población -> " + " | ".join(partes))

    # Fase 5: colonias de plantas contadas con recursión
    tamanos = colonias(mundo)
    if tamanos:
        print(f"Colonias de plantas: {len(tamanos)} | la más grande: {tamanos[0]} plantas")


def simular(mundo, turnos):
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

        extintas = [nombre for nombre in ESPECIES if mundo.poblacion().get(nombre, 0) == 0]
        if extintas:
            print(f"\nExtinción de: {', '.join(extintas)}. Fin de la simulación.")
            break


def leer_argumentos():
    lector = argparse.ArgumentParser(description="Ecosistema Simulado por consola")
    lector.add_argument("turnos", type=int, nargs="?", default=10,
                        help="cuántos turnos simular (por defecto 10)")
    lector.add_argument("semilla", type=int, nargs="?", default=42,
                        help="semilla del azar para una partida nueva (por defecto 42)")
    lector.add_argument("--guardar", nargs="?", const=persistencia.RUTA_POR_DEFECTO,
                        metavar="RUTA", help="guardar la partida al terminar")
    lector.add_argument("--cargar", nargs="?", const=persistencia.RUTA_POR_DEFECTO,
                        metavar="RUTA", help="continuar una partida guardada")
    return lector.parse_args()


def main():
    argumentos = leer_argumentos()

    if argumentos.cargar:
        try:
            mundo = persistencia.cargar(argumentos.cargar)
        except (FileNotFoundError, ValueError) as error:
            print(f"No se pudo cargar la partida: {error}")
            sys.exit(1)
        print(f"=== Partida cargada de {argumentos.cargar} (turno {mundo.turno}) ===\n")
    else:
        mundo = crear_mundo(argumentos.semilla)
        print(f"=== Partida nueva (semilla {argumentos.semilla}) ===\n")

    simular(mundo, argumentos.turnos)

    if argumentos.guardar:
        persistencia.guardar(mundo, argumentos.guardar)
        print(f"\nPartida guardada en {argumentos.guardar} (turno {mundo.turno})")


if __name__ == "__main__":
    main()
