# Panta Rhei — Ecosistema simulado

**Documento de entrega (Fase 8): decisiones de diseño y bibliografía**

- **Curso:** MO-0002 Programación I, II Ciclo 2026 — Universidad de Costa Rica, Sede de Occidente
- **Docentes:** Prof. Manfred Mejías Acevedo y Prof. James McIntosh Molina
- **Integrantes:** Fatima Lizbeth Rios Obando (C4I927) y Manyel Lizandro Torrez (C4L962)
- **Fecha de entrega:** 24 de noviembre de 2026
- **Repositorio:** https://github.com/torrez-style/ecosistema-simulado

## Introducción

Este proyecto simula un ecosistema sobre una cuadrícula de 20 × 20 celdas que
representa el bosque tropical seco de Guanacaste. Viven en él tres especies:
plantas (arbustos y corteza amarilla), guatusas (herbívoros) y tigrillos
(carnívoros). El tiempo avanza en turnos y, en cada uno, todo organismo vivo
actúa según su especie: las plantas hacen fotosíntesis, las guatusas buscan
plantas y los tigrillos buscan guatusas. Además, todos gastan energía, envejecen,
se reproducen y mueren según las reglas de la sección 4 de la guía.

Nadie controla a los animales: el programa no es un juego, sino una simulación
para **observar** cómo el ecosistema prolifera o perece. La interfaz gráfica
(pygame) muestra el grid con personajes en pixel art, la población de cada
especie, las colonias de plantas y el ranking por energía, y permite iniciar,
pausar, avanzar turno por turno, cambiar la velocidad, guardar y cargar.

El código integra los temas centrales del curso: una clase abstracta
`Organismo` con tres subclases y polimorfismo real en `actuar()`,
encapsulamiento con propiedades, una matriz de objetos, búsqueda secuencial y el
algoritmo de la burbuja, persistencia en archivo y una función recursiva.

Este documento parte de la propuesta de la Fase 0 (`fase0_propuesta.md`) y la
actualiza con lo que realmente se construyó. Resume primero cómo se cumple cada
requisito obligatorio de la guía y las decisiones que tomamos donde la guía deja
libertad. Luego detalla las reglas implementadas, la relación con el material
del curso, el ajuste de parámetros, el diseño del código y la bibliografía
consultada.

**Cómo correrlo:** `pip install -r requirements.txt` y luego `python main.py`.
Las pruebas automáticas se corren con `python -m unittest discover -s pruebas -t .`.

## Cumplimiento del checklist de la guía (sección 6)

