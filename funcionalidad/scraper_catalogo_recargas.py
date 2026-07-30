"""
Scraper del catálogo de Grupos y Servicios del portal de recargas.

Obtiene, directamente de la página, la relación dependiente grupo -> servicios
(los servicios disponibles cambian según el grupo). El resultado alimenta un
Excel de catálogo que reemplaza las listas antes hardcodeadas.

Diseño:
- Independiente de la UI (tkinter): recibe un web_controller ya logueado y
  posicionado en el formulario de paquetes, y devuelve la estructura leída.
- Lee por TEXTO (no por id), porque los ids de Angular cambian entre sesiones.
- No realiza ninguna recarga: solo abre dropdowns y lee opciones.
"""

import time


# XPaths de las opciones dentro de los dropdowns abiertos (componentes ng-select).
# Se leen los <span class="ng-option-label"> visibles cuando el panel está abierto.
_XPATH_OPCIONES = "//div[contains(@class,'ng-dropdown-panel')]//span[contains(@class,'ng-option-label')]"


class ScraperCatalogoRecargas:
    """Lee la relación grupo -> servicios desde el formulario de paquetes."""

    def __init__(self, recargas, logger=None, pausa=0.6):
        """
        Args:
            recargas: web_controller ya logueado y en el formulario de paquetes.
            logger: callable opcional para reportar progreso (p. ej.
                ventana_informacion.write).
            pausa: espera tras abrir un dropdown para que Angular renderice.
        """
        self.recargas = recargas
        self.logger = logger
        self.pausa = pausa

    def _log(self, msg):
        if self.logger:
            try:
                self.logger(msg)
            except Exception:
                pass

    def _abrir_dropdown(self, id_dropdown):
        self.recargas.click(id_dropdown, 'id')
        time.sleep(self.pausa)

    def _leer_opciones_abiertas(self):
        """Devuelve la lista de textos de las opciones del dropdown abierto."""
        opciones = self.recargas.listarElemetos(_XPATH_OPCIONES, 'xpath')
        # Limpiar espacios (el portal a veces trae 'Reventa ' con espacio final).
        return [o.strip() for o in opciones if o and o.strip()]

    def _cerrar_dropdown(self, id_dropdown):
        # Volver a hacer click en el control cierra el panel abierto.
        try:
            self.recargas.click(id_dropdown, 'id')
            time.sleep(0.2)
        except Exception:
            pass

    def scrape(self):
        """
        Lee todos los grupos y, por cada uno, sus servicios.

        Returns:
            list[tuple[str, str]]: pares (grupo, servicio), uno por servicio.

        Raises:
            Exception: si no se pudo leer ningún grupo (formulario no disponible).
        """
        self._log("🔎 Leyendo grupos disponibles...")
        self._abrir_dropdown('groupSelect')
        grupos = self._leer_opciones_abiertas()
        self._cerrar_dropdown('groupSelect')

        if not grupos:
            raise Exception(
                "No se pudieron leer los grupos. Verifique que esté en el "
                "formulario de paquetes y que la página haya cargado."
            )
        self._log(f"   {len(grupos)} grupos encontrados.")

        catalogo = []
        for grupo in grupos:
            # Seleccionar el grupo (abrir dropdown y elegir por texto).
            self._abrir_dropdown('groupSelect')
            try:
                self.recargas.click(f".//span[text()='{grupo}']")
            except Exception:
                # Reintento tolerante a espacios: algunos textos traen trailing space.
                self.recargas.click(f".//span[normalize-space(text())='{grupo}']")
            time.sleep(self.pausa)

            # Abrir el dropdown de servicios (ya filtrado por el grupo elegido).
            self._abrir_dropdown('subServiceSelect')
            servicios = self._leer_opciones_abiertas()
            self._cerrar_dropdown('subServiceSelect')

            self._log(f"   '{grupo}': {len(servicios)} servicios.")
            for servicio in servicios:
                catalogo.append((grupo, servicio))

        if not catalogo:
            raise Exception("Se leyeron grupos pero ningún servicio. Revise el portal.")

        self._log(f"✅ Catálogo leído: {len(catalogo)} pares grupo/servicio.")
        return catalogo
