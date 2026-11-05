"""
Pruebas de la interfaz que no necesitan abrir una ventana.

Correr desde la carpeta del proyecto:
    python -m unittest discover -s pruebas -t .
"""

import unittest

import numpy as np

import interfaz  # noqa: F401  (oculta el saludo de pygame)
from ecosistema.mundo import Mundo
from ecosistema.organismos import Planta, Herbivoro
from interfaz import musica
from interfaz.distribucion import calcular_distribucion
from interfaz.sprites import DIBUJOS, PALETA, etapa_de

TAMANOS_DE_PANTALLA = [
    (1920, 1080), (1366, 768), (1280, 800), (900, 900),
    (700, 1000), (640, 480), (390, 844), (3840, 2160),
]


class PruebasDistribucion(unittest.TestCase):

    def test_el_grid_siempre_cabe_completo(self):
        for ancho, alto in TAMANOS_DE_PANTALLA:
            with self.subTest(pantalla=(ancho, alto)):
                d = calcular_distribucion(ancho, alto, 20, 20)
                self.assertGreaterEqual(d.grid.left, 0)
                self.assertGreaterEqual(d.grid.top, 0)
                self.assertLessEqual(d.grid.right, ancho)
                self.assertLessEqual(d.grid.bottom, alto)

    def test_el_grid_no_tapa_el_panel(self):
        for ancho, alto in TAMANOS_DE_PANTALLA:
            with self.subTest(pantalla=(ancho, alto)):
                d = calcular_distribucion(ancho, alto, 20, 20)
                self.assertFalse(d.grid.colliderect(d.panel))

    def test_celdas_cuadradas_y_grid_exacto(self):
        d = calcular_distribucion(1280, 800, 20, 20)
        self.assertEqual(d.grid.w, d.celda * 20)
        self.assertEqual(d.grid.h, d.celda * 20)

    def test_panel_al_costado_si_la_pantalla_es_ancha(self):
        self.assertTrue(calcular_distribucion(1920, 1080, 20, 20).panel_al_costado)
        self.assertFalse(calcular_distribucion(700, 1000, 20, 20).panel_al_costado)

    def test_pantalla_mas_grande_da_celdas_mas_grandes(self):
        chica = calcular_distribucion(1280, 720, 20, 20).celda
        grande = calcular_distribucion(3840, 2160, 20, 20).celda
        self.assertGreater(grande, chica)


class PruebasSprites(unittest.TestCase):

    def test_dibujos_de_16_por_16_con_colores_validos(self):
        for especie, etapas in DIBUJOS.items():
            for etapa, dibujo in etapas.items():
                with self.subTest(especie=especie, etapa=etapa):
                    self.assertEqual(len(dibujo), 16)
                    for fila in dibujo:
                        self.assertEqual(len(fila), 16)
                        self.assertTrue(set(fila) <= set(PALETA) | {"."})

    def test_etapas(self):
        self.assertEqual(etapa_de(Planta(0, 0)), "cria")
        self.assertEqual(etapa_de(Planta(0, 0, energia=14)), "listo")   # florece
        self.assertEqual(etapa_de(Herbivoro(0, 0, energia=12, edad=5)), "adulto")


class PruebasMusica(unittest.TestCase):

    SANO = musica.EstadoMusical(plantas=3.0, herbivoros=1.2, carnivoros=1.3, pausado=False)

    def test_animo_cambia_si_una_especie_baja_de_la_mitad(self):
        self.assertEqual(musica.animo(self.SANO), "calma")
        pocas = musica.EstadoMusical(plantas=3.0, herbivoros=0.3, carnivoros=1.0, pausado=False)
        self.assertEqual(musica.animo(pocas), "tension")

    def test_estado_musical_usa_proporciones(self):
        estado = musica.estado_musical({"Planta": 30, "Herbivoro": 4},
                                       {"Planta": 15, "Herbivoro": 8, "Carnivoro": 3}, False)
        self.assertEqual((estado.plantas, estado.herbivoros, estado.carnivoros), (2.0, 0.5, 0.0))

    def test_es_tenue(self):
        compositor = musica.Compositor(np.random.default_rng(1))
        onda = np.concatenate([compositor.siguiente(self.SANO) for _ in range(8)])
        self.assertLess(np.abs(onda).max(), 0.5)
        for nombre, crear in musica.EFECTOS.items():
            with self.subTest(efecto=nombre):
                self.assertLess(np.abs(crear()).max(), 0.5)

    def test_no_se_corta_entre_compases(self):
        compositor = musica.Compositor(np.random.default_rng(2))
        onda = np.concatenate([compositor.siguiente(self.SANO) for _ in range(4)])
        ventana = musica.FRECUENCIA_MUESTREO // 10
        inicio = musica.FRECUENCIA_MUESTREO * 3   # después de que entra el primer colchón
        volumenes = [np.sqrt((onda[i:i + ventana] ** 2).mean())
                     for i in range(inicio, len(onda) - ventana, ventana)]
        self.assertGreater(min(volumenes), 0.03)

    def test_en_pausa_solo_suena_el_colchon(self):
        pausado = musica.EstadoMusical(3.0, 1.2, 1.3, pausado=True)
        con_animales, _ = musica.componer_compas(self.SANO, 0, np.random.default_rng(5))
        solo_colchon, _ = musica.componer_compas(pausado, 0, np.random.default_rng(5))
        self.assertGreater(np.abs(con_animales - solo_colchon).max(), 0.01)

    def test_sin_guatusas_no_hay_melodia(self):
        sin = musica.EstadoMusical(3.0, 0.0, 0.0, pausado=False)
        pausado = musica.EstadoMusical(3.0, 0.0, 0.0, pausado=True)
        a, _ = musica.componer_compas(sin, 0, np.random.default_rng(5))
        b, _ = musica.componer_compas(pausado, 0, np.random.default_rng(5))
        self.assertTrue(np.allclose(a, b))


class PruebasSucesos(unittest.TestCase):

    def test_cuenta_nacimientos_comidas_y_muertes(self):
        mundo = Mundo(5, 5)
        mundo.colocar(Planta(2, 2, energia=13))       # florecerá: nace una planta
        mundo.colocar(Herbivoro(0, 0))
        mundo.colocar(Planta(0, 1))                   # el herbívoro se la come
        mundo.colocar(Herbivoro(4, 4, energia=1))     # muere de hambre
        mundo.ejecutar_turno()
        sucesos = mundo.sucesos
        self.assertEqual(sucesos.get(("nacimiento", "Planta")), 1)
        self.assertEqual(sucesos.get(("comida", "Herbivoro")), 1)
        self.assertEqual(sucesos.get(("muerte", "Herbivoro")), 1)

    def test_se_reinician_cada_turno(self):
        mundo = Mundo(5, 5)
        mundo.colocar(Herbivoro(4, 4, energia=1))
        mundo.ejecutar_turno()
        mundo.ejecutar_turno()
        self.assertEqual(mundo.sucesos, {})


if __name__ == "__main__":
    unittest.main()
