"""
Personajes en pixel art, dibujados por código (sin imágenes externas).

Cada dibujo es una lista de textos de 16 x 16: cada letra es un píxel y
PALETA dice de qué color es. Un punto "." es transparente.

Escenario: bosque tropical seco de Guanacaste.
    Planta    -> brote, arbusto y corteza amarilla en flor
    Herbívoro -> guatusa
    Carnívoro -> tigrillo
"""

import pygame

from interfaz.colores import hex_a_rgb


# Letra -> color. Los organismos NO usan rojo: se perderían en el fondo.
PALETA = {
    "v": hex_a_rgb("#2F7A3A"),   # verde planta
    "o": hex_a_rgb("#1F5428"),   # verde oscuro (sombra)
    "b": hex_a_rgb("#7FBF5A"),   # verde brote (brillo)
    "f": hex_a_rgb("#F2C94C"),   # flor amarilla
    "a": hex_a_rgb("#C99A2E"),   # flor, sombra
    "t": hex_a_rgb("#6B4E2E"),   # tronco / tallo
    "g": hex_a_rgb("#B5763A"),   # guatusa
    "G": hex_a_rgb("#7E4F24"),   # guatusa, lomo oscuro
    "c": hex_a_rgb("#E6C98A"),   # tigrillo
    "C": hex_a_rgb("#B8975A"),   # tigrillo, sombra
    "m": hex_a_rgb("#1E1A16"),   # manchas y contornos
    "w": hex_a_rgb("#F4EEDC"),   # brillo del ojo
}

BROTE = [
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "....bb....bb....",
    "...bbvb..bvbb...",
    "....bvvbbvvb....",
    ".....bvvvvb.....",
    ".......tt.......",
    ".......tt.......",
    ".......tt.......",
    ".....tttttt.....",
    "................",
]

ARBUSTO = [
    "................",
    "................",
    "................",
    "......bbbb......",
    "....bbvvvvbb....",
    "...bvvvbvvvvb...",
    "..bvvbvvvvbvvo..",
    "..vvvvvvbvvvvo..",
    ".bvbvvvvvvvbvvo.",
    ".vvvvvbvvvvvvvo.",
    ".ovvvvvvvbvvvoo.",
    "..oovvvvvvvvoo..",
    "....ooootoooo...",
    ".......tt.......",
    "......tttt......",
    "................",
]

FLOR = [
    "......ffff......",
    "....ffaffffa....",
    "...fafffffaff...",
    "..fffffaffffaf..",
    "..affffffffffa..",
    ".ffffaffffafffa.",
    ".afffffffffffaa.",
    "..aafffaffffaa..",
    "....aaafffaa....",
    ".......tt.......",
    "......t.tt......",
    ".......tt.......",
    ".......tt.......",
    ".......tt.......",
    ".....tttttt.....",
    "................",
]

GUATUSA = [
    "................",
    "................",
    "................",
    "................",
    "................",
    "..........GG....",
    "......GGGGGgG...",
    "....GGGGGGgggg..",
    "...GGGGGGggwmgg.",
    "..GGggggggggggmm",
    "..Gggggggggggg..",
    "..gggggggggggg..",
    "...ggggggggggg..",
    "....m.m...m.m...",
    "....m.m...m.m...",
    "................",
]

TIGRILLO = [
    "................",
    "................",
    "................",
    "...........mc.cm",
    ".C.........ccccc",
    "C..........cwmcc",
    "C..........ccccm",
    ".C.cccccccccCcc.",
    "..cmccmccmcccC..",
    "..ccccccccmcc...",
    "..cmccmccccmc...",
    "..cCCccCCcCCc...",
    "..cc.cc..cc.cc..",
    "..mm.mm..mm.mm..",
    "................",
    "................",
]

# Especie -> etapa -> dibujo. La interfaz busca aquí sin preguntar el tipo.
DIBUJOS = {
    "Planta": {"cria": BROTE, "adulto": ARBUSTO, "listo": FLOR},
    "Herbivoro": {"cria": GUATUSA, "adulto": GUATUSA},
    "Carnivoro": {"cria": TIGRILLO, "adulto": TIGRILLO},
}

# Las crías se dibujan más pequeñas dentro de su celda.
ESCALA_CRIA = {"Planta": 1.0, "Herbivoro": 0.7, "Carnivoro": 0.7}

EDAD_CRIA = 3   # turnos que un organismo se ve como cría


def etapa_de(organismo):
    """
    Etapa visual del organismo:
        "listo"  -> ya puede reproducirse (la planta florece)
        "cria"   -> tiene menos de EDAD_CRIA turnos
        "adulto" -> en cualquier otro caso
    """
    if organismo.puede_reproducirse():
        return "listo"
    if organismo.edad < EDAD_CRIA:
        return "cria"
    return "adulto"


def superficie_desde_dibujo(dibujo):
    """Convierte un dibujo de texto en una superficie de 1 píxel por letra."""
    alto, ancho = len(dibujo), len(dibujo[0])
    superficie = pygame.Surface((ancho, alto), pygame.SRCALPHA)
    for y, fila in enumerate(dibujo):
        for x, letra in enumerate(fila):
            if letra in PALETA:
                superficie.set_at((x, y), PALETA[letra])
    return superficie


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
