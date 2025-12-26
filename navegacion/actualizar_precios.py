from navegacion import sub_menu as sm, ventana_informacion
from recursos import label, botones, colors
from funcionalidad import web_controller, excel, scraping
from subprocess import Popen
import threading
import tkinter as tk
import customtkinter as ctk
import time
from datetime import datetime
import pandas as pd
import traceback
import re
import math

# --- Selenium helpers (usaremos el webdriver que expone self.compras.browser) ---
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


# -------------------------------------------------------
# Utilidad para parsear valores monetarios con coma/punto
# -------------------------------------------------------
def parse_money(v):
    """
    Convierte un valor (str/num) tipo dinero a float.
    - Elimina símbolos ($, COP, NBSP)
    - Quita separadores de miles (.)
    - Convierte coma decimal (,) a punto (.)
    - Devuelve float o NaN
    """
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        return float(v)

    s = str(v).strip()
    if not s:
        return math.nan

    # Normalizar espacios duros y símbolos
    s = s.replace('\u00a0', '')  # NBSP
    s = s.replace('$', '').replace('COP', '').replace('COL$', '')

    # Quitar separadores de miles (.)
    s = s.replace('.', '')
    # Convertir coma decimal a punto
    s = s.replace(',', '.')

    # Dejar solo dígitos, punto y signo
    s = re.sub(r'[^0-9\.\-]', '', s)

    try:
        return float(s)
    except ValueError:
        return math.nan


