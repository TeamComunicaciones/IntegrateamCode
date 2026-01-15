import os
from urllib.parse import urljoin, urlparse

DEFAULT_TRAFFIC_BASE = "https://prod-md.azpol.claro.com.co/"

TRAFFIC_BASE_URL = os.getenv("TRAFFIC_BASE_URL", DEFAULT_TRAFFIC_BASE).rstrip("/") + "/"

# (Opcional) lista de dominios permitidos para “autodetectar” base desde el navegador
_ALLOWED_SUFFIXES = (
    "azpol.claro.com.co",
    "traffic.claro.com.co",
)

def traffic_url(path: str) -> str:
    """Construye una URL completa a partir del base (sin duplicar slashes)."""
    return urljoin(TRAFFIC_BASE_URL, path.lstrip("/"))

def try_sync_traffic_base_from_current_url(current_url: str) -> str | None:
    """
    (Opcional) Si quieres que el bot se adapte si mañana cambian el host:
    toma el host del navegador, pero SOLO si es un dominio permitido.
    """
    p = urlparse(current_url)
    if p.scheme not in ("http", "https") or not p.netloc:
        return None
    if not p.netloc.endswith(_ALLOWED_SUFFIXES):
        return None
    return f"{p.scheme}://{p.netloc}/"