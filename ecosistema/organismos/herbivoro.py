from ecosistema import config
from ecosistema.busqueda import presa_mas_cercana
from ecosistema.organismos.organismo import Organismo
from ecosistema.organismos.planta import Planta


class Herbivoro(Organismo):
    """Se mueve y come Plantas."""

    PARAMETROS = config.PARAMETROS["Herbivoro"]
    SIMBOLO = "H"
    ORDEN_EN_TURNO = 2

    def actuar(self, mundo):
        if not self._pagar_metabolismo_o_morir(mundo):
            return
        planta = presa_mas_cercana(mundo, self, Planta)
        if planta is not None:
            self._comer(mundo, planta)
        else:
            self._moverse_al_azar(mundo)

    def reproducirse(self, mundo):
        celda = self._preparar_cria(mundo)
        if celda is None:
            return None
        cria = Herbivoro(*celda, energia=self.energia_al_nacer)
        self._registrar_nacimiento(mundo, cria)
        return cria
