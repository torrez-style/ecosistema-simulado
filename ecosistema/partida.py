"""
Funciones para empezar y revisar una partida. Las usan main.py, la interfaz
gráfica y herramientas/probar_balance.py, para no repetir el mismo código.
"""

import numpy as np

from ecosistema import config
from ecosistema.mundo import Mundo
from ecosistema.organismos import ESPECIES


def semilla_aleatoria():
    """Semilla nueva al azar; se muestra en pantalla para poder repetir la partida."""
    return int(np.random.default_rng().integers(1_000_000))


def crear_mundo(semilla=None):
    """Mundo nuevo con el tamaño y la población inicial de config.py."""
    mundo = Mundo(config.FILAS, config.COLUMNAS, semilla)
    mundo.poblar_aleatorio({ESPECIES[nombre]: cantidad
                            for nombre, cantidad in config.POBLACION_INICIAL.items()})
    return mundo


def especies_extintas(mundo):
    """Nombres de las especies que ya no tienen ningún organismo vivo."""
    poblacion = mundo.poblacion()
    return [nombre for nombre in ESPECIES if poblacion.get(nombre, 0) == 0]
