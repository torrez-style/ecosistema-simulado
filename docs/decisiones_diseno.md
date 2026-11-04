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
- **Cambios a los parámetros de referencia:** _ninguno por ahora_. Con los valores
  de la guía los herbívoros se extinguen entre el turno 7 y el 17 (probado con
  10 semillas); la corrida de ejemplo del profe muestra la misma tendencia
  (herbívoros de 8 a 2 en 10 turnos). Hay que ajustarlos para cumplir la
  sección 4: "estable durante varias decenas de turnos".
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
- **Persistencia (Fase 6):** JSON con turno, semilla y, por organismo, especie,
  posición, energía, edad y estado.
- **Interfaz (Fase 7):** pygame; primero cuadrados de colores, sprites al final.

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
