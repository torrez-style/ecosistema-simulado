"""
Fase 7 — Interfaz gráfica con pygame.

La interfaz MUESTRA la simulación, no la reemplaza: solo llama a
mundo.ejecutar_turno() y dibuja lo que hay en la matriz.

Controles (botones o teclado):
    ESPACIO  iniciar / pausar          G    guardar partida
    + / -    más o menos velocidad     C    cargar partida
    N        partida nueva             F11  pantalla completa
    ESC      salir (o dejar la pantalla completa)

Ventana adaptable (idea de Maze Run): la ventana es RESIZABLE; en cada
cuadro se compara su tamaño y, si cambió, se recalcula la distribución.
"""

import pygame

from ecosistema import persistencia
from ecosistema.organismos import ESPECIES
from ecosistema.partida import crear_mundo, especies_extintas, semilla_aleatoria
from ecosistema.recursividad import colonias
from interfaz import colores
from interfaz.distribucion import calcular_distribucion
from interfaz.sprites import ESCALA_CRIA, Sprites, etapa_de

TITULO_VENTANA = "Panta Rhei — Ecosistema simulado"
NOMBRES = {"Planta": "Plantas", "Herbivoro": "Herbívoros", "Carnivoro": "Carnívoros"}
VELOCIDADES = (0.5, 1, 2, 4, 8, 15)   # turnos por segundo
VELOCIDAD_INICIAL = 2                 # índice en VELOCIDADES
FPS = 60
TAMANO_POR_DEFECTO = (1100, 720)
PROPORCION_DE_LA_PANTALLA = 0.85      # la ventana abre al 85 % del monitor
DURACION_MENSAJE = 3000               # milisegundos
MAX_TURNOS_POR_CUADRO = 3


class Texto:
    """
    Texto pixelado: se dibuja SIN suavizado (idea de Maze Run), así los bordes
    quedan en escalón como en los juegos de 8 bits. El tamaño de letra se elige
    según el espacio disponible.
    """

    def __init__(self):
        self._fuentes = {}
        self._cache = {}

    def _fuente(self, tamano):
        if tamano not in self._fuentes:
            self._fuentes[tamano] = pygame.font.Font(None, tamano)
        return self._fuentes[tamano]

    def medir(self, texto, tamano):
        """(ancho, alto) en píxeles, sin dibujar nada."""
        return self._fuente(tamano).size(texto)

    def render(self, texto, tamano, color):
        clave = (texto, tamano, color)
        if clave not in self._cache:
            if len(self._cache) > 500:
                self._cache.clear()
            self._cache[clave] = self._fuente(tamano).render(texto, False, color)
        return self._cache[clave]


class Boton:
    """Botón clicable. La etiqueta puede ser un texto o una función que lo devuelve."""

    def __init__(self, etiqueta, accion):
        self._etiqueta = etiqueta
        self._accion = accion
        self._rect = pygame.Rect(0, 0, 0, 0)

    @property
    def etiqueta(self):
        return self._etiqueta() if callable(self._etiqueta) else self._etiqueta

    @property
    def rect(self):
        return self._rect.copy()

    def ubicar(self, rect):
        self._rect = pygame.Rect(rect)

    def contiene(self, punto):
        return self._rect.collidepoint(punto)

    def pulsar(self):
        self._accion()


