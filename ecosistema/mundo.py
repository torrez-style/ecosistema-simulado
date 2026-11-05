"""
El mundo: una cuadrícula N x M donde viven los organismos (Fase 2).

Mundo es una clase administradora: CONTIENE la lista de organismos,
no hereda de Organismo.
"""

import numpy as np


class Mundo:

    # Las 8 celdas adyacentes, incluidas las diagonales (FAQ P8)
    DIRECCIONES = [(-1, -1), (-1, 0), (-1, 1),
                   (0, -1),           (0, 1),
                   (1, -1),  (1, 0),  (1, 1)]

    def __init__(self, filas, columnas, semilla=None):
        if filas <= 0 or columnas <= 0:
            raise ValueError("El grid debe tener al menos una fila y una columna.")
        self._filas = filas
        self._columnas = columnas
        self._grid = [[None for _ in range(columnas)] for _ in range(filas)]
        self._organismos = []
        self._turno = 0
        # Generador de azar de numpy: con la misma semilla, la misma corrida.
        self._semilla = semilla
        self._azar = np.random.default_rng(semilla)
        # Lo que pasó en el último turno, en texto (para la consola)
        self._bitacora = []

    # ------------------------------------------------------------------
    # Propiedades
    # ------------------------------------------------------------------
    @property
    def filas(self):
        return self._filas

    @property
    def columnas(self):
        return self._columnas

    @property
    def turno(self):
        return self._turno

    @property
    def semilla(self):
        return self._semilla

    @property
    def bitacora(self):
        return list(self._bitacora)

    def registrar(self, texto):
        """Anota un suceso del turno actual en la bitácora."""
        self._bitacora.append(texto)

    def poblacion(self):
        """Cantidad de organismos vivos por especie: {"Planta": 9, ...}."""
        conteo = {}
        for organismo in self._organismos:
            if organismo.vivo:
                conteo[organismo.nombre] = conteo.get(organismo.nombre, 0) + 1
        return conteo

    @property
    def organismos(self):
        """Copia de la lista, para que nadie la modifique desde afuera."""
        return list(self._organismos)

    # ------------------------------------------------------------------
    # Fase 6: convertir el mundo a diccionario y reconstruirlo
    # ------------------------------------------------------------------
    def a_diccionario(self):
        """
        Estado completo del mundo, listo para guardarse en JSON.
        Incluye el estado del generador de azar: así, al cargar, los
        movimientos al azar siguen exactamente igual que sin interrupción.
        La lista de organismos conserva su orden, que decide quién actúa primero.
        """
        return {
            "filas": self._filas,
            "columnas": self._columnas,
            "turno": self._turno,
            "semilla": self._semilla,
            "estado_azar": self._azar.bit_generator.state,
            "organismos": [organismo.a_diccionario() for organismo in self._organismos],
        }

    @classmethod
    def desde_diccionario(cls, datos, especies):
        """
        Reconstruye un mundo guardado con a_diccionario().
        especies: diccionario {"Planta": Planta, ...} para crear cada organismo
        sin un if/elif por especie. Lanza ValueError si los datos no son válidos.
        """
        mundo = cls(datos["filas"], datos["columnas"], datos["semilla"])
        if not isinstance(datos["turno"], int) or datos["turno"] < 0:
            raise ValueError("El turno guardado no es válido.")
        mundo._turno = datos["turno"]
        mundo._azar.bit_generator.state = datos["estado_azar"]

        for guardado in datos["organismos"]:
            if not guardado["vivo"]:
                continue
            clase = especies.get(guardado["especie"])
            if clase is None:
                raise ValueError(f"Especie desconocida: {guardado['especie']}")
            organismo = clase(guardado["fila"], guardado["columna"],
                              energia=guardado["energia"], edad=guardado["edad"])
            mundo.colocar(organismo)   # valida bordes y celdas repetidas
        return mundo

    # ------------------------------------------------------------------
    # Consultas sobre el grid
    # ------------------------------------------------------------------
    def esta_dentro(self, fila, columna):
        """Bordes duros: nada se sale del grid (FAQ P6)."""
        return 0 <= fila < self._filas and 0 <= columna < self._columnas

    def celda(self, fila, columna):
        """Devuelve el organismo de esa celda, o None si está libre."""
        return self._grid[fila][columna]

    def vecinas(self, fila, columna):
        """Lista de posiciones vecinas que quedan dentro del grid."""
        resultado = []
        for df, dc in self.DIRECCIONES:
            f, c = fila + df, columna + dc
            if self.esta_dentro(f, c):
                resultado.append((f, c))
        return resultado

    def vecinas_libres(self, fila, columna):
        return [(f, c) for f, c in self.vecinas(fila, columna)
                if self.celda(f, c) is None]

    # ------------------------------------------------------------------
    # Fase 2: colocar, mover y retirar organismos
    # ------------------------------------------------------------------
    def _validar_destino(self, fila, columna):
        """Lanza ValueError si la celda está fuera del grid u ocupada."""
        if not self.esta_dentro(fila, columna):
            raise ValueError(f"La celda ({fila}, {columna}) está fuera del grid.")
        if self.celda(fila, columna) is not None:
            raise ValueError(f"La celda ({fila}, {columna}) ya está ocupada.")

    def colocar(self, organismo):
        """Pone un organismo en su propia posición (fila, columna)."""
        if organismo in self._organismos:
            raise ValueError("Ese organismo ya está en el mundo.")
        fila, columna = organismo.posicion
        self._validar_destino(fila, columna)
        self._grid[fila][columna] = organismo
        self._organismos.append(organismo)

    def celdas_libres(self):
        """Todas las celdas vacías del grid, recorriéndolo fila por fila."""
        return [(f, c)
                for f in range(self._filas)
                for c in range(self._columnas)
                if self._grid[f][c] is None]

    def elegir(self, opciones):
        """Devuelve un elemento al azar de la lista (o None si está vacía)."""
        if not opciones:
            return None
        indice = self._azar.integers(len(opciones))
        return opciones[indice]

    def poblar_aleatorio(self, poblacion_inicial):
        """
        poblacion_inicial: diccionario {ClaseEspecie: cantidad}.
        Cada organismo recibe una celda libre sorteada (sección 4.1).
        """
        for clase, cantidad in poblacion_inicial.items():
            for _ in range(cantidad):
                libre = self.elegir(self.celdas_libres())
                if libre is None:
                    raise ValueError("No hay espacio para toda la población inicial.")
                fila, columna = libre
                self.colocar(clase(fila, columna))

    def mover(self, organismo, fila, columna):
        """Mueve el organismo a una celda libre; la vieja queda vacía."""
        self._validar_destino(fila, columna)
        fila_vieja, columna_vieja = organismo.posicion
        self._grid[fila_vieja][columna_vieja] = None
        self._grid[fila][columna] = organismo
        organismo.mover_a(fila, columna)

    def retirar(self, organismo):
        """Saca al organismo del grid y de la lista; su celda queda libre ya."""
        fila, columna = organismo.posicion
        if self._grid[fila][columna] is organismo:
            self._grid[fila][columna] = None
        if organismo in self._organismos:
            self._organismos.remove(organismo)

    # ------------------------------------------------------------------
    # Fase 3: ciclo de un turno (orden fijo de la sección 4.5)
    # ------------------------------------------------------------------
    def ejecutar_turno(self):
        """
        Un turno completo en el orden fijo de la sección 4.5.
        Nada de if/elif por especie: cada organismo hace lo suyo con actuar().
        """
        self._bitacora = []

        # 0. Lista fija de los vivos al inicio, ordenada por ORDEN_EN_TURNO
        #    (Plantas 1, Herbívoros 2, Carnívoros 3). sorted() es estable:
        #    dentro de cada especie se respeta el orden de la lista del mundo.
        vivos_al_inicio = sorted(
            (o for o in self._organismos if o.vivo),
            key=lambda organismo: organismo.ORDEN_EN_TURNO,
        )

        # 1-3. Actúan Plantas, luego Herbívoros, luego Carnívoros
        for organismo in vivos_al_inicio:
            if organismo.vivo:                 # pudo ser comido en este turno
                organismo.actuar(self)
                if not organismo.vivo:         # murió de hambre al actuar
                    self.retirar(organismo)

        # 4. Barrido de muertes: energía en 0 o edad máxima superada
        for organismo in vivos_al_inicio:
            if organismo.vivo:
                organismo.envejecer()
                if organismo.supera_edad_maxima():
                    organismo.morir()
                    self.registrar(f"{organismo.nombre} {organismo.posicion} murió de vieja "
                                   f"(edad {organismo.edad})")
            if not organismo.vivo:
                self.retirar(organismo)

        # 5. Reproducciones (las crías no están en la lista: no actúan hoy)
        for organismo in vivos_al_inicio:
            if organismo.vivo:
                organismo.reproducirse(self)

        # 6. Fin del turno
        self._turno += 1

    # ------------------------------------------------------------------
    # Mostrar el grid como texto
    # ------------------------------------------------------------------
    def __str__(self):
        lineas = []
        for fila in self._grid:
            simbolos = [org.SIMBOLO if org is not None else "·" for org in fila]
            lineas.append(" ".join(simbolos))
        return "\n".join(lineas)
