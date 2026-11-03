"""
Música 8-bit generada por código con numpy (capa opcional, no da puntos).

- Cada evento es una tupla (nota_midi, duracion_segundos, volumen).
- Una canción es una matriz pasos × canales.
- Ondas: cuadrada, triangular y ruido, convertidas a uint8.
- Melodías propias (nada de Pokémon ni Mega Man).
- Idea reactiva: plantas = bajo, herbívoros = melodía, carnívoros = percusión.
"""

FRECUENCIA_MUESTREO = 22050


def frecuencia(nota_midi):
    """f = 440 · 2^((n − 69) / 12); la nota 69 es La4 = 440 Hz."""
    return 440.0 * 2 ** ((nota_midi - 69) / 12)


# Melodía de prueba (cámbienla por una propia)
MELODIA = (
    (69, 0.25, 0.3),   # La4
    (72, 0.25, 0.3),   # Do5
    (76, 0.50, 0.3),   # Mi5
)


def onda_cuadrada(nota_midi, duracion, volumen):
    # TODO: t = np.arange(int(FRECUENCIA_MUESTREO * duracion)) / FRECUENCIA_MUESTREO
    #       onda = np.sign(np.sin(2 * np.pi * frecuencia(nota_midi) * t))
    #       pasar de [-1, 1] a uint8 [0, 255] aplicando el volumen
    raise NotImplementedError("Extra: onda_cuadrada()")
