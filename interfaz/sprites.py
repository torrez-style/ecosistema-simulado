"""Guarda los sprites ya escalados (una clase por archivo, como en el curso)."""

import pygame

from interfaz.pixel_art import DIBUJOS, superficie_desde_dibujo


class Sprites:
    """Guarda cada sprite ya escalado para no volver a escalarlo en cada cuadro."""

    def __init__(self):
        self._originales = {}
        self._escalados = {}

    def _original(self, especie, etapa):
        clave = (especie, etapa)
        if clave not in self._originales:
            dibujos = DIBUJOS[especie]
            dibujo = dibujos.get(etapa, dibujos["adulto"])
            self._originales[clave] = superficie_desde_dibujo(dibujo)
        return self._originales[clave]

    def obtener(self, especie, etapa, tamano):
        """Sprite de la especie y etapa, escalado a tamano x tamano píxeles."""
        clave = (especie, etapa, tamano)
        if clave not in self._escalados:
            # transform.scale usa vecino más cercano: los píxeles quedan nítidos
            self._escalados[clave] = pygame.transform.scale(
                self._original(especie, etapa), (tamano, tamano))
        return self._escalados[clave]

    def limpiar(self):
        """Se llama cuando cambia el tamaño de celda."""
        self._escalados.clear()
