"""
Validador reutilizable de códigos de distribuidor bloqueados.

Diseñado para ser independiente de la UI y de Selenium: recibe la URL de una
fuente remota (CSV/XLSX de descarga directa), la descarga y permite consultar
si un código de distribuidor está bloqueado.

Pensado para reutilizarse en cualquier proceso (PRE-EQUIPOS, PRE-SIM, etc.):
cada proceso instancia su propio validador con su propia fuente, de modo que
las listas de códigos son independientes por proceso.

Notas de diseño:
- La descarga está aislada en `_descargar()` para que, si más adelante la fuente
  pasa a requerir autenticación (p. ej. Microsoft Graph) o se mueve a una carpeta
  de red, solo haya que tocar ese método.
- La política ante fallo de descarga es "avisar y detener": `cargar()` lanza
  `FuenteNoDisponibleError` para que el módulo llamador informe al operador y
  detenga el ciclo (no se asume ni bloqueo ni paso libre de forma silenciosa).
"""

import io
import csv

import requests


class ValidacionCodigosError(Exception):
    """Error base del validador de códigos."""
    pass


class FuenteNoDisponibleError(ValidacionCodigosError):
    """No se pudo descargar/leer la lista de códigos bloqueados."""
    pass


class ValidadorCodigos:
    """
    Valida códigos de distribuidor contra una lista remota de códigos bloqueados.

    Uso típico:
        validador = ValidadorCodigos(url, columna='codigo')
        validador.cargar()                    # descarga la lista (puede lanzar FuenteNoDisponibleError)
        if validador.esta_bloqueado(codigo):  # consulta
            ...
    """

    def __init__(self, url=None, columna=None, formato='csv', timeout=15, descargador=None):
        """
        Args:
            url (str|None): URL de descarga directa de la fuente (CSV/XLSX). Se usa
                en el modo directo. Ignorado si se pasa `descargador`.
            columna (str|None): nombre de la columna con los códigos. Si es None,
                se usa la primera columna del archivo.
            formato (str): 'csv' o 'xlsx'.
            timeout (int): timeout de la descarga en segundos.
            descargador (callable|None): función sin argumentos que devuelve los
                bytes del archivo. Permite inyectar otra fuente (p. ej. Microsoft
                Graph) sin acoplar el validador a ella. Si se pasa, tiene prioridad
                sobre `url`.
        """
        self.url = url
        self.columna = columna
        self.formato = (formato or 'csv').lower()
        self.timeout = timeout
        self._descargador = descargador
        self._bloqueados = None  # set de códigos normalizados; None = aún no cargado

    # ------------------------------------------------------------------ #
    # Normalización
    # ------------------------------------------------------------------ #
    @staticmethod
    def normalizar(codigo):
        """Normaliza un código para comparar de forma robusta (trim + mayúsculas)."""
        return str(codigo).strip().upper()

    # ------------------------------------------------------------------ #
    # Descarga (aislada para poder cambiar de fuente sin tocar el resto)
    # ------------------------------------------------------------------ #
    def _descargar(self):
        """Descarga el contenido crudo de la fuente. Lanza FuenteNoDisponibleError."""
        # Modo inyectado (p. ej. Microsoft Graph): delega la descarga.
        if self._descargador is not None:
            try:
                return self._descargador()
            except FuenteNoDisponibleError:
                raise
            except Exception as e:
                raise FuenteNoDisponibleError(f"No se pudo descargar la lista de códigos: {e}") from e

        # Modo directo: URL pública de descarga directa.
        if not self.url:
            raise FuenteNoDisponibleError("No hay URL configurada para la lista de códigos bloqueados.")
        try:
            resp = requests.get(self.url, timeout=self.timeout)
            resp.raise_for_status()
        except requests.RequestException as e:
            raise FuenteNoDisponibleError(f"No se pudo descargar la lista de códigos: {e}") from e

        # Si en vez del archivo llega una página de login (SharePoint pidiendo auth),
        # el contenido será HTML. Lo detectamos para dar un mensaje claro.
        content_type = (resp.headers.get('Content-Type') or '').lower()
        if 'text/html' in content_type:
            raise FuenteNoDisponibleError(
                "La fuente devolvió una página web (posible login requerido), no el archivo. "
                "Verifique que el enlace sea de descarga directa sin inicio de sesión."
            )
        return resp.content

    # ------------------------------------------------------------------ #
    # Parseo
    # ------------------------------------------------------------------ #
    def _parsear(self, contenido):
        """Convierte el contenido descargado en un set de códigos normalizados."""
        if self.formato == 'xlsx':
            codigos = self._parsear_xlsx(contenido)
        else:
            codigos = self._parsear_csv(contenido)

        bloqueados = {self.normalizar(c) for c in codigos if str(c).strip()}
        return bloqueados

    def _parsear_csv(self, contenido):
        texto = contenido.decode('utf-8-sig', errors='replace')
        lector = csv.DictReader(io.StringIO(texto))
        columna = self._resolver_columna(lector.fieldnames)
        return [fila.get(columna, '') for fila in lector]

    def _parsear_xlsx(self, contenido):
        # Import local: openpyxl solo se necesita si la fuente es xlsx.
        import openpyxl
        wb = openpyxl.load_workbook(io.BytesIO(contenido), read_only=True, data_only=True)
        ws = wb.active
        filas = ws.iter_rows(values_only=True)
        try:
            encabezados = [str(h).strip() if h is not None else '' for h in next(filas)]
        except StopIteration:
            return []
        idx = self._resolver_indice_columna(encabezados)
        return [fila[idx] for fila in filas if idx < len(fila) and fila[idx] is not None]

    def _resolver_columna(self, fieldnames):
        if not fieldnames:
            raise FuenteNoDisponibleError("La lista de códigos está vacía o sin encabezados.")
        if self.columna:
            if self.columna not in fieldnames:
                raise FuenteNoDisponibleError(
                    f"El archivo no tiene la columna '{self.columna}'. "
                    f"Columnas encontradas: {', '.join(str(c) for c in fieldnames)}."
                )
            return self.columna
        # Si no se especificó columna, usar la primera.
        return fieldnames[0]

    def _resolver_indice_columna(self, encabezados):
        if self.columna:
            if self.columna not in encabezados:
                raise FuenteNoDisponibleError(
                    f"El archivo no tiene la columna '{self.columna}'. "
                    f"Columnas encontradas: {', '.join(str(c) for c in encabezados)}."
                )
            return encabezados.index(self.columna)
        return 0

    # ------------------------------------------------------------------ #
    # API pública
    # ------------------------------------------------------------------ #
    def cargar(self, forzar=False):
        """
        Descarga y parsea la lista de códigos bloqueados.

        Args:
            forzar (bool): si ya estaba cargada, vuelve a descargar.

        Returns:
            int: cantidad de códigos bloqueados cargados.

        Raises:
            FuenteNoDisponibleError: si no se pudo descargar/leer la fuente.
        """
        if self._bloqueados is not None and not forzar:
            return len(self._bloqueados)
        contenido = self._descargar()
        self._bloqueados = self._parsear(contenido)
        return len(self._bloqueados)

    def esta_cargado(self):
        return self._bloqueados is not None

    def esta_bloqueado(self, codigo):
        """
        Indica si un código está en la lista de bloqueados.

        Requiere haber llamado `cargar()` antes; si no, lanza ValidacionCodigosError
        (para evitar dar un "no bloqueado" engañoso cuando la lista nunca se cargó).
        """
        if self._bloqueados is None:
            raise ValidacionCodigosError("La lista de códigos no ha sido cargada. Llame a cargar() primero.")
        if codigo is None:
            return False
        return self.normalizar(codigo) in self._bloqueados