| Requisito obligatorio | Dónde está en el código | Cómo comprobarlo |
|---|---|---|
| Una clase abstracta (`Organismo`) con tres subclases concretas que la extienden | `ecosistema/organismos/organismo.py`: `Organismo(ABC)` con `@abstractmethod` en `actuar()` y `reproducirse()`. Subclases en `planta.py`, `herbivoro.py` y `carnivoro.py` | `Organismo(0, 0)` lanza `TypeError` (prueba `test_organismo_es_abstracto`); `python -m herramientas.demostraciones` |
| Polimorfismo real: el mismo método se comporta distinto según la subclase | Cada subclase sobrescribe `actuar()` y `reproducirse()`: fotosíntesis, comer plantas o comer herbívoros. `Mundo.ejecutar_turno()` solo llama a `organismo.actuar(self)`, sin ningún `if/elif` por especie; el orden del turno sale de ordenar por el atributo de clase `ORDEN_EN_TURNO` | Pruebas `test_herbivoro_come_planta_y_ocupa_su_celda` y `test_prefiere_presa_de_lado_a_diagonal`; bitácora del turno con `python main.py --consola` |
| Encapsulamiento: energía y edad no se modifican libremente desde afuera | Atributos protegidos (`self._energia`, `self._edad`, `self._vivo`) con `@property` de solo lectura; solo cambian con `ganar_energia()`, `perder_energia()`, `envejecer()` y `morir()`. `fila` y `columna` tienen setter que lanza `ValueError`. `Mundo.organismos` devuelve una copia de la lista | Pruebas `test_energia_no_pasa_del_maximo`, `test_muere_al_llegar_a_cero` y `test_edad_negativa` |
| Una matriz o grid que representa el mundo, con al menos una búsqueda u ordenamiento aplicado con sentido | Matriz `Mundo._grid` (lista de listas de 20 × 20) con bordes y colisiones controlados en `colocar()`, `mover()` y `retirar()`. Búsqueda: `presa_mas_cercana()` (búsqueda secuencial del mínimo), usada dentro de `actuar()` para decidir a quién comer. Ordenamiento: `ranking_por_energia()` (burbuja), cuyo top 3 se muestra en cada turno | Pruebas `test_no_se_coloca_en_celda_ocupada`, `test_no_se_coloca_fuera_del_grid` y las 5 de `PruebasRanking` |
| Persistencia: guardar y cargar el estado completo en un archivo | `ecosistema/persistencia.py` guarda en JSON el grid, el turno, la semilla, el estado del azar y cada organismo (`a_diccionario()`), y lo reconstruye con `Mundo.desde_diccionario()`. Botones **Guardar** y **Cargar** (teclas `G` y `C`) | Prueba `test_la_partida_continua_exactamente_igual`: 10 turnos seguidos dan el mismo resultado que guardar, cargar y seguir |
| Una función recursiva que resuelve algo real | `ecosistema/recursividad.py`: `tamano_colonia()` cuenta las plantas conectadas (flood-fill), con dos casos base. Se usa en cada turno para mostrar cuántas colonias hay y la más grande | Las 6 pruebas de `PruebasRecursividad`, incluido un grid lleno de 400 plantas sin recursión infinita |
| Interfaz gráfica funcional que visualiza la simulación | `interfaz/ventana.py` (pygame): un ícono en pixel art por especie y controles para iniciar/pausar, avanzar un turno, cambiar la velocidad, guardar, cargar y empezar una partida nueva. La ventana se adapta a cualquier tamaño de pantalla | `python main.py`; pruebas de `test_interfaz.py` (el grid cabe sin tapar el panel en 8 tamaños de pantalla) |

Los otros dos criterios de la rúbrica: la **propuesta corta** está en
`docs/fase0_propuesta.md` y `docs/diagrama_clases.md`, con el diagrama
actualizado al código final, y la **defensa oral** se hace en la fecha de
presentación.

## Decisiones propias que la guía no define

Donde la guía o el FAQ dejan la decisión al equipo, o no dicen nada, esto es lo
que elegimos.

