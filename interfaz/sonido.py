"""
Reproduce con pygame la música y los efectos que genera musica.py.

Si la computadora no tiene sonido (o pygame no pudo abrirlo), todo sigue
funcionando en silencio: el sonido es una capa opcional del juego.
"""

import numpy as np
import pygame

from interfaz import musica

# Suceso del turno -> efecto. Excepción: cuando "nace" una planta, florece.
EFECTO_POR_SUCESO = {"nacimiento": "nacimiento", "comida": "comida", "muerte": "muerte"}
EFECTO_ESPECIAL = {("nacimiento", "Planta"): "florecer"}

# Segundos mínimos entre dos veces el mismo efecto (a alta velocidad no satura)
ESPERA_ENTRE_EFECTOS = {"florecer": 1.6, "nacimiento": 0.8, "comida": 0.5, "muerte": 0.8}
ESPERA_POR_DEFECTO = 0.1


class Sonido:

    def __init__(self, poblacion_inicial):
        self._poblacion_inicial = dict(poblacion_inicial)
        self._silenciado = False
        self._extincion_sonada = False
        self._ultimo_efecto = {}
        # Azar propio: la música NUNCA usa el azar del mundo, así no cambia la simulación
        self._compositor = musica.Compositor(np.random.default_rng())

        configuracion = pygame.mixer.get_init()
        self._disponible = configuracion is not None
        if not self._disponible:
            return
        self._frecuencia, _, self._canales = configuracion
        pygame.mixer.set_reserved(1)                 # el canal 0 es solo para la música
        self._canal_musica = pygame.mixer.Channel(0)
        self._efectos = {nombre: self._a_sonido(crear())
                         for nombre, crear in musica.EFECTOS.items()}

    @property
    def disponible(self):
        return self._disponible

    @property
    def silenciado(self):
        return self._silenciado

    def alternar_silencio(self):
        self._silenciado = not self._silenciado
        if self._disponible and self._silenciado:
            self._canal_musica.stop()

    def reiniciar(self):
        """Para una partida nueva o cargada: la música empieza de nuevo."""
        self._compositor.reiniciar()
        self._extincion_sonada = False
        if self._disponible:
            self._canal_musica.stop()

    # ------------------------------------------------------------------
    # Música de fondo: siempre hay un compás sonando y el siguiente en cola
    # ------------------------------------------------------------------
    def actualizar(self, poblacion, extintas, pausado):
        """Se llama en cada cuadro; solo compone cuando la cola está libre."""
        if not self._disponible or self._silenciado:
            return
        if self._canal_musica.get_queue() is not None:
            return

        if extintas:
            if self._extincion_sonada:
                return
            self._extincion_sonada = True
            self._reproducir_musica(self._compositor.final(musica.frase_extincion()))
            return
        self._extincion_sonada = False

        estado = musica.estado_musical(poblacion, self._poblacion_inicial, pausado)
        self._reproducir_musica(self._compositor.siguiente(estado))

    def _reproducir_musica(self, onda):
        sonido = self._a_sonido(onda)
        if self._canal_musica.get_busy():
            self._canal_musica.queue(sonido)
        else:
            self._canal_musica.play(sonido)

    # ------------------------------------------------------------------
    # Efectos
    # ------------------------------------------------------------------
    def reaccionar(self, sucesos):
        """Al final de cada turno: un efecto por tipo de suceso, como máximo."""
        for (suceso, especie) in sucesos:
            nombre = EFECTO_ESPECIAL.get((suceso, especie), EFECTO_POR_SUCESO.get(suceso))
            if nombre is not None:
                self.efecto(nombre)

    def efecto(self, nombre):
        if not self._disponible or self._silenciado:
            return
        ahora = pygame.time.get_ticks() / 1000
        espera = ESPERA_ENTRE_EFECTOS.get(nombre, ESPERA_POR_DEFECTO)
        if ahora - self._ultimo_efecto.get(nombre, -espera) < espera:
            return
        self._ultimo_efecto[nombre] = ahora
        self._efectos[nombre].play()

    # ------------------------------------------------------------------
    def _a_sonido(self, onda):
        """Arreglo de numpy (-1 a 1) -> pygame.mixer.Sound."""
        if self._frecuencia != musica.FRECUENCIA_MUESTREO:   # ajustar si el equipo usa otra
            n = int(len(onda) * self._frecuencia / musica.FRECUENCIA_MUESTREO)
            onda = np.interp(np.linspace(0, len(onda) - 1, n), np.arange(len(onda)), onda)
        muestras = (np.clip(onda, -1, 1) * 32767).astype(np.int16)
        if self._canales > 1:
            muestras = np.column_stack([muestras] * self._canales)
        return pygame.sndarray.make_sound(np.ascontiguousarray(muestras))
