from ecosistema import config
from ecosistema.organismos.organismo import Organismo


class Planta(Organismo):
    """No se mueve; gana energía por fotosíntesis cada turno."""

    PARAMETROS = config.PARAMETROS["Planta"]
    SIMBOLO = "P"

    def actuar(self, mundo):
        # Fotosíntesis: solo actualiza su propia energía, no toca otras celdas.
        self.ganar_energia(self.PARAMETROS["ganancia"])

    def reproducirse(self, mundo):
        # TODO (Fase 3):
        #   1. Si no puede_reproducirse(), no hace nada.
        #   2. Pedirle al mundo las celdas vecinas libres; si no hay, no hace nada.
        #   3. Elegir una al azar, pagar_reproduccion() y crear
        #      Planta(fila, col, self.energia_al_nacer) en esa celda.
        raise NotImplementedError("Fase 3: Planta.reproducirse()")
