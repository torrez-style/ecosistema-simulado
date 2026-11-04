# Ecosistema Simulado

Proyecto final de **MO-0002 Programación I** (UCR, Sede de Occidente, II Ciclo 2026).
Una cuadrícula donde plantas, herbívoros y carnívoros nacen, se mueven, comen,
se reproducen y mueren por turnos.

**Entrega:** 17 de noviembre de 2026, 8 a. m.

## Cómo correrlo

```bash
pip install -r requirements.txt
python main.py
```

## Estructura

```
ecosistema-simulado/
├── main.py                    # punto de entrada
├── ecosistema/                # motor de la simulación
│   ├── config.py              # parámetros de la tabla de referencia
│   ├── mundo.py               # grid y ciclo de turnos (Fases 2 y 3)
│   ├── busqueda.py            # Fase 4
│   ├── recursividad.py        # Fase 5
│   ├── persistencia.py        # Fase 6
│   └── organismos/
│       ├── organismo.py       # clase abstracta base
│       ├── planta.py
│       ├── herbivoro.py
│       └── carnivoro.py
├── interfaz/                  # Fase 7 (pygame) + música 8-bit
│   ├── ventana.py
│   └── musica.py
├── docs/
│   ├── fase0_propuesta.md
│   └── decisiones_diseno.md
└── guardados/                 # partidas guardadas (JSON)
```

## Avance por fases

- [ ] Fase 0 — Propuesta corta (`docs/fase0_propuesta.md`)
- [ ] Fase 1 — Núcleo de clases (Organismo listo; faltan reproducción y actuar de H y C)
- [x] Fase 2 — Mundo: colocar, mover, retirar, poblar al azar
- [ ] Fase 3 — Ciclo de turnos y comportamientos
- [ ] Fase 4 — Búsqueda u ordenamiento
- [ ] Fase 5 — Recursividad (colonias de plantas)
- [ ] Fase 6 — Guardar / cargar en JSON
- [ ] Fase 7 — Interfaz gráfica con pygame
- [ ] Fase 8 — Documento de decisiones y defensa oral

Cada parte pendiente está marcada con `TODO` y lanza `NotImplementedError`
con el nombre de su fase, para que se note de inmediato qué falta.

## Convenciones del curso

- Todo atributo de instancia es protegido: `self._atributo`.
- Validaciones en setters con `ValueError`.
- `Mundo` **contiene** a los organismos; no hereda de `Organismo`.
- Nada de `if/elif` por tipo de especie: cada subclase sobrescribe `actuar()`.
