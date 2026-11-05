"""
Música 8 bits generada por código con numpy: tenue y reactiva al ecosistema.

Aquí solo se GENERAN los sonidos (arreglos de numpy con valores entre -1 y 1);
sonido.py se encarga de reproducirlos con pygame.

Cómo suena "a consola de 8 bits" sin copiar ninguna canción:
    - onda triangular  -> colchón y bajo suaves (como los bajos del NES)
    - onda cuadrada    -> melodía; al 25 % suena fina, como el canal "pulse"
    - ruido            -> percusión
    - escalas pentatónicas: no tienen notas que choquen, ideales para ambiente

La música se compone compás por compás según lo que pasa en el ecosistema:
    plantas    -> colchón (más plantas, más lleno)
    herbívoros -> melodía (más guatusas, más notas)
    carnívoros -> percusión suave (más tigrillos, más toques)
    si alguna especie baja de la mitad de su población inicial, la escala
    pasa de pentatónica mayor (calma) a menor (tensión) y el tempo sube un poco.
    En pausa solo suena el colchón: el bosque "respira".
"""

from dataclasses import dataclass

import numpy as np

FRECUENCIA_MUESTREO = 22050

# Todo se mezcla bajito: es un ambiente, no una canción de acción
VOLUMEN_COLCHON = 0.12
VOLUMEN_MELODIA = 0.07
VOLUMEN_PERCUSION = 0.035
VOLUMEN_EFECTOS = 0.06

ESCALAS = {
    "calma": (0, 2, 4, 7, 9),       # pentatónica mayor
    "tension": (0, 3, 5, 7, 10),    # pentatónica menor
}
# Raíz de cada compás (notas MIDI); se repiten en ciclos de 4
PROGRESIONES = {
    "calma": (48, 45, 41, 43),      # Do, La, Fa, Sol
    "tension": (48, 44, 41, 43),    # Do, La bemol, Fa, Sol
}
TEMPOS = {"calma": 72, "tension": 84}   # pulsos por minuto
UMBRAL_TENSION = 0.5                    # fracción de la población inicial
CORCHEAS_POR_COMPAS = 8
COLA = 1.0      # segundos que cada compás se traslapa con el siguiente


@dataclass(frozen=True)
class EstadoMusical:
    """Lo que la música necesita saber del ecosistema."""
    plantas: float       # población / población inicial
    herbivoros: float
    carnivoros: float
    pausado: bool


def estado_musical(poblacion, poblacion_inicial, pausado):
    """Convierte {"Planta": 30, ...} en proporciones respecto al inicio."""
    def proporcion(especie):
        inicial = poblacion_inicial.get(especie, 0)
        return poblacion.get(especie, 0) / inicial if inicial else 0.0
    return EstadoMusical(proporcion("Planta"), proporcion("Herbivoro"),
                         proporcion("Carnivoro"), pausado)


def animo(estado):
    """'tension' si alguna especie está por debajo de la mitad de su inicio."""
    menor = min(estado.plantas, estado.herbivoros, estado.carnivoros)
    return "tension" if menor < UMBRAL_TENSION else "calma"


# ----------------------------------------------------------------------
# Instrumentos
# ----------------------------------------------------------------------
def frecuencia(nota_midi):
    """f = 440 · 2^((n − 69) / 12); la nota 69 es La4 = 440 Hz."""
    return 440.0 * 2 ** ((nota_midi - 69) / 12)


def _muestras(duracion):
    return max(1, int(FRECUENCIA_MUESTREO * duracion))


def _fase(nota_midi, duracion):
    """Posición dentro de cada ciclo de la onda, entre 0 y 1."""
    t = np.arange(_muestras(duracion)) / FRECUENCIA_MUESTREO
    return (t * frecuencia(nota_midi)) % 1.0


def suavizar(onda, ancho):
    """Media móvil: quita lo áspero del sonido (un filtro pasa bajos sencillo)."""
    if ancho <= 1:
        return onda
    return np.convolve(onda, np.ones(ancho) / ancho, mode="same")


def onda_triangular(nota_midi, duracion):
    return 4 * np.abs(_fase(nota_midi, duracion) - 0.5) - 1


def onda_cuadrada(nota_midi, duracion, ciclo=0.25):
    onda = np.where(_fase(nota_midi, duracion) < ciclo, 1.0, -1.0)
    return suavizar(onda, 5)


