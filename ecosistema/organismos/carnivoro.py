from ecosistema import config
from ecosistema.organismos.organismo import Organismo


class Carnivoro(Organismo):
    """Se mueve y come Herbívoros."""

    PARAMETROS = config.PARAMETROS["Carnivoro"]
    SIMBOLO = "C"

    def actuar(self, mundo):
        # TODO (Fase 3): misma idea que Herbivoro.actuar(), pero la presa
        # es un Herbivoro. Antes de comer, comprobar que la presa siga viva.
        raise NotImplementedError("Fase 3: Carnivoro.actuar()")

    def reproducirse(self, mundo):
        # TODO (Fase 3)
        raise NotImplementedError("Fase 3: Carnivoro.reproducirse()")
