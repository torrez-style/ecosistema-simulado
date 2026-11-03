"""
Punto de entrada del proyecto.

Por ahora corre la prueba de consola de la Fase 1: crear organismos y
llamar a sus métodos por separado, sin grid ni interfaz.
"""

from ecosistema import config
from ecosistema.mundo import Mundo
from ecosistema.organismos import Organismo, Planta, Herbivoro, Carnivoro


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


def prueba_mundo_vacio():
    print("\n=== Fase 2 (inicio): grid vacío ===\n")
    mundo = Mundo(config.FILAS, config.COLUMNAS)
    print(mundo)


if __name__ == "__main__":
    prueba_fase1()
    prueba_mundo_vacio()
