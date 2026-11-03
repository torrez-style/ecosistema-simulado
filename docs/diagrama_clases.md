# Diagrama de clases — Fase 0

GitHub dibuja este diagrama automáticamente. Para exportarlo a PDF o PNG,
copien el bloque `mermaid` en [mermaid.live](https://mermaid.live).

```mermaid
classDiagram
    direction TB

    class Organismo {
        <<abstracta>>
        +PARAMETROS: dict$
        +SIMBOLO: str$
        #_fila: int
        #_columna: int
        #_energia: int
        #_edad: int
        #_vivo: bool
        +fila: int
        +columna: int
        +posicion: tuple
        +energia: int
        +edad: int
        +vivo: bool
        +energia_max: int
        +umbral_reproduccion: int
        +energia_al_nacer: int
        +mover_a(fila, columna)
        +ganar_energia(cantidad)
        +perder_energia(cantidad)
        +pagar_metabolismo()
        +envejecer()
        +supera_edad_maxima() bool
        +puede_reproducirse() bool
        +pagar_reproduccion()
        +morir()
        +actuar(mundo)*
        +reproducirse(mundo)*
    }

    class Planta {
        +SIMBOLO = "P"$
        +actuar(mundo)
        +reproducirse(mundo)
    }

    class Herbivoro {
        +SIMBOLO = "H"$
        +actuar(mundo)
        +reproducirse(mundo)
    }

    class Carnivoro {
        +SIMBOLO = "C"$
        +actuar(mundo)
        +reproducirse(mundo)
    }

    class Mundo {
        +DIRECCIONES: list$
        #_filas: int
        #_columnas: int
        #_grid: list~list~
        #_organismos: list~Organismo~
        #_turno: int
        +filas: int
        +columnas: int
        +turno: int
        +organismos: list~Organismo~
        +esta_dentro(fila, columna) bool
        +celda(fila, columna) Organismo
        +vecinas(fila, columna) list
        +vecinas_libres(fila, columna) list
        +colocar(organismo)
        +poblar_aleatorio(poblacion_inicial)
        +mover(organismo, fila, columna)
        +retirar(organismo)
        +ejecutar_turno()
    }

    Organismo <|-- Planta
    Organismo <|-- Herbivoro
    Organismo <|-- Carnivoro
    Mundo "1" o-- "0..*" Organismo : contiene
    Herbivoro ..> Planta : come
    Carnivoro ..> Herbivoro : come
```

## Cómo leerlo

| Símbolo | Significado |
|---|---|
| `#` | atributo protegido (`self._atributo`) |
| `+` | público (métodos y `@property`) |
| «abstracta» | clase que no se instancia |
| método en *cursiva* | método abstracto: cada subclase lo sobrescribe |
| subrayado | atributo de clase (compartido por todos los objetos) |
| triángulo hueco | herencia |
| rombo hueco | `Mundo` **contiene** la lista de organismos (no hereda de `Organismo`) |
| flecha punteada | dependencia: quién come a quién |

## Notas

- `energia`, `edad` y `vivo` son de solo lectura: se cambian únicamente con
  `ganar_energia()`, `perder_energia()`, `envejecer()` y `morir()`.
- `fila` y `columna` tienen setter que valida (lanza `ValueError`).
- Los módulos `busqueda.py`, `recursividad.py` y `persistencia.py` son funciones,
  no clases, por eso no aparecen en el diagrama.
