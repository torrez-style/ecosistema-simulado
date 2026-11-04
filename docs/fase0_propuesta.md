# Fase 0 — Propuesta corta

> Media página: diagrama de clases, especies y boceto de reglas.

## Especies

| Especie | Qué hace | Qué come |
|---|---|---|
| Planta | No se mueve; fotosíntesis | Nada (luz solar) |
| Herbívoro | Se mueve | Plantas |
| Carnívoro | Se mueve | Herbívoros |

## Diagrama de clases

```
«abstracta» Organismo
  # _fila, _columna, _energia, _edad, _vivo
  + actuar(mundo)          «abstracto»
  + reproducirse(mundo)    «abstracto»
        ▲
        ├── Planta
        ├── Herbivoro
        └── Carnivoro

Mundo  (contiene la lista de organismos y el grid)
  # _filas, _columnas, _grid, _organismos, _turno
  + ejecutar_turno()
```

## Boceto de reglas

- Grid de 20 × 20 (la guía sugiere 10 × 10, ajustable), bordes duros, 8 vecinas (con diagonales).
- Orden del turno: Plantas → Herbívoros → Carnívoros → muertes → reproducciones → refrescar.
- Parámetros: los de referencia de la guía, con el metabolismo del carnívoro en 1 (ver `ecosistema/config.py` y `docs/decisiones_diseno.md`).
