# Fase 8 — Decisiones de diseño

Anoten aquí cada decisión a medida que la toman; al final esto se convierte
en el documento breve de la entrega.

## Reglas del mundo

- **Vecindad:** 8 celdas (con diagonales), bordes duros.
- **Redondeo:** divisiones y porcentajes redondean hacia arriba (`math.ceil`),
  según la nota de la tabla de parámetros. Ej.: un herbívoro con 17 de energía
  que se reproduce paga 9 y queda con 8. _Confirmar con los profes: el ejemplo
  paso a paso usa decimales (8.5, 11.5)._
- **Orden del turno:** cada especie tiene un atributo de clase `ORDEN_EN_TURNO`
  (Planta 1, Herbívoro 2, Carnívoro 3). `Mundo` ordena la lista congelada con
  `sorted()` por ese atributo; como `sorted()` es estable, dentro de cada especie
  se respeta el orden de la lista del mundo (no se baraja).
- **Elección de presa:** entre las vecinas, la más cercana por distancia
  euclidiana (las de lado antes que las diagonales); en empate, la primera
  encontrada en el orden de `Mundo.DIRECCIONES`.
- **Muertes:** quien muere de hambre al actuar o es comido se retira del grid
  de inmediato; el paso 4 envejece a todos y retira a los que superan la edad máxima.
- **Bitácora:** `Mundo` guarda en una lista de texto lo que pasó en el turno,
  para mostrarlo en consola (no es un sistema de eventos).

## Ajuste de parámetros (sección 4: "estable durante varias decenas de turnos")

**Cambios respecto a la tabla de referencia (solo dos; ninguna mecánica cambia):**

| Parámetro | Referencia | Usado | Por qué |
|---|---|---|---|
| Tamaño del grid | 10 × 10 | 20 × 20 | La guía lo marca como "ajustable". Más espacio evita que las plantas llenen el grid y dejen atrapados a los carnívoros. |
| Metabolismo del carnívoro | −2 | −1 | Los carnívoros sobreviven más tiempo entre presas en un mundo más grande, sin reproducirse más rápido. |

La población inicial sigue siendo 15 / 8 / 3 (ocupa el 6,5 % del grid, por debajo
del 30-40 % del FAQ P7). Sigue cumpliéndose el FAQ P17: el umbral de 70 % hace
que el padre conserve energía positiva después de reproducirse.

**Resultados (100 semillas, `python -m herramientas.probar_balance`):**

| | Mediana de duración | Llegan a 30 turnos | Llegan a 50 turnos |
|---|---|---|---|
| Tabla de referencia, 10 × 10 | 14 turnos | 8 % | 0 % |
| Con los dos ajustes, 20 × 20 | 38 turnos | 77 % | 14 % |

**Cómo se eligieron:**

1. Con la tabla de referencia, el ecosistema dura una mediana de 14 turnos y casi
   siempre caen primero los herbívoros. La corrida de ejemplo de los profesores
   muestra la misma tendencia (herbívoros de 8 a 2 en 10 turnos).
2. Se probó cada cambio por separado: ninguno alcanzó.
3. Se probaron **todas** las combinaciones de uno y dos cambios (1 257 en total).
   La mejor fue grid 20 × 20 + metabolismo del carnívoro en 1.
4. Agregar un tercer cambio solo subía la mediana de 38 a unos 40 turnos, así que
   no se justificaba alejarse más de la tabla.

**Hallazgo:** con estas mecánicas, ningún ajuste de números logra un equilibrio
permanente. Incluso cambiando 9 valores de la tabla, el promedio no pasa de unos
70 turnos. Las poblaciones oscilan como en el modelo depredador-presa de
Lotka-Volterra y, en un grid finito, la especie que está en su mínimo termina
extinguiéndose. Por eso el juego termina con la extinción y el puntaje son los
turnos sobrevividos: *panta rhei*, todo fluye, y nada dura para siempre.
- **Fin de partida:** cuando una especie llega a 0 (pantalla de extinción);
  puntaje = turnos sobrevividos. _Validar con los profes._

## Diseño del código

- Python puro, sin estilo Java: `@property` en vez de getters/setters,
  `snake_case`, nada de métodos con guion bajo llamados desde otras clases.
- **Bucle de turnos explícito** en `Mundo.ejecutar_turno()`; sin sistema de
  eventos ni Observer.
