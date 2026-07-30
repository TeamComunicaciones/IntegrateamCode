"""
Descarga de archivos desde SharePoint usando Microsoft Graph API
(flujo client credentials / app-only).

Se usa cuando el archivo de códigos NO tiene enlace de descarga anónima y
SharePoint exige inicio de sesión corporativo. Aísla toda la lógica de OAuth +
Graph para que `ValidadorCodigos` no dependa de ella.

Requisitos (registro de app en Azure AD, lo provee TI del cliente):
    - tenant_id, client_id, client_secret
    - permiso de aplicación Microsoft Graph: Sites.Read.All (con admin consent)

Config esperada (dict), ver config/codigos_bloqueados.py -> GRAPH:
    {
      "tenant_id": "...",
      "client_id": "...",
      "host": "contoso.sharepoint.com",
      "site_path": "/sites/Auditoria",
      "file_path": "Documentos/archivo.xlsx",
    }
y el secret se pasa aparte (por variable de entorno).

Nota: el token se cachea en memoria y se renueva cuando está por expirar.
"""

import time

import requests


class GraphError(Exception):
    """Error al autenticar o descargar vía Microsoft Graph."""
    pass


_PLACEHOLDER_PREFIX = "REEMPLAZAR"


def _es_placeholder(valor):
    return (not valor) or str(valor).startswith(_PLACEHOLDER_PREFIX)


class GraphDownloader:
    """Descarga un archivo de SharePoint vía Microsoft Graph (app-only)."""

    def __init__(self, config, client_secret, timeout=20):
        """
        Args:
            config (dict): parámetros de Graph (ver módulo).
            client_secret (str): secret del registro de app (no se versiona).
            timeout (int): timeout de red en segundos.
        """
        self.cfg = config or {}
        self.client_secret = client_secret
        self.timeout = timeout
        self._token = None
        self._token_exp = 0  # epoch en el que expira el token cacheado

    # ------------------------------------------------------------------ #
    # Validación de configuración
    # ------------------------------------------------------------------ #
    def _validar_config(self):
        requeridos = ("tenant_id", "client_id", "host", "site_path", "file_path")
        faltantes = [k for k in requeridos if _es_placeholder(self.cfg.get(k))]
        if _es_placeholder(self.client_secret):
            faltantes.append("client_secret")
        if faltantes:
            raise GraphError(
                "Configuración de Microsoft Graph incompleta (pendiente de TI). "
                f"Faltan/placeholder: {', '.join(faltantes)}."
            )

    # ------------------------------------------------------------------ #
    # Token (client credentials)
    # ------------------------------------------------------------------ #
    def _obtener_token(self):
        # Reusar token cacheado si aún es válido (con margen de 60s).
        if self._token and time.time() < (self._token_exp - 60):
            return self._token

        url = f"https://login.microsoftonline.com/{self.cfg['tenant_id']}/oauth2/v2.0/token"
        data = {
            "client_id": self.cfg["client_id"],
            "client_secret": self.client_secret,
            "scope": "https://graph.microsoft.com/.default",
            "grant_type": "client_credentials",
        }
        try:
            resp = requests.post(url, data=data, timeout=self.timeout)
            resp.raise_for_status()
            payload = resp.json()
        except requests.RequestException as e:
            raise GraphError(f"No se pudo obtener el token de Microsoft Graph: {e}") from e
        except ValueError as e:
            raise GraphError(f"Respuesta de token inválida (no JSON): {e}") from e

        self._token = payload.get("access_token")
        if not self._token:
            raise GraphError(f"Azure AD no devolvió access_token: {payload.get('error_description', payload)}")
        self._token_exp = time.time() + int(payload.get("expires_in", 3600))
        return self._token

    def _headers(self):
        return {"Authorization": f"Bearer {self._obtener_token()}"}

    # ------------------------------------------------------------------ #
    # Descarga
    # ------------------------------------------------------------------ #
    def _resolver_site_id(self):
        host = self.cfg["host"]
        site_path = self.cfg["site_path"]
        url = f"https://graph.microsoft.com/v1.0/sites/{host}:{site_path}"
        try:
            resp = requests.get(url, headers=self._headers(), timeout=self.timeout)
            resp.raise_for_status()
            return resp.json()["id"]
        except requests.RequestException as e:
            raise GraphError(f"No se pudo resolver el sitio de SharePoint: {e}") from e
        except (ValueError, KeyError) as e:
            raise GraphError(f"Respuesta inesperada al resolver el sitio: {e}") from e

    def descargar(self):
        """
        Descarga el contenido del archivo. Devuelve bytes.

        Raises:
            GraphError: si falta configuración o falla la autenticación/descarga.
        """
        self._validar_config()
        site_id = self._resolver_site_id()
        file_path = self.cfg["file_path"].lstrip("/")
        # Descarga el contenido del archivo por ruta relativa a la biblioteca.
        url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive/root:/{file_path}:/content"
        try:
            resp = requests.get(url, headers=self._headers(), timeout=self.timeout)
            resp.raise_for_status()
        except requests.RequestException as e:
            raise GraphError(f"No se pudo descargar el archivo vía Graph: {e}") from e
        return resp.content
