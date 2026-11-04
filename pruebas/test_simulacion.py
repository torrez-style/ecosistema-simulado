"""
Pruebas automáticas con unittest.

Correr desde la carpeta del proyecto:
    python -m unittest discover -s pruebas -t .
"""

import unittest

from ecosistema import config
from ecosistema.mundo import Mundo
from ecosistema.organismos import Organismo, Planta, Herbivoro, Carnivoro, ESPECIES
from ecosistema.recursividad import tamano_colonia, colonias


def mundo_poblado(semilla):
    mundo = Mundo(config.FILAS, config.COLUMNAS, semilla)
    mundo.poblar_aleatorio({ESPECIES[n]: c for n, c in config.POBLACION_INICIAL.items()})
    return mundo


class PruebasOrganismo(unittest.TestCase):

    def test_organismo_es_abstracto(self):
        with self.assertRaises(TypeError):
            Organismo(0, 0, 10)

    def test_energia_no_pasa_del_maximo(self):
        planta = Planta(0, 0)
        for _ in range(20):
            planta.actuar(None)
        self.assertEqual(planta.energia, planta.energia_max)

    def test_muere_al_llegar_a_cero(self):
        herbivoro = Herbivoro(0, 0, energia=1)
        herbivoro.pagar_metabolismo()
        self.assertFalse(herbivoro.vivo)
        self.assertEqual(herbivoro.energia, 0)

    def test_umbrales_con_redondeo_hacia_arriba(self):
        self.assertEqual(Planta(0, 0).umbral_reproduccion, 14)
        self.assertEqual(Herbivoro(0, 0).umbral_reproduccion, 17)
        self.assertEqual(Carnivoro(0, 0).umbral_reproduccion, 21)


class PruebasMundo(unittest.TestCase):

    def test_no_se_coloca_en_celda_ocupada(self):
        mundo = Mundo(5, 5)
        mundo.colocar(Planta(2, 2))
        with self.assertRaises(ValueError):
            mundo.colocar(Herbivoro(2, 2))

    def test_no_se_coloca_fuera_del_grid(self):
        mundo = Mundo(5, 5)
        with self.assertRaises(ValueError):
            mundo.colocar(Planta(5, 0))

    def test_esquina_tiene_tres_vecinas(self):
        self.assertEqual(len(Mundo(5, 5).vecinas(0, 0)), 3)

    def test_herbivoro_come_planta_y_ocupa_su_celda(self):
        mundo = Mundo(5, 5)
        planta = Planta(2, 3)
        herbivoro = Herbivoro(2, 2)
        mundo.colocar(planta)
        mundo.colocar(herbivoro)
        herbivoro.actuar(mundo)
        self.assertFalse(planta.vivo)
        self.assertEqual(herbivoro.posicion, (2, 3))
        self.assertEqual(herbivoro.energia, 12 - 1 + 6)
        self.assertIsNone(mundo.celda(2, 2))

    def test_prefiere_presa_de_lado_a_diagonal(self):
        mundo = Mundo(5, 5)
        diagonal = Planta(1, 1)
        de_lado = Planta(2, 1)
        herbivoro = Herbivoro(2, 2)
        for organismo in (diagonal, de_lado, herbivoro):
            mundo.colocar(organismo)
        herbivoro.actuar(mundo)
        self.assertFalse(de_lado.vivo)
        self.assertTrue(diagonal.vivo)

    def test_cria_no_actua_el_turno_en_que_nace(self):
        mundo = Mundo(5, 5)
        mundo.colocar(Planta(2, 2, energia=13))    # 13 + 2 = 15 >= 14: se reproduce
        mundo.ejecutar_turno()
        crias = [o for o in mundo.organismos if o.posicion != (2, 2)]
        self.assertEqual(len(crias), 1)
        self.assertEqual(crias[0].energia, 10)     # no hizo fotosíntesis
        self.assertEqual(crias[0].edad, 0)         # no envejeció

    def test_misma_semilla_misma_corrida(self):
        a, b = mundo_poblado(7), mundo_poblado(7)
        for _ in range(10):
            a.ejecutar_turno()
            b.ejecutar_turno()
        self.assertEqual(str(a), str(b))

    def test_invariantes_durante_muchos_turnos(self):
        for semilla in range(5):
            mundo = mundo_poblado(semilla)
            for _ in range(30):
                mundo.ejecutar_turno()
                for organismo in mundo.organismos:
                    self.assertTrue(organismo.vivo)
                    self.assertGreater(organismo.energia, 0)
                    self.assertIs(mundo.celda(*organismo.posicion), organismo)
                ocupadas = sum(mundo.celda(f, c) is not None
                               for f in range(mundo.filas)
                               for c in range(mundo.columnas))
                self.assertEqual(ocupadas, len(mundo.organismos))


class PruebasRecursividad(unittest.TestCase):

    def test_colonia_en_forma_de_l(self):
        mundo = Mundo(5, 5)
        for fila, columna in ((0, 0), (1, 0), (2, 0), (2, 1), (2, 2)):
            mundo.colocar(Planta(fila, columna))
        self.assertEqual(tamano_colonia(mundo, 0, 0), 5)
        self.assertEqual(tamano_colonia(mundo, 2, 2), 5)

    def test_diagonal_conecta(self):
        mundo = Mundo(5, 5)
        mundo.colocar(Planta(0, 0))
        mundo.colocar(Planta(1, 1))
        self.assertEqual(tamano_colonia(mundo, 0, 0), 2)

    def test_animales_cortan_la_colonia(self):
        mundo = Mundo(5, 5)
        mundo.colocar(Planta(0, 0))
        mundo.colocar(Herbivoro(0, 1))
        mundo.colocar(Planta(0, 2))
        self.assertEqual(tamano_colonia(mundo, 0, 0), 1)
        self.assertEqual(colonias(mundo), [1, 1])

    def test_celda_vacia_es_caso_base(self):
        self.assertEqual(tamano_colonia(Mundo(5, 5), 2, 2), 0)

    def test_grid_lleno_de_plantas_no_se_enciclan(self):
        mundo = Mundo(20, 20)
        for fila in range(20):
            for columna in range(20):
                mundo.colocar(Planta(fila, columna))
        self.assertEqual(tamano_colonia(mundo, 10, 10), 400)

    def test_colonias_suman_todas_las_plantas(self):
        mundo = mundo_poblado(3)
        for _ in range(10):
            mundo.ejecutar_turno()
        self.assertEqual(sum(colonias(mundo)), mundo.poblacion().get("Planta", 0))


if __name__ == "__main__":
    unittest.main()