| Tema | Qué dice la guía o el FAQ | Qué decidimos | Por qué |
|---|---|---|---|
| Cómo aplicar el redondeo | Redondear hacia arriba en divisiones y multiplicaciones (nota de la tabla). El documento *Simulación paso a paso* usa decimales (8,5) | `math.ceil` en el umbral (14 / 17 / 21), la energía al nacer (10 / 12 / 15) y el costo de reproducción: se pierde la mitad redondeada hacia arriba (17 → pierde 9 → queda 8) | Se siguió la nota de la guía, así toda la energía es entera; por eso hay una diferencia de 0,5 con el ejemplo |
| Qué presa elegir si hay varias | "Por ejemplo, la más cercana" | La más cercana por distancia euclidiana: las de lado (distancia 1) antes que las diagonales (distancia 2). En empate, la primera en el orden de `Mundo.DIRECCIONES` (empezando arriba a la izquierda) | Es un criterio fijo y explicable, y convierte la búsqueda en algo con sentido dentro de `actuar()` |
| Orden dentro de una misma especie | Por defecto, el orden de la lista del mundo; se puede barajar si se documenta (FAQ P19) | **No barajamos**: se respeta el orden de la lista. `sorted()` por `ORDEN_EN_TURNO` es estable y no altera ese orden | Hace la simulación reproducible con la misma semilla y más fácil de seguir turno por turno |
| Cuándo envejece un organismo | Muere si "al final de su turno" su edad supera la máxima | En el paso 4 todos los que estaban vivos al inicio del turno suman 1 a su edad y mueren si `edad > edad máxima`. Las crías nacen con edad 0 en el paso 5 y no envejecen ese turno | Respeta que la cría no participa en el turno en que nace (sección 4.4) |
| Cuándo termina la simulación | No lo define | Cuando una especie se extingue: aparece la pantalla de extinción y el puntaje son los turnos que sobrevivió el ecosistema | La guía no lo prohíbe, y con estas reglas ningún ajuste logra un equilibrio permanente (ver *Ajuste de parámetros*) |
| Tamaño del grid y parámetros | 10 × 10 sugerido y ajustable; los números se pueden ajustar si se documentan | Grid de 20 × 20 y metabolismo del carnívoro en 1; todo lo demás igual a la tabla | Es el menor cambio que logra que el ecosistema dure varias decenas de turnos (ver *Ajuste de parámetros*) |
| Bibliotecas externas | Tkinter o Pygame para la interfaz (FAQ P23); no menciona numpy | `pygame` (interfaz) y `numpy` (azar con semilla, audio y sprites), investigadas por cuenta propia: no se vieron en clase. `numpy` nunca decide el comportamiento de la simulación | Pygame da más control visual; numpy permite azar reproducible y generar la música |
| Azar | No lo define | Generador de numpy con semilla. La semilla se muestra en el panel para poder repetir una partida (`python main.py --semilla 42`). La música usa un generador aparte | Reproducibilidad para la defensa; encender o apagar el sonido no cambia la simulación |
| Qué se guarda en el archivo | Formato libre, se recomienda JSON (FAQ P20); "continuar exactamente donde quedó" | JSON con grid, turno, semilla, **estado del generador de azar**, el orden de la lista y, por organismo, especie, posición, energía, edad y estado. Si el archivo falta o está dañado, se avisa con un error claro | Sin el estado del azar y el orden, la partida cargada se movería distinto a la original |
| Qué cuenta como colonia de plantas | La guía sugiere el flood-fill como idea, sin detalles | Dos plantas son de la misma colonia si son vecinas en cualquiera de las 8 direcciones, igual que la vecindad del resto del proyecto | Consistencia con la regla de las 8 vecinas (FAQ P8) |
| Búsqueda u ordenamiento | Basta con uno (Fase 4 y FAQ P11) | Usamos los dos: la búsqueda de presa y el ranking por energía con la burbuja | La búsqueda decide el comportamiento; el ranking ayuda a observar el ecosistema |
| Biblioteca gráfica y controles | Tkinter o Pygame; controles mínimos de iniciar, pausar y velocidad | Pygame. Además: botón **Paso** (un turno a la vez), guardar, cargar, partida nueva, sonido, pantalla completa y ventana adaptable. Empieza en 1 turno cada 2 segundos | Al probarlo, la velocidad original era demasiado rápida para ver qué pasaba |
| Representación de las especies | Un color o ícono distinto por especie | Personajes en pixel art propios: brote, arbusto y corteza amarilla en flor (cuando la planta ya puede reproducirse), guatusa y tigrillo; las crías se ven más pequeñas | Permite ver de un vistazo quién está por reproducirse y quién acaba de nacer |
| Sonido | No lo pide | Música 8 bits tenue generada con numpy que cambia según la población, y efectos suaves al nacer, comer y morir | Extra opcional; ayuda a "escuchar" cuándo el ecosistema entra en tensión |

## Reglas del mundo

- **Vecindad:** 8 celdas (con diagonales), bordes duros.
- **Redondeo:** divisiones y porcentajes redondean hacia arriba (`math.ceil`),
  según la nota de la tabla de parámetros. Ej.: un herbívoro con 17 de energía
  que se reproduce paga 9 y queda con 8. El documento "simulación paso a paso"
  muestra decimales (8.5, 11.5) en su ejemplo; se siguió la nota de la guía
  (redondeo hacia arriba), por eso hay esa diferencia de 0,5.
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

## Relación con el material del curso

Revisamos el código contra las guías y soluciones de clase (semanas 9 a 14).

