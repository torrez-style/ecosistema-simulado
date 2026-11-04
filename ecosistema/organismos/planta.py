from ecosistema import config
from ecosistema.organismos.organismo import Organismo


class Planta(Organismo):
    """No se mueve; gana energía por fotosíntesis cada turno."""

    PARAMETROS = config.PARAMETROS["Planta"]
    SIMBOLO = "P"
    ORDEN_EN_TURNO = 1   # base de la cadena alimentaria: actúa primero

    def actuar(self, mundo):
        # Fotosíntesis: solo actualiza su propia energía, no toca otras celdas.
        self.ganar_energia(self.PARAMETROS["ganancia"])

    def reproducirse(self, mundo):
        celda = self._preparar_cria(mundo)
        if celda is None:
            return None
        cria = Planta(*celda, energia=self.energia_al_nacer)
        self._registrar_nacimiento(mundo, cria)
        return cria