class Ventana:

    def __init__(self, mundo):
        pygame.init()
        pygame.display.set_caption(TITULO_VENTANA)
        self._tamano_ventana = self._tamano_inicial()
        pygame.display.set_mode(self._tamano_ventana, pygame.RESIZABLE)
        self._pantalla_completa = False

        self._reloj = pygame.time.Clock()
        self._texto = Texto()
        self._sprites = Sprites()
        pygame.display.set_icon(self._sprites.obtener("Planta", "listo", 32))

        self._mundo = mundo
        self._pausado = True
        self._indice_velocidad = VELOCIDAD_INICIAL
        self._acumulado = 0
        self._abierta = True
        self._mensaje = ""
        self._mensaje_hasta = 0

        # Lo que depende del tamaño de la pantalla (se calcula en _reacomodar)
        self._tamano_actual = None
        self._distribucion = None
        self._fondo = None
        self._fondo_grid = None

        self._botones = [
            Boton(lambda: "Pausar" if not self._pausado else "Iniciar", self._alternar_pausa),
            Boton("-", self._mas_lento),
            Boton("+", self._mas_rapido),
            Boton("Guardar", self._guardar),
            Boton("Cargar", self._cargar),
            Boton("Nueva", self._nueva_partida),
        ]
        # Tecla -> acción (un diccionario en vez de una cadena de if/elif)
        self._atajos = {
            pygame.K_SPACE: self._alternar_pausa,
            pygame.K_PLUS: self._mas_rapido,
            pygame.K_EQUALS: self._mas_rapido,
            pygame.K_KP_PLUS: self._mas_rapido,
            pygame.K_MINUS: self._mas_lento,
            pygame.K_KP_MINUS: self._mas_lento,
            pygame.K_g: self._guardar,
            pygame.K_c: self._cargar,
            pygame.K_n: self._nueva_partida,
            pygame.K_F11: self._alternar_pantalla_completa,
            pygame.K_ESCAPE: self._escape,
        }
        self._actualizar_estadisticas()

    # ------------------------------------------------------------------
    # Bucle principal
    # ------------------------------------------------------------------
    def ejecutar(self):
        while self._abierta:
            transcurrido = self._reloj.tick(FPS)
            self._procesar_eventos()
            self._avanzar_simulacion(transcurrido)

            tamano = pygame.display.get_surface().get_size()
            if tamano != self._tamano_actual:
                self._reacomodar(tamano)
            self._dibujar(pygame.display.get_surface())
            pygame.display.flip()
        pygame.quit()

    def _procesar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self._abierta = False
            elif evento.type == pygame.KEYDOWN and evento.key in self._atajos:
                self._atajos[evento.key]()
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                for boton in self._botones:
                    if boton.contiene(evento.pos):
                        boton.pulsar()

    def _avanzar_simulacion(self, transcurrido):
        if self._pausado or self._extintas:
            self._acumulado = 0
            return
        self._acumulado += transcurrido
        intervalo = 1000 / VELOCIDADES[self._indice_velocidad]
        turnos = 0
        while self._acumulado >= intervalo and turnos < MAX_TURNOS_POR_CUADRO:
            self._mundo.ejecutar_turno()
            self._actualizar_estadisticas()
            self._acumulado -= intervalo
            turnos += 1
            if self._extintas:
                self._pausado = True
                break
        if turnos == MAX_TURNOS_POR_CUADRO:
            self._acumulado = 0   # la computadora no da abasto: no acumular atraso

    def _actualizar_estadisticas(self):
        """Se calcula una vez por turno, no en cada cuadro."""
        self._poblacion = self._mundo.poblacion()
        self._colonias = colonias(self._mundo)
        self._extintas = especies_extintas(self._mundo)

    # ------------------------------------------------------------------
    # Acciones de los controles
    # ------------------------------------------------------------------
    def _alternar_pausa(self):
        if self._extintas:
            self._avisar("La partida terminó: N para una nueva o C para cargar")
            return
        self._pausado = not self._pausado

    def _mas_rapido(self):
        self._indice_velocidad = min(self._indice_velocidad + 1, len(VELOCIDADES) - 1)

    def _mas_lento(self):
        self._indice_velocidad = max(self._indice_velocidad - 1, 0)

    def _guardar(self):
        persistencia.guardar(self._mundo)
        self._avisar(f"Partida guardada (turno {self._mundo.turno})")

    def _cargar(self):
        try:
            self._mundo = persistencia.cargar()
        except (FileNotFoundError, ValueError) as error:
            self._avisar(f"No se pudo cargar: {error}")
            return
        self._pausado = True
        self._actualizar_estadisticas()
        self._avisar(f"Partida cargada (turno {self._mundo.turno})")

    def _nueva_partida(self):
        self._mundo = crear_mundo(semilla_aleatoria())
        self._pausado = True
        self._actualizar_estadisticas()
        self._avisar(f"Partida nueva (semilla {self._mundo.semilla})")

    def _alternar_pantalla_completa(self):
        if self._pantalla_completa:
            # En dos pasos: si se pide directo con RESIZABLE, SDL conserva el
            # tamaño de la pantalla completa en vez de volver al de la ventana.
            pygame.display.set_mode(self._tamano_ventana)
            pygame.display.set_mode(self._tamano_ventana, pygame.RESIZABLE)
        else:
            self._tamano_ventana = pygame.display.get_surface().get_size()
            pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self._pantalla_completa = not self._pantalla_completa

    def _escape(self):
        if self._pantalla_completa:
            self._alternar_pantalla_completa()
        else:
            self._abierta = False

    def _avisar(self, texto):
        self._mensaje = texto
        self._mensaje_hasta = pygame.time.get_ticks() + DURACION_MENSAJE

    # ------------------------------------------------------------------
    # Tamaño de la pantalla
    # ------------------------------------------------------------------
    @staticmethod
    def _tamano_inicial():
        info = pygame.display.Info()
        if info.current_w > 0 and info.current_h > 0:
            return (int(info.current_w * PROPORCION_DE_LA_PANTALLA),
                    int(info.current_h * PROPORCION_DE_LA_PANTALLA))
        return TAMANO_POR_DEFECTO

    def _reacomodar(self, tamano):
        """Recalcula todo lo que depende del tamaño de la pantalla."""
        celda_anterior = self._distribucion.celda if self._distribucion else None
        self._tamano_actual = tamano
        self._distribucion = calcular_distribucion(
            tamano[0], tamano[1], self._mundo.filas, self._mundo.columnas)
        if self._distribucion.celda != celda_anterior:
            self._sprites.limpiar()
        self._fondo = self._crear_fondo(tamano)
        self._fondo_grid = self._crear_fondo_grid()

    @staticmethod
    def _crear_fondo(tamano):
        """Fondo rojo-negro en bandas horizontales (8 bits)."""
        ancho, alto = tamano
        fondo = pygame.Surface(tamano)
        cantidad = len(colores.BANDAS_FONDO)
        for i, color in enumerate(colores.BANDAS_FONDO):
            y_inicio = alto * i // cantidad
            y_fin = alto * (i + 1) // cantidad
            fondo.fill(color, pygame.Rect(0, y_inicio, ancho, y_fin - y_inicio))
        return fondo

    def _crear_fondo_grid(self):
        """Suelo nocturno con un tablero muy sutil."""
        celda = self._distribucion.celda
        fondo = pygame.Surface(self._distribucion.grid.size)
        fondo.fill(colores.SUELO)
        for fila in range(self._mundo.filas):
            for columna in range(self._mundo.columnas):
                if (fila + columna) % 2 == 0:
                    fondo.fill(colores.SUELO_CLARO,
                               pygame.Rect(columna * celda, fila * celda, celda, celda))
        return fondo

    # ------------------------------------------------------------------
    # Dibujo
    # ------------------------------------------------------------------
    def _dibujar(self, pantalla):
        pantalla.blit(self._fondo, (0, 0))
        self._dibujar_grid(pantalla)
        self._dibujar_panel(pantalla)
        if self._extintas:
            self._dibujar_extincion(pantalla)
        elif self._pausado and self._mundo.turno == 0:
            self._dibujar_aviso_inicio(pantalla)

    def _dibujar_grid(self, pantalla):
        grid = self._distribucion.grid
        celda = self._distribucion.celda
        borde = max(2, celda // 10)
        pygame.draw.rect(pantalla, colores.SOMBRA, grid.inflate(borde * 4, borde * 4))
        pygame.draw.rect(pantalla, colores.ROJO_BASE, grid.inflate(borde * 2, borde * 2), borde)
        pantalla.blit(self._fondo_grid, grid.topleft)

        for organismo in self._mundo.organismos:
            etapa = etapa_de(organismo)
            lado = celda
            if etapa == "cria":
                lado = max(2, int(celda * ESCALA_CRIA[organismo.nombre]))
            sprite = self._sprites.obtener(organismo.nombre, etapa, lado)
            fila, columna = organismo.posicion
            x = grid.x + columna * celda + (celda - lado) // 2
            y = grid.y + fila * celda + (celda - lado)        # apoyado en el suelo
            pantalla.blit(sprite, (x, y))

    def _filas_del_panel(self):
        """Contenido del panel en dos bloques: información y controles."""
        estado = "EN MARCHA" if not self._pausado else "EN PAUSA"
        velocidad = VELOCIDADES[self._indice_velocidad]
        velocidad_texto = f"{velocidad:g} turno/s" if velocidad == 1 else f"{velocidad:g} turnos/s"
        mayor = self._colonias[0] if self._colonias else 0

        informacion = [
            ("titulo", "PANTA RHEI"),
            ("chico", "Ecosistema simulado"),
            ("normal", f"Turno {self._mundo.turno}"),
        ]
        for especie in ESPECIES:
            informacion.append(("especie", especie,
                                f"{NOMBRES[especie]}: {self._poblacion.get(especie, 0)}"))
        informacion.append(("chico", f"Colonias de plantas: {len(self._colonias)} (mayor: {mayor})"))

        controles = [
            ("normal", estado),
            ("chico", f"Velocidad: {velocidad_texto}"),
            ("chico", f"Semilla: {self._mundo.semilla}"),
            ("botones", self._botones[0:3]),
            ("botones", self._botones[3:6]),
            ("ayuda", "ESPACIO pausa   +/- velocidad"),
            ("ayuda", "G guardar  C cargar  N nueva"),
            ("ayuda", "F11 pantalla completa  ESC salir"),
        ]
        if pygame.time.get_ticks() < self._mensaje_hasta:
            controles.append(("mensaje", self._mensaje))
        return informacion, controles

    @staticmethod
    def _tamano_de(tipo, unidad):
        """Tamaño de letra de cada tipo de fila a partir de la unidad del panel."""
        proporcion = {"titulo": 2.0, "normal": 1.15, "especie": 1.15, "botones": 1.0}
        return max(10, int(unidad * proporcion.get(tipo, 0.85)))

    @staticmethod
    def _espacio(unidad):
        return max(2, unidad // 4)

    def _medir(self, filas, unidad):
        """Ancho y alto que ocupan las filas con esa unidad de texto."""
        ancho_total = alto_total = 0
        for fila in filas:
            tipo = fila[0]
            tamano = self._tamano_de(tipo, unidad)
            if tipo == "botones":
                relleno = self._espacio(unidad) * 2
                anchos = [self._texto.medir(b.etiqueta, tamano)[0] + 2 * relleno for b in fila[1]]
                ancho = sum(anchos) + self._espacio(unidad) * (len(anchos) - 1)
                alto = self._texto.medir("Ag", tamano)[1] + relleno
            else:
                ancho, alto = self._texto.medir(fila[-1], tamano)
                if tipo == "especie":
                    ancho += alto + self._espacio(unidad)
            ancho_total = max(ancho_total, ancho)
            alto_total += alto + self._espacio(unidad)
        return ancho_total, alto_total

    def _dibujar_panel(self, pantalla):
        panel = self._distribucion.panel
        margen = max(10, min(panel.w, panel.h) // 25)
        informacion, controles = self._filas_del_panel()

        # La letra más grande con la que todo cabe (búsqueda binaria)
        menor, mayor = 8, 48
        while menor < mayor:
            medio = (menor + mayor + 1) // 2
            if self._cabe(informacion, controles, medio, panel, margen):
                menor = medio
            else:
                mayor = medio - 1
        unidad = menor

        if self._distribucion.panel_al_costado:
            x, y = panel.x + margen, panel.y + margen
            ancho_columna = panel.w - 2 * margen
            y = self._dibujar_filas(pantalla, informacion, x, y, ancho_columna, unidad)
            self._dibujar_filas(pantalla, controles, x, y + self._espacio(unidad) * 2,
                                ancho_columna, unidad)
        else:
            ancho_columna = (panel.w - 3 * margen) // 2
            self._dibujar_filas(pantalla, informacion, panel.x + margen, panel.y + margen,
                                ancho_columna, unidad)
            self._dibujar_filas(pantalla, controles, panel.x + 2 * margen + ancho_columna,
                                panel.y + margen, ancho_columna, unidad)

    def _cabe(self, informacion, controles, unidad, panel, margen):
        ancho_info, alto_info = self._medir(informacion, unidad)
        ancho_ctrl, alto_ctrl = self._medir(controles, unidad)
        if self._distribucion.panel_al_costado:
            return (max(ancho_info, ancho_ctrl) <= panel.w - 2 * margen
                    and alto_info + alto_ctrl + self._espacio(unidad) * 2 <= panel.h - 2 * margen)
        ancho_columna = (panel.w - 3 * margen) // 2
        return (max(ancho_info, ancho_ctrl) <= ancho_columna
                and max(alto_info, alto_ctrl) <= panel.h - 2 * margen)

    def _dibujar_filas(self, pantalla, filas, x, y, ancho_columna, unidad):
        """Dibuja las filas una debajo de otra y devuelve la y donde terminó."""
        raton = pygame.mouse.get_pos()
        espacio = self._espacio(unidad)
        color_por_tipo = {"titulo": colores.ROJO_BRILLO, "chico": colores.TEXTO_TENUE,
                          "ayuda": colores.TEXTO_TENUE, "mensaje": colores.AMARILLO}
        for fila in filas:
            tipo = fila[0]
            tamano = self._tamano_de(tipo, unidad)
            if tipo == "botones":
                botones = fila[1]
                ancho_boton = (ancho_columna - espacio * (len(botones) - 1)) // len(botones)
                alto_boton = self._texto.medir("Ag", tamano)[1] + espacio * 2
                for i, boton in enumerate(botones):
                    rect = pygame.Rect(x + i * (ancho_boton + espacio), y,
                                       ancho_boton, alto_boton)
                    boton.ubicar(rect)
                    encima = boton.contiene(raton)
                    pygame.draw.rect(pantalla, colores.SOMBRA, rect)
                    pygame.draw.rect(pantalla, colores.ROJO_BRILLO if encima else colores.ROJO_BASE,
                                     rect, max(1, unidad // 10))
                    etiqueta = self._texto.render(boton.etiqueta, tamano, colores.TEXTO)
                    pantalla.blit(etiqueta, etiqueta.get_rect(center=rect.center))
                y += alto_boton
            elif tipo == "especie":
                especie, texto = fila[1], fila[2]
                superficie = self._texto.render(texto, tamano, colores.TEXTO)
                lado = superficie.get_height()
                pantalla.blit(self._sprites.obtener(especie, "adulto", lado), (x, y))
                pantalla.blit(superficie, (x + lado + espacio, y))
                y += lado
            else:
                superficie = self._texto.render(fila[1], tamano,
                                                color_por_tipo.get(tipo, colores.TEXTO))
                pantalla.blit(superficie, (x, y))
                y += superficie.get_height()
            y += espacio
        return y

    def _unidad_del_grid(self):
        return max(14, self._distribucion.grid.w // 22)

    def _texto_centrado(self, pantalla, lineas, rect):
        """Dibuja líneas (texto, tamaño de letra, color) centradas en el rectángulo."""
        superficies = [self._texto.render(t, tamano, c) for t, tamano, c in lineas]
        separacion = self._unidad_del_grid() // 3
        alto = sum(s.get_height() for s in superficies) + separacion * (len(superficies) - 1)
        y = rect.centery - alto // 2
        for superficie in superficies:
            pantalla.blit(superficie, superficie.get_rect(midtop=(rect.centerx, y)))
            y += superficie.get_height() + separacion

    def _dibujar_aviso_inicio(self, pantalla):
        unidad = self._unidad_del_grid()
        self._texto_centrado(pantalla, [("ESPACIO para iniciar", unidad, colores.TEXTO)],
                             self._distribucion.grid)

    def _dibujar_extincion(self, pantalla):
        """Pantalla de fin: el puntaje son los turnos que sobrevivió el ecosistema."""
        grid = self._distribucion.grid
        velo = pygame.Surface(grid.size, pygame.SRCALPHA)
        velo.fill((0, 0, 0, 200))
        pantalla.blit(velo, grid.topleft)
        unidad = self._unidad_del_grid()
        extintas = ", ".join(NOMBRES[nombre] for nombre in self._extintas)
        self._texto_centrado(pantalla, [
            ("EXTINCIÓN", unidad * 3, colores.ROJO_BRILLO),
            (f"Desaparecieron: {extintas}", unidad, colores.TEXTO),
            (f"El ecosistema sobrevivió {self._mundo.turno} turnos", unidad, colores.AMARILLO),
            ("N: partida nueva    C: cargar", unidad, colores.TEXTO_TENUE),
        ], grid)
