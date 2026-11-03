from ecosistema import config
from ecosistema.organismos.organismo import Organismo


class Herbivoro(Organismo):
    """Se mueve y come Plantas."""

    PARAMETROS = config.PARAMETROS["Herbivoro"]
    SIMBOLO = "H"

    def actuar(self, mundo):
        # TODO (Fase 3), sección 4.2:
        #   1. pagar_metabolismo(); si murió, termina aquí.
        #   2. Buscar Plantas VIVAS en las 8 celdas vecinas.
        #   3. Si hay: elegir una, marcarla muerta, moverse a su celda
        #      y ganar_energia(PARAMETROS["ganancia"]).
        #   4. Si no: moverse a una vecina libre al azar (si no hay, se queda).
        raise NotImplementedError("Fase 3: Herbivoro.actuar()")

    def reproducirse(self, mundo):
        # TODO (Fase 3): misma lógica que Planta.reproducirse()
        raise NotImplementedError("Fase 3: Herbivoro.reproducirse()")
