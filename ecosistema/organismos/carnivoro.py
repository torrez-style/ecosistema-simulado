from ecosistema import config
from ecosistema.busqueda import presa_mas_cercana
from ecosistema.organismos.organismo import Organismo
from ecosistema.organismos.herbivoro import Herbivoro


class Carnivoro(Organismo):
    """Se mueve y come Herbívoros."""

    PARAMETROS = config.PARAMETROS["Carnivoro"]
    SIMBOLO = "C"
    ORDEN_EN_TURNO = 3   # actúa último: ve a los herbívoros ya movidos (FAQ P18)

    def actuar(self, mundo):
        if not self._pagar_metabolismo_o_morir(mundo):
            return
        herbivoro = presa_mas_cercana(mundo, self, Herbivoro)
        if herbivoro is not None:
            self._comer(mundo, herbivoro)
        else:
            self._moverse_al_azar(mundo)

    def reproducirse(self, mundo):
        celda = self._preparar_cria(mundo)
        if celda is None:
            return None
        cria = Carnivoro(*celda, energia=self.energia_al_nacer)
        self._registrar_nacimiento(mundo, cria)
        return cria
