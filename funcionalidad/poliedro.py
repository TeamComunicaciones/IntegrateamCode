from selenium.webdriver.common.keys import Keys
from urllib.parse import urlparse
import time

from config.urls import POLIEDRO_BASE_URL, TRAFFIC_BASE_URL, poliedro_url

HOST_POLIEDRO = urlparse(POLIEDRO_BASE_URL).netloc.lower()
HOST_TRAFFIC = urlparse(TRAFFIC_BASE_URL).netloc.lower()
# Puerta por la que el menú de Poliedro pasa la sesión a Traffic.
RUTA_ENTRADA_TRAFFIC = '/dispatcher/entrancepre'
XPATH_REGRESAR_POLIEDRO = '/html/body/div/div[2]/section/div/div[1]/aside/nav/div[2]/ul/li[last()]/a'
INTENTOS_ENTRADA_TRAFFIC = 3
ESPERA_ENTRADA_TRAFFIC = 45  # segundos por intento


class EntradaTrafficError(Exception):
    """Traffic no respondió al entrar desde el menú de Poliedro."""


class Poliedro:

    def __init__(self, legalizador=False):
        self.tropas = False
        self.legalizador = legalizador
    
    def manejoTropas(self,tropas):
        self.tropas = tropas

    def definirBrowser(self, browser):
        self.browser = browser

    def seleccionAcceso(self, opcion, start = True):
        if self.tropas or start:
            self._entrar_a_traffic()
        self.browser.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div[1]/div[1]/div[2]/div/span/span[1]/span/span[1]')
        self.browser.write('/html/body/span/span/span[1]/input', opcion)
        self.browser.write('/html/body/span/span/span[1]/input', Keys.ENTER)
        self.opcion = opcion

    # ------------------------------------------------------------------ #
    # Entrada a Traffic desde el menú de Poliedro
    # ------------------------------------------------------------------ #
    def _clic_menu_activacion(self):
        """Clic del menú que pasa de Poliedro a Traffic (por /dispatcher/entrancePre)."""
        if self.tropas:
            self.browser.click('//*[@id="containerNavBar"]/ul/li[*]/a/span[contains(text(),"Activación Pospago")]', 'xpath')
            self.browser.click('//*[@id="containerNavBar"]/ul/li[*]/ul/li[*]/a[contains(text(),"Activación Única Modernización")]', 'xpath')
        else:
            self.browser.click('/html/body/div/div[2]/section/div/div[1]/aside/nav/div[2]/ul/li[5]/a')
            self.browser.click('/html/body/div/div[2]/section/div/div[1]/aside/nav/div[2]/ul/li[5]/ul/li[2]')

    def _url_actual(self):
        try:
            return str(self.browser.browser.current_url or '').lower()
        except Exception:
            return ''

    def _cookies_traffic(self):
        """Cookies del navegador que pertenecen al dominio de Traffic."""
        todas = self.browser.browser.execute_cdp_cmd('Network.getAllCookies', {}).get('cookies', [])
        return [c for c in todas if c.get('domain', '').lstrip('.').lower() == HOST_TRAFFIC]

    def _borrar_cookies_traffic(self):
        """Borra las cookies viejas de Traffic, solo si el navegador está en Poliedro.

        Se llama antes del clic del menú: las cookies nuevas de Traffic se crean
        después, cuando Traffic responde en entrancePre. Si el navegador ya está
        en Traffic no se borra nada (la sesión está viva). Nunca detiene el proceso.
        """
        try:
            if urlparse(self._url_actual()).netloc != HOST_POLIEDRO:
                return
            for c in self._cookies_traffic():
                self.browser.browser.execute_cdp_cmd('Network.deleteCookies', {
                    'name': c['name'], 'domain': c['domain'], 'path': c.get('path', '/'),
                })
            quedan = self._cookies_traffic()
            if quedan:
                print(f"[Traffic] No se pudieron borrar las cookies: {[c['name'] for c in quedan]}")
        except Exception as e:
            print(f'[Traffic] Error borrando cookies de Traffic: {e}')

    def _entrada_traffic_fallida(self, url, html):
        """True si el navegador quedó en entrancePre (o en una página de error de Edge) con error."""
        en_entrada = RUTA_ENTRADA_TRAFFIC in url or url.startswith('chrome-error://')
        error_red = ('err_' in html and ('main-frame-error' in html or 'neterror' in html)) \
            or 'err_empty_response' in html
        return en_entrada and error_red

    def _esperar_entrada_traffic(self):
        """Espera a que el clic termine en Traffic. True = entró; False = falló."""
        limite = time.time() + ESPERA_ENTRADA_TRAFFIC
        while time.time() < limite:
            time.sleep(1)
            url = self._url_actual()
            try:
                html = str(self.browser.retornarHtml() or '').lower()
            except Exception:
                html = ''
            if self._entrada_traffic_fallida(url, html):
                return False
            if HOST_TRAFFIC in urlparse(url).netloc and RUTA_ENTRADA_TRAFFIC not in url:
                return True
        return False

    def _volver_a_poliedro(self):
        """Antes de reintentar: volver al menú de Poliedro como lo hacen los módulos."""
        try:
            # El menú, no la raíz: la raíz de Poliedro muestra el login aunque haya sesión.
            self.browser.selectPage(poliedro_url('POL_MENU/'))
        except Exception:
            pass
        if not self.tropas:
            try:
                self.browser.click(XPATH_REGRESAR_POLIEDRO)
            except Exception:
                pass
        time.sleep(2)

    def _entrar_a_traffic(self):
        """Borra cookies viejas de Traffic, hace el clic del menú y reintenta si Traffic no responde."""
        for intento in range(1, INTENTOS_ENTRADA_TRAFFIC + 1):
            if intento > 1:
                print(f'[Traffic] Reintentando la entrada a activaciones ({intento}/{INTENTOS_ENTRADA_TRAFFIC})')
                self._volver_a_poliedro()
            self._borrar_cookies_traffic()
            # En tropas con start=False el clic se hace ya dentro de Traffic: se mantiene igual que antes.
            venia_de_traffic = HOST_TRAFFIC in urlparse(self._url_actual()).netloc
            try:
                self._clic_menu_activacion()
            except Exception as e:
                print(f'[Traffic] Falló el clic del menú (intento {intento}): {e}')
                continue
            if venia_de_traffic or self._esperar_entrada_traffic():
                return
        raise EntradaTrafficError(
            'Traffic no respondió al entrar a activaciones (entrancePre). Intente de nuevo.')

    def seleccionNit(self):
        self.browser.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div[2]/div[1]/div[1]/div[1]/div/span/span[1]/span/span[1]')
        self.browser.write('/html/body/span/span/span[1]/input', 'nit')
        self.browser.write('/html/body/span/span/span[1]/input', Keys.ENTER)
        
    
    def rellenoFormulario(self,campos,lista):

        for i in range (campos):
            if len(lista[i]) == 2: lista[i].append('xpath')
            self.browser.eraseLetter(lista[i][0], 20, by=lista[i][2])
            time.sleep(1) 
            self.browser.insert(lista[i][0],lista[i][1],lista[i][2])
            time.sleep(1) 
    
    def detectOption(self, options, functions, NoneFunc = None, short2 = False):
        self.selectOption = None
        for i in range (len(options)):
            if len(options[i]) == 1: options[i].append('xpath')
            try:
                if short2:
                    self.browser.readShort2(options[i][0], options[i][1])
                else:
                    self.browser.readShort(options[i][0], options[i][1])
                self.selectOption = i
                break
            except:
                pass
        if self.selectOption is not None:
            func = functions[self.selectOption]
            func()
        else:
            if NoneFunc is not None:
                NoneFunc()
    
    def reinicio(self, start = True):
        try:
            if self.legalizador:                       
                self.browser.click('/html/body/div/div[2]/section/div/div[1]/aside/nav/div[2]/ul/li[12]/a/span')
                self.browser.click('/html/body/p/table[2]/tbody/tr[2]/td[1]/table/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr[12]/td[1]/a')
            else:
                self.browser.click('/html/body/div/div[2]/section/div/div[1]/aside/nav/div[2]/ul/li[12]/a')
                if self.tropas == False:
                    if self.legalizador:
                        try:
                            self.browser.click('/html/body/p/table[2]/tbody/tr[2]/td[1]/table/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr[13]/td[1]/a')
                        except:
                            self.browser.click('/html/body/p/table[2]/tbody/tr[2]/td[1]/table/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr[12]/td[1]/a')
                    else:
                        try:
                            self.browser.click('/html/body/p/table[2]/tbody/tr[2]/td[1]/table/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr[13]/td[1]/a')
                        except:
                            self.browser.click('/html/body/p/table[2]/tbody/tr[2]/td[1]/table/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr[12]/td[1]/a')
        except: 
            pass
        self.seleccionAcceso(self.opcion, start)
    
    def saludo(self):
        self.browser.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[1]/div[1]/div/span/span[1]/span/span[1]')
        self.browser.write('/html/body/span/span/span[1]/input', 'r')
        self.browser.write('/html/body/span/span/span[1]/input', Keys.ENTER)

    def correo(self, correo):
        self.browser.insert('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[1]/div[4]/div/input',correo)

    def tipoDoc(self, tipo, xpath='/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[2]/div[1]/div/span/span[1]/span/span[1]'):
        tipoDoc = self.browser.read(xpath)
        if 'Seleccione' in tipoDoc:
            self.browser.click(xpath)
            self.browser.write('/html/body/span/span/span[1]/input', tipo)
            self.browser.write('/html/body/span/span/span[1]/input', Keys.ENTER)

    def rellenoNombre(self, nombre):
        readonly = self.browser.readonly('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[1]/div[2]/div/input')
        if readonly != True:
            self.browser.insert('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[1]/div[2]/div/input', nombre)

    def rellenoApellido(self, apellido):
        readonly = self.browser.readonly('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[1]/div[3]/div/input')
        if readonly != True:
            self.browser.insert('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[1]/div[3]/div/input', apellido)
    
    def rellenoCedula(self, cedula):
        readonly = self.browser.readonly('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[2]/div[2]/div/input')
        if readonly != True:
            self.browser.insert('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[2]/div[2]/div/input', cedula)

    def rellenoNumero(self):
        try:
            self.browser.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[1]/div[5]/div[2]/fieldset/div/div[1]/div/span/span[1]/span/span[1]')
            self.browser.write('/html/body/span/span/span[1]/input', 'fijo')
            self.browser.write('/html/body/span/span/span[1]/input', Keys.ENTER)
            self.browser.click('//html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[1]/div[5]/div[2]/fieldset/div/div[2]/div/span/span[1]/span/span[1]')
            time.sleep(1)
            self.browser.write('/html/body/span/span/span[1]/input', '604')
            self.browser.write('/html/body/span/span/span[1]/input', Keys.ENTER)
            self.browser.write('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[1]/div[5]/div[2]/fieldset/div/div[3]/div/input', '3131234')
        except:
            try:
                self.browser.insert('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[1]/div[5]/div[2]/fieldset/div/div[1]/div/select', 'fijo')
                time.sleep(1)
                self.browser.insert('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[1]/div[5]/div[2]/fieldset/div/div[2]/div/select', '604')
                time.sleep(1)
                self.browser.insert('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[1]/div[5]/div[2]/fieldset/div/div[3]/div/input', '3131234')
            except:
                raise('No logra ingresar datos de Numero')

    def rellenoNumero2(self):
        try: 
            self.browser.waitExist('PhoneClass', 'id', write=True)
            self.browser.select('PhoneClass', '2', 'id')
            self.browser.select('Prefix', '604', 'id')
            # self.browser.erase('Prefix', 'id')
            self.browser.insert('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[2]/div[1]/div[1]/div[5]/div[2]/fieldset/div/div[3]/div/input', '3131234')
        except:
            self.browser.waitExist('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[2]/div[1]/div[1]/div[5]/div[2]/fieldset/div/div[1]/div/span/span[1]/span/span[1]', write=True)
            self.browser.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[2]/div[1]/div[1]/div[5]/div[2]/fieldset/div/div[1]/div/span/span[1]/span/span[1]')
            self.browser.write('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[2]/div[1]/div[1]/div[5]/div[2]/fieldset/div/div[1]/div/select', 'fijo')
            self.browser.write('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[2]/div[1]/div[1]/div[5]/div[2]/fieldset/div/div[1]/div/select', Keys.ENTER)
            self.browser.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[2]/div[1]/div[1]/div[5]/div[2]/fieldset/div/div[2]/div/select')
            time.sleep(1)
            self.browser.write('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[2]/div[1]/div[1]/div[5]/div[2]/fieldset/div/div[2]/div/select', '604')
            self.browser.write('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[2]/div[1]/div[1]/div[5]/div[2]/fieldset/div/div[2]/div/select', Keys.ENTER)
            self.browser.write('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[2]/div[1]/div[1]/div[5]/div[2]/fieldset/div/div[3]/div/input', '3131234')
     
    def rellenoDireccion(self, legalizador=False):
        try:
            if legalizador:
                self.browser.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[2]/div[3]/div[2]/fieldset/div[1]/div[1]/span/span[1]/span/span[1]')
                self.browser.write('/html/body/span/span/span[1]/input', 'otras')
                self.browser.write('/html/body/span/span/span[1]/input', Keys.ENTER)
            else:
                self.browser.select('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[2]/div[3]/div[2]/fieldset/div[1]/div[1]/span/span[1]/span/span[1]','otras')
            self.browser.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[2]/div[3]/div[2]/fieldset/div[1]/div[1]/span/span[1]/span/span[1]')
            self.browser.write('/html/body/span/span/span[1]/input', 'otras')
            self.browser.write('/html/body/span/span/span[1]/input', Keys.ENTER)
            self.browser.insert('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[2]/div[3]/div[2]/fieldset/div[2]/div/input', 'central')
            self.browser.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[2]/div[3]/div[2]/fieldset/div[3]/div/span/span[1]/span/span[1]')
            self.browser.write('/html/body/span/span/span[1]/input', 'antio')
            self.browser.write('/html/body/span/span/span[1]/input', Keys.ENTER)
            self.browser.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[2]/div[3]/div[2]/fieldset/div[4]/div/span/span[1]/span/span[1]')
            self.browser.write('/html/body/span/span/span[1]/input', 'mede')
            self.browser.write('/html/body/span/span/span[1]/input', Keys.ENTER)
            self.browser.insert('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[2]/div[3]/div[2]/fieldset/div[5]/div/input', 'central')
        except:
            try:
                self.browser.insert('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[2]/div[3]/div[2]/fieldset/div[1]/div[1]/select', 'otras')
                time.sleep(1)
                self.browser.insert('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[2]/div[3]/div[2]/fieldset/div[2]/div/input', 'central')
                time.sleep(1)
                self.browser.insert('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[2]/div[3]/div[2]/fieldset/div[3]/div/select', 'ANTIOQUIA')
                time.sleep(1)
                self.browser.insert('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[2]/div[3]/div[2]/fieldset/div[4]/div/select', 'MEDELLIN')
                time.sleep(1)
                self.browser.insert('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[2]/div[3]/div[2]/fieldset/div[5]/div/input', 'central')
            except:
                raise('No logra ingresar datos Direccion')

    def rellenoDireccion2(self):
        try:
            self.browser.waitExist('AddressClassId', 'id', write=True)
            self.browser.select('AddressClassId', 'Otras', 'id')
            self.browser.insert('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[2]/div[1]/div[2]/div[3]/div[2]/fieldset/div[2]/div/input', 'central')
            self.browser.select('Department', 'ANTIOQUIA', 'id')
            self.browser.select('City', 'MEDELLIN', 'id')
            self.browser.insert('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[2]/div[1]/div[2]/div[3]/div[2]/fieldset/div[5]/div/input', 'central')
        except:
            self.browser.waitExist('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[2]/div[1]/div[2]/div[3]/div[2]/fieldset/div[1]/div[1]/select', write=True)
            self.browser.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[2]/div[1]/div[2]/div[3]/div[2]/fieldset/div[1]/div[1]/select')
            self.browser.write('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[2]/div[1]/div[2]/div[3]/div[2]/fieldset/div[1]/div[1]/select', 'otras')
            self.browser.write('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[2]/div[1]/div[2]/div[3]/div[2]/fieldset/div[1]/div[1]/select', Keys.ENTER)
            self.browser.insert('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[2]/div[1]/div[2]/div[3]/div[2]/fieldset/div[2]/div/input', 'central')
            self.browser.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[2]/div[1]/div[2]/div[3]/div[2]/fieldset/div[3]/div/select')
            self.browser.write('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[2]/div[1]/div[2]/div[3]/div[2]/fieldset/div[3]/div/select', 'antio')
            self.browser.write('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[2]/div[1]/div[2]/div[3]/div[2]/fieldset/div[3]/div/select', Keys.ENTER)
            self.browser.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[2]/div[1]/div[2]/div[3]/div[2]/fieldset/div[4]/div/select')
            self.browser.write('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[2]/div[1]/div[2]/div[3]/div[2]/fieldset/div[4]/div/select', 'mede')
            self.browser.write('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[2]/div[1]/div[2]/div[3]/div[2]/fieldset/div[4]/div/select', Keys.ENTER)
            self.browser.insert('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[2]/div[1]/div[2]/div[3]/div[2]/fieldset/div[5]/div/input', 'central')