"""
Fase 6 — Guardar y cargar el estado completo del ecosistema (JSON).

El archivo guarda el tamaño del grid, el turno, la semilla, el estado del
generador de azar y, por cada organismo y en el orden de la lista del mundo:
especie, fila, columna, energía, edad y si está vivo.

Guardar -> cerrar -> abrir -> cargar: la simulación sigue exactamente igual
que si nunca se hubiera cerrado.
"""

import json
import os

from ecosistema.mundo import Mundo
from ecosistema.organismos import ESPECIES

RUTA_POR_DEFECTO = os.path.join("guardados", "partida.json")


def guardar(mundo, ruta=RUTA_POR_DEFECTO):
    """Escribe el estado del mundo en un archivo JSON (crea la carpeta si falta)."""
    carpeta = os.path.dirname(ruta)
    if carpeta:
        os.makedirs(carpeta, exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(mundo.a_diccionario(), archivo, indent=4, ensure_ascii=False)


def cargar(ruta=RUTA_POR_DEFECTO):
    """
    Lee un archivo JSON y reconstruye el mundo guardado.
    Lanza FileNotFoundError si no existe y ValueError si está dañado.
    """
    if not os.path.exists(ruta):
        raise FileNotFoundError(f"No existe la partida guardada: {ruta}")

    with open(ruta, "r", encoding="utf-8") as archivo:
        try:
            datos = json.load(archivo)
        except json.JSONDecodeError as error:
            raise ValueError(f"La partida guardada está dañada: {error}") from error

    try:
        return _armar_mundo(datos)
    except KeyError as error:
        raise ValueError(f"A la partida guardada le falta el dato {error}") from error


def _armar_mundo(datos):
    """
    Reconstruye el mundo a partir del diccionario leído del archivo
    (texto -> objetos, como el cargar() del cuaderno del fiado).
    ESPECIES convierte el nombre guardado en su clase, sin if/elif por especie.
    """
    mundo = Mundo(datos["filas"], datos["columnas"], datos["semilla"])
    mundo.restaurar(datos["turno"], datos["estado_azar"])
    for guardado in datos["organismos"]:
        if not guardado["vivo"]:
            continue
        clase = ESPECIES.get(guardado["especie"])
        if clase is None:
            raise ValueError(f"Especie desconocida: {guardado['especie']}")
        organismo = clase(guardado["fila"], guardado["columna"],
                          energia=guardado["energia"], edad=guardado["edad"])
        mundo.colocar(organismo)   # valida bordes y celdas repetidas
    return mundo
