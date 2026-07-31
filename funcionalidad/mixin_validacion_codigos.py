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

from recursos import checkbox
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
        - self._crear_checkbox_validacion(master, proceso)  en __init__
        - self._codigo_distribuidor_permitido(codigo)       antes del bucle
    """

    def _crear_checkbox_validacion(self, master, proceso, texto='Validar códigos distribuidor',
                                   place=False, x=None, y=None, widht=None, height=None):
        """
        Crea el checkbox on/off y prepara el validador para `proceso`.

        Args:
            master: contenedor tkinter donde va el checkbox (self.menu.submenu).
            proceso (str): clave en config.codigos_bloqueados.COLUMNAS (p.ej. 'pre-sim').
            place/x/y/widht/height: si place=True, posiciona el checkbox con
                coordenadas relativas (evita que quede apilado con pack y tape
                otros campos). Si place=False, usa el pack por defecto.
        """
        import tkinter as tk

        self._proceso_validacion = proceso
        self.validar_codigos = tk.BooleanVar(value=cfg.VALIDACION_ACTIVA_DEFAULT)
        self.checkbox_validar_codigos = checkbox.Checkbox().create_checkbox(
            master, texto, self._on_checkbox_change_validar_codigos, self.validar_codigos,
            place=place, x=x, y=y, widht=widht, height=height,
        )

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

    def _on_checkbox_change_validar_codigos(self):
        if self.validar_codigos.get():
            self.ventana_informacion.write('✅ Validación de códigos de distribuidor ACTIVADA')
            url = getattr(cfg, 'URL_ARCHIVO_HUMANO', '')
            if url:
                self.ventana_informacion.write('📄 Edite los códigos bloqueados aquí:')
                self.ventana_informacion.write(url)
        else:
            self.ventana_informacion.write('⛔ Validación de códigos de distribuidor DESACTIVADA')

    def _leer_codigo_distribuidor_sesion(self, navegador):
        """Lee el código de distribuidor de la sesión de Poliedro (userDataCodDistribuidor)."""
        try:
            return navegador.read('userDataCodDistribuidor', 'id')
        except Exception:
            return None

    def _codigo_distribuidor_permitido(self, navegador):
        """
        Verifica, al inicio del ciclo, si la sesión puede operar.

        - Si la validación está desactivada -> True (permitido).
        - Si está activada: descarga la lista y compara el código de la sesión.
            * código bloqueado      -> False (el módulo debe abortar el ciclo)
            * fuente no disponible  -> False + aviso (política "avisar y detener")
            * código permitido      -> True

        Returns:
            bool: True si se puede continuar; False si hay que abortar.
        """
        if not getattr(self, 'validar_codigos', None) or not self.validar_codigos.get():
            return True

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
