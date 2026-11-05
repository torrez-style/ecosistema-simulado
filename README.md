# Panta Rhei — Ecosistema Simulado

Proyecto final de **MO-0002 Programación I** (UCR, Sede de Occidente, II Ciclo 2026).
Una cuadrícula del bosque tropical seco de Guanacaste donde plantas, guatusas
(herbívoros) y tigrillos (carnívoros) nacen, se mueven, comen, se reproducen y
mueren por turnos. Nadie controla a los animales: el que sobrevive es el ecosistema.

> «Nadie se baña dos veces en el mismo río» — Heráclito

**Entrega:** 24 de noviembre de 2026.

## Cómo correrlo

```bash
pip install -r requirements.txt
python main.py                          # abre la ventana con una partida nueva
python main.py --semilla 42             # partida con semilla fija (se puede repetir)
python main.py --cargar                 # abre la ventana con la partida guardada
```

### Controles de la ventana

| Botón / tecla | Acción |
|---|---|
| **Iniciar / Pausar** · `ESPACIO` | iniciar o pausar la simulación |
| **+** / **−** · `+` / `-` | más o menos velocidad (0,5 a 15 turnos por segundo) |
| **Guardar** · `G` | guardar en `guardados/partida.json` |
| **Cargar** · `C` | cargar la partida guardada |
| **Nueva** · `N` | partida nueva con otra semilla |
| `F11` | pantalla completa |
| `ESC` | salir (o dejar la pantalla completa) |

La ventana se adapta a cualquier pantalla: se puede agrandar, achicar o poner en
pantalla completa, y el grid siempre se ve entero y centrado. La partida termina
cuando una especie se extingue; el puntaje son los turnos que sobrevivió.

### Modo consola

```bash
python main.py --consola                     # 10 turnos por consola
python main.py --consola 30 --semilla 7      # 30 turnos con semilla 7
python main.py --consola 10 --guardar        # ... y guarda la partida al final
python main.py --consola 10 --cargar         # sigue 10 turnos desde la partida guardada
```

## Pruebas y herramientas

```bash
python -m unittest discover -s pruebas -t .   # pruebas automáticas
python -m herramientas.probar_balance         # cuánto dura el ecosistema
python -m herramientas.demostraciones         # demostraciones de las Fases 1 y 2
```

## Estructura

```
ecosistema-simulado/
├── main.py                    # punto de entrada (ventana o consola)
├── ecosistema/                # motor de la simulación
│   ├── config.py              # parámetros (tabla de referencia + 2 ajustes)
│   ├── mundo.py               # grid y ciclo de turnos (Fases 2 y 3)
│   ├── busqueda.py            # Fase 4
│   ├── recursividad.py        # Fase 5
│   ├── persistencia.py        # Fase 6
│   ├── partida.py             # crear partidas y detectar extinciones
│   └── organismos/
│       ├── organismo.py       # clase abstracta base
│       ├── planta.py
│       ├── herbivoro.py
│       └── carnivoro.py
├── interfaz/                  # Fase 7 (pygame)
│   ├── ventana.py             # ventana, panel, controles y bucle
│   ├── distribucion.py        # cómo se reparte la pantalla (adaptable)
│   ├── sprites.py             # personajes en pixel art
│   ├── colores.py             # paleta rojo-negro
│   └── musica.py              # música 8 bits (pendiente, opcional)
├── herramientas/
│   ├── probar_balance.py      # mide cuántos turnos dura el ecosistema
│   └── demostraciones.py      # pruebas por consola de las Fases 1 y 2
├── pruebas/                   # pruebas automáticas (unittest)
│   ├── test_simulacion.py
│   └── test_interfaz.py
├── docs/
│   ├── fase0_propuesta.md
│   ├── diagrama_clases.md
│   └── decisiones_diseno.md
└── guardados/                 # partidas guardadas (JSON)
```

## Avance por fases

- [x] Fase 0 — Propuesta corta (`docs/fase0_propuesta.md`, `docs/diagrama_clases.md`)
- [x] Fase 1 — Núcleo de clases
- [x] Fase 2 — Mundo: colocar, mover, retirar, poblar al azar
- [x] Fase 3 — Ciclo de turnos y comportamientos
- [x] Fase 4 — Búsqueda de la presa más cercana y ranking por energía
      (ordenamiento por inserción, top 3 en cada turno)
- [x] Ajuste de parámetros: grid 20 × 20 y metabolismo del carnívoro en 1
      (mediana de 38 turnos; ver `docs/decisiones_diseno.md`)
- [x] Fase 5 — Recursividad: colonias de plantas con flood-fill
- [x] Fase 6 — Guardar / cargar en JSON (la partida continúa exactamente igual)
- [x] Fase 7 — Interfaz gráfica con pygame (ventana adaptable y pixel art)
- [ ] Fase 8 — Documento de decisiones y defensa oral
- [ ] Extra opcional: música 8 bits

## Convenciones del curso

- Todo atributo de instancia es protegido: `self._atributo`.
- Validaciones en setters con `ValueError`.
- `Mundo` **contiene** a los organismos; no hereda de `Organismo`.
- Nada de `if/elif` por tipo de especie: cada subclase sobrescribe `actuar()`.
