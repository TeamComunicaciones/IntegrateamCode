"""
Lectura del código OTP de Poliedro desde el buzón de correo del operario (IMAP).

No usa el navegador: se conecta al mismo servidor IMAP que usa el webmail.

Cómo se identifica el correo correcto:
    1. Antes de pedir el código se anota el UID más alto de la bandeja (línea base).
       El servidor asigna los UID en orden creciente y no los reutiliza.
    2. Solo se aceptan correos con UID mayor a la línea base, del remitente
       configurado y con la palabra configurada en el asunto.
    3. Si hay varios, se toma el de UID más alto.
    4. El código es el grupo de dígitos del largo configurado; si hay varios, el
       más cercano a "código"/"OTP". Si sigue la duda, no se adivina.

Nunca marca correos como leídos ni borra nada: la bandeja se abre en solo lectura
y el contenido se pide con BODY.PEEK.
"""

import email
import html
import imaplib
import re
import socket
import ssl
import time
import unicodedata
from email import policy
from email.header import decode_header, make_header
from email.utils import parseaddr

from config import otp_correo as cfg


# --------------------------------------------------------------------------- #
# Errores: cada uno trae el texto para el operario y el detalle técnico aparte.
# --------------------------------------------------------------------------- #
class ErrorOtpCorreo(Exception):
    """Error base de la lectura del OTP por correo."""

    def __init__(self, mensaje_usuario, detalle=None):
        super().__init__(mensaje_usuario)
        self.mensaje_usuario = mensaje_usuario
        self.detalle = detalle or mensaje_usuario


class CorreoConexionError(ErrorOtpCorreo):
    """No se pudo conectar con el servidor de correo."""


class CorreoCredencialesError(ErrorOtpCorreo):
    """El servidor rechazó el usuario o la clave del correo."""


class OtpNoLlegoError(ErrorOtpCorreo):
    """No llegó el correo con el código en el tiempo de espera."""


class OtpAmbiguoError(ErrorOtpCorreo):
    """El correo trae varios números y no se puede saber cuál es el código."""


class CorreoNoReconocidoError(ErrorOtpCorreo):
    """Llegó un correo del remitente pero no tiene la forma esperada."""


# --------------------------------------------------------------------------- #
# Funciones puras (sin red): extracción del texto y del código.
# --------------------------------------------------------------------------- #
def normalizar(texto):
    """Minúsculas y sin tildes, para comparar sin depender de cómo se escribió."""
    sin_tildes = unicodedata.normalize("NFKD", texto or "")
    sin_tildes = "".join(c for c in sin_tildes if not unicodedata.combining(c))
    return sin_tildes.lower()


def texto_cabecera(valor):
    try:
        return str(make_header(decode_header(valor or "")))
    except Exception:
        return valor or ""


def texto_del_mensaje(mensaje):
    """Texto plano del correo; si solo hay HTML, se le quitan las etiquetas."""
    cuerpo = mensaje.get_body(preferencelist=("plain", "html"))
    if cuerpo is None:
        return ""
    contenido = cuerpo.get_content()
    if cuerpo.get_content_type() == "text/html":
        contenido = re.sub(r"(?is)<(script|style).*?</\1>", " ", contenido)
        contenido = re.sub(r"<[^>]+>", " ", contenido)
        contenido = html.unescape(contenido)
    return re.sub(r"\s+", " ", contenido).strip()


