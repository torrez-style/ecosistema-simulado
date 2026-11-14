"""Lo que la música necesita saber del ecosistema (una clase por archivo)."""

UMBRAL_TENSION = 0.5   # fracción de la población inicial


class EstadoMusical:
    """
    Proporción de cada especie respecto a su población inicial (1.0 = igual
    que al inicio, 0.5 = la mitad) y si la simulación está en pausa.
    """

    def __init__(self, plantas, herbivoros, carnivoros, pausado):
        for proporcion in (plantas, herbivoros, carnivoros):
            if proporcion < 0:
                raise ValueError("Una proporción de población no puede ser negativa.")
        self._plantas = plantas
        self._herbivoros = herbivoros
        self._carnivoros = carnivoros
        self._pausado = pausado

    @property
    def plantas(self):
        return self._plantas

    @property
    def herbivoros(self):
        return self._herbivoros

    @property
    def carnivoros(self):
        return self._carnivoros

    @property
    def pausado(self):
        return self._pausado

    @property
    def animo(self):
        """'tension' si alguna especie está por debajo de la mitad de su inicio."""
        menor = min(self._plantas, self._herbivoros, self._carnivoros)
        if menor < UMBRAL_TENSION:
            return "tension"
        return "calma"