def ruido(duracion, azar):
    return suavizar(azar.uniform(-1, 1, _muestras(duracion)), 10)


def deslizar(nota_inicio, nota_fin, duracion):
    """Onda triangular cuya nota baja (o sube) poco a poco: un 'glissando'."""
    n = _muestras(duracion)
    notas = np.linspace(nota_inicio, nota_fin, n)
    frecuencias = 440.0 * 2 ** ((notas - 69) / 12)
    fase = np.cumsum(frecuencias) / FRECUENCIA_MUESTREO % 1.0
    return 4 * np.abs(fase - 0.5) - 1


def envolvente(n, ataque, liberacion, decaimiento=None):
    """
    Da forma al volumen de una nota para que no 'golpee' ni corte en seco:
    sube en `ataque` segundos, baja en los últimos `liberacion` segundos y,
    si se indica, se apaga poco a poco con `decaimiento` (como una cuerda).
    """
    t = np.arange(n) / FRECUENCIA_MUESTREO
    forma = np.ones(n)
    if ataque > 0:
        forma = np.minimum(forma, t / ataque)
    if liberacion > 0:
        forma = np.minimum(forma, (t[-1] - t) / liberacion)
    if decaimiento:
        forma = forma * np.exp(-t / decaimiento)
    return np.clip(forma, 0, 1)


def nota(onda, volumen, ataque=0.01, liberacion=0.05, decaimiento=None):
    return onda * envolvente(len(onda), ataque, liberacion, decaimiento) * volumen


def _sumar(mezcla, sonido, inicio):
    """Suma `sonido` dentro de `mezcla` a partir de la muestra `inicio` (recorta lo que sobra)."""
    fin = min(len(mezcla), inicio + len(sonido))
    if inicio < fin:
        mezcla[inicio:fin] += sonido[:fin - inicio]


def secuencia(*sonidos):
    return np.concatenate(sonidos)


# ----------------------------------------------------------------------
# Composición
# ----------------------------------------------------------------------
def componer_compas(estado, numero_compas, azar):
    """
    Un compás de 4 tiempos que refleja el estado actual del ecosistema.
    Devuelve (onda, largo): la onda dura un poco más que el compás (COLA
    segundos extra) para fundirse con el siguiente; `largo` es el compás exacto.
    """
    modo = animo(estado)
    duracion = 4 * 60 / TEMPOS[modo]
    largo = _muestras(duracion)
    mezcla = np.zeros(largo + _muestras(COLA))
    raiz = PROGRESIONES[modo][numero_compas % len(PROGRESIONES[modo])]

    # Colchón: las plantas. Siempre suena, aun en pausa. Entra despacio y se
    # apaga durante la cola, mientras entra el colchón del compás siguiente.
    volumen = VOLUMEN_COLCHON * (0.5 + 0.5 * min(1.0, estado.plantas))
    sostenido = duracion + COLA * 0.9
    _sumar(mezcla, nota(onda_triangular(raiz, sostenido), volumen,
                        ataque=COLA * 0.9, liberacion=COLA * 0.9), 0)
    if estado.plantas >= 1:   # con muchas plantas se suma la quinta: más lleno
        _sumar(mezcla, nota(onda_triangular(raiz + 7, sostenido), volumen * 0.5,
                            ataque=COLA, liberacion=COLA * 0.9), 0)

    if estado.pausado:
        return mezcla, largo

    corchea = duracion / CORCHEAS_POR_COMPAS

    # Melodía: las guatusas. Pocas guatusas, pocas notas.
    cantidad = int(np.clip(round(estado.herbivoros * 3), 0, 6))
    if cantidad:
        escala = ESCALAS[modo]
        notas = [72 + grado for grado in escala] + [84 + grado for grado in escala]
        indice = int(azar.integers(len(escala)))
        for posicion in sorted(azar.choice(CORCHEAS_POR_COMPAS, cantidad, replace=False)):
            indice = int(np.clip(indice + azar.integers(-2, 3), 0, len(notas) - 1))
            sonido = nota(onda_cuadrada(notas[indice], corchea * 1.8), VOLUMEN_MELODIA,
                          ataque=0.01, liberacion=0.12, decaimiento=0.35)
            _sumar(mezcla, sonido, int(posicion * corchea * FRECUENCIA_MUESTREO))

    # Percusión: los tigrillos. Toques muy suaves en los tiempos del compás.
    golpes = int(np.clip(round(estado.carnivoros * 2), 0, 4))
    if golpes:
        for tiempo in sorted(azar.choice(4, golpes, replace=False)):
            sonido = nota(ruido(0.08, azar), VOLUMEN_PERCUSION,
                          ataque=0.002, liberacion=0.02, decaimiento=0.025)
            _sumar(mezcla, sonido, int(tiempo * 2 * corchea * FRECUENCIA_MUESTREO))
    return mezcla, largo


