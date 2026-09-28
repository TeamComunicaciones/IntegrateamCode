"""
Perfiles de credenciales de Poliedro, compartidos por los módulos que usan Poliedro.

Un perfil es un usuario de Poliedro con su clave, el método por el que llega el
OTP y las credenciales del buzón de correo del operario.

Los perfiles recordados se guardan en el Administrador de credenciales de Windows
(cifrados y atados a la cuenta de Windows), fuera de la carpeta del repositorio,
así que sobreviven a las actualizaciones. Se usa win32ctypes, que ya viene con
pywin32-ctypes (req.txt): no hay que instalar nada.

Además hay un perfil "activo" en memoria, el que muestra el modal de credenciales
y el que toma cada módulo al pulsar START.
"""

import copy
import json
import threading

try:
    from win32ctypes.pywin32 import win32cred
except Exception:  # pragma: no cover - solo si falta la librería
    win32cred = None


METODO_CORREO = "correo"
METODO_MYSMS = "mysms"
METODO_GOOGLE = "google"
METODOS = (METODO_CORREO, METODO_MYSMS, METODO_GOOGLE)

_PREFIJO = "IntegrateamCode/perfil/"
_INDICE = "IntegrateamCode/perfiles"
_ERROR_NO_ENCONTRADO = 1168  # ERROR_NOT_FOUND de Windows

CAMPOS = ("usuario_poliedro", "clave_poliedro", "metodo_otp", "usuario_correo", "clave_correo")


class ErrorAlmacenCredenciales(Exception):
    """No se pudo leer o escribir en el Administrador de credenciales de Windows."""


def perfil_vacio():
    return {
        "usuario_poliedro": "",
        "clave_poliedro": "",
        "metodo_otp": METODO_CORREO,
        "usuario_correo": "",
        "clave_correo": "",
    }


def normalizar_perfil(perfil):
    """Devuelve un perfil con todos los campos, recortados y con método válido."""
    base = perfil_vacio()
    for campo in CAMPOS:
        valor = (perfil or {}).get(campo, base[campo])
        base[campo] = (valor or "").strip() if campo in ("usuario_poliedro", "usuario_correo", "metodo_otp") else (valor or "")
    if base["metodo_otp"] not in METODOS:
        base["metodo_otp"] = METODO_CORREO
    return base


def campos_faltantes(perfil):
    """Lista de nombres legibles de lo que falta para poder iniciar sesión."""
    p = normalizar_perfil(perfil)
    faltan = []
    if not p["usuario_poliedro"]:
        faltan.append("usuario de Poliedro")
    if not p["clave_poliedro"]:
        faltan.append("clave de Poliedro")
    if p["metodo_otp"] == METODO_CORREO:
        if not p["usuario_correo"]:
            faltan.append("usuario del correo")
        if not p["clave_correo"]:
            faltan.append("clave del correo")
    return faltan


def esta_completo(perfil):
    return not campos_faltantes(perfil)


# --------------------------------------------------------------------------- #
# Perfil activo en memoria (compartido por toda la app).
# --------------------------------------------------------------------------- #
_candado = threading.Lock()
_activo = None


def perfil_activo():
    """Copia del perfil activo (o uno vacío). Cada módulo guarda su propia copia al pulsar START."""
    global _activo
    with _candado:
        if _activo is None:
            _activo = _perfil_inicial()
        return copy.deepcopy(_activo)


def fijar_perfil_activo(perfil):
    global _activo
    with _candado:
        _activo = normalizar_perfil(perfil)


def _perfil_inicial():
    try:
        usuario = ultimo_usado()
        if usuario:
            perfil = cargar(usuario)
            if perfil:
                return perfil
    except ErrorAlmacenCredenciales:
        pass
    return perfil_vacio()


# --------------------------------------------------------------------------- #
# Almacén en el Administrador de credenciales de Windows.
# --------------------------------------------------------------------------- #
def disponible():
    return win32cred is not None


