"""
Configuración de la fuente de códigos de distribuidor bloqueados.

Hay UN SOLO archivo (un solo enlace de descarga directa) con UNA hoja y VARIAS
columnas: una columna por proceso. Cada proceso (PRE-EQUIPOS, PRE-SIM, ...) lee
su propia columna, de modo que las listas de códigos son INDEPENDIENTES entre
procesos aunque compartan el archivo.

Estructura del archivo (una hoja):

    | pre-equipos | pre-sim |
    |-------------|---------|
    | D001234     | A555000 |
    | D005678     | A555111 |
    | D009999     |         |

    - La primera fila son los encabezados (= claves de COLUMNAS abajo).
    - Un código por fila en cada columna. Las columnas pueden tener distinta
      cantidad de filas (las celdas vacías se ignoran).
    - Espacios y mayúsculas/minúsculas no importan (se normaliza).

MODO DE ACCESO (MODO_ACCESO):
    - "directo": descarga el archivo desde una URL pública de descarga directa
      (SharePoint "cualquiera con el vínculo", Google Sheets publicado, etc.).
    - "graph": descarga el archivo desde SharePoint autenticando con Microsoft
      Graph (client credentials). Se usa cuando el enlace exige inicio de sesión
      corporativo. Requiere registrar una app en Azure AD (ver GRAPH abajo).

Cómo agregar un proceso nuevo:
    1. Agregar una columna al archivo con el encabezado del proceso.
    2. Agregar una entrada a COLUMNAS con la clave del proceso -> nombre de la columna.
"""

import os

# Modo de acceso a la fuente: "directo" | "graph".
MODO_ACCESO = "graph"

# --- Modo "directo": enlace público de descarga directa ---------------------
# (Se usa solo si MODO_ACCESO == "directo".)
URL_FUENTE = "REEMPLAZAR_CON_ENLACE_DIRECTO_SHAREPOINT"

# --- Modo "graph": credenciales y ubicación del archivo en SharePoint -------
# (Se usa solo si MODO_ACCESO == "graph". Rellenar con los datos de Azure AD.)
GRAPH = {
    # Identificadores del registro de app (Azure AD).
    "tenant_id": "69002990-8016-415d-a552-cd21c7ad750c",
    "client_id": "ca657731-24b7-46e6-ab15-f6724dc9a6d9",
    # Se permite sobrescribir el secret por variable de entorno (opcional); si no
    # existe, se usa el valor embebido (necesario porque el bot corre en muchas
    # máquinas y no se configura env en cada una). Riesgo aceptado: la app solo
    # tiene permiso de LECTURA (Sites.Read.All) sobre este SharePoint.
    "client_secret_env": "GRAPH_CLIENT_SECRET",
    "client_secret_fallback": "Pi98Q~uVLq-uzf5WbxBWhf6pSgVob3LncN33dar_",
    # Ubicación del archivo en SharePoint:
    #   host        -> dominio del tenant
    #   site_path   -> ruta del sitio
    #   file_path   -> ruta del archivo dentro de la biblioteca de documentos
    "host": "teamcommunicationsa.sharepoint.com",
    "site_path": "/sites/Auditoria",
    "file_path": "CODIGOS INTEGRATEAM/codigos_bloqueados_PLANTILLA.xlsx",
}


def graph_client_secret():
    """Devuelve el client secret desde la variable de entorno, o el embebido."""
    return os.getenv(GRAPH["client_secret_env"], GRAPH["client_secret_fallback"])


# Formato del archivo de la fuente: 'csv' o 'xlsx'.
FORMATO_FUENTE = "xlsx"

# Columna que lee cada proceso dentro del archivo único.
COLUMNAS = {
    # PRE-EQUIPOS -> navegacion/equipos.py
    "pre-equipos": "pre-equipos",
    # PRE-SIM -> navegacion/preactivador.py
    "pre-sim": "pre-sim",
}

# Estado por defecto del checkbox de validación (desactivada por defecto).
VALIDACION_ACTIVA_DEFAULT = False


def columna_de(proceso):
    """Devuelve el nombre de columna que lee un proceso, o None si no existe."""
    return COLUMNAS.get(proceso)
