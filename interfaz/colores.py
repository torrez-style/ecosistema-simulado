"""
Paleta rojo-negro de la interfaz (estilo Maze Run, pero en bandas 8 bits).
Los colores de los personajes están en sprites.py.
"""


def hex_a_rgb(codigo):
    """'#B40000' -> (180, 0, 0)"""
    codigo = codigo.lstrip("#")
    return tuple(int(codigo[i:i + 2], 16) for i in (0, 2, 4))


# Fondo en bandas, de arriba hacia abajo
BANDAS_FONDO = tuple(hex_a_rgb(c) for c in
                     ("#3C0A0A", "#280000", "#1E0000", "#140000", "#0A0000", "#000000"))

SOMBRA = hex_a_rgb("#280000")
ROJO_BASE = hex_a_rgb("#B40000")
ROJO_BRILLO = hex_a_rgb("#FF3232")
TEXTO = hex_a_rgb("#FFC8C8")
TEXTO_TENUE = hex_a_rgb("#B08080")
AMARILLO = hex_a_rgb("#F2C94C")

SUELO = hex_a_rgb("#1A1214")
SUELO_CLARO = hex_a_rgb("#211719")
