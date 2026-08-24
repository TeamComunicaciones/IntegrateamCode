import os
import re
import shutil
import tempfile
import zipfile

import pandas as pd

# Excel guarda los filtros de la hoja (Datos > Filtro) dentro del archivo, y
# openpyxl no sabe leer los de texto plano: revienta con "Value must be either
# numerical or a string containing a wildcard". Se quitan estos dos elementos.
_AUTOFILTRO_SOLO = re.compile(rb'<autoFilter[^>]*/>')
_AUTOFILTRO_PAR = re.compile(rb'<autoFilter[^>]*>.*?</autoFilter>', re.DOTALL)


class Excel_controller:

    def _copia_sin_autofiltro(self, file):
        """
        Devuelve la ruta de una copia temporal del .xlsx sin los filtros.

        Un .xlsx es un ZIP de XMLs, asi que se copia entero quitando el
        autoFilter de las hojas. El archivo original no se modifica.
        """
        destino = os.path.join(tempfile.mkdtemp(), os.path.basename(file))
        with zipfile.ZipFile(file) as origen:
            with zipfile.ZipFile(destino, 'w', zipfile.ZIP_DEFLATED) as copia:
                for elemento in origen.infolist():
                    contenido = origen.read(elemento.filename)
                    if elemento.filename.startswith('xl/worksheets/'):
                        contenido = _AUTOFILTRO_SOLO.sub(b'', contenido)
                        contenido = _AUTOFILTRO_PAR.sub(b'', contenido)
                    copia.writestr(elemento, contenido)
        return destino

    def leer_excel(self, file, tituloColumna=None, dtype=None):

        try:
            self.excel = pd.read_excel(file, dtype=dtype)
        except ValueError as error_original:
            # Puede ser un filtro guardado en el archivo: se intenta leer una
            # copia sin el. Si tampoco carga, se reporta el error de siempre.
            try:
                copia = self._copia_sin_autofiltro(file)
            except Exception:
                raise error_original
            try:
                self.excel = pd.read_excel(copia, dtype=dtype)
            except Exception:
                raise error_original
            finally:
                shutil.rmtree(os.path.dirname(copia), ignore_errors=True)
        self.cantidad = None
        if tituloColumna is not None:
            self.cantidad = len(self.excel[tituloColumna])

    def guardar(self, posicion, columna, text, destino ='src\legalizador\legalizador.xlsx', nuevo= False):
        # Verificar si la columna existe, si no, crearla
        if columna not in self.excel.columns:
            self.excel[columna] = ''  # inicializa con cadenas vacías

        # Guardar valor en la celda
        if nuevo:
            self.excel.loc[posicion] = {columna: text}
        else:
            self.excel.at[posicion, columna] = text
            self.excel.to_excel(destino, index=False)

    def borrar(self, destino):
        self.excel = pd.DataFrame(columns=self.excel.columns)
        self.excel.to_excel(destino, index=False)

    def quitarFormatoCientifico(self, tituloColumna):
        if self.cantidad is not None:
            for i in range(self.cantidad):
                #self.excel[tituloColumna][i] = " "+str(self.excel[tituloColumna][i]).strip()
                valor = str(self.excel.loc[i, tituloColumna]).strip()
                self.excel.loc[i, tituloColumna] = " " + valor
        else:
            raise('No tiene cantidad determinada en la funcion de lectura, por no agregar titulo')

    def export(self, result, file, type=True):
        if type:
            df = pd.DataFrame(result[1:], columns=result[0])
        else:
            df = result
        df.to_excel(file, index=False)
