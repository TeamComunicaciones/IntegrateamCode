"""
Registro técnico de incidentes, separado de lo que ve el operario.

Se escribe en Documents\\TeamComunicaciones\\logs\\, fuera del repositorio: la
actualización (git stash -u + git stash drop) no lo borra.

Cada incidente recibe una referencia corta que se le muestra al operario, para
poder buscarla en el archivo cuando escriba a soporte.
"""

import datetime
import os
import secrets
import threading
import traceback

from config.version import VERSION

CARPETA_LOGS = os.path.join(os.path.expanduser("~"), "Documents", "TeamComunicaciones", "logs")
_ALFABETO = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"  # sin 0/O ni 1/I para dictarlo sin confusión
_candado = threading.Lock()


def nueva_referencia():
    return "".join(secrets.choice(_ALFABETO) for _ in range(5))


def registrar(archivo, modulo, contexto, texto="", exc=None, referencia=None):
    """
    Escribe una entrada en <CARPETA_LOGS>/<archivo>. Nunca lanza excepciones.

    Returns:
        str: la referencia del incidente.
    """
    referencia = referencia or nueva_referencia()
    try:
        ahora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        lineas = [f"[{ahora}] ref={referencia} version={VERSION} modulo={modulo or '-'} contexto={contexto}"]
        if texto:
            lineas.append(f"  {texto}")
        if exc is not None:
            lineas.append(f"  {type(exc).__name__}: {exc}")
            traza = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__)).rstrip()
            lineas.extend("  " + linea for linea in traza.splitlines())
        with _candado:
            os.makedirs(CARPETA_LOGS, exist_ok=True)
            with open(os.path.join(CARPETA_LOGS, archivo), "a", encoding="utf-8") as f:
                f.write("\n".join(lineas) + "\n")
    except Exception:
        pass
    return referencia
