"""Texto pixelado para la interfaz (una clase por archivo, como en el curso)."""

import pygame


class Texto:
    """
    Texto pixelado: se dibuja SIN suavizado (idea de Maze Run), así los bordes
    quedan en escalón como en los juegos de 8 bits. El tamaño de letra se elige
    según el espacio disponible.
    """

    def __init__(self):
        self._fuentes = {}
        self._cache = {}

    def _fuente(self, tamano):
        if tamano not in self._fuentes:
            self._fuentes[tamano] = pygame.font.Font(None, tamano)
        return self._fuentes[tamano]

    def medir(self, texto, tamano):
        """(ancho, alto) en píxeles, sin dibujar nada."""
        return self._fuente(tamano).size(texto)

    def render(self, texto, tamano, color):
        clave = (texto, tamano, color)
        if clave not in self._cache:
            if len(self._cache) > 500:
                self._cache.clear()
            self._cache[clave] = self._fuente(tamano).render(texto, False, color)
        return self._cache[clave]
