"""
Lectura/escritura del catálogo de Grupos y Servicios de recargas.

El catálogo vive en su PROPIO archivo (catalogo.xlsx), separado de recargas.xlsx
porque este último se borra/reescribe en cada corrida. Formato "largo":

    | grupo            | servicio                              |
    |------------------|---------------------------------------|
    | Paquetes de datos| DT-Paq 200 MB WA - 1 Dias - $3,000    |
    | Reventa          | VZ - Reventa Ilim 15 dias - $17,500   |

Expone utilidades para: guardar el resultado del scraping, y leer el catálogo
como grupos y como mapa grupo -> [servicios] (para los combobox dependientes).
"""

import os

import pandas as pd

RUTA_CATALOGO = os.path.join('src', 'recargas', 'catalogo.xlsx')
COL_GRUPO = 'grupo'
COL_SERVICIO = 'servicio'


def guardar_catalogo(pares, ruta=RUTA_CATALOGO):
    """
    Escribe el catálogo (lista de pares (grupo, servicio)) en Excel.

    Regenera el archivo completo en cada llamada.
    """
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    df = pd.DataFrame(pares, columns=[COL_GRUPO, COL_SERVICIO])
    df.to_excel(ruta, index=False)
    return len(df)


def _leer_df(ruta=RUTA_CATALOGO):
    if not os.path.exists(ruta):
        return pd.DataFrame(columns=[COL_GRUPO, COL_SERVICIO])
    return pd.read_excel(ruta, dtype=str).fillna('')


def catalogo_existe(ruta=RUTA_CATALOGO):
    return os.path.exists(ruta)


def leer_mapa(ruta=RUTA_CATALOGO):
    """
    Devuelve un dict {grupo: [servicios...]} preservando el orden de aparición.
    """
    df = _leer_df(ruta)
    mapa = {}
    for _, fila in df.iterrows():
        grupo = str(fila[COL_GRUPO]).strip()
        servicio = str(fila[COL_SERVICIO]).strip()
        if not grupo or not servicio:
            continue
        mapa.setdefault(grupo, [])
        if servicio not in mapa[grupo]:
            mapa[grupo].append(servicio)
    return mapa


def leer_grupos(ruta=RUTA_CATALOGO):
    """Lista de grupos (claves del mapa)."""
    return list(leer_mapa(ruta).keys())
