"""Botón clicable del panel (una clase por archivo, como en el curso)."""

import pygame


class Boton:
    """Botón clicable. La etiqueta puede ser un texto o una función que lo devuelve."""

    def __init__(self, etiqueta, accion):
        self._etiqueta = etiqueta
        self._accion = accion
        self._rect = pygame.Rect(0, 0, 0, 0)

    @property
    def etiqueta(self):
        return self._etiqueta() if callable(self._etiqueta) else self._etiqueta

    @property
    def rect(self):
        return self._rect.copy()

    def ubicar(self, rect):
        self._rect = pygame.Rect(rect)

    def contiene(self, punto):
        return self._rect.collidepoint(punto)

    def pulsar(self):
        self._accion()
