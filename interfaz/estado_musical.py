"""Lo que la música necesita saber del ecosistema (una clase por archivo)."""

from dataclasses import dataclass

UMBRAL_TENSION = 0.5   # fracción de la población inicial


@dataclass(frozen=True)
class EstadoMusical:
    """
    Proporción de cada especie respecto a su población inicial (1.0 = igual
    que al inicio, 0.5 = la mitad) y si la simulación está en pausa.

    @dataclass escribe solo el __init__ con estos cuatro atributos;
    frozen=True impide cambiarlos después de crear el objeto.
    """
    plantas: float
    herbivoros: float
    carnivoros: float
    pausado: bool

    @classmethod
    def desde_poblacion(cls, poblacion, poblacion_inicial, pausado):
        """Constructor alternativo: a partir de {"Planta": 30, ...} y la población inicial."""
        proporciones = {}
        for especie in ("Planta", "Herbivoro", "Carnivoro"):
            inicial = poblacion_inicial.get(especie, 0)
            if inicial > 0:
                proporciones[especie] = poblacion.get(especie, 0) / inicial
            else:
                proporciones[especie] = 0.0
        return cls(proporciones["Planta"], proporciones["Herbivoro"],
                   proporciones["Carnivoro"], pausado)

    @property
    def animo(self):
        """'tension' si alguna especie está por debajo de la mitad de su inicio."""
        menor = min(self.plantas, self.herbivoros, self.carnivoros)
        if menor < UMBRAL_TENSION:
            return "tension"
        return "calma"
