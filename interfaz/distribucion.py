"""
Dónde va cada cosa en la pantalla, para cualquier tamaño o proporción.

Idea tomada de Maze Run (_configurar_tablero): el tamaño de celda es el
MENOR entre lo que cabe a lo ancho y lo que cabe a lo alto, así el grid
siempre se ve completo, y luego se centra. Diferencia: aquí no hay un
tope de 48 px, para aprovechar las pantallas grandes.
"""

from dataclasses import dataclass

import pygame

PROPORCION_ANCHA = 1.15   # ancho/alto a partir del cual el panel va al costado
CELDA_MINIMA = 4          # píxeles


@dataclass(frozen=True)
class Distribucion:
    panel: pygame.Rect       # zona de textos y botones
    grid: pygame.Rect        # zona exacta donde se dibuja la cuadrícula
    celda: int               # lado de cada celda en píxeles
    panel_al_costado: bool   # True: panel a la derecha; False: panel arriba


def calcular_distribucion(ancho, alto, filas, columnas):
    """Reparte la pantalla entre el panel y el grid (función pura, sin dibujar)."""
    panel_al_costado = ancho >= alto * PROPORCION_ANCHA
    if panel_al_costado:
        ancho_panel = min(max(240, ancho // 4), ancho // 2)
        panel = pygame.Rect(ancho - ancho_panel, 0, ancho_panel, alto)
        zona = pygame.Rect(0, 0, ancho - ancho_panel, alto)
    else:
        alto_panel = min(max(190, alto // 4), alto // 2)
        panel = pygame.Rect(0, 0, ancho, alto_panel)
        zona = pygame.Rect(0, alto_panel, ancho, alto - alto_panel)

    margen = max(8, min(zona.w, zona.h) // 30)
    zona = zona.inflate(-2 * margen, -2 * margen)

    celda = max(CELDA_MINIMA, min(zona.w // columnas, zona.h // filas))
    grid = pygame.Rect(0, 0, celda * columnas, celda * filas)
    grid.center = zona.center
    return Distribucion(panel, grid, celda, panel_al_costado)