| Tema del curso | Material de clase | Dónde está en el proyecto |
|---|---|---|
| Matriz de objetos (5.4.9) | *Salón de pupitres*, *Batalla naval*: `[[None] * columnas for _ in range(filas)]`, `None` = casilla vacía | `Mundo._grid`, con `colocar`, `mover`, `retirar` (incluir / mover / eliminar) |
| Búsqueda secuencial (5.4.11, 5.4.14) | *Pulpería* y *Feria*: `buscar_mas_barato()` recorre y guarda el mejor | `presa_mas_cercana()`: mismo patrón, guarda la presa más cercana |
| Burbuja (5.4.13) | *Ordenamiento y burbuja*: versión 2 con `hubo_intercambio`, con objetos comparando un atributo, sobre una copia | `ranking_por_energia()` |
| `sorted()` con `key` y `lambda` | *Ordenamiento*, pasos 11 a 13 | `Mundo.ejecutar_turno()` ordena por `ORDEN_EN_TURNO` |
| Referencias (5.5) | `copy()` copia las flechas, no los objetos; la trampa de `[[None] * c] * f`; `is None` | `Mundo.organismos` devuelve una copia de la lista; `retirar()` usa `is` para identidad |
| Archivos (5.6) | *El cuaderno del fiado*: `with open(..., encoding="utf-8")`, modos `"r"`/`"w"`, `a_linea()` convierte objeto → texto, `cargar()` texto → objetos, `FileNotFoundError` con `"r"` | `persistencia.py`: `a_diccionario()` es nuestro `a_linea()`, y se guarda en JSON (recomendado por la guía del proyecto) |
| Recursividad (5.7) | *La fila*: caso base + caso recursivo que se acerca al base, límite de ~1000 llamadas; "un laberinto es naturalmente recursivo" | `tamano_colonia()`: dos casos base, profundidad máxima 400 |
| Herencia, abstracción, polimorfismo | Tarea 2, Laboratorios 1 y 2 | `Organismo` (ABC) → `Planta`, `Herbivoro`, `Carnivoro` |
| Una clase por archivo | Todas las guías: "una clase por archivo y ninguna función suelta mezclada con una clase" | Cada clase en su propio módulo; las funciones en módulos aparte |

Ajustes hechos al revisar: el ranking pasó de ordenamiento por inserción a la
**burbuja** del curso; la matriz se crea con la forma vista en clase; y las
clases de la interfaz quedaron cada una en su archivo.

Decoradores vistos en clase y dónde se usan:
- `@property` / `@x.setter`: en todas las clases (encapsulamiento).
- `@abstractmethod`: `Organismo.actuar()` y `Organismo.reproducirse()`.
- `@classmethod` como **constructor alternativo**: `Mundo.desde_diccionario()`
  (crea el mundo desde el archivo guardado), `EstadoMusical.desde_poblacion()` y
  `Distribucion.calcular()`.
- `@staticmethod` en los métodos de `Ventana` que no usan `self` (tamaño
  inicial, fondo en bandas, tamaños de letra).
- `@dataclass(frozen=True)` en `EstadoMusical` y `Distribucion`: clases que
  solo guardan datos; `frozen=True` impide cambiarlos después de creados.

Fuera del temario, pero decididos por el equipo y fáciles de explicar: `numpy`
(azar con semilla y música), `pygame` (interfaz) y `json` (guardado).

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

## Diseño del código

- Python puro, sin estilo Java: `@property` en vez de getters/setters,
  `snake_case`, nada de métodos con guion bajo llamados desde otras clases.
- **Bucle de turnos explícito** en `Mundo.ejecutar_turno()`; sin sistema de
  eventos ni Observer.
- **numpy:** audio, sprites, estadísticas, historial de poblaciones y aleatoriedad
  con semilla. Si se usa una matriz numpy del grid, es solo una "fotografía" para
  dibujar o contar; nunca decide el comportamiento.