def extraer_codigo(texto, digitos_min=cfg.DIGITOS_MIN, digitos_max=cfg.DIGITOS_MAX,
                   palabras=cfg.PALABRAS_CERCANAS):
    """
    Devuelve el código OTP contenido en `texto`.

    Raises:
        CorreoNoReconocidoError: no hay ningún número del largo esperado.
        OtpAmbiguoError: hay varios y ninguno está claramente más cerca de las palabras clave.
    """
    patron = r"(?<!\d)\d{%d,%d}(?!\d)" % (digitos_min, digitos_max)
    candidatos = [(m.group(), m.start()) for m in re.finditer(patron, texto or "")]
    distintos = {valor for valor, _ in candidatos}

    if not distintos:
        raise CorreoNoReconocidoError(
            "Llegó el correo de Claro, pero no trae un código de "
            f"{digitos_min} a {digitos_max} dígitos. Avise a soporte.",
            detalle="extraer_codigo: 0 candidatos",
        )
    if len(distintos) == 1:
        return distintos.pop()

    # Varios números: el más cercano a una palabra clave.
    texto_norm = normalizar(texto)
    posiciones = [m.start() for p in palabras for m in re.finditer(re.escape(normalizar(p)), texto_norm)]
    if not posiciones:
        raise OtpAmbiguoError(
            "El correo de Claro trae varios números y no se pudo saber cuál es el código. Avise a soporte.",
            detalle=f"extraer_codigo: {len(distintos)} candidatos, sin palabras clave",
        )
    distancia = {}
    for valor, inicio in candidatos:
        d = min(abs(inicio - p) for p in posiciones)
        distancia[valor] = min(d, distancia.get(valor, d))
    orden = sorted(distancia.items(), key=lambda par: par[1])
    if orden[0][1] == orden[1][1]:
        raise OtpAmbiguoError(
            "El correo de Claro trae varios números y no se pudo saber cuál es el código. Avise a soporte.",
            detalle=f"extraer_codigo: empate entre {len(distintos)} candidatos",
        )
    return orden[0][0]


def uids_posteriores(respuesta_search, linea_base):
    """
    Convierte la respuesta de 'UID SEARCH' en enteros mayores a la línea base.

    IMAP devuelve el último correo aunque no haya ninguno posterior ("N:*"),
    por eso se filtra otra vez. Se comparan como enteros, no como texto.
    """
    if not respuesta_search or not respuesta_search[0]:
        return []
    return sorted(int(u) for u in respuesta_search[0].split() if int(u) > linea_base)


def es_del_remitente(cabecera_from, remitente=cfg.REMITENTE):
    return parseaddr(texto_cabecera(cabecera_from))[1].strip().lower() == remitente.lower()


def asunto_valido(cabecera_subject, palabra=cfg.PALABRA_ASUNTO):
    return normalizar(palabra) in normalizar(texto_cabecera(cabecera_subject))


