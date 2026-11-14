"""Entrega la música compás por compás (una clase por archivo)."""

import numpy as np

from interfaz.musica import componer_compas, sumar_en


class Compositor:
    """
    Entrega los compases uno tras otro, sumando la cola del anterior al
    inicio del siguiente para que la música no se corte entre compases.
    """

    def __init__(self, azar):
        self._azar = azar
        self._compas = 0
        self._cola = np.zeros(0)

    def reiniciar(self):
        self._compas = 0
        self._cola = np.zeros(0)

    def siguiente(self, estado):
        onda, largo = componer_compas(estado, self._compas, self._azar)
        sumar_en(onda, self._cola, 0)
        self._cola = onda[largo:].copy()
        self._compas += 1
        return onda[:largo]

    def final(self, onda):
        """Termina con `onda` (ej. la frase de extinción), fundida con la última cola."""
        resultado = np.zeros(max(len(onda), len(self._cola)))
        sumar_en(resultado, onda, 0)
        sumar_en(resultado, self._cola, 0)
        self._cola = np.zeros(0)
        return resultado