- **Búsqueda y ordenamiento (Fase 4):**
  - `presa_mas_cercana()`: búsqueda lineal del mínimo entre las 8 vecinas,
    usada dentro de `actuar()` para decidir a quién comer.
  - `ranking_por_energia()`: **algoritmo de la burbuja** visto en clase
    (versión 2, con la bandera `hubo_intercambio`), de mayor a menor energía,
    sobre una copia de la lista (`.copy()`) para no cambiar la original. El top 3
    se muestra al final de cada turno en la ventana y en la consola. Una prueba
    automática comprueba que da el mismo resultado que `sorted()`.
  - Además, `Mundo` ordena la lista de cada turno por `ORDEN_EN_TURNO`.
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
    cadena de `if/elif`): iniciar/pausar, avanzar un solo turno (Paso / flecha
    derecha), velocidad de 1 turno cada 4 s a 15 turnos por segundo, guardar,
    cargar, partida nueva, pantalla completa y salir.
  - **Velocidad inicial: 1 turno cada 2 segundos.** Al probarlo en una computadora
    real, 2 turnos por segundo era demasiado rápido para ver qué pasaba. El botón
    Paso permite revisar la simulación turno por turno, como en el documento
    *Simulación paso a paso* de los profesores.
  - **Fin de partida:** cuando una especie se extingue se muestra la pantalla de
    extinción con los turnos sobrevividos como puntaje.
  - **Lección de Maze Run:** su chequeo de `VIDEORESIZE` comparaba con el estado
    `"JUGANDO"`, que nunca existía (el estado real era `"JUEGO"`); funcionaba solo
    gracias a un segundo chequeo de tamaño en cada cuadro. Aquí se usa solo ese
    chequeo, sin código muerto.
- **Gráficos:** todos los personajes se dibujan con píxeles (pixel art), sin
  imágenes externas. Cada sprite es una lista de textos de 16 × 16 donde cada
  letra es un color de la paleta (`interfaz/pixel_art.py`), y se escala con vecino
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
- Paleta rojo-negro en bandas (ver `interfaz/colores.py`); los organismos no usan rojo.
- Pixel art: sprites como matrices 8×8 o 16×16 de índices de paleta.
- **Música 8 bits propia, generada con numpy** (capa opcional, no da puntos).
  Es tenue, como un paisaje sonoro del bosque, y reacciona a lo que pasa:
  - Se compone **compás por compás** (`interfaz/musica.py`): plantas = colchón de
    onda triangular (más plantas, más lleno), guatusas = melodía de onda cuadrada
    al 25 % (más guatusas, más notas), tigrillos = toques de ruido muy suaves.
  - Escala **pentatónica mayor** en calma; si alguna especie baja de la mitad de
    su población inicial, pasa a **pentatónica menor** y el tempo sube un poco.
  - En pausa solo suena el colchón. Con la extinción suena una frase lenta que
    baja y después el bosque queda en silencio.
  - Cada compás se traslapa un segundo con el siguiente para que no haya cortes.
  - Efectos suaves al final de cada turno (florecer, nacer, comer, morir) con una
    espera mínima entre repeticiones, para que a alta velocidad no saturen.
  - `Mundo` cuenta los sucesos de cada turno (`mundo.sucesos`) para que el
    sonido no tenga que leer el texto de la bitácora.
  - La música usa **su propio generador de azar**, nunca el del mundo: así
    encender o apagar el sonido no cambia la simulación.
  - No se copió ninguna canción: el "sonido a consola" viene de las ondas
    (triangular, cuadrada y ruido), no de melodías con derechos de autor.
  - Si la computadora no tiene sonido, el juego sigue funcionando en silencio.

## Bibliografía

- Mejías Acevedo, M., & McIntosh Molina, J. (2026). *Proyecto final: Ecosistema simulado* [Guía del proyecto]. Programación I (MO-0002), Universidad de Costa Rica, Sede de Occidente.
- Mejías Acevedo, M., & McIntosh Molina, J. (2026). *Preguntas frecuentes: Proyecto final — Ecosistema simulado* [Complemento de la guía]. Programación I (MO-0002), Universidad de Costa Rica, Sede de Occidente.
- Mejías Acevedo, M., & McIntosh Molina, J. (2026). *Simulación paso a paso* [Material del curso]. Programación I (MO-0002), Universidad de Costa Rica, Sede de Occidente.
- Marzal Varó, A., García Sevilla, P. & Gracia Luengo, I. (2016). *Introducción a la programación con Python 3*. Universitat Jaume I.
- Documentación oficial de Python: módulos `abc`, `json`, `random`.
- Documentación de pygame y numpy.