class Actualizar_precios:

    def __init__(self, master, on_of):
        self.on_of = on_of
        self.titulo = label.Label().create_label(
            master, 'ACTUALIZAR PRECIOS', 0.2, 0.0, 0.5, 0.2, letterSize=25
        )
        self.link = 'https://ventas-dot-krediapp-colombia.uw.r.appspot.com/auth/login'
        self.link2 = 'https://190.144.217.66/Front_PortalComercial/Portal/consultas/con_factura.asp'
        self.link3 = 'https://190.144.217.66/Front_PortalComercial/Portal/consultas/con_seriales_factura.asp'
        self.menu = sm.Sub_menu(
            master, 2, boton1=['START', self.ejecuccionHilo], boton2=['EXCEL', self.abrir_excel]
        )
        self.compras = ''
        self.entry_user = tk.StringVar()
        self.entry_password = tk.StringVar()
        self.entry_first_date = tk.StringVar()
        self.entry_last_Date = tk.StringVar()
        self.title_user = label.Label().create_label(
            self.menu.submenu, 'Usuario: ', 0.0, 0.50, 0.3, 0.2, letterSize=14
        )
        self.title_password = label.Label().create_label(
            self.menu.submenu, 'Clave: ', 0.0, 0.65, 0.25, 0.05, letterSize=14
        )
        input_user = ctk.CTkEntry(self.menu.submenu, textvariable=self.entry_user)
        input_user.place(relx=0.4, rely=0.58, relheight=0.05, relwidth=0.6)
        input_password = ctk.CTkEntry(self.menu.submenu, textvariable=self.entry_password)
        input_password.place(relx=0.4, rely=0.65, relheight=0.05, relwidth=0.6)
        self.ventana_informacion = ventana_informacion.Ventana_informacion(master)
        self.excel = excel.Excel_controller()

    # ------------------------------------------------------------------
    # Helper: scroll dentro del contenedor scrolleable (tabla)
    # ------------------------------------------------------------------
    def _scroll_inside_container(self, xpath: str):
        """
        Hace scroll dentro del contenedor scrolleable más cercano al nodo localizado por XPATH.
        Centra el elemento dentro del viewport del contenedor (útil para tablas con overflow).
        """
        driver = self.compras.browser
        js = r"""
        const xpath = arguments[0];
        const r = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null);
        const el = r.singleNodeValue;
        if (!el) return 'notfound';

        function getScrollableAncestor(node){
          let cur = node.parentElement;
          while (cur){
            const style = window.getComputedStyle(cur);
            const oy = style.overflowY || style.overflow;
            if (['auto','scroll'].includes(oy)){
              return cur;
            }
            cur = cur.parentElement;
          }
          return null;
        }

        const container = getScrollableAncestor(el);
        if (!container){
          return 'nocontainer';
        }

        // posicion relativa del elemento dentro del contenedor
        let offset = 0, n = el;
        while (n && n !== container){
          offset += n.offsetTop;
          n = n.offsetParent;
        }

        const target = Math.max(0, offset - (container.clientHeight/2 - el.clientHeight/2));
        container.scrollTop = target;

        return 'ok';
        """
        return driver.execute_script(js, xpath)

    # ------------------------------------------------------------------
    # Helper: escribir de forma robusta en un input localizado por XPATH
    # ------------------------------------------------------------------
    def _type_into_xpath(self, xpath: str, text: str, timeout: int = 20):
        """
        Escribe 'text' en un input XPATH con:
        - Presencia, (si se puede) visibilidad
        - Scroll dentro del contenedor scrolleable (tabla)
        - Intento de clicabilidad (corto). Si no es clickable, NO falla: usa fallback JS.
        - Clear con CTRL+A + DELETE cuando es interactuable
        - Fallback JS: set value + eventos 'input' y 'change'
        """
        driver = self.compras.browser
        wait = WebDriverWait(driver, timeout)

        # 1) Presencia en el DOM
        element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))

        # 2) Intentar visibilidad (si no, seguimos con fallback)
        try:
            WebDriverWait(driver, 3).until(EC.visibility_of(element))
        except TimeoutException:
            pass

        # 3) Scroll dentro del contenedor (tabla con overflow)
        try:
            self._scroll_inside_container(xpath)
        except Exception:
            pass

        # 4) Intentar clicabilidad con tiempo corto
        clickable = None
        try:
            clickable = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        except TimeoutException:
            clickable = None

        # 5) Si es clickable, usar send_keys normal
        if clickable is not None:
            try:
                try:
                    clickable.click()
                except Exception:
                    # probar input interno visible de PrimeNG
                    try:
                        inner = clickable.find_element(By.CSS_SELECTOR, "input.p-inputnumber-input")
                        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", inner)
                        inner.click()
                        clickable = inner
                    except Exception:
                        pass

                clickable.send_keys(Keys.CONTROL, 'a')
                clickable.send_keys(Keys.DELETE)
                clickable.send_keys(str(text))
                return 'ok'
            except Exception:
                pass  # fall back to JS

        # 6) Fallback JS (Angular/PrimeNG): set value + eventos
        js = """
        const xpath = arguments[0], value = arguments[1];
        const r = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null);
        const el = r.singleNodeValue;
        if(!el) return 'notfound';
        // buscar input visible preferentemente .p-inputnumber-input
        let input = el.matches('input') ? el : el.querySelector('input.p-inputnumber-input, input');
        if(!input) return 'noinput';
        try { input.focus(); } catch(e) {}
        input.value = '';
        input.dispatchEvent(new Event('input', {bubbles:true}));
        input.value = value;
        input.dispatchEvent(new Event('input', {bubbles:true}));
        input.dispatchEvent(new Event('change', {bubbles:true}));
        return 'ok';
        """
        res = driver.execute_script(js, xpath, str(text))
        if res != 'ok':
            raise RuntimeError(f"No se pudo escribir en {xpath}. Fallback JS={res}")
        return 'ok'

    def ejecuccionHilo(self):
        hilo_legalizador = threading.Thread(target=self.ejecuccion)
        hilo_legalizador.start()

    def abrir_excel(self):
        self.ventana_informacion.write('Abriendo resultado en Excel')
        p = Popen("src\\actualizar_precios\\openExcel.bat")
        stdout, stderr = p.communicate()

    def ejecuccion(self):
        self.on_of(False)
        self.ventana_informacion.write('Empezando ejecuccion')
        try:
            self.abrirPagina()
        except Exception as e:
            error_completo = traceback.format_exc()
            self.ventana_informacion.write(f'ERROR CRÍTICO:\n{error_completo}')
        finally:
            self.on_of(True)
            self.ventana_informacion.write('Proceso finalizado.')

    def abrirPagina(self):
        self.ventana_informacion.write('Navegador abierto')
        class Abrir_pagina1(web_controller.Web_Controller):
            pass

        self.compras = Abrir_pagina1(0)
        self.compras.openEdge()
        self.compras.selectPage(self.link)
        self.compras.insert('/html/body/app-root/app-auth/div/div/div/app-login/div/div[2]/div[2]/form/div[1]/div[1]/div/input', self.entry_user.get())
        self.compras.insert('/html/body/app-root/app-auth/div/div/div/app-login/div/div[2]/div[2]/form/div[1]/div[2]/div/input', self.entry_password.get())
        self.compras.click('/html/body/app-root/app-auth/div/div/div/app-login/div/div[2]/div[2]/form/div[3]/button')
        self.compras.click('/html/body/app-root/app-app/main/div/div/app-sidebar/aside/div[2]/div[2]/p-scrollpanel/div/div[1]/div/app-menu/div/div/ul/li/div[2]/ul/li[5]/a')
        self.compras.click('/html/body/app-root/app-app/main/div/div/app-sidebar/aside/div[2]/div[2]/p-scrollpanel/div/div[1]/div/app-menu/div/div/ul/li/div[2]/ul/li[5]/div/ul/li[2]/a/span')
        self.compras.click('/html/body/app-root/app-tpl-logged-in/div[1]/div/div/div/div/app-product-batch-edit/div/div[2]/div[2]/button')

        time.sleep(5)
        html = self.compras.retornarHtml()
        soup = scraping.Scraping(html)
        data = soup.extrarDataTablas()

        # productos: diccionario por código visible en la tabla de la página
        # data[row] -> [col0, col1(codigo), col2(nombre), col3(minimo), ..., col-1(maximo)]
        productos = {
            data[row][1]: {
                'id': row,
                'nombre': data[row][2],
                'minimo': data[row][3],
                'maximo': data[row][-1]
            }
            for row in range(len(data)) if row != 0
        }

        # -------------------------------------------------------
        # Leer Excel (la función interna puede normalizar columnas)
        # -------------------------------------------------------
        self.excel.leer_excel('src\\actualizar_precios\\actualizar_precios.xlsx', 'codigo')

        # Detección flexible de nombres de columnas por si vienen con mayúsculas o acentos
        df = self.excel.excel
        col_codigo = None
        col_precio = None

        candidatos_codigo = ['codigo', 'Código', 'CODIGO', 'Codigo']
        candidatos_precio = ['precio', 'Precio', 'PRECIO']

        for c in candidatos_codigo:
            if c in df.columns:
                col_codigo = c
                break
        if col_codigo is None:
            mapa_lower = {c.lower(): c for c in df.columns}
            for c in candidatos_codigo:
                if c.lower() in mapa_lower:
                    col_codigo = mapa_lower[c.lower()]
                    break

        for c in candidatos_precio:
            if c in df.columns:
                col_precio = c
                break
        if col_precio is None:
            mapa_lower = {c.lower(): c for c in df.columns}
            for c in candidatos_precio:
                if c.lower() in mapa_lower:
                    col_precio = mapa_lower[c.lower()]
                    break

        if col_codigo is None or col_precio is None:
            raise KeyError(
                f"No se encontraron columnas esperadas en el Excel. "
                f"Disponibles: {list(df.columns)}. "
                f"Se esperaba alguna de {candidatos_codigo} para código y {candidatos_precio} para precio."
            )

        # ----------------------------
        # Normalizar lista de productos
        # ----------------------------
        lista_productos = []
        for i in range(len(df)):
            codigo_val = df[col_codigo].iloc[i]
            precio_val = df[col_precio].iloc[i]
            lista_productos.append({
                'codigo': str(codigo_val).strip() if pd.notna(codigo_val) else '',
                'precio': parse_money(precio_val)
            })

        codigos_en_excel = {str(item['codigo']) for item in lista_productos if item['codigo']}

        # Nombre de columna de salida
        nombre_col_resultado = 'Resultado Ejecucion'

        # ----------------------------
        # Recorrido principal
        # ----------------------------
        for row in range(len(lista_productos)):
            self.ventana_informacion.write(f'Procesando registro {row + 1} de {len(lista_productos)}')
            i = lista_productos[row]

            codigo = str(i['codigo'])
            precio_num = i['precio']

            if not codigo:
                self.excel.guardar(row, nombre_col_resultado, 'codigo vacío en Excel', destino='src\\actualizar_precios\\actualizar_precios.xlsx')
                continue

            if codigo in productos.keys():
                linea = productos[codigo]['id']
                minimo = parse_money(productos[codigo]['minimo'])
                maximo = parse_money(productos[codigo]['maximo'])

                if not (pd.notna(minimo) and pd.notna(maximo) and pd.notna(precio_num)):
                    texto = (f'no se pudo parsear alguno: '
                             f'precio_excel={df[col_precio].iloc[row]}, '
                             f'minimo_pagina={productos[codigo]["minimo"]}, '
                             f'maximo_pagina={productos[codigo]["maximo"]}')
                    self.excel.guardar(row, nombre_col_resultado, texto, destino='src\\actualizar_precios\\actualizar_precios.xlsx')
                    continue

                if minimo <= precio_num <= maximo:
                    # Check
                    xpath_checkbox = (
                        f'/html/body/app-root/app-tpl-logged-in/div[1]/div/div/div/div/'
                        f'app-product-batch-edit-by-product/div/div[3]/form/div/div[1]/p-table/div/div/'
                        f'table/tbody/tr[{linea}]/td[1]/p-checkbox/div/div[2]'
                    )
                    self.compras.js_click(xpath_checkbox)

                    # XPATH del input de precio
                    xpath_input = (
                        f'/html/body/app-root/app-tpl-logged-in/div[1]/div/div/div/div/'
                        f'app-product-batch-edit-by-product/div/div[3]/form/div/div[1]/p-table/div/div/'
                        f'table/tbody/tr[{linea}]/td[5]/div/p-inputnumber/span/input'
                    )

                    # Desplazar dentro del contenedor de la tabla hacia la fila
                    xpath_row = (
                        f'/html/body/app-root/app-tpl-logged-in/div[1]/div/div/div/div/'
                        f'app-product-batch-edit-by-product/div/div[3]/form/div/div[1]/p-table/div/div/'
                        f'table/tbody/tr[{linea}]'
                    )
                    try:
                        self._scroll_inside_container(xpath_row)
                    except Exception:
                        pass

                    # Esperar a que el input no esté disabled/readonly (si falla, igual intentamos con fallback JS)
                    try:
                        WebDriverWait(self.compras.browser, 10).until(lambda d: d.execute_script(
                            "const r=document.evaluate(arguments[0],document,null,XPathResult.FIRST_ORDERED_NODE_TYPE,null);"
                            "const el=r.singleNodeValue; const i=el&&el.matches('input')?el:el&&el.querySelector('input');"
                            "return i && !i.hasAttribute('disabled') && !i.hasAttribute('readonly');",
                            xpath_input
                        ))
                    except TimeoutException:
                        pass

                    # Input precio (si es entero, escribir sin .0)
                    precio_texto = str(int(precio_num)) if float(precio_num).is_integer() else str(precio_num)

                    # Usar helper robusto para escribir (hará scroll interno y fallback JS si es necesario)
                    self._type_into_xpath(xpath_input, precio_texto)

                    self.excel.guardar(row, nombre_col_resultado, 'exitosa', destino='src\\actualizar_precios\\actualizar_precios.xlsx')
                else:
                    texto = f'{precio_num} no está dentro del rango {minimo} a {maximo}'
                    self.excel.guardar(row, nombre_col_resultado, texto, destino='src\\actualizar_precios\\actualizar_precios.xlsx')
            else:
                self.excel.guardar(row, nombre_col_resultado, 'codigo no encontrado en la pagina', destino='src\\actualizar_precios\\actualizar_precios.xlsx')

        # --------------------------------------------------------
        # Verificar productos en página que no están en el Excel
        # --------------------------------------------------------
        self.ventana_informacion.write('Verificando productos de la pagina sin correspondencia en Excel...')
        cantidad = len(lista_productos)
        for codigo_pagina, datos_producto in productos.items():
            if codigo_pagina not in codigos_en_excel:
                nombre_producto = datos_producto['nombre']
                self.excel.guardar(cantidad, 'codigo', codigo_pagina, destino='src\\actualizar_precios\\actualizar_precios.xlsx', nuevo=True)
                self.excel.guardar(cantidad, 'Producto', nombre_producto, destino='src\\actualizar_precios\\actualizar_precios.xlsx')
                self.excel.guardar(cantidad, 'Resultado Ejecucion', 'producto en pagina pero no en excel', destino='src\\actualizar_precios\\actualizar_precios.xlsx')
                cantidad += 1

        self.abrir_excel()
