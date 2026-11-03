"""
Música 8-bit generada por código con numpy (extra, no evaluado).

Idea: la melodía es una tupla de (frecuencia_hz, duracion_segundos);
cada nota se convierte en una onda cuadrada con numpy y se concatenan
en un solo arreglo que pygame.sndarray puede reproducir.
"""

FRECUENCIA_MUESTREO = 22050

MELODIA = (
    (440.0, 0.25),   # La4
    (523.3, 0.25),   # Do5
    (659.3, 0.50),   # Mi5
)


def onda_cuadrada(frecuencia, duracion, volumen=0.3):
    # TODO: t = np.linspace(...); np.sign(np.sin(2 * np.pi * frecuencia * t))
    raise NotImplementedError("Extra: onda_cuadrada()")
