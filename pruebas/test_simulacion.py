"""
Pruebas automáticas con unittest.

Correr desde la carpeta del proyecto:
    python -m unittest discover -s pruebas -t .
"""

import json
import os
import tempfile
import unittest

from ecosistema import config, persistencia
from ecosistema.mundo import Mundo
from ecosistema.organismos import Organismo, Planta, Herbivoro, Carnivoro, ESPECIES
from ecosistema.busqueda import ranking_por_energia
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


class PruebasRanking(unittest.TestCase):

    def test_ordena_de_mayor_a_menor_energia(self):
        organismos = [Planta(0, 0, energia=5), Carnivoro(0, 1, energia=28),
                      Herbivoro(0, 2, energia=12), Planta(0, 3, energia=19)]
        energias = [o.energia for o in ranking_por_energia(organismos)]
        self.assertEqual(energias, [28, 19, 12, 5])

    def test_es_estable_con_empates(self):
        primero = Planta(0, 0, energia=10)
        segundo = Herbivoro(0, 1, energia=10)
        tercero = Planta(0, 2, energia=10)
        self.assertEqual(ranking_por_energia([primero, segundo, tercero]),
                         [primero, segundo, tercero])

    def test_top_y_no_modifica_la_original(self):
        organismos = [Planta(0, c, energia=e) for c, e in enumerate((3, 9, 1, 7, 5))]
        copia = list(organismos)
        top = ranking_por_energia(organismos, 3)
        self.assertEqual([o.energia for o in top], [9, 7, 5])
        self.assertEqual(organismos, copia)

    def test_coincide_con_sorted_en_un_mundo_real(self):
        mundo = mundo_poblado(8)
        for _ in range(15):
            mundo.ejecutar_turno()
        esperado = sorted(mundo.organismos, key=lambda o: o.energia, reverse=True)
        self.assertEqual(ranking_por_energia(mundo.organismos), esperado)

    def test_lista_vacia(self):
        self.assertEqual(ranking_por_energia([]), [])


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


class PruebasPersistencia(unittest.TestCase):

    def setUp(self):
        self._carpeta = tempfile.TemporaryDirectory()
        self.ruta = os.path.join(self._carpeta.name, "partida.json")

    def tearDown(self):
        self._carpeta.cleanup()

    def test_guardar_y_cargar_da_el_mismo_mundo(self):
        mundo = mundo_poblado(4)
        for _ in range(8):
            mundo.ejecutar_turno()
        persistencia.guardar(mundo, self.ruta)
        cargado = persistencia.cargar(self.ruta)
        self.assertEqual(cargado.turno, mundo.turno)
        self.assertEqual(str(cargado), str(mundo))
        self.assertEqual([o.a_diccionario() for o in cargado.organismos],
                         [o.a_diccionario() for o in mundo.organismos])

    def test_la_partida_continua_exactamente_igual(self):
        # Una partida sin interrupción vs. la misma partida guardada y cargada
        original = mundo_poblado(11)
        for _ in range(10):
            original.ejecutar_turno()
        persistencia.guardar(original, self.ruta)
        cargada = persistencia.cargar(self.ruta)
        for _ in range(10):
            original.ejecutar_turno()
            cargada.ejecutar_turno()
            self.assertEqual(cargada.bitacora, original.bitacora)
            self.assertEqual(str(cargada), str(original))

    def test_archivo_inexistente(self):
        with self.assertRaises(FileNotFoundError):
            persistencia.cargar(self.ruta)

    def test_json_danado(self):
        with open(self.ruta, "w", encoding="utf-8") as archivo:
            archivo.write("{ esto no es json")
        with self.assertRaises(ValueError):
            persistencia.cargar(self.ruta)

    def _guardar_y_modificar(self, cambiar):
        mundo = mundo_poblado(5)
        persistencia.guardar(mundo, self.ruta)
        with open(self.ruta, encoding="utf-8") as archivo:
            datos = json.load(archivo)
        cambiar(datos)
        with open(self.ruta, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo)

    def test_especie_desconocida(self):
        self._guardar_y_modificar(lambda d: d["organismos"][0].update(especie="Dragon"))
        with self.assertRaises(ValueError):
            persistencia.cargar(self.ruta)

    def test_dos_organismos_en_la_misma_celda(self):
        def duplicar(datos):
            primero, segundo = datos["organismos"][0], datos["organismos"][1]
            segundo["fila"], segundo["columna"] = primero["fila"], primero["columna"]
        self._guardar_y_modificar(duplicar)
        with self.assertRaises(ValueError):
            persistencia.cargar(self.ruta)

    def test_falta_un_dato(self):
        self._guardar_y_modificar(lambda d: d.pop("turno"))
        with self.assertRaises(ValueError):
            persistencia.cargar(self.ruta)

    def test_edad_negativa(self):
        with self.assertRaises(ValueError):
            Planta(0, 0, edad=-1)


if __name__ == "__main__":
    unittest.main()
