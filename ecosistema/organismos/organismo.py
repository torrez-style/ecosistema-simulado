"""
Clase base abstracta de todas las especies (sección 3 de la guía).

Organismo no se instancia nunca: solo sus subclases concretas
(Planta, Herbivoro, Carnivoro, ...). Cada subclase define:
    - PARAMETROS: su diccionario de config.PARAMETROS
    - SIMBOLO:    letra para imprimir el grid ("P", "H", "C")
    - actuar(mundo) y reproducirse(mundo): su propio comportamiento
"""

import math
from abc import ABC, abstractmethod

from ecosistema import config


class Organismo(ABC):

    PARAMETROS = {}
    SIMBOLO = "?"

    def __init__(self, fila, columna, energia=None):
        self.fila = fila
        self.columna = columna
        if energia is None:
            energia = self.PARAMETROS["energia_inicial"]
        if energia <= 0:
            raise ValueError("Un organismo no puede nacer sin energía.")
        self._energia = energia
        self._edad = 0
        self._vivo = True

    # ------------------------------------------------------------------
    # Propiedades
    # ------------------------------------------------------------------
    @property
    def fila(self):
        return self._fila

    @fila.setter
    def fila(self, valor):
        if not isinstance(valor, int) or valor < 0:
            raise ValueError("La fila debe ser un entero no negativo.")
        self._fila = valor

    @property
    def columna(self):
        return self._columna

    @columna.setter
    def columna(self, valor):
        if not isinstance(valor, int) or valor < 0:
            raise ValueError("La columna debe ser un entero no negativo.")
        self._columna = valor

    @property
    def posicion(self):
        return (self._fila, self._columna)

    # energia, edad y vivo son de solo lectura: se cambian únicamente con
    # los métodos de abajo (encapsulamiento, sección 6 de la guía).
    @property
    def energia(self):
        return self._energia

    @property
    def edad(self):
        return self._edad

    @property
    def vivo(self):
        return self._vivo

    @property
    def energia_max(self):
        return self.PARAMETROS["energia_max"]

    @property
    def umbral_reproduccion(self):
        # Redondeo hacia arriba (nota de la tabla de parámetros)
        return math.ceil(self.energia_max * config.PORCENTAJE_UMBRAL_REPRODUCCION / 100)

    @property
    def energia_al_nacer(self):
        return math.ceil(self.energia_max * config.PORCENTAJE_ENERGIA_AL_NACER / 100)

    # ------------------------------------------------------------------
    # Métodos comunes a todas las especies
    # ------------------------------------------------------------------
    def mover_a(self, fila, columna):
        """Actualiza la posición del organismo. El Mundo se encarga del grid."""
        self.fila = fila
        self.columna = columna

    def ganar_energia(self, cantidad):
        if cantidad < 0:
            raise ValueError("Use perder_energia() para restar energía.")
        self._energia = min(self._energia + cantidad, self.energia_max)

    def perder_energia(self, cantidad):
        """Resta energía; si llega a 0 o menos, muere de inmediato (sección 4.3)."""
        if cantidad < 0:
            raise ValueError("Use ganar_energia() para sumar energía.")
        self._energia -= cantidad
        if self._energia <= 0:
            self._energia = 0
            self.morir()

    def pagar_metabolismo(self):
        self.perder_energia(self.PARAMETROS["metabolismo"])

    def envejecer(self):
        self._edad += 1

    def supera_edad_maxima(self):
        return self._edad > self.PARAMETROS["edad_max"]

    def puede_reproducirse(self):
        """Solo revisa la energía; la celda libre la revisa el Mundo."""
        return self._vivo and self._energia >= self.umbral_reproduccion

    def pagar_reproduccion(self):
        """Pierde la mitad de su energía actual (redondeo hacia arriba)."""
        self._energia -= math.ceil(self._energia / 2)

    def morir(self):
        self._vivo = False

    # ------------------------------------------------------------------
    # Comportamiento propio de cada especie (polimorfismo)
    # ------------------------------------------------------------------
    @abstractmethod
    def actuar(self, mundo):
        """Lo que hace la especie en su fase del turno (sección 4.2)."""

    @abstractmethod
    def reproducirse(self, mundo):
        """Crea una cría en una celda vecina libre (sección 4.4)."""

    def __str__(self):
        estado = "vivo" if self._vivo else "muerto"
        return (f"{type(self).__name__} en {self.posicion} | "
                f"energía {self._energia}/{self.energia_max} | "
                f"edad {self._edad} | {estado}")
