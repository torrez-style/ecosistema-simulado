"""
Fase 7 — Interfaz gráfica con pygame.

Controles mínimos que pide la guía: iniciar, pausar y ajustar la velocidad.
"""

def hex_a_rgb(codigo):
    """'#B40000' -> (180, 0, 0)"""
    codigo = codigo.lstrip("#")
    return tuple(int(codigo[i:i + 2], 16) for i in (0, 2, 4))


# Paleta rojo-negro en bandas (estilo 8 bits).
# Regla: los organismos NO usan rojo; se distinguen por luminosidad y silueta.
BANDAS_FONDO = tuple(hex_a_rgb(c) for c in
                     ("#3C0A0A", "#280000", "#1E0000", "#140000", "#0A0000", "#000000"))

COLOR_SOMBRA = hex_a_rgb("#280000")
COLOR_ROJO_BASE = hex_a_rgb("#B40000")
COLOR_ROJO_BRILLO = hex_a_rgb("#FF3232")
COLOR_TEXTO = hex_a_rgb("#FFC8C8")

COLOR_SUELO = hex_a_rgb("#1A1214")
COLOR_PLANTA = hex_a_rgb("#2F7A3A")
COLOR_BROTE = hex_a_rgb("#7FBF5A")
COLOR_FLOR = hex_a_rgb("#F2C94C")
COLOR_GUATUSA = hex_a_rgb("#B5763A")      # Herbívoro
COLOR_TIGRILLO = hex_a_rgb("#E6C98A")     # Carnívoro
COLOR_MANCHAS = hex_a_rgb("#1E1A16")

# Primero cuadrados de colores; los sprites pixel art se agregan al final.
COLORES_POR_ESPECIE = {
    "Planta": COLOR_PLANTA,
    "Herbivoro": COLOR_GUATUSA,
    "Carnivoro": COLOR_TIGRILLO,
}

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