class Compositor:
    """
    Entrega los compases uno tras otro, sumando la cola del anterior al
    inicio del siguiente para que la música no se corte entre compases.
    """

    def __init__(self, azar):
        self._azar = azar
        self._compas = 0
        self._cola = np.zeros(0)

    def reiniciar(self):
        self._compas = 0
        self._cola = np.zeros(0)

    def siguiente(self, estado):
        onda, largo = componer_compas(estado, self._compas, self._azar)
        _sumar(onda, self._cola, 0)
        self._cola = onda[largo:].copy()
        self._compas += 1
        return onda[:largo]

    def final(self, onda):
        """Termina con `onda` (ej. la frase de extinción), fundida con la última cola."""
        resultado = np.zeros(max(len(onda), len(self._cola)))
        _sumar(resultado, onda, 0)
        _sumar(resultado, self._cola, 0)
        self._cola = np.zeros(0)
        return resultado


def frase_extincion():
    """Frase lenta que baja, en menor: suena una sola vez al terminar la partida."""
    notas = (67, 63, 60, 55)
    return secuencia(*(nota(onda_triangular(n, 1.1), VOLUMEN_COLCHON * 1.2,
                            ataque=0.05, liberacion=0.6) for n in notas),
                     np.zeros(_muestras(1.5)))


# ----------------------------------------------------------------------
# Efectos de sonido (cortos y suaves)
# ----------------------------------------------------------------------
def _arpegio(notas, duracion_nota, onda, volumen):
    return secuencia(*(nota(onda(n, duracion_nota), volumen, ataque=0.005,
                            liberacion=duracion_nota * 0.6) for n in notas))


def efecto_florecer():
    return _arpegio((88, 91, 96), 0.06, onda_triangular, VOLUMEN_EFECTOS * 0.7)


def efecto_nacimiento():
    return _arpegio((72, 76, 79), 0.06, onda_cuadrada, VOLUMEN_EFECTOS * 0.8)


def efecto_comida():
    tono = _arpegio((67, 62), 0.05, onda_cuadrada, VOLUMEN_EFECTOS * 0.8)
    golpe = nota(ruido(0.04, np.random.default_rng(0)), VOLUMEN_EFECTOS * 0.4,
                 ataque=0.002, liberacion=0.02)
    _sumar(tono, golpe, 0)
    return tono


def efecto_muerte():
    return nota(deslizar(69, 57, 0.35), VOLUMEN_EFECTOS * 0.8, ataque=0.01, liberacion=0.2)


def efecto_pausa():
    return _arpegio((79, 72), 0.06, onda_triangular, VOLUMEN_EFECTOS)


def efecto_reanudar():
    return _arpegio((72, 79), 0.06, onda_triangular, VOLUMEN_EFECTOS)


def efecto_guardar():
    return _arpegio((72, 76, 84), 0.07, onda_triangular, VOLUMEN_EFECTOS)


def efecto_cargar():
    return _arpegio((84, 76, 72, 79), 0.06, onda_triangular, VOLUMEN_EFECTOS)


def efecto_error():
    return nota(onda_cuadrada(45, 0.18, ciclo=0.5), VOLUMEN_EFECTOS * 0.7, liberacion=0.08)


EFECTOS = {
    "florecer": efecto_florecer,
    "nacimiento": efecto_nacimiento,
    "comida": efecto_comida,
    "muerte": efecto_muerte,
    "pausa": efecto_pausa,
    "reanudar": efecto_reanudar,
    "guardar": efecto_guardar,
    "cargar": efecto_cargar,
    "nueva": efecto_reanudar,
    "error": efecto_error,
}