# --------------------------------------------------------------------------- #
# Proveedor del OTP por correo.
# --------------------------------------------------------------------------- #
class ProveedorOtpCorreo:
    """
    Uso:
        proveedor = ProveedorOtpCorreo(usuario, clave, avisar=ventana.write)
        proveedor.probar()              # antes de tocar Poliedro
        proveedor.tomar_linea_base()    # antes de enviar credenciales a Poliedro
        ...                             # Poliedro envía el correo
        codigo = proveedor.esperar_codigo()
        proveedor.cerrar()
    """

    def __init__(self, usuario, clave, avisar=None, registrar=None):
        """
        Args:
            usuario, clave: credenciales del buzón.
            avisar (callable|None): recibe textos para el operario.
            registrar (callable|None): recibe textos técnicos para el log.
        """
        self.usuario = (usuario or "").strip()
        self.clave = clave or ""
        self._avisar = avisar or (lambda _texto: None)
        self._registrar = registrar or (lambda _texto: None)
        self._conexion = None
        self._uidvalidity = None
        self._linea_base = None
        self._hora_base = None

    # ------------------------------ conexión ------------------------------ #
    def _conectar(self):
        self.cerrar()
        try:
            conexion = imaplib.IMAP4_SSL(
                cfg.SERVIDOR_IMAP, cfg.PUERTO_IMAP,
                ssl_context=ssl.create_default_context(), timeout=cfg.TIMEOUT_RED,
            )
        except (OSError, ssl.SSLError, socket.timeout, imaplib.IMAP4.error) as e:
            raise CorreoConexionError(
                "No se pudo conectar con el servidor de correo. Revise la conexión a internet e intente de nuevo.",
                detalle=f"conectar {cfg.SERVIDOR_IMAP}:{cfg.PUERTO_IMAP}: {type(e).__name__}: {e}",
            ) from e
        try:
            conexion.login(self.usuario, self.clave)
        except imaplib.IMAP4.error as e:
            try:
                conexion.shutdown()
            except Exception:
                pass
            raise CorreoCredencialesError(
                "El correo rechazó el usuario o la clave. Revíselos en CREDENCIALES "
                "(el usuario es la dirección completa, p. ej. 123@teamcomunicaciones.com.co).",
                detalle=f"login IMAP de {self.usuario}: {e}",
            ) from e
        self._conexion = conexion
        self._seleccionar("INBOX")
        return conexion

    def _seleccionar(self, carpeta):
        """Abre una carpeta en solo lectura y devuelve (cantidad, uidvalidity)."""
        estado, datos = self._conexion.select(carpeta, readonly=True)
        if estado != "OK":
            raise CorreoConexionError(
                "No se pudo abrir la bandeja de entrada del correo.",
                detalle=f"select {carpeta}: {estado} {datos}",
            )
        _, validez = self._conexion.response("UIDVALIDITY")
        uidvalidity = int(validez[0]) if validez and validez[0] else None
        cantidad = int(datos[0]) if datos and datos[0] else 0
        return cantidad, uidvalidity

    def cerrar(self):
        if self._conexion is not None:
            try:
                self._conexion.logout()
            except Exception:
                pass
        self._conexion = None

    # ------------------------------ API ------------------------------ #
    def probar(self):
        """Comprueba acceso al buzón. Devuelve la cantidad de correos de la bandeja."""
        self._conectar()
        try:
            cantidad, _ = self._seleccionar("INBOX")
            return cantidad
        finally:
            self.cerrar()

    def tomar_linea_base(self):
        """Anota el UID más alto de la bandeja. Llamar ANTES de pedir el código a Poliedro."""
        self._conectar()
        _, self._uidvalidity = self._seleccionar("INBOX")
        _, datos = self._conexion.uid("search", None, "ALL")
        uids = [int(u) for u in datos[0].split()] if datos and datos[0] else []
        self._linea_base = max(uids) if uids else 0
        self._hora_base = time.time()
        self._registrar(f"linea base OTP correo: uid={self._linea_base} uidvalidity={self._uidvalidity}")
        return self._linea_base

    def esperar_codigo(self, timeout=None):
        """
        Espera el correo del OTP posterior a la línea base y devuelve el código.

        Raises:
            OtpNoLlegoError, CorreoNoReconocidoError, OtpAmbiguoError,
            CorreoConexionError, CorreoCredencialesError
        """
        if self._linea_base is None:
            raise ErrorOtpCorreo(
                "Error interno al esperar el código.",
                detalle="esperar_codigo sin tomar_linea_base",
            )
        timeout = cfg.TIMEOUT_ESPERA if timeout is None else timeout
        limite = time.time() + timeout
        revisados = set()
        no_reconocidos = []
        reconexiones = 0

        self._avisar(f"📧 Esperando el correo con el código (hasta {timeout} s)...")
        try:
            while time.time() < limite:
                try:
                    if self._conexion is None:
                        self._conectar()
                    nuevos = self._uids_nuevos()
                except CorreoCredencialesError:
                    raise
                except (CorreoConexionError, OSError, imaplib.IMAP4.error) as e:
                    reconexiones += 1
                    self._registrar(f"esperar_codigo: reconexión {reconexiones} por {type(e).__name__}: {e}")
                    self.cerrar()
                    if reconexiones > 3:
                        raise CorreoConexionError(
                            "Se perdió la conexión con el servidor de correo mientras se esperaba el código. "
                            "Revise la conexión a internet e intente de nuevo.",
                            detalle=f"esperar_codigo: {reconexiones} reconexiones, último error {e}",
                        ) from e
                    time.sleep(cfg.INTERVALO_SONDEO)
                    continue

                candidatos = []
                for uid in nuevos:
                    if uid in revisados:
                        continue
                    revisados.add(uid)
                    remitente, asunto = self._cabeceras(uid)
                    if not es_del_remitente(remitente):
                        continue
                    if asunto_valido(asunto):
                        candidatos.append(uid)
                    else:
                        no_reconocidos.append(asunto)
                        self._registrar(f"correo del remitente sin la palabra del asunto: uid={uid} asunto={asunto!r}")
                        self._avisar(
                            f"⚠️ Llegó un correo de Claro que no parece un código ({texto_cabecera(asunto)}). "
                            "Sigo esperando el código."
                        )

                if candidatos:
                    if len(candidatos) > 1:
                        self._registrar(f"varios correos de OTP tras la linea base: {candidatos}; se usa el mayor")
                    uid = max(candidatos)
                    codigo = extraer_codigo(self._texto(uid))
                    self._registrar(f"OTP leído del correo uid={uid}")
                    self._avisar("✅ Código recibido por correo.")
                    return codigo

                time.sleep(cfg.INTERVALO_SONDEO)

            if no_reconocidos:
                raise CorreoNoReconocidoError(
                    "Llegó un correo de Claro, pero no parece el del código. Avise a soporte.",
                    detalle=f"timeout con correos no reconocidos: {no_reconocidos}",
                )
            raise OtpNoLlegoError(self._mensaje_no_llego(timeout), detalle=f"timeout {timeout}s sin OTP")
        finally:
            self.cerrar()

    # ------------------------------ auxiliares ------------------------------ #
    def _uids_nuevos(self):
        """UID de la bandeja posteriores a la línea base."""
        _, uidvalidity = self._seleccionar("INBOX")  # refresca la vista del buzón
        if self._uidvalidity is not None and uidvalidity != self._uidvalidity:
            # El servidor renumeró el buzón: se compara por hora de llegada.
            self._registrar(f"UIDVALIDITY cambió de {self._uidvalidity} a {uidvalidity}; se usa la hora de llegada")
            return self._uids_desde_hora()
        _, datos = self._conexion.uid("search", None, f"UID {self._linea_base + 1}:*")
        return uids_posteriores(datos, self._linea_base)

    def _uids_desde_hora(self):
        desde = time.strftime("%d-%b-%Y", time.localtime(self._hora_base))
        _, datos = self._conexion.uid("search", None, f"SINCE {desde}")
        uids = [int(u) for u in datos[0].split()] if datos and datos[0] else []
        return [u for u in uids if self._llego_despues_de_base(u)]

    def _llego_despues_de_base(self, uid):
        _, partes = self._conexion.uid("fetch", str(uid), "(INTERNALDATE)")
        for parte in partes or []:
            linea = parte if isinstance(parte, bytes) else (parte[0] if parte else b"")
            fecha = imaplib.Internaldate2tuple(linea)
            if fecha is not None:
                # Margen de 60 s por diferencias de reloj entre el equipo y el servidor.
                return time.mktime(fecha) >= self._hora_base - 60
        return False

    def _cabeceras(self, uid):
        _, partes = self._conexion.uid("fetch", str(uid), "(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT)])")
        crudo = next((p[1] for p in partes or [] if isinstance(p, tuple)), b"")
        cab = email.message_from_bytes(crudo)
        return cab.get("From", ""), cab.get("Subject", "")

    def _texto(self, uid):
        _, partes = self._conexion.uid("fetch", str(uid), "(BODY.PEEK[])")
        crudo = next((p[1] for p in partes or [] if isinstance(p, tuple)), b"")
        return texto_del_mensaje(email.message_from_bytes(crudo, policy=policy.default))

    def _mensaje_no_llego(self, timeout):
        """Mensaje de 'no llegó'; si el correo cayó en spam, lo dice."""
        carpeta = self._carpeta_con_otp_reciente()
        if carpeta:
            return (
                f"El correo con el código llegó a la carpeta '{carpeta}' del correo, no a la bandeja de entrada. "
                "Marque a no-reply@gpin.com.co como remitente seguro en el webmail e intente de nuevo."
            )
        return (
            f"No llegó el correo con el código en {timeout} segundos. "
            "Verifique en el webmail si llegó e intente de nuevo; si no llega, avise a soporte."
        )

    def _carpeta_con_otp_reciente(self):
        try:
            self._conectar()
            for carpeta in cfg.CARPETAS_EXTRA:
                try:
                    estado, _ = self._conexion.select(carpeta, readonly=True)
                except imaplib.IMAP4.error:
                    continue
                if estado != "OK":
                    continue
                desde = time.strftime("%d-%b-%Y", time.localtime(self._hora_base))
                _, datos = self._conexion.uid("search", None, f'SINCE {desde} FROM "{cfg.REMITENTE}"')
                uids = [int(u) for u in datos[0].split()] if datos and datos[0] else []
                if any(self._llego_despues_de_base(u) for u in uids):
                    return carpeta
        except Exception as e:
            self._registrar(f"revisión de carpetas extra falló: {type(e).__name__}: {e}")
        finally:
            self.cerrar()
        return None
