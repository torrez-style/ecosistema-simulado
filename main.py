"""
Punto de entrada del proyecto.

Por ahora corre la simulación por consola (Fase 3). Las pruebas de las
Fases 1 y 2 siguen aquí: se pueden llamar desde el bloque de abajo.
"""

import sys

from ecosistema import config
from ecosistema.mundo import Mundo
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


def prueba_fase3(turnos=10, semilla=42):
    print(f"=== Fase 3: simulación por consola ({turnos} turnos, semilla {semilla}) ===\n")
    mundo = crear_mundo(semilla)
    print("Turno 0")
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


if __name__ == "__main__":
    # Uso: python main.py [turnos] [semilla]
    turnos = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    semilla = int(sys.argv[2]) if len(sys.argv) > 2 else 42
    prueba_fase3(turnos, semilla)
