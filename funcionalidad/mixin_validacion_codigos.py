"""
Mixin reutilizable para agregar validación de códigos de distribuidor a un
módulo de activación (PRE-EQUIPOS, PRE-SIM, ...).

Encapsula todo lo común para no duplicarlo en cada módulo:
    - crear el checkbox on/off ("Validar códigos distribuidor"),
    - instanciar el ValidadorCodigos con la fuente propia del proceso,
    - la verificación al inicio del ciclo (leer código de sesión, cargar lista,
      decidir si abortar).

Requisitos del módulo que lo use (ya presentes en equipos.py y preactivador.py):
    - self.ventana_informacion  (con .write)
    - un objeto navegador con .read(id, 'id')  para leer 'userDataCodDistribuidor'
    - el patrón de checkbox del proyecto (recursos.checkbox)

Cada proceso configura su clave en config/codigos_bloqueados.py, de modo que las
listas de códigos son independientes por proceso.
"""

from config import codigos_bloqueados as cfg
from funcionalidad.validador_codigos import (
    ValidadorCodigos,
    FuenteNoDisponibleError,
    ValidacionCodigosError,
)


class ValidacionCodigosMixin:
    """
    Mixin de validación de códigos de distribuidor.

    El módulo anfitrión debe llamar:
        - self._init_validacion_codigos(proceso)       en __init__
        - self._codigo_distribuidor_permitido(navegador) antes del bucle

    La validación SIEMPRE está activa. Para no bloquear a nadie, el archivo de
    códigos simplemente se deja sin códigos en la columna del proceso.
    """

    def _init_validacion_codigos(self, proceso):
        """
        Prepara el validador para `proceso`. La validación es siempre activa
        (no hay checkbox): se controla poniendo/quitando códigos del archivo.

        Args:
            proceso (str): clave en config.codigos_bloqueados.COLUMNAS (p.ej. 'pre-sim').
        """
        self._proceso_validacion = proceso

        # Archivo único compartido; cada proceso lee su propia columna.
        # El modo de acceso (directo / graph) se define en la config.
        columna = cfg.columna_de(proceso)
        if getattr(cfg, 'MODO_ACCESO', 'directo') == 'graph':
            from funcionalidad.graph_downloader import GraphDownloader
            descargador = GraphDownloader(cfg.GRAPH, cfg.graph_client_secret()).descargar
            self._validador_codigos = ValidadorCodigos(
                columna=columna,
                formato=cfg.FORMATO_FUENTE,
                descargador=descargador,
            )
        else:
            self._validador_codigos = ValidadorCodigos(
                url=cfg.URL_FUENTE,
                columna=columna,
                formato=cfg.FORMATO_FUENTE,
            )

    def _leer_codigo_distribuidor_sesion(self, navegador):
        """Lee el código de distribuidor de la sesión de Poliedro (userDataCodDistribuidor)."""
        try:
            return navegador.read('userDataCodDistribuidor', 'id')
        except Exception:
            return None

    def _codigo_distribuidor_permitido(self, navegador):
        """
        Verifica, al inicio del ciclo, si la sesión puede operar.

        La validación SIEMPRE se ejecuta (no hay checkbox). Descarga la lista y
        compara el código de la sesión:
            * código bloqueado      -> False (el módulo debe abortar el ciclo)
            * fuente no disponible  -> False + aviso (política "avisar y detener")
            * código permitido      -> True
        Si el archivo no tiene códigos en la columna del proceso, ningún código
        estará bloqueado y el proceso continúa normalmente.

        Returns:
            bool: True si se puede continuar; False si hay que abortar.
        """
        codigo = self._leer_codigo_distribuidor_sesion(navegador)
        if not codigo or not str(codigo).strip():
            self.ventana_informacion.write(
                '⚠️ Validación activa pero no se pudo leer el código de distribuidor de la sesión. '
                'Se detiene el proceso por seguridad.'
            )
            return False

        try:
            cantidad = self._validador_codigos.cargar(forzar=True)
            self.ventana_informacion.write(f'🔎 Lista de códigos bloqueados cargada ({cantidad} códigos).')
        except FuenteNoDisponibleError as e:
            self.ventana_informacion.write(
                f'⚠️ No se pudo cargar la lista de códigos bloqueados: {e} '
                'Se detiene el proceso; revise la conexión/enlace y reintente con START.'
            )
            return False
        except ValidacionCodigosError as e:
            self.ventana_informacion.write(f'⚠️ Error en validación de códigos: {e} Se detiene el proceso.')
            return False

        if self._validador_codigos.esta_bloqueado(codigo):
            self.ventana_informacion.write(
                f'⛔ Código de distribuidor {codigo} está BLOQUEADO para este proceso. '
                'No se realizarán activaciones.'
            )
            return False

        self.ventana_informacion.write(f'✅ Código de distribuidor {codigo} permitido. Continuando.')
        return True