def _leer(objetivo):
    if win32cred is None:
        raise ErrorAlmacenCredenciales("win32ctypes no está disponible")
    try:
        cred = win32cred.CredRead(objetivo, win32cred.CRED_TYPE_GENERIC)
    except Exception as e:
        if getattr(e, "winerror", None) == _ERROR_NO_ENCONTRADO:
            return None
        raise ErrorAlmacenCredenciales(f"CredRead {objetivo}: {e}") from e
    if not cred:
        return None
    blob = cred.get("CredentialBlob") or b""
    try:
        return json.loads(blob.decode("utf-16-le")) if blob else None
    except ValueError as e:
        raise ErrorAlmacenCredenciales(f"contenido ilegible en {objetivo}: {e}") from e


def _escribir(objetivo, datos, usuario=""):
    if win32cred is None:
        raise ErrorAlmacenCredenciales("win32ctypes no está disponible")
    try:
        win32cred.CredWrite({
            "Type": win32cred.CRED_TYPE_GENERIC,
            "TargetName": objetivo,
            "UserName": usuario or "IntegrateamCode",
            "CredentialBlob": json.dumps(datos, ensure_ascii=False),
            "Persist": win32cred.CRED_PERSIST_LOCAL_MACHINE,
            "Comment": "IntegrateamCode - credenciales de Poliedro",
        })
    except Exception as e:
        raise ErrorAlmacenCredenciales(f"CredWrite {objetivo}: {e}") from e


def _borrar(objetivo):
    if win32cred is None:
        raise ErrorAlmacenCredenciales("win32ctypes no está disponible")
    try:
        win32cred.CredDelete(objetivo, win32cred.CRED_TYPE_GENERIC)
    except Exception as e:
        if getattr(e, "winerror", None) == _ERROR_NO_ENCONTRADO:
            return
        raise ErrorAlmacenCredenciales(f"CredDelete {objetivo}: {e}") from e


def _leer_indice():
    datos = _leer(_INDICE) or {}
    usuarios = [u for u in datos.get("usuarios", []) if isinstance(u, str) and u]
    return {"usuarios": usuarios, "ultimo": datos.get("ultimo") or ""}


def listar():
    """Usuarios de Poliedro con perfil recordado en este equipo."""
    return list(_leer_indice()["usuarios"])


def ultimo_usado():
    return _leer_indice()["ultimo"]


def cargar(usuario_poliedro):
    """Perfil recordado de ese usuario, o None."""
    datos = _leer(_PREFIJO + usuario_poliedro.strip())
    return normalizar_perfil(datos) if datos else None


def guardar(perfil):
    """Recuerda el perfil en este equipo y lo marca como último usado."""
    p = normalizar_perfil(perfil)
    usuario = p["usuario_poliedro"]
    if not usuario:
        raise ValueError("el perfil no tiene usuario de Poliedro")
    _escribir(_PREFIJO + usuario, p, usuario)
    indice = _leer_indice()
    if usuario not in indice["usuarios"]:
        indice["usuarios"].append(usuario)
    indice["ultimo"] = usuario
    _escribir(_INDICE, indice)


def marcar_ultimo(usuario_poliedro):
    indice = _leer_indice()
    if usuario_poliedro in indice["usuarios"]:
        indice["ultimo"] = usuario_poliedro
        _escribir(_INDICE, indice)


def olvidar(usuario_poliedro):
    """Borra el perfil de este equipo. No toca los demás perfiles."""
    usuario = usuario_poliedro.strip()
    _borrar(_PREFIJO + usuario)
    indice = _leer_indice()
    indice["usuarios"] = [u for u in indice["usuarios"] if u != usuario]
    if indice["ultimo"] == usuario:
        indice["ultimo"] = indice["usuarios"][-1] if indice["usuarios"] else ""
    _escribir(_INDICE, indice)
