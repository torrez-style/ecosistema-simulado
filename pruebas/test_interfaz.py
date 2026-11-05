"""
Pruebas de la interfaz que no necesitan abrir una ventana.

Correr desde la carpeta del proyecto:
    python -m unittest discover -s pruebas -t .
"""

import unittest

import interfaz  # noqa: F401  (oculta el saludo de pygame)
from ecosistema.organismos import Planta, Herbivoro
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


if __name__ == "__main__":
    unittest.main()