- **numpy:** audio, sprites, estadísticas, historial de poblaciones y aleatoriedad
  con semilla. Si se usa una matriz numpy del grid, es solo una "fotografía" para
  dibujar o contar; nunca decide el comportamiento.
- **Búsqueda (Fase 4):** presa viva más cercana entre las vecinas, usada dentro de `actuar()`.
- **Recursividad (Fase 5):** flood-fill de colonias de plantas conectadas, escrito
  por nosotros (sin scipy).
- **Persistencia (Fase 6):** JSON con tamaño del grid, turno, semilla, **estado
  del generador de azar** y, por organismo, especie, posición, energía, edad y
  estado. Cada clase se convierte a sí misma en diccionario (`a_diccionario()`),
  así nadie toca atributos protegidos desde afuera. Guardar el estado del azar y
  el orden de la lista hace que una partida cargada continúe *exactamente* igual
  que una que nunca se cerró (hay una prueba automática que lo comprueba). Si el
  archivo no existe o está dañado, se lanza un error claro en vez de seguir con
  datos vacíos.
- **Interfaz (Fase 7):** pygame. La interfaz solo muestra el motor: llama a
  `mundo.ejecutar_turno()` y dibuja la matriz; no decide nada de la simulación.
  - **Ventana adaptable (idea de Maze Run):** ventana `RESIZABLE` y F11 para
    pantalla completa. En cada cuadro se compara el tamaño de la pantalla y, si
    cambió, se recalcula `celda = min(ancho // columnas, alto // filas)` y se
    centra el grid (`interfaz/distribucion.py`). A diferencia de Maze Run, no hay
    tope de 48 px, para aprovechar pantallas grandes. Si la pantalla es ancha, el
    panel va al costado; si es alta, va arriba. El tamaño de letra se elige con
    una búsqueda binaria para que todo el panel quepa.
  - **Controles:** botones clicables y teclado (un diccionario tecla → acción, sin
    cadena de `if/elif`): iniciar/pausar, velocidad de 0,5 a 15 turnos por
    segundo, guardar, cargar, partida nueva, pantalla completa y salir.
  - **Fin de partida:** cuando una especie se extingue se muestra la pantalla de
    extinción con los turnos sobrevividos como puntaje.
  - **Lección de Maze Run:** su chequeo de `VIDEORESIZE` comparaba con el estado
    `"JUGANDO"`, que nunca existía (el estado real era `"JUEGO"`); funcionaba solo
    gracias a un segundo chequeo de tamaño en cada cuadro. Aquí se usa solo ese
    chequeo, sin código muerto.
- **Gráficos:** todos los personajes se dibujan con píxeles (pixel art), sin
  imágenes externas. Cada sprite es una lista de textos de 16 × 16 donde cada
  letra es un color de la paleta (`interfaz/sprites.py`), y se escala con vecino
  más cercano para que los píxeles queden nítidos. Las plantas tienen tres etapas:
  brote (recién nacida), arbusto y corteza amarilla en flor (cuando ya puede
  reproducirse). Las crías de los animales se dibujan más pequeñas. El texto se
  dibuja sin suavizado para que combine con el estilo 8 bits.

## Estética — *Panta Rhei* (nombre provisional)

> «Nadie se baña dos veces en el mismo río» — Heráclito.
> Con semilla fija y persistencia, sí te bañas dos veces en el mismo río.

- Bosque tropical seco de Guanacaste en época seca.
- Planta = arbustos / corteza amarilla en flor; Herbívoro = guatusa; Carnívoro = tigrillo.
- Nadie controla a los animales: el que sobrevive es el ecosistema.
- Paleta rojo-negro en bandas (ver `interfaz/ventana.py`); los organismos no usan rojo.
- Pixel art: sprites como matrices 8×8 o 16×16 de índices de paleta.
- Música 8-bit propia generada con numpy (capa opcional).

## Pendiente de confirmar con los profes

- Tamaño del grupo.
- Redondeo hacia arriba vs. decimales del ejemplo.
- Si numpy se permite para el grid.
- Si terminar la partida por extinción es aceptable.

## Bibliografía

- Marzal Varó, A., García Sevilla, P. & Gracia Luengo, I. (2016). *Introducción a la programación con Python 3*. Universitat Jaume I.
- Documentación oficial de Python: módulos `abc`, `json`, `random`.
- Documentación de pygame y numpy.
