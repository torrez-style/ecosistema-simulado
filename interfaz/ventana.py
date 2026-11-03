"""
Fase 7 — Interfaz gráfica con pygame.

Controles mínimos que pide la guía: iniciar, pausar y ajustar la velocidad.
"""

# Paleta inicial (negros y rojos); ajústenla a su estilo pixel art.
COLOR_FONDO = (10, 10, 12)
COLOR_CUADRICULA = (40, 12, 16)
COLOR_PLANTA = (60, 170, 80)
COLOR_HERBIVORO = (220, 190, 90)
COLOR_CARNIVORO = (200, 30, 40)

TAMANO_CELDA = 48  # píxeles


class Ventana:

    def __init__(self, mundo):
        self._mundo = mundo
        self._pausado = True
        self._turnos_por_segundo = 2

    def dibujar(self, pantalla):
        # TODO: recorrer el grid con mundo.celda(f, c) y pintar cada organismo.
        raise NotImplementedError("Fase 7: Ventana.dibujar()")

    def ejecutar(self):
        # TODO: bucle de pygame
        #   - ESPACIO: iniciar / pausar
        #   - + / -: más o menos turnos por segundo
        #   - cada cierto tiempo, si no está pausado: mundo.ejecutar_turno()
        raise NotImplementedError("Fase 7: Ventana.ejecutar()")
