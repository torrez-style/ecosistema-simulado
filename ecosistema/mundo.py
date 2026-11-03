"""
El mundo: una cuadrícula N x M donde viven los organismos (Fase 2).

Mundo es una clase administradora: CONTIENE la lista de organismos,
no hereda de Organismo.
"""


class Mundo:

    # Las 8 celdas adyacentes, incluidas las diagonales (FAQ P8)
    DIRECCIONES = [(-1, -1), (-1, 0), (-1, 1),
                   (0, -1),           (0, 1),
                   (1, -1),  (1, 0),  (1, 1)]

    def __init__(self, filas, columnas):
        if filas <= 0 or columnas <= 0:
            raise ValueError("El grid debe tener al menos una fila y una columna.")
        self._filas = filas
        self._columnas = columnas
        self._grid = [[None for _ in range(columnas)] for _ in range(filas)]
        self._organismos = []
        self._turno = 0

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
    def organismos(self):
        """Copia de la lista, para que nadie la modifique desde afuera."""
        return list(self._organismos)

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
    def colocar(self, organismo):
        # TODO: validar que la posición esté dentro y libre (si no, ValueError),
        # ponerlo en self._grid y agregarlo a self._organismos.
        raise NotImplementedError("Fase 2: Mundo.colocar()")

    def poblar_aleatorio(self, poblacion_inicial):
        # TODO: para cada especie, sortear una celda libre al azar por
        # organismo (sección 4.1). Nunca en patrón fijo.
        raise NotImplementedError("Fase 2: Mundo.poblar_aleatorio()")

    def mover(self, organismo, fila, columna):
        # TODO: liberar la celda vieja, ocupar la nueva y llamar a
        # organismo.mover_a(fila, columna).
        raise NotImplementedError("Fase 2: Mundo.mover()")

    def retirar(self, organismo):
        # TODO: quitarlo del grid y de la lista; su celda queda libre de inmediato.
        raise NotImplementedError("Fase 2: Mundo.retirar()")

    # ------------------------------------------------------------------
    # Fase 3: ciclo de un turno (orden fijo de la sección 4.5)
    # ------------------------------------------------------------------
    def ejecutar_turno(self):
        # TODO:
        #   0. Tomar una lista fija de los organismos vivos al inicio del turno.
        #   1. Actúan las Plantas.
        #   2. Actúan los Herbívoros.
        #   3. Actúan los Carnívoros.
        #   4. Muertes por energía 0 o por edad máxima (envejecer primero).
        #   5. Reproducciones.
        #   6. self._turno += 1
        #
        # Ojo: nada de if/elif por "tipo" para decidir el comportamiento;
        # cada organismo hace lo suyo con organismo.actuar(self).
        raise NotImplementedError("Fase 3: Mundo.ejecutar_turno()")

    # ------------------------------------------------------------------
    # Mostrar el grid como texto
    # ------------------------------------------------------------------
    def __str__(self):
        lineas = []
        for fila in self._grid:
            simbolos = [org.SIMBOLO if org is not None else "·" for org in fila]
            lineas.append(" ".join(simbolos))
        return "\n".join(lineas)
