# Fase 8 — Decisiones de diseño

Anoten aquí cada decisión a medida que la toman; al final esto se convierte
en el documento breve de la entrega.

## Decisiones

- **Vecindad:** 8 celdas (con diagonales), bordes duros.
- **Redondeo:** divisiones y porcentajes redondean hacia arriba (`math.ceil`),
  según la nota de la tabla de parámetros. Ej.: un herbívoro con 17 de energía
  que se reproduce paga 9 y queda con 8.
- **Orden dentro de cada especie:** _pendiente_ (orden de la lista o barajado cada turno).
- **Formato de guardado:** JSON.
- **Interfaz:** pygame.
- **Cambios a los parámetros de referencia:** _ninguno por ahora_.

## Bibliografía

- Marzal Varó, A., García Sevilla, P. & Gracia Luengo, I. (2016). *Introducción a la programación con Python 3*. Universitat Jaume I.
- Documentación oficial de Python: módulos `abc`, `json`, `random`.
- Documentación de pygame.
