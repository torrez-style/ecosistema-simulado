"""
Dónde va cada cosa en la pantalla, para cualquier tamaño o proporción.

Idea tomada de Maze Run (_configurar_tablero): el tamaño de celda es el
MENOR entre lo que cabe a lo ancho y lo que cabe a lo alto, así el grid
siempre se ve completo, y luego se centra. Diferencia: aquí no hay un
tope de 48 px, para aprovechar las pantallas grandes.
"""

import pygame

PROPORCION_ANCHA = 1.15   # ancho/alto a partir del cual el panel va al costado
CELDA_MINIMA = 4          # píxeles


class Distribucion:
    """Reparte una pantalla de ancho x alto entre el panel y el grid."""

    def __init__(self, ancho, alto, filas, columnas):
        if ancho <= 0 or alto <= 0:
            raise ValueError("La pantalla debe tener ancho y alto positivos.")
        self._panel_al_costado = ancho >= alto * PROPORCION_ANCHA
        if self._panel_al_costado:
            ancho_panel = min(max(240, ancho // 4), ancho // 2)
            self._panel = pygame.Rect(ancho - ancho_panel, 0, ancho_panel, alto)
            zona = pygame.Rect(0, 0, ancho - ancho_panel, alto)
        else:
            alto_panel = min(max(190, alto // 4), alto // 2)
            self._panel = pygame.Rect(0, 0, ancho, alto_panel)
            zona = pygame.Rect(0, alto_panel, ancho, alto - alto_panel)

        margen = max(8, min(zona.w, zona.h) // 30)
        zona = zona.inflate(-2 * margen, -2 * margen)

        self._celda = max(CELDA_MINIMA, min(zona.w // columnas, zona.h // filas))
        self._grid = pygame.Rect(0, 0, self._celda * columnas, self._celda * filas)
        self._grid.center = zona.center

    @property
    def panel(self):
        """Zona de textos y botones."""
        return self._panel.copy()

    @property
    def grid(self):
        """Zona exacta donde se dibuja la cuadrícula."""
        return self._grid.copy()

    @property
    def celda(self):
        """Lado de cada celda, en píxeles."""
        return self._celda

    @property
    def panel_al_costado(self):
        """True: panel a la derecha (pantalla ancha); False: panel arriba."""
        return self._panel_al_costado
